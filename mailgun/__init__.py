# coding: utf-8

__title__ = 'pymailgun'
__summary__ = "Simple Mailgun API wrapper."
__uri__ = 'https://github.com/Aeron/PyMailgun'

__version__ = '0.4.0'

__author__ = u"Eugene “Aeron” Glybin"
__email__ = 'aeron@aeron.cc'

__license__ = 'LGPLv3'
__copyright__ = "Copyright 2014 Eugene Glybin"

from .campaigns import Campaigns
from .lists import MailingLists
from .messages import Messages
from .unsubscribes import Unsubscribes
from .domains import Domains

__all__ = (
	'Mailgun',
	'Messages',
	'Campaigns',
	'MailingLists',
	'Unsubscribes',
	'Domains',
)


class Mailgun(object):
	def __init__(self, api_key, domain=None):
		self.api_key = api_key
		self.domain = domain
		self.lists = MailingLists(api_key)
		self.domains = Domains(api_key)
		if self.domain:
			self.messages = Messages(api_key, domain)
			self.campaigns = Campaigns(api_key, domain)
			self.unsubscribes = Unsubscribes(api_key, domain)

	def __repr__(self):
		return "%s(%s, %s) instance at %s" % (self.__class__.__name__, self.api_key, self.domain, hex(id(self)))
