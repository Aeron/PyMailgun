# coding: utf-8
import requests

MAILGUN_API_URL = "https://api.mailgun.net/v2/%s/%s"


class MailgunAPI(object):
	API_URL = MAILGUN_API_URL
	# ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'DELETE')

	def __init__(self, api_key, domain):
		self.auth = ("api", api_key)
		self.domain = domain
		self.api_url = self.API_URL % (self.domain, self.__class__.__name__.lower())

	def __repr__(self):
		return "%s(%s) instance at %s" % (self.__class__.__name__, self.flow_api_token, hex(id(self)))

	@staticmethod
	def _respond(response):
		# print(response.request.url, response.request.method, response.request.body)
		if not response.ok:
			response.raise_for_status()
		return response.json()

	def get(self, _id=None, _sub=None, **params):
		url = "%s/%s" % (self.api_url, "%s/%s" % (_id, _sub) if _sub else _id) if _id else self.api_url
		response = requests.get(url, auth=self.auth, params=params)
		return self._respond(response)

	def post(self, **data):
		response = requests.post(self.api_url, auth=self.auth, data=data)
		return self._respond(response)

	def put(self, _id, **data):
		url = "%s/%s" % (self.api_url, _id)
		response = requests.put(url, auth=self.auth, data=data)
		return self._respond(response)

	def delete(self, _id):
		url = "%s/%s" % (self.api_url, _id)
		response = requests.delete(url, auth=self.auth)
		return self._respond(response)


class Campaigns(MailgunAPI):
	EVENTS_EVENTS = ('clicked', 'opened', 'unsubscribed', 'bounced', 'complained')
	STATS_GROUPS = ('domain', 'daily_hour')
	CLICKS_GROUPS = ('link', 'recipient', 'domain', 'country', 'region', 'city', 'month', 'day', 'hour', 'minute', 'daily_hour')
	OPENS_GROUPS = ('recipient', 'domain', 'country', 'region', 'city', 'month', 'day', 'hour', 'minute', 'daily_hour')
	UNSUBSCRIBES_GROUPS = ('domain', 'country', 'region', 'city', 'month', 'day', 'hour', 'minute', 'daily_hour')
	COMPLAINTS_GROUPS = ('recipient', 'domain', 'month', 'day', 'hour', 'minute', 'daily_hour')

	INVALID_EVENT_MSG = 'The `%s` event is not valid. Valid events: %s.'
	INVALID_COUNTRY_MSG = 'Country code must be two-letters length.'
	INVALID_PAGE_MSG = 'The `page` must be greater than 0.'
	INVALID_GROUP_MSG = 'The `%s` group is not valid. Valid groups: %s.'

	def post(self, name, id=None):
		return super(Campaigns, self).post(name=name, id=id)

	def put(self, _id, name, id=None):
		return super(Campaigns, self).put(_id, name=name, id=id)

	def events(self, _id, event=None, recipient=None, country=None, region=None, limit=100, page=1, count=None):
		if event:
			assert event in self.EVENTS, self.INVALID_EVENT_MSG % (event, self.EVENTS_EVENTS)
		if country:
			assert len(country) == 2, self.INVALID_COUNTRY_MSG
		if page:
			assert page > 0, self.INVALID_PAGE_MSG
		return super(Campaigns, self).get(_id, 'events', event=event, recipient=recipient, country=country, region=region, limit=limit, page=page, count=count)

	def stats(self, _id, groupby=None):
		if groupby:
			assert groupby in self.STATS_GROUPS, self.INVALID_GROUP_MSG % (groupby, self.STATS_GROUPS)
		return super(Campaigns, self).get(_id, 'stats', groupby=groupby)

	def clicks(self, _id, groupby=CLICKS_GROUPS[0], country=None, region=None, city=None, limit=100, page=1, count=None):
		assert groupby in self.CLICKS_GROUPS, self.INVALID_GROUP_MSG % (groupby, self.CLICKS_GROUPS)
		if country:
			assert len(country) == 2, self.INVALID_COUNTRY_MSG
		if page:
			assert page > 0, self.INVALID_PAGE_MSG
		return super(Campaigns, self).get(_id, 'clicks', groupby=groupby, country=country, region=region, city=city, limit=limit, page=page, count=count)

	def opens(self, _id, groupby=OPENS_GROUPS[0], country=None, region=None, city=None, limit=100, page=1, count=None):
		assert groupby in self.OPENS_GROUPS, self.INVALID_GROUP_MSG % (groupby, self.OPENS_GROUPS)
		if country:
			assert len(country) == 2, self.INVALID_COUNTRY_MSG
		if page:
			assert page > 0, self.INVALID_PAGE_MSG
		return super(Campaigns, self).get(_id, 'opens', groupby=groupby, country=country, region=region, city=city, limit=limit, page=page, count=count)

	def unsubscribes(self, _id, groupby=UNSUBSCRIBES_GROUPS[0], country=None, region=None, city=None, limit=100, page=1, count=None):
		assert groupby in self.UNSUBSCRIBES_GROUPS, self.INVALID_GROUP_MSG % (groupby, self.UNSUBSCRIBES_GROUPS)
		if country:
			assert len(country) == 2, self.INVALID_COUNTRY_MSG
		if page:
			assert page > 0, self.INVALID_PAGE_MSG
		return super(Campaigns, self).get(_id, 'unsubscribes', groupby=groupby, country=country, region=region, city=city, limit=limit, page=page, count=count)

	def complaints(self, _id, groupby=COMPLAINTS_GROUPS[0], limit=100, page=1, count=None):
		assert groupby in self.COMPLAINTS_GROUPS, self.INVALID_GROUP_MSG % (groupby, self.COMPLAINTS_GROUPS)
		if page:
			assert page > 0, self.INVALID_PAGE_MSG
		return super(Campaigns, self).get(_id, 'complaints', groupby=groupby, limit=limit, page=page, count=count)


class Lists(MailgunAPI):
	pass
