# coding: utf-8
from .api import MailgunAPI


class Domains(MailgunAPI):
	API_NAME = 'domains'
	DOMAIN_FREE = True

	def all(self, limit=100, skip=0):
		return super(Domains, self).all(params=locals())

	def get(self, domain):
		return super(Domains, self).get(domain)

	def create(self, name, smtp_password='something'):
		return super(Domains, self).create(data=locals())

	def delete(self, domain):
		return super(Domains, self).delete(domain)
