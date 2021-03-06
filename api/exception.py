import web
import json

class Unauthorized(web.Unauthorized):
    """`401 Unauthorized` error."""
    message = 'unauthorized'
    def __init__(self, message=None):
        status = "401 Unauthorized"
        headers = {'Content-Type': 'text/json'}
        message = json.dumps({'message': message or self.message})
        web.HTTPError.__init__(self, status, headers, message)
        
class InternalError(web.HTTPError):
    """500 Internal Server Error`."""
    message = "internal server error"
    
    def __init__(self, message=None, code = None):
        status = '500 Internal Server Error'
        headers = {'Content-Type': 'text/json'}
        message = {'message': message or self.message}
        if code:
        	message['code'] = code
        message = json.dumps(message)
        web.HTTPError.__init__(self, status, headers, message)
        

class NotFound(web.HTTPError):
	"""`404 Not Found` error."""
	message = "not found"
	def __init__(self, message=None):
		status = '404 Not Found'
		headers = {'Content-Type': 'text/json'}
		message = json.dumps({'message': message or self.message})
		web.HTTPError.__init__(self, status, headers, message)    
		
class Forbidden(web.HTTPError):
	"""`403 Forbidden` error."""
	message = "forbidden"
	def __init__(self, message=None):
		status = "403 Forbidden"
		headers = {'Content-Type': 'text/json'}
		message = json.dumps({'message': message or self.message})
		web.HTTPError.__init__(self, status, headers, message)    
