import base64
import logging

import simplejson
import tornado
import tornado.httpclient

def _callback(response):
	if response.error:
		logging.error("Failed to send data to mixpane. Reason: " + response.error)

def track(token, event, properties=None):
	if "token" not in properties:
		properties["token"] = token

	params = {"event": event, "properties": properties}
	data = base64.b64encode(simplejson.dumps(params))
	request = "http://api.mixpanel.com/track/?data=" + data

	http_client = tornado.httpclient.AsyncHTTPClient()
	http_client.fetch(request, _callback)