from .campaigns import Campaigns
from .lists import MailingLists
from .messages import Messages


__all__ = (
	'Mailgun',
	'Messages',
	'Campaigns',
	'MailingLists',
)


class Mailgun(object):
	def __init__(self, api_key, domain):
		self.api_key = api_key
		self.domain = domain
		self.messages = Messages(api_key, domain)
		self.lists = MailingLists(api_key)
		self.campaigns = Campaigns(api_key, domain)

	def __repr__(self):
		return "%s(%s, %s) instance at %s" % (self.__class__.__name__, self.api_key, self.domain, hex(id(self)))
