__all__ = ["User",]

import web
from db import connection as db


class User:
	
	__table = "users"
	__fields = ('id', 'login', 'name', 'email', 'password', 'lang', 'currency', 'useEncryption', 'dateRegistration', 'role')
	__fieldsRequiredForInsert = ('login', 'name', 'email', 'password', 'lang', 'currency', 'useEncryption')
	__fieldsUpdateAllowed = ('name', 'email', 'password', 'lang', 'currency', 'useEncryption', 'user')
		
	def create(self, **fields):

		self.__checkIsFieldsExists(**fields)
		self.__checkIsRequiredFieldsForInsertExists(**fields)

		fields['dateRegistration'] = web.SQLLiteral("NOW()")
		userId = db.insert(self.__table, **fields)
		return userId
		
	def update(self, login, currentPassword, **fields):
		
		self.__checkIsFieldsExists(**fields)
		self.__checkIsFieldsAllowedForUpdate(**fields)
		
		where = "`login` = '"+login+"'"
		db.update(self.__table, where, **fields)
		
	def __checkIsFieldsAllowedForUpdate(self, **fields):
		
		for field in fields:
			if not field in self.__fieldsUpdateAllowed:
				raise Exception, 'Field "'+field+'" is not allowed for update'
	
	def __checkIsFieldsExists(self, **fields):
		
		for field in fields:
			if not field in self.__fields:
				raise Exception, 'Field "'+field+'" not exists'
			
	def __checkIsRequiredFieldsForInsertExists(self, **fields):
		
		for field in self.__fieldsRequiredForInsert:
			if not field in fields:
				raise Exception, 'Field "'+field+'" required for insert not exists'
				
	def getByLoginAndPassword(self, login, password):
		
		''' Method returns user id if user exists or False otherwise '''
		
		result = False
		myvar = dict(login=login, password=password)
		users = db.select(self.__table, myvar, where="login = $login AND password = $password")
		if len(users) == 1:
			result = users[0].id
			
		return result
		
