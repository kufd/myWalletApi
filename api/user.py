__all__ = ["User",]

import web
import hashlib
from db import connection as db


class User:
	
	__table = "users"
	__fields = ('id', 'login', 'name', 'email', 'password', 'lang', 'currency', 'useEncryption', 'dateRegistration', 'role')
	__fieldsRequiredForInsert = ('login', 'name', 'email', 'password', 'lang', 'currency', 'useEncryption')
	__fieldsUpdateAllowed = ('name', 'email', 'password', 'lang', 'currency', 'useEncryption', 'user')
		
	def create(self, **fields):

		self.__checkIsFieldsExists(**fields)
		self.__checkIsRequiredFieldsForInsertExists(**fields)

		fields['password'] = self.__getPasswordHash(fields['password'])
		fields['dateRegistration'] = web.SQLLiteral("NOW()")
		userId = db.insert(self.__table, **fields)
		return userId
		
	def update(self, login, currentPassword, **fields):
		
		self.__checkIsFieldsExists(**fields)
		self.__checkIsFieldsAllowedForUpdate(**fields)
		
		if 'password' in fields:
			fields['password'] = self.__getPasswordHash(fields['password'])
		
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
			
	def __getPasswordHash(self, password):
		return hashlib.md5(hashlib.md5(password).hexdigest()).hexdigest()
				
	def getByLoginAndPassword(self, login, password):
		
		''' Method returns user id if user exists or False otherwise '''
		
		result = None
		
		if login and password: 
			password = self.__getPasswordHash(password)
			myvar = dict(login=login, password=password)
			users = db.select(self.__table, myvar, where="login = $login AND password = $password")
			if len(users) == 1:
				result = users[0]
			
		return result
	
	def isLoginExists(self, login):
		
		result = db.query("SELECT COUNT(*) AS foundLoginNumber FROM "+self.__table+" WHERE login='"+login+"'")
		return result[0].foundLoginNumber == 1
	
	def isEmailExists(self, email):
		
		result = db.query("SELECT COUNT(*) AS foundEmailNumber FROM "+self.__table+" WHERE email='"+email+"'")
		return result[0].foundEmailNumber == 1
		
