import web
import api	
	
render = web.template.render('api/templates/')

urls = (
	'/v1/spendings/?', 'api.action.Spendings',
	'/v1/spendings/([0-9]+)/?', 'api.action.Spendings',
	'/v1/spendings/top/?', 'api.action.SpendingsTop',
	'/v1/spendings/autocomplete/?', 'api.action.SpendingsAutocomplete',
	'/v1/auth-users/', 'api.action.AuthUsers',
	'/v1/users/?', 'api.action.Users',
	'/v1/users/([^/]+)/?', 'api.action.Users',
	'/v1/reports/group-by-spending-name/?', 'api.action.ReportGroupBySpengingName',
	'/v1/reports/amount-by-period/?', 'api.action.ReportAmountByPeriod'
)

web.config.debug = False


	

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
	
app = web.application(urls, globals(), autoreload=False)
app.add_processor(errorProcessor)
	
if __name__ == "__main__":	
	app.run()
	
application = app.wsgifunc()
		
	
		
		
	   