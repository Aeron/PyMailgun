# coding: utf-8
import json
from .api import MailgunAPI


class Messages(MailgunAPI):
	API_NAME = 'messages'

	def create(self, from_address, to, subject, text, html=None, cc=None, bcc=None, attachment=None, inline=None, o=None, h=None, v=None, recipient_variables=None):
		for param in (to, cc, bcc):
			if param and isinstance(param, (list, tuple)):
				param = ", ".join(param)
		data = locals()
		data['from'] = data.pop('from_address')
		for param_name in ('o', 'h', 'v'):
			if data[param_name] and isinstance(data[param_name], dict):
				for k, v in data[param_name].iteritems():
					data["%s:%s" % (param_name, k)] = v
		data['recipient-variables'] = json.dumps(data.pop('recipient_variables'))
		return self._request('post', data=data)


# class MessagesMime(MailgunAPI):
# 	API_NAME = 'messages.mime'
