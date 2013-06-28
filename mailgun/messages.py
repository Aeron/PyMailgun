# coding: utf-8
from .api import MailgunAPI


class Messages(MailgunAPI):
	API_NAME = 'messages'

	def create(self, from_address, to, subject, text, html=None, cc=None, bcc=None, attachment=None, inline=None, o=None, h=None, v=None):
		for param in (to, cc, bcc):
			if param and isinstance(param, (list, tuple)):
				param = ", ".join(param)
		data = locals()
		data['from'] = data.pop('from_address')
		for param in (o, h, v):
			if param:
				for k, v in param.iteritems():
					data["o:%s" % k] = v
		return self._request('post', data=data)


# class MessagesMime(MailgunAPI):
# 	API_NAME = 'messages.mime'
