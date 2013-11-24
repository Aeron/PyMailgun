# coding: utf-8
from .api import MailgunAPI

INVALID_SPAM_ACTION_MSG = 'The `%s` spam action is not valid. Valid actions: %s.'


class Domains(MailgunAPI):
	API_NAME = 'domains'
	DOMAIN_FREE = True

	SPAM_ACTIONS = ('disabled', 'tag')

	def all(self, limit=100, skip=0):
		return super(Domains, self).all(params=locals())

	def get(self, domain):
		return super(Domains, self).get(domain)

	def create(self, name, smtp_password='something', spam_action=SPAM_ACTIONS[0], wildcard=False):
		assert spam_action in self.SPAM_ACTIONS, INVALID_SPAM_ACTION_MSG % (spam_action, self.SPAM_ACTIONS)
		return super(Domains, self).create(data=locals())

	def delete(self, domain):
		return super(Domains, self).delete(domain)
