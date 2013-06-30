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
		self.messages = Messages(api_key, domain)
		self.lists = MailingLists(api_key)
		self.campaigns = Campaigns(api_key, domain)
