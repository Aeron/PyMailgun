# coding: utf-8
import json
from .api import MailgunAPI


class Messages(MailgunAPI):
	API_NAME = 'messages'

	def create(self, from_address, to, subject, text, html=None, cc=None, bcc=None, attachment=None, inline=None, o=None, h=None, v=None, recipient_variables=None):
		data = [
			('from', from_address),
			('subject', subject),
			('text', text),
			('html', html),
			('attachment', attachment),
			('inline', inline),
			('recipient-variables', recipient_variables)
		]
		for k, v in dict(to=to, cc=cc, bcc=bcc).iteritems():
			data.append(
				(k, ", ".join(v) if v and isinstance(v, (list, tuple)) else v)
			)
		for k, v in dict(o=o, h=h, v=v).iteritems():
			if isinstance(v, (list, tuple)):
				data.extend(
					map(lambda p: ("{name}:{key}".format(name=k, key=p[0]), p[1]), v)
				)
			elif isinstance(v, dict):
				data.extend(
					map(lambda p: ("{name}:{key}".format(name=k, key=p[0]), p[1]), v.iteritems())
				)
		return self._request('post', data=data)


# class MessagesMime(MailgunAPI):
# 	API_NAME = 'messages.mime'
