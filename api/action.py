import web
import re
import base64
import json
import decimal
import datetime
from user import *
from exception import *

class Action:
	
	__login = None
	__password = None
	__auth_user_id = None
	
	def __init__(self):
		
		self.__parseAuthData()
		
		user = User()
		self.__auth_user_id = user.getByLoginAndPassword(self.getLogin(), self.getPassword())
		
		if self.__auth_user_id == False:
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
		return self.__auth_user_id
	
	def prepareResult(self, result):
		return json.dumps(result, cls=CustomJsonEncoder)

class CustomJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, decimal.Decimal):
			return float(obj)
		elif isinstance(obj, web.utils.IterBetter):
			return list(obj)
		elif isinstance(obj, web.utils.Storage):
			return dict(obj)
		elif isinstance(obj, datetime.date):
			return obj.isoformat()
		# Let the base class default method raise the TypeError
		return json.JSONEncoder.default(self, obj)
