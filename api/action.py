import web
import re
import base64
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
			raise Unauthorized
	
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