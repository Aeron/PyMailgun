# coding: utf-8
import requests

MAILGUN_API_URL = "https://api.mailgun.net/v2"


class MailgunAPI(object):
	API_URL = MAILGUN_API_URL
	API_NAME = None
	DOMAIN_FREE = False
	ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'DELETE')

	subclasses = {}

	def __init__(self, api_key, domain=None, pk=None, sub=None):
		self.api_key = api_key
		self.auth = ("api", self.api_key)
		self.domain = domain
		self._pk = pk
		self._sub = sub
		self._sub_pk = None
		self._instances = {}

	def __repr__(self):
		return "%s(%s, %s) instance at %s" % (self.__class__.__name__, self.api_key, self.domain, hex(id(self)))

	def __getattr__(self, name):
		if name not in self._instances:
			if name in self.subclasses:
				self._instances[name] = self.subclasses[name](self.api_key, self.domain, self._pk, name)
				self._pk = None
			else:
				return super(MailgunAPI, self).__getattribute__(name)
		return self._instances[name]

	@property
	def api_url(self):
		assert self.API_NAME, 'API name not specified.'
		if self.DOMAIN_FREE is False and self.domain is None:
			raise Exception('This API call requires to specify domain name.')
		url = self.API_URL
		if self.DOMAIN_FREE:
			self.domain = None
		parts = (self.domain, self.API_NAME, self._pk, self._sub, self._sub_pk)
		for part in parts:
			if part:
				url = "%s/%s" % (url, part)
		return url

	def _set_pk(self, pk=None):
		if pk is not None:
			if self._sub:
				self._sub_pk = pk
			else:
				self._pk = pk

	def _request(self, method, **kwargs):
		assert method.upper() in self.ALLOWED_METHODS, '%s method is not allowed.' % method.upper()
		kw = {
			'method': method,
			'url': self.api_url,
			'auth': self.auth,
			'params': kwargs if method == 'get' else {},
			'data': kwargs if method in ('post', 'put') else {},
		}
		r = requests.request(**kw)
		print(r.request.method, r.request.url, r.request.body)
		if not r.ok:
			r.raise_for_status()
		return r.json()

	def with_id(self, pk):
		self._pk = pk
		return self

	def all(self, **kwargs):
		return self._request('get', **kwargs)

	def get(self, pk, **kwargs):
		self._set_pk(pk)
		return self._request('get', **kwargs)

	def create(self, **kwargs):
		return self._request('post', **kwargs)

	def update(self, pk, **kwargs):
		self._set_pk(pk)
		return self._request('put', **kwargs)

	def delete(self, pk):
		return self._request('delete')
