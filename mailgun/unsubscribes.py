# coding: utf-8
from .api import MailgunAPI


class Unsubscribes(MailgunAPI):
	API_NAME = 'unsubscribes'

	def all(self, limit=100, skip=0):
		return super(Unsubscribes, self).all(params=locals())

	def get(self, address):
		return super(Unsubscribes, self).get(address)

	def create(self, address, tag='*'):
		return super(Unsubscribes, self).create(data=locals())

	def delete(self, address_or_id):
		"""Removes an address from the unsubscribes table. Address defines which events to delete.
		Can be one of two things:
		- an email address: all unsubscribe events for that email address will be removed;
		- id string: deletes a specific event.
		"""
		return super(Unsubscribes, self).delete(address_or_id)
