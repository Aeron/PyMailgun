# coding: utf-8
from .api import MailgunAPI
from .exceptions import MailgunValidationError


class Domains(MailgunAPI):
	API_NAME = 'domains'
	DOMAIN_FREE = True

	SPAM_ACTIONS = ('disabled', 'tag')

	def all(self, limit=100, skip=0):
		return super(Domains, self).all(params=dict(
			limit=limit,
			skip=skip
		))

	def get(self, domain):
		return super(Domains, self).get(domain)

	def create(self, name, smtp_password='something', spam_action=SPAM_ACTIONS[0], wildcard=False):
		if spam_action not in self.SPAM_ACTIONS:
			raise MailgunValidationError(spam_action, self.SPAM_ACTIONS)
		return super(Domains, self).create(data=dict(
			name=name,
			smtp_password=smtp_password,
			spam_action=spam_action,
			wildcard=wildcard
		))

	def delete(self, domain):
		return super(Domains, self).delete(domain)
