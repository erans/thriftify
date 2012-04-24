#!/usr/bin/python
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
from tornado.options import define, options

from handlers import *

import settings

define("port", default=8888, help="run on the given port", type=int)
define("mixpaneltoken", default=None, help="MixPanel token to track events", type=str)

class Application(tornado.web.Application):
	def _get_thrift_versions(self):
		thrift_bins = []

		for thrift_bin in settings.THRIFT_BINS:
			cmd = [thrift_bin, "-version"]		
			cmd = " ".join(cmd)

			p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			result, error = p.communicate()
			
			if p.returncode != 1:
				raise Exception(result)

			thrift_bins.append({
				"name" : result.strip().replace("Thrift version", "").strip(),
				"bin" : thrift_bin
			})

		return thrift_bins

	def __init__(self):
		handlers = [
			(r"/", RootHandler),
			(r"/about", AboutHandler),
			(r"/docs", DocsHandler),
			(r"/api/v1/generate", GenerateThriftBindingHandler),
		]
		
		_settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=settings.DEBUG,
			gzip=True,
			mixpanel_token=options.mixpaneltoken
		)

		thrift_bins = self._get_thrift_versions()
		if not thrift_bins or len(thrift_bins) == 0:
			raise Exception("Failed to get Thrift compiler binaries and version numbers")

		self.thrift_bins = thrift_bins

		tornado.web.Application.__init__(self, handlers, **_settings)


def main():	
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
