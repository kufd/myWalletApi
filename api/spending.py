import web
from db import connection as db


class Spending:
	
	__table = "spendings"
	__fields = ('id', 'userId', 'date', 'spendingNameId', 'amount', 'amountEncrypted')
	__fieldsUpdateAllowed = ('date', 'spendingNameId', 'amount', 'amountEncrypted')
	
	__encryptionKey = None
		
	def add(self, **fields):

		spendingName = SpendingName()
		fields['spendingNameId'] = spendingName.getIdByName(fields['spendingName'])
		del fields['spendingName']
		
		self.__checkIsFieldsExists(**fields)

		fields = self.__encryptData(**fields)

		spendingId = db.insert(self.__table, **fields)
		return spendingId
		
	def update(self, id, userId, **fields):
		
		if 'spendingName' in fields:
			spendingName = SpendingName()
			fields['spendingNameId'] = spendingName.getIdByName(fields['spendingName'])
			del fields['spendingName']
		
		self.__checkIsFieldsExists(**fields)
		self.__checkIsFieldsAllowedForUpdate(**fields)
		
		fields = self.__encryptData(**fields)
		
		where = "`id` = '"+str(id)+"' AND `userId` = '"+str(userId)+"'"
		updatedRowsNum = db.update(self.__table, where, **fields)
		
		return updatedRowsNum == 1
		
	def getList(self, userId, dateBegin = None, dateEnd = None):
		
		where = self.__table + ".userId = " + str(userId)
		if dateBegin:
			where += " AND " + self.__table + ".date >= '" + dateBegin + "'"
		if dateEnd:
			where += " AND " + self.__table + ".date <= '" + dateEnd + "'"
			
		spendingName = SpendingName()
		
		
		fieldsToSelect = []
		for field in self.__fields:
			if field not in ['amountEncrypted']:
				if self.__encryptionKey and field == 'amount':
					fieldsToSelect.append(str("AES_DECRYPT(" + self.__table + ".amountEncrypted, "+web.db.sqlquote(self.__encryptionKey)+") AS amount "))
				else:
					fieldsToSelect.append(self.__table + "." + field)
		fieldsToSelect.append(spendingName.getTableName() + ".name AS spendingName") 
 		
 		fieldsToSelect = ', '.join(fieldsToSelect)
		
		spendings = db.query(
			"SELECT " + fieldsToSelect + "\
			FROM " + self.__table + " \
			JOIN " + spendingName.getTableName() + " ON " + self.__table + ".spendingNameId = " + spendingName.getTableName() + ".id  \
			WHERE " + where
		)
		
		return spendings
	
	def isExists(self, id, userId):
		
		result = db.query("SELECT COUNT(*) AS foundSpendingsNumber FROM "+self.__table+" WHERE id='"+str(id)+"' AND userId='"+str(userId)+"'")
		return result[0].foundSpendingsNumber == 1
	
	def delete(self, id, userId):
		
		vars = dict(id=id, userId=userId)
		return db.delete(self.__table, vars=vars, where="id=$id AND userId=$userId") == 1
	
	def __encryptData(self, **fields):
		
		if self.__encryptionKey and 'amount' in fields:
			fields['amountEncrypted'] = web.SQLLiteral("AES_ENCRYPT("+web.db.sqlquote(fields['amount'])+", "+web.db.sqlquote(self.__encryptionKey)+")")
			del fields['amount']
		
		return fields
		
	
	def setEncryptionKey(self, encryptionKey):
		self.__encryptionKey = encryptionKey
	
	def __checkIsFieldsAllowedForUpdate(self, **fields):
		
		for field in fields:
			if not field in self.__fieldsUpdateAllowed:
				raise Exception, 'Field "'+field+'" is not allowed for update'
		
	def __checkIsFieldsExists(self, **fields):
		
		for field in fields:
			if not field in self.__fields:
				raise Exception, 'Field "'+field+'" not exists'
			
	def getTopSpendings(self, userId, limit = 10):
		
		spendingName = SpendingName()
		
		spendingsNames = db.query(
			"SELECT "+
				spendingName.getTableName()+".name "+
			"FROM "+self.__table+" "+
			"JOIN " + spendingName.getTableName() + " ON " + self.__table + ".spendingNameId = " + spendingName.getTableName() + ".id  "+
			"WHERE "+
				self.__table+".userId='"+str(userId)+"' "+
			"GROUP BY "+self.__table+".spendingNameId \
			ORDER BY COUNT(*) DESC\
			LIMIT "+str(limit)
		)
		
		result = list()
		
		for spendingsName in spendingsNames:
			result.append(spendingsName.name)
		
		return result
	
	def updateEncryptedData(self, userId, oldKey, newKey):
		"""
		This method must be called when user's password is changing
		Or when encryption option for user is changing
		if oldKey or newKey is None it means than amount was not encrypted or will not be encrypted
		"""
		amount = '';
		updateExpression = '';

		if oldKey == None:
			amount = 'amount'
		else:
			amount = "AES_DECRYPT(amountEncrypted, "+web.db.sqlquote(oldKey)+")"

		if newKey != None:
			amount = "AES_ENCRYPT("+amount+", "+web.db.sqlquote(newKey)+")"
			updateExpression = "SET amountEncrypted = "+amount+", amount = 0"
		else:
			updateExpression = "SET amount = "+amount+", amountEncrypted = ''"

		spendingsNames = db.query(
			"UPDATE "+self.__table+" \
			"+updateExpression+" \
			WHERE userId = '"+str(userId)+"'"
		)

class SpendingName:
	
	__table = "spendingName"
	__fields = ('id', 'name')
	
	def getTableName(self):
		return self.__table
	
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
	
	def getForAutocomplete(self, name, limit=10):
		
		spendingsNames = db.query(
			"SELECT  name \
			FROM "+self.__table+" \
			WHERE \
				name LIKE '"+str(name)+"%' \
			ORDER BY id\
			LIMIT "+str(limit)
		)
		
		result = list()
		
		for spendingsName in spendingsNames:
			result.append(spendingsName.name)
		
		return result
