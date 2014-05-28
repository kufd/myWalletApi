__all__ = ["GroupBySpengingName",]

import web
from db import connection as db
from api.spending import *

class GroupBySpengingName:
	
	__encryptionKey = None
	
	def setEncryptionKey(self, encryptionKey):
		self.__encryptionKey = encryptionKey
		
	def getData(self, userId, dateBegin = None, dateEnd = None):
		
		spendingName = SpendingName()
		spending = Spending()
		
		where = spending.getTableName() + ".userId = " + str(userId)
		if dateBegin:
			where += " AND " + spending.getTableName() + ".date >= '" + dateBegin + "'"
		if dateEnd:
			where += " AND " + spending.getTableName() + ".date <= '" + dateEnd + "'"
			
		fieldsToSelect = ['spendingNameId']
		if self.__encryptionKey:
			fieldsToSelect.append(str("SUM(AES_DECRYPT(" + spending.getTableName() + ".amountEncrypted, "+web.db.sqlquote(self.__encryptionKey)+")) AS amount "))
		else:
			fieldsToSelect.append("SUM(" + spending.getTableName() + ".amount)  AS amount")
		fieldsToSelect.append(spendingName.getTableName() + ".name AS spendingName") 
 		
 		fieldsToSelect = ', '.join(fieldsToSelect)
		
		spendings = db.query(
			"SELECT " + fieldsToSelect + "\
			FROM " + spending.getTableName() + " \
			JOIN " + spendingName.getTableName() + " ON " + spending.getTableName() + ".spendingNameId = " + spendingName.getTableName() + ".id  \
			WHERE " + where + "\
			GROUP BY " + spending.getTableName() + ".spendingNameId"
		)
		
		return spendings
		
