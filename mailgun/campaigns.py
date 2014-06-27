# coding: utf-8
from .api import MailgunAPI
from .exceptions import MailgunValidationError

INVALID_COUNTRY_MSG = 'Country code must be two-letters length.'
INVALID_PAGE_MSG = 'The `page` value must be greater than 0.'
INVALID_CAMPAIGN_NAME_OR_ID_LENGTH = "Campaign name and campaign ID should not exceed the maximum length of 64 characters."

CAMPAIGN_NAME_OR_ID_MAX_LENGTH = 64


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
		return super(CampaignEvents, self).all(params=dict(
			event=event,
			recipient=recipient,
			country=country,
			region=region,
			limit=limit,
			page=page,
			count=count
		))


class CampaignStats(MailgunAPI):
	API_NAME = 'campaigns'
	GROUPS = ('domain', 'daily_hour')

	def all(self, groupby=None):
		if groupby and groupby not in self.GROUPS:
			raise MailgunValidationError(groupby, self.GROUPS)
		return super(CampaignStats, self).all(params=dict(
			groupby=groupby
		))


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
		return super(CampaignClicks, self).all(params=dict(
			groupby=groupby,
			country=country,
			region=region,
			city=city,
			limit=limit,
			page=page,
			count=count
		))


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
		return super(CampaignComplaints, self).all(params=dict(
			groupby=groupby,
			limit=limit,
			page=page,
			count=count
		))


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
		return super(Campaigns, self).all(params=dict(
			limit=limit,
			skip=skip
		))

	def create(self, name, id=None):
		if len(name) > CAMPAIGN_NAME_OR_ID_MAX_LENGTH or len(str(id)) > CAMPAIGN_NAME_OR_ID_MAX_LENGTH:
			raise MailgunValidationError(message=INVALID_CAMPAIGN_NAME_OR_ID_LENGTH)
		return super(Campaigns, self).create(data=dict(
			name=name,
			id=id
		))

	def update(self, pk, name, id=None):
		if len(name) > CAMPAIGN_NAME_OR_ID_MAX_LENGTH or len(str(id)) > CAMPAIGN_NAME_OR_ID_MAX_LENGTH:
			raise MailgunValidationError(message=INVALID_CAMPAIGN_NAME_OR_ID_LENGTH)
		return super(Campaigns, self).update(pk, data=dict(
			name=name,
			id=id
		))
