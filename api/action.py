import web
import re
import base64
import json
import validators
from user import *
from spending import *
from exception import *
from utils import *

''' Action  Action'''
class Action:
	
	__login = None
	__password = None
	__auth_user = None
	
	def __init__(self):
		
		#TODO FIX THIS HARDCODE
		if (web.ctx.env.get('PATH_INFO') != '/v1/users' and web.ctx.env.get('PATH_INFO') != '/v1/users/') or web.ctx.env.get('REQUEST_METHOD') != 'POST':
			self.__parseAuthData()
		
			user = User()
			self.__auth_user = user.getByLoginAndPassword(self.getLogin(), self.getPassword())
		
			if self.__auth_user == None:
				raise Unauthorized('Wrong login or password')
		
	
	def __parseAuthData(self):
		if self.__login == None or self.__password == None:
			auth_data = web.ctx.env.get('HTTP_AUTHORIZATION')
			if auth_data != None:
				auth_data = re.sub('^Basic ' ,'', auth_data)
				(self.__login,self.__password) = base64.decodestring(auth_data).split(':')
				self.__login = self.__login if self.__login != None else ''
				self.__password = self.__password if self.__login != None else ''
	
	def getLogin(self):
		return self.__login
		
	def getPassword(self):
		return self.__password
	
	def getAuthUserId(self):
		return self.__auth_user.id
	
	def getAuthUser(self):
		return self.__auth_user
	
	def prepareResult(self, result):
		return json.dumps(result, cls=CustomJsonEncoder)


''' Action  Spendings'''	
class Spendings(Action):
	def POST(self):
		
		inputParams = web.input(
			date=None, 
			spendingName=None, 
			amount=None, 
			amountEncrypted=None, 
			_method='post'
		)
		
		spending = Spending();
		
		if self.getAuthUser().useEncryption:
			spending.setEncryptionKey(self.getPassword())
		
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
		
		spending = Spending()
		
		if self.getAuthUser().useEncryption:
			spending.setEncryptionKey(self.getPassword())
		
		list = spending.getList(
			self.getAuthUserId(), 
			dateBegin = inputParams.dateBegin, 
			dateEnd = inputParams.dateEnd
		)

		return self.prepareResult({'spendings': list})
	
	def PATCH(self, spendingId):
		
		self.__checkSpendingExists(spendingId)
		
		inputParams = web.input(_method='post')
		
		spending = Spending()
		
		if self.getAuthUser().useEncryption:
			spending.setEncryptionKey(self.getPassword())
		
		updated = spending.update(spendingId, self.getAuthUserId(), **inputParams)
		
		return self.prepareResult({'updated': updated})
	
	def DELETE(self, spendingId):
		
		self.__checkSpendingExists(spendingId)
		
		spending = Spending()
		deleted = spending.delete(spendingId, self.getAuthUserId())
		
		return self.prepareResult({'deleted': deleted})
	
	def __checkSpendingExists(self, spendingId):
		spending = Spending()
		if not spending.isExists(spendingId, spendingId):
			raise NotFound('spending not found')
		

''' Action  AuthUsers'''	
class AuthUsers(Action):
	
	def GET(self):
		
		user = self.getAuthUser()
		
		if isinstance(user, User):
			del user['password']
		
		return self.prepareResult(user)
	
''' Action  User'''	
class Users(Action):
	
	def POST(self):
		
		inputParams = web.input(
			_method='post'
		)
		inputParams['useEncryption'] = int(inputParams['useEncryption']);
		
		validators.user.post(inputParams)
		
		user = User()
		userId = user.create(**inputParams)
		
		return self.prepareResult({"userId": userId})

		
