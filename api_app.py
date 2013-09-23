import web
import api

render = web.template.render('api/templates/')

urls = (
  '/', 'User',
  '/add', 'add'
)

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
	
	def UPDATE(self):
		
		user = api.user.User()
		user.update(
			'test2', 
			'', 
			**{
				'id': 'test3567', 
			}
		)
		
		return "OK"
	
	def POST(self):
		
		#get_input = web.input(_method='get')
		#post_input = web.input(_method='post')
		
		user = api.user.User()
		userId = user.create(**{
			'login': 'test4', 
			'name': 'test1', 
			'email': 'test4', 
			'password': 'test1', 
			'lang': 'ua', 
			'currency': 'usd', 
			'useEncryption': '1',
		})
		
		return userId
	
	
	
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
	app = web.application(urls, globals())
	app.run()   