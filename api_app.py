import web
import api	
	
render = web.template.render('api/templates/')

urls = (
	'/v1/spendings/?', 'api.action.Spendings',
	'/v1/spendings/([0-9]+)/?', 'api.action.Spendings',
	'/v1/auth-users/', 'api.action.AuthUsers',
	'/v1/users/?', 'api.action.Users',
	'/v1/users/(.+)/?', 'api.action.Users'
)

web.config.debug = False


	

if __name__ == "__main__":	 
	
	def errorProcessor(handler): 
		
		result = ''
		
		try:
			result = handler() 
		except web.HTTPError as e:
			if e.__class__.__name__ == '_InternalError' :
				raise api.exception.InternalError
			else:
				raise e 
		return result
	
	app = web.application(urls, globals())
	app.add_processor(errorProcessor)
	app.run()
		
	
		
		
	   