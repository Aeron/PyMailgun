# coding: utf-8
INVALID_ERROR_MESSAGE = 'The `{0}` value is invalid. Available options: {1}.'


class MailgunError(Exception):
	pass


class MailgunValidationError(MailgunError):
	def __init__(self, value=None, options=None, message=None):
		if value and options:
			self.message = INVALID_ERROR_MESSAGE.format(value, str(options).strip('()[]'))
		else:
			self.message = message
		super(MailgunValidationError, self).__init__(message=self.message)
