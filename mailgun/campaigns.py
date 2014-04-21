# coding: utf-8
from .api import MailgunAPI
from .exceptions import MailgunValidationError

INVALID_COUNTRY_MSG = 'Country code must be two-letters length.'
INVALID_PAGE_MSG = 'The `page` value must be greater than 0.'


class CampaignEvents(MailgunAPI):
	API_NAME = 'campaigns'
	EVENTS = ('clicked', 'opened', 'unsubscribed', 'bounced', 'complained')

	def all(self, event=None, recipient=None, country=None, region=None, limit=100, page=1, count=None):
		if event and event not in self.EVENTS:
			raise MailgunValidationError(event, self.EVENTS)
		if country and len(country) != 2:
			raise MailgunValidationError(message=INVALID_COUNTRY_MSG)
		if page and page <= 0:
			raise MailgunValidationError(message=INVALID_PAGE_MSG)
		return super(CampaignEvents, self).all(params=locals())


class CampaignStats(MailgunAPI):
	API_NAME = 'campaigns'
	GROUPS = ('domain', 'daily_hour')

	def all(self, groupby=None):
		if groupby and groupby not in self.GROUPS:
			raise MailgunValidationError(groupby, self.GROUPS)
		return super(CampaignStats, self).all(params=locals())


class CampaignClicks(MailgunAPI):
	API_NAME = 'campaigns'
	GROUPS = ('link', 'recipient', 'domain', 'country', 'region', 'city', 'month', 'day', 'hour', 'minute', 'daily_hour')

	def all(self, groupby=GROUPS[0], country=None, region=None, city=None, limit=100, page=1, count=None):
		if groupby not in self.GROUPS:
			raise MailgunValidationError(groupby, self.GROUPS)
		if country and len(country) != 2:
			raise MailgunValidationError(message=INVALID_COUNTRY_MSG)
		if page and page <= 0:
			raise MailgunValidationError(message=INVALID_PAGE_MSG)
		return super(CampaignClicks, self).all(params=locals())


class CampaignOpens(CampaignClicks):
	API_NAME = 'campaigns'
	GROUPS = ('recipient', 'domain', 'country', 'region', 'city', 'month', 'day', 'hour', 'minute', 'daily_hour')


class CampaignUnsubscribes(CampaignClicks):
	API_NAME = 'campaigns'
	GROUPS = ('domain', 'country', 'region', 'city', 'month', 'day', 'hour', 'minute', 'daily_hour')


class CampaignComplaints(CampaignClicks):
	API_NAME = 'campaigns'
	GROUPS = ('recipient', 'domain', 'month', 'day', 'hour', 'minute', 'daily_hour')

	def all(self, groupby=GROUPS[0], limit=100, page=1, count=None):
		if groupby not in self.GROUPS:
			raise MailgunValidationError(groupby, self.GROUPS)
		if page and page <= 0:
			raise MailgunValidationError(message=INVALID_PAGE_MSG)
		return super(CampaignComplaints, self).all(params=locals())


class Campaigns(MailgunAPI):
	API_NAME = 'campaigns'

	subclasses = {
		'events': CampaignEvents,
		'stats': CampaignStats,
		'clicks': CampaignClicks,
		'opens': CampaignOpens,
		'unsubscribes': CampaignUnsubscribes,
		'complaints': CampaignComplaints,
	}

	def all(self, limit=100, skip=0):
		return super(Campaigns, self).all(params=locals())

	def create(self, name, id=None):
		return super(Campaigns, self).create(data=locals())

	def update(self, pk, name, id=None):
		return super(Campaigns, self).update(pk, data=locals())
