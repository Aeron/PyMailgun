# coding: utf-8
import requests
from .exceptions import MailgunError

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
		return "{cls}({api_key}, {domain}) instance at {_id:#x}".format(
			cls=self.__class__.__name__,
			api_key=self.api_key,
			domain=self.domain,
			_id=id(self)
		)

	def __getattr__(self, name):
		if name not in self._instances or self._instances[name]._pk != self._pk:
			if name in self.subclasses:
				self._instances[name] = self.subclasses[name](self.api_key, self.domain, self._pk, name)
				self._pk = None
			else:
				return super(MailgunAPI, self).__getattribute__(name)
		return self._instances[name]

	# fixing state control for pickle
	def __getstate__(self):
		return self.__dict__

	def __setstate__(self, d):
		self.__dict__.update(d)

	@property
	def api_url(self):
		if not self.API_NAME:
			raise MailgunError('API name not specified.')
		if self.DOMAIN_FREE is False and self.domain is None:
			raise MailgunError('This API call requires to specify domain name.')
		if self.DOMAIN_FREE:
			self.domain = None
		return reduce(
			lambda initial, part: '/'.join([initial, part] if part else [initial]),
			(
				self.domain,
				self.API_NAME,
				self._pk,
				self._sub,
				self._sub_pk
			),
			self.API_URL
		)

	def _set_pk(self, pk=None):
		if pk is not None:
			if self._sub:
				self._sub_pk = pk
			else:
				self._pk = pk

	def _request(self, method, params=None, data=None, files=None):
		if method.upper() not in self.ALLOWED_METHODS:
			raise MailgunError('{method} method is not allowed.'.format(method=method.upper()))
		kwargs = {
			'method': method,
			'url': self.api_url,
			'auth': self.auth,
			'params': params,
			'data': data,
			'files': files,
		}
		r = requests.request(**kwargs)
		if not r.ok:
			r.raise_for_status()
		return r.json()

	def with_id(self, pk):
		self._pk = pk
		return self

	def all(self, params=None):
		return self._request('get', params=params)

	def get(self, pk, params=None):
		self._set_pk(pk)
		return self._request('get', params=params)

	def create(self, data=None):
		return self._request('post', data=data)

	def update(self, pk, data=None):
		self._set_pk(pk)
		return self._request('put', data=data)

	def delete(self, pk):
		self._set_pk(pk)
		return self._request('delete')
