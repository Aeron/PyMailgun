# coding: utf-8
import requests
import json

MAILGUN_API_URL = "https://api.mailgun.net/v2"

INVALID_EVENT_MSG = 'The `%s` event is not valid. Valid events: %s.'
INVALID_COUNTRY_MSG = 'Country code must be two-letters length.'
INVALID_PAGE_MSG = 'The `page` must be greater than 0.'
INVALID_GROUP_MSG = 'The `%s` group is not valid. Valid groups: %s.'


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
		return "%s(%s, %s) instance at %s" % (self.__class__.__name__, self.api_key, self.domain, hex(id(self)))

	def __getattr__(self, name):
		if name not in self._instances:
			if name in self.subclasses:
				self._instances[name] = self.subclasses[name](self.api_key, self.domain, self._pk, name)
				self._pk = None
			else:
				return super(MailgunAPI, self).__getattribute__(name)
		return self._instances[name]

	@property
	def api_url(self):
		assert self.API_NAME, 'API name not specified.'
		if self.DOMAIN_FREE is False and self.domain is None:
			raise Exception('This API call requires to specify domain name.')
		url = self.API_URL
		if self.DOMAIN_FREE:
			self.domain = None
		parts = (self.domain, self.API_NAME, self._pk, self._sub, self._sub_pk)
		for part in parts:
			if part:
				url = "%s/%s" % (url, part)
		return url

	def _set_pk(self, pk=None):
		if pk is not None:
			if self._sub:
				self._sub_pk = pk
			else:
				self._pk = pk

	def _request(self, method, **kwargs):
		assert method.upper() in self.ALLOWED_METHODS, '%s method is not allowed.' % method.upper()
		kw = {
			'method': method,
			'url': self.api_url,
			'auth': self.auth,
			'params': kwargs if method == 'get' else {},
			'data': kwargs if method in ('post', 'put') else {},
		}
		r = requests.request(**kw)
		print(r.request.method, r.request.url, r.request.body)
		if not r.ok:
			r.raise_for_status()
		return r.json()

	def with_id(self, pk):
		self._pk = pk
		return self

	def all(self, **kwargs):
		return self._request('get', **kwargs)

	def get(self, pk, **kwargs):
		self._set_pk(pk)
		return self._request('get', **kwargs)

	def create(self, **kwargs):
		return self._request('post', **kwargs)

	def update(self, pk, **kwargs):
		self._set_pk(pk)
		return self._request('put', **kwargs)

	def delete(self, pk):
		return self._request('delete')


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


class MailingListMembers(MailgunAPI):
	API_NAME = 'lists'
	DOMAIN_FREE = True
	UPSERT = SUBSCRIBED = ('yes', 'no')

	def all(self, subscribed=None, limit=100, skip=0):
		if subscribed:
			assert subscribed in self.SUBSCRIBED, 'The `subscribed` must be `%s` or `%s`.' % self.SUBSCRIBED
		return super(MailingListMembers, self).all(subscribed=subscribed, limit=limit, skip=skip)

	def create(self, address, name=None, vars=None, subscribed=SUBSCRIBED[0], upsert=UPSERT[1]):
		if subscribed:
			assert subscribed in self.SUBSCRIBED, 'The `subscribed` must be `%s` or `%s`.' % self.SUBSCRIBED
		if vars:
			vars = json.dumps(vars)
		return super(MailingListMembers, self).create(address=address, name=name, vars=vars, subscribed=subscribed, upsert=upsert)

	def update(self, pk, address=None, name=None, vars=None, subscribed=SUBSCRIBED[0]):
		if subscribed:
			assert subscribed in self.SUBSCRIBED, 'The `subscribed` must be `%s` or `%s`.' % self.SUBSCRIBED
		if vars:
			vars = json.dumps(vars)
		return super(MailingListMembers, self).update(pk, address=address, name=name, vars=vars, subscribed=subscribed)


class MailingListStats(MailgunAPI):
	API_NAME = 'lists'
	DOMAIN_FREE = True

	def all(self):
		return super(CampaignStats, self).all()


class MailingLists(MailgunAPI):
	API_NAME = 'lists'
	DOMAIN_FREE = True
	ACCESS_LEVELS = ('readonly', 'members', 'everyone')

	subclasses = {
		'members': MailingListMembers,
		'stats': MailingListStats,
	}

	def all(self, address=None, limit=100, skip=0):
		return super(MailingLists, self).all(address=address, limit=limit, skip=skip)

	def create(self, address, name=None, description=None, access_level=ACCESS_LEVELS[0]):
		return super(MailingLists, self).create(address=address, name=name, description=description, access_level=access_level)

	def update(self, pk, address=None, name=None, description=None, access_level=ACCESS_LEVELS[0]):
		return super(MailingLists, self).update(pk, address=address, name=name, description=description, access_level=access_level)
