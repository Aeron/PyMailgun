# coding: utf-8
import json
from .api import MailgunAPI
from .exceptions import MailgunValidationError


class MailingListMembers(MailgunAPI):
	API_NAME = 'lists'
	DOMAIN_FREE = True

	def all(self, subscribed=None, limit=100, skip=0):
		return super(MailingListMembers, self).all(params=dict(
			subscribed=subscribed,
			limit=limit,
			skip=skip
		))

	def create(self, address, name=None, vars=None, subscribed=True, upsert=False):
		return super(MailingListMembers, self).create(data=dict(
			address=address,
			name=name,
			vars=json.dumps(vars) if vars else None,
			subscribed=subscribed,
			upsert=upsert
		))

	def update(self, pk, address=None, name=None, vars=None, subscribed=True):
		return super(MailingListMembers, self).update(pk, data=dict(
			address=address,
			name=name,
			vars=json.dumps(vars) if vars else None,
			subscribed=subscribed
		))

	def bulk(self, members, subscribed=True, upsert=False):
		if not isinstance(members, (list, set, tuple)):
			raise MailgunValidationError(message='The `members` must be list, tuple or set.')
		self._sub = 'members.csv'
		return self._request('post', data=dict(
			subscribed=subscribed,
			upsert=upsert
		), files=dict(
			members=('list.csv', "\n".join(members))
		))


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
		return super(MailingLists, self).all(params=dict(
			address=address
		))

	def create(self, address, name=None, description=None, access_level=ACCESS_LEVELS[0]):
		return super(MailingLists, self).create(data=dict(
			address=address,
			name=name,
			description=description,
			access_level=access_level
		))

	def update(self, pk, address=None, name=None, description=None, access_level=ACCESS_LEVELS[0]):
		return super(MailingLists, self).update(pk, data=dict(
			address=address,
			name=name,
			description=description,
			access_level=access_level
		))
