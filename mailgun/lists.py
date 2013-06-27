# coding: utf-8
import json
from .api import MailgunAPI

INVALID_SUBSCRIBED_MSG = "The `subscribed` must be `%s` or `%s`."


class MailingListMembers(MailgunAPI):
	API_NAME = 'lists'
	DOMAIN_FREE = True
	UPSERT = SUBSCRIBED = ('yes', 'no')

	def all(self, subscribed=None, limit=100, skip=0):
		if subscribed:
			assert subscribed in self.SUBSCRIBED, INVALID_SUBSCRIBED_MSG % self.SUBSCRIBED
		return super(MailingListMembers, self).all(params=locals())

	def create(self, address, name=None, vars=None, subscribed=SUBSCRIBED[0], upsert=UPSERT[1]):
		if subscribed:
			assert subscribed in self.SUBSCRIBED, INVALID_SUBSCRIBED_MSG % self.SUBSCRIBED
		if vars:
			vars = json.dumps(vars)
		return super(MailingListMembers, self).create(data=locals())

	def update(self, pk, address=None, name=None, vars=None, subscribed=SUBSCRIBED[0]):
		if subscribed:
			assert subscribed in self.SUBSCRIBED, INVALID_SUBSCRIBED_MSG % self.SUBSCRIBED
		if vars:
			vars = json.dumps(vars)
		return super(MailingListMembers, self).update(pk, data=locals())


class MailingListStats(MailgunAPI):
	API_NAME = 'lists'
	DOMAIN_FREE = True

	def all(self):
		return super(MailingListStats, self).all()


class MailingLists(MailgunAPI):
	API_NAME = 'lists'
	DOMAIN_FREE = True
	ACCESS_LEVELS = ('readonly', 'members', 'everyone')

	subclasses = {
		'members': MailingListMembers,
		'stats': MailingListStats,
	}

	def all(self, address=None, limit=100, skip=0):
		return super(MailingLists, self).all(params=locals())

	def create(self, address, name=None, description=None, access_level=ACCESS_LEVELS[0]):
		return super(MailingLists, self).create(data=locals())

	def update(self, pk, address=None, name=None, description=None, access_level=ACCESS_LEVELS[0]):
		return super(MailingLists, self).update(pk, data=locals())
