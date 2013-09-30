import web
import api

render = web.template.render('api/templates/')

urls = (
  '/v1/spendings/([0-9]+)', 'Spendings'
)

web.config.debug = False

class Spendings(api.action.Action):
	def POST(self, spendingId):
		
		self.__checkSpendingExists(spendingId)
		
		inputParams = web.input(
			date=None, 
			spendingName=None, 
			amount=None, 
			amountEncrypted=None, 
			_method='post'
		)
		
		spending = api.spending.Spending();
		
		spendingId = spending.add(**{
			'userId': self.getAuthUserId(),
			'date': inputParams.date,
			'spendingName': inputParams.spendingName,
			'amount': inputParams.amount,
			'amountEncrypted': inputParams.amountEncrypted
		});
		
		return self.prepareResult({"spendingId": spendingId})
	
	def GET(self):
		
		inputParams = web.input(dateBegin=None, dateEnd=None, _method='get')
		
		spending = api.spending.Spending()
		list = spending.getList(
			self.getAuthUserId(), 
			dateBegin = inputParams.dateBegin, 
			dateEnd = inputParams.dateEnd
		)
		
		return self.prepareResult({'spendings': list})
	
	def PATCH(self, spendingId):
		
		self.__checkSpendingExists(spendingId)
		
		inputParams = web.input(_method='post')
		
		spending = api.spending.Spending()
		updated = spending.update(spendingId, self.getAuthUserId(), **inputParams)
		
		return self.prepareResult({'updated': updated})
	
	def DELETE(self, spendingId):
		
		self.__checkSpendingExists(spendingId)
		
		spending = api.spending.Spending()
		deleted = spending.delete(spendingId, self.getAuthUserId())
		
		return self.prepareResult({'deleted': deleted})
	
	def __checkSpendingExists(self, spendingId):
		spending = api.spending.Spending()
		if not spending.isExists(spendingId, spendingId):
			raise api.exception.NotFound('spending not found')
		

class User(api.action.Action):
	
	def GET(self):
		
		spending = api.spending.Spending();
		spending.add(**{
			'userId': 1,
			'date': '2013-09-23',
			'spendingName': 'kkkkk',
			'amount': 9,
			'amountEncrypted': '', 
		});
		
		return 'OK'
	

	
	
	
class index:
	def GET(self):
		db = web.database(dbn='mysql', user='myWalletApi', pw='xK7YfmKKTXEzpfJ6', db='myWalletApi')
		spendingNames = db.select('spendingName')
		return render.index(spendingNames)

class add:
	def POST(self):
		db = web.database(dbn='mysql', user='myWalletApi', pw='xK7YfmKKTXEzpfJ6', db='myWalletApi')
		i = web.input()
		n = db.insert('spendingName', name=i.name)
		raise web.seeother('/')


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
		
		
		
		
		
	   