import web
from db import connection as db


class Spending:
	
	__table = "spendings"
	__fields = ('id', 'userId', 'date', 'spendingNameId', 'amount', 'amountEncrypted')
		
	def add(self, **fields):

		spendingName = SpendingName()
		fields['spendingNameId'] = spendingName.getIdByName(fields['spendingName'])
		del fields['spendingName']
		
		self.__checkIsFieldsExists(**fields)

		spendingId = db.insert(self.__table, **fields)
		return spendingId
		
	def update(self, id, userId, **fields):
		
		self.__checkIsFieldsExists(**fields)
		
		where = "`id` = '"+id+"' AND `userId` = '"+userId+"'"
		db.update(self.__table, where, **fields)
		
	def __checkIsFieldsExists(self, **fields):
		
		for field in fields:
			if not field in self.__fields:
				raise Exception, 'Field "'+field+'" not exists'
	
class SpendingName:
	
	__table = "spendingName"
	__fields = ('id', 'name')
	
	def __add(self, **fields):

		self.__checkIsFieldsExists(**fields)

		spendingId = db.insert(self.__table, **fields)
		return spendingId
		
	def __checkIsFieldsExists(self, **fields):
		
		for field in fields:
			if not field in self.__fields:
				raise Exception, 'Field "'+field+'" not exists'
	
	def getIdByName(self, name):
		
		''' Method returns user id if user exists or False otherwise '''
		
		searchParams = dict(name=name)
		foundNames = db.select(self.__table, searchParams, where="name = $name")
		if len(foundNames) == 1:
			result = foundNames[0].id
		else:
			result = self.__add(**{'name': name,});
			
		return result
