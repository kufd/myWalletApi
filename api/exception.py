
class AipiException(Exception):
	
	code = None
	message = None
	
	def __init__(self, code = None, message = None):
		if code :
			self.code = code
		if message :
			self.message = message
			
	def __str__(self):

		msg = str(self.code) if self.code else 'undefined code'
		msg += ' - '
		msg += self.message if self.message else 'undefined message'
		
		return msg
	
	def getCode(self):
		return self.code
	
	def getMessage(self):
		return self.message
	
class Unauthorized(AipiException):
	code = 401
	message = 'Unauthorized'