import os
import re
import subprocess
import logging
import json
import uuid
from urlparse import urlparse
import shutil
import cStringIO

import tornado
from tornado import httpclient
from tornado.options import define, options

import settings
from consts import *
from ziputil import create_zip
import mixpanel

class BaseHandler(tornado.web.RequestHandler):
	has_mixpanel = None

	def _get_default_thrift_version(self):
		for t in self.application.thrift_bins:
			return t["name"]

	def render(self, template_name, **kwargs):
		if self.has_mixpanel is None:
			if settings.ENABLE_ANALYTICS:
				try:
					mixpanel_data = self.render_string("mixpanel.html")
					self.has_mixpanel = True
				except IOError:
					self.has_mixpanel = False
		
		kwargs["has_mixpanel"] = self.has_mixpanel
		kwargs["thrift_bins"] = self.application.thrift_bins
		kwargs["settings"] = settings
		return super(BaseHandler, self).render(template_name, **kwargs)


class RootHandler(BaseHandler):
	def get(self):
		self.render("root.html", supported_languages=SUPPORTED_LANGUAGES)


class GenerateThriftBindingHandler(BaseHandler):
	def _get_thrift_bin_by_version(self, version):
		for t in self.application.thrift_bins:
			if not version:
				return t["bin"]
			else:
				if t["name"] == version:
					return t["bin"]

		return None

	def _generate_temp_id(self):
		return str(uuid.uuid4()).replace("-", "")

	def _pack_zip_result(self, path, filename, language):
		"Returns a path to a zip file which contains all the output files (and the input thrift file)"
		package_filename = DEFAULT_PACKAGE_NAME_TEMPLATE % (filename, language.replace(":", "_"))
		p = os.path.join(path, package_filename)
		logging.debug("Packing to " + p)
		create_zip(path, "", p, excludelist={ package_filename : None })
		return package_filename

	def _pack_json_result(self, path, filename, language):
		"Returns a json string with the list of all files and their content"
		files = []
		for file_name in self._collect_files_from_subtree(path):
			file_language = 'thrift' if file_name.endswith('.thrift') else language
			file = {
				'name': file_name[len(path) + 1:],
				'content': open(file_name, 'r').read(),
				'language': file_language,
			}
			files.append(file)

		data = {
			'files': files
		}
		return json.dumps(data)

	def _collect_files_from_subtree(self, path):
		"Collects all the file paths (files only, not dirs) under the given tree path"
		files = []
		for file in os.listdir(path):
			full_path = os.path.join(path, file)
			if os.path.isdir(full_path):
				files += (self._collect_files_from_subtree(full_path))
			else:
				files.append(full_path)
		return files

	def _generate_bindings(self, thrift_bin, path, filename, **kwargs):
		cmd = [
			thrift_bin,
			"-o %s" % path,
			"--gen %s" % kwargs["gen"],
			os.path.join(path, filename)
		]

		cmd = " ".join(cmd)

		logging.debug("Using path=" + path)
		logging.debug("Executing cmd='" + cmd + "'")

		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		result, error = p.communicate()
		if p.returncode != 0:
			raise Exception(result)

		paths = os.listdir(path)

		found_bindings = False
		for p in paths:
			if p.find("gen-") > -1:
				found_bindings = True
				break

		if not found_bindings:
			raise Exception(result)
				
	def _handle_request(self, response):
		if response.error:
			self.set_status(500)
			self.finish(json.dumps({ "result" : 500, "text" : "failed to retrieve file. Reasone: %s" % reponse.error }))

		thrift_bin = self._get_thrift_bin_by_version(self.get_argument("thriftversion", None))	
		
		language = self.get_argument("gen")

		parsed_url = urlparse(response.request.url)
		path_parts = parsed_url.path.split("/")

		filename = path_parts[-1]

		path = os.path.join(settings.TEMP_PATH, self._generate_temp_id())
		os.makedirs(path)
		try:
			f = open(os.path.join(path, filename), "wb")
			try:
				f.write(response.body)
			finally:
				f.close()

			self._generate_bindings(thrift_bin, path, filename, gen=language)
			package_filename = self._pack_zip_result(path, filename, language)

			self.set_header("Content-Type", "application/octet-stream")
			self.set_header("Content-Disposition","attachment; filename=%s" % package_filename)
			f = open(os.path.join(path, package_filename), "rb")
			try:
				self.write(f.read())
			finally:
				f.close()			
		finally:
			logging.debug("Removing temp path '" + path + "'")
			shutil.rmtree(path)

		self.finish()

	def _do_zip(self):
		"Tests whether this request should zip the response"
		download_zip = self.get_argument("download_zip", "on")
		do_zip = download_zip != "off"

		# For AJAX requests, always disable downloading zip.
		if do_zip and "X-Requested-With" in self.request.headers:
			do_zip = False

		return do_zip

	def _is_valid_gen_value(self, value):
		if value and value != "":
			parts = value.split(":")
			if parts[0] in SUPPORTED_LANGUAGES:
				if len(parts) > 1:
					if parts[1] in SUPPORTED_LANGUAGES[parts[0]]["parameters"]:
						return True
				else:
					return True

		return False

	def write_error(self, status_code, **kwargs):
		if self.get_argument("ui", "0") == "1" and self._do_zip():
			self.render("error.html", status_code=status_code, error_text=str(kwargs["exc_info"][1]))
		else:
			self.finish({ "result" : "fail", "text" : str(kwargs["exc_info"][1]) })

	@tornado.web.asynchronous
	def post(self):
		gen = self.get_argument("gen")
		if gen: gen = gen.lower()

		if not self._is_valid_gen_value(gen):
			raise tornado.web.HTTPError(400, "Invalid 'gen' value. Please refer to the documentation at http://thriftify.org/documentation")

		do_zip = self._do_zip()

		thrift_bin = self._get_thrift_bin_by_version(self.get_argument("thriftversion", None))	
		

		first_filename = None

		url = self.get_argument("url", None)

		if url:
			http_client = httpclient.AsyncHTTPClient()
			http_client.fetch(url, self._handle_request)
			return

		path = os.path.join(settings.TEMP_PATH, self._generate_temp_id())
		os.makedirs(path)
		try:
			if len(self.request.files) > 0:
				for k in self.request.files:
					o = self.request.files[k][0]
					filename = o["filename"]

					if not first_filename:
						first_filename = filename

					f = open(os.path.join(path, filename), "wb")
					try:
						f.write(o["body"])
					finally:
						f.close()
			else:
				thrift_file_content = self.get_argument("thriftcontent")
				f = open(os.path.join(path, "file.thrift"), "w")
				try:
					f.write(thrift_file_content)
					first_filename = "file.thrift"
				finally:
					f.close()

			self._generate_bindings(thrift_bin, path, first_filename, gen=gen)

			if do_zip:
				package_filename = self._pack_zip_result(path, first_filename, gen)
				self.set_header("Content-Type", "application/octet-stream")
				self.set_header("Content-Disposition","attachment; filename=%s" % package_filename)
				f = open(os.path.join(path, package_filename), "rb")
				try:
					self.write(f.read())
				finally:
					f.close()

				if options.mixpaneltoken:
					mixpanel.track(options.mixpaneltoken, "GenerateAPI", { "gen" : gen })
			else:
				json = self._pack_json_result(path, first_filename, gen)
				self.set_header("Content-Type", "application/json")
				self.write(json)

			self.finish()
		finally:
			logging.debug("Removing temp path '" + path + "'")
			shutil.rmtree(path)


class AboutHandler(BaseHandler):
	def get(self):
		self.render("about.html")

class DocsHandler(BaseHandler):
	def get(self):
		self.render("docs.html", supported_languages=SUPPORTED_LANGUAGES, default_thrift_version=self._get_default_thrift_version())
