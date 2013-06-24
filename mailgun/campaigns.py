# coding: utf-8
from .api import MailgunAPI

INVALID_EVENT_MSG = 'The `%s` event is not valid. Valid events: %s.'
INVALID_COUNTRY_MSG = 'Country code must be two-letters length.'
INVALID_PAGE_MSG = 'The `page` must be greater than 0.'
INVALID_GROUP_MSG = 'The `%s` group is not valid. Valid groups: %s.'


class CampaignEvents(MailgunAPI):
	API_NAME = 'campaigns'
	EVENTS = ('clicked', 'opened', 'unsubscribed', 'bounced', 'complained')

	def all(self, event=None, recipient=None, country=None, region=None, limit=100, page=1, count=None):
		if event:
			assert event in self.EVENTS, INVALID_EVENT_MSG % (event, self.EVENTS)
		if country:
			assert len(country) == 2, INVALID_COUNTRY_MSG
		if page:
			assert page > 0, INVALID_PAGE_MSG
		return super(CampaignEvents, self).all(event=event, recipient=recipient, country=country, region=region, limit=limit, page=page, count=count)


class CampaignStats(MailgunAPI):
	API_NAME = 'campaigns'
	GROUPS = ('domain', 'daily_hour')

	def all(self, groupby=None):
		if groupby:
			assert groupby in self.GROUPS, INVALID_GROUP_MSG % (groupby, self.GROUPS)
		return super(CampaignStats, self).all(groupby=groupby)


class CampaignClicks(MailgunAPI):
	API_NAME = 'campaigns'
	GROUPS = ('link', 'recipient', 'domain', 'country', 'region', 'city', 'month', 'day', 'hour', 'minute', 'daily_hour')

	def all(self, groupby=GROUPS[0], country=None, region=None, city=None, limit=100, page=1, count=None):
		assert groupby in self.GROUPS, INVALID_GROUP_MSG % (groupby, self.GROUPS)
		if country:
			assert len(country) == 2, INVALID_COUNTRY_MSG
		if page:
			assert page > 0, INVALID_PAGE_MSG
		return super(CampaignClicks, self).all(groupby=groupby, country=country, region=region, city=city, limit=limit, page=page, count=count)


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
		assert groupby in self.GROUPS, INVALID_GROUP_MSG % (groupby, self.GROUPS)
		if page:
			assert page > 0, INVALID_PAGE_MSG
		return super(CampaignComplaints, self).all(groupby=groupby, limit=limit, page=page, count=count)


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
		return super(Campaigns, self).all(limit=limit, skip=skip)

	def create(self, name, id=None):
		return super(Campaigns, self).create(name=name, id=id)

	def update(self, pk, name, id=None):
		return super(Campaigns, self).update(pk, name=name, id=id)
