# coding: utf-8
import requests

MAILGUN_API_URL = "https://api.mailgun.net/v2/%s/%s"


class MailgunAPI(object):
	API_URL = MAILGUN_API_URL
	# ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'DELETE')

	def __init__(self, api_key, domain):
		self.auth = ("api", api_key)
		self.domain = domain
		self.api_url = self.API_URL % (self.domain, self.__class__.__name__.lower())

	def __repr__(self):
		return "%s(%s) instance at %s" % (self.__class__.__name__, self.flow_api_token, hex(id(self)))

	@staticmethod
	def _respond(response):
		if not response.ok:
			response.raise_for_status()
		return response.json()

	def get(self, id=None, **params):
		url = "%s/%s" % (self.api_url, id) if id else self.api_url
		response = requests.get(url, params=params)
		return self._respond(response)

	def post(self, **data):
		response = requests.post(self.api_url, data=data)
		return self._respond(response)

	def put(self, id, **data):
		url = "%s/%s" % (self.api_url, id)
		response = requests.put(url, data=data)
		return self._respond(response)

	def delete(self, id):
		url = "%s/%s" % (self.api_url, id)
		response = requests.delete(url)
		return self._respond(response)


class Campaigns(MailgunAPI):
	pass
