# coding: utf-8
import json
from .api import MailgunAPI


class MailingListMembers(MailgunAPI):
	API_NAME = 'lists'
	DOMAIN_FREE = True

	def all(self, subscribed=None, limit=100, skip=0):
		return super(MailingListMembers, self).all(params=locals())

	def create(self, address, name=None, vars=None, subscribed=True, upsert=False):
		data = locals()
		if data['vars']:
			data['vars'] = json.dumps(data['vars'])
		return super(MailingListMembers, self).create(data=locals())

	def update(self, pk, address=None, name=None, vars=None, subscribed=True):
		data = locals()
		if data['vars']:
			data['vars'] = json.dumps(data['vars'])
		return super(MailingListMembers, self).update(pk, data=locals())

	def bulk(self, members, subscribed=True, upsert=False):
		assert isinstance(members, (list, set, tuple)), 'The `members` must be list, tuple or set.'
		self._sub = 'members.csv'
		data = locals()
		del data['members']
		files = {
			# 'members': ('list.csv', self._prepare_members(members)),
			'members': ('list.csv', "\n".join(members)),
		}
		return self._request('post', data=data, files=files)

	# @staticmethod
	# def _prepare_members(members):  # there is no need to use csv module, data is simple enough
	# 	for n, member in enumerate(members):
	# 		if isinstance(member, (list, tuple)):
	# 			members[n] = "{1} <{0}>".format(member)
	# 	return "\n".join(members)


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
