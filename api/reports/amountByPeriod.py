__all__ = ["AmountByPeriod",]

import web
from db import connection as db
from api.spending import *

class AmountByPeriod:
	
	__encryptionKey = None
	__periods = ['week', 'month', 'year']
	
	def setEncryptionKey(self, encryptionKey):
		self.__encryptionKey = encryptionKey
		
	def getData(self, userId, period, spendingNameId = None, dateBegin = None, dateEnd = None):
		
		if not period in self.__periods:
			raise Exception('Wrong period')
		
		spendingName = SpendingName()
		spending = Spending()
		
		where = spending.getTableName() + ".userId = " + str(userId)
		if spendingNameId:
			where += " AND " + spending.getTableName() + ".spendingNameId = '" + spendingNameId + "'"
		if dateBegin:
			where += " AND " + spending.getTableName() + ".date >= '" + dateBegin + "'"
		if dateEnd:
			where += " AND " + spending.getTableName() + ".date <= '" + dateEnd + "'"
			
		fieldsToSelect = ['YEAR(date) AS year']
		if self.__encryptionKey:
			fieldsToSelect.append(str("ROUND(SUM(AES_DECRYPT(" + spending.getTableName() + ".amountEncrypted, "+web.db.sqlquote(self.__encryptionKey)+")), 2) AS amount "))
		else:
			fieldsToSelect.append("ROUND(SUM(" + spending.getTableName() + ".amount), 2)  AS amount")
 		
 		fieldsToGroup = ['YEAR(date)']
 		
 		if period != 'year':
  			fieldsToSelect.append('MONTH(date) AS month')
  			fieldsToGroup.append('MONTH(date)')
  			
  			if period != 'month':
 		  		fieldsToSelect.append('WEEKOFYEAR(date) AS week')
  			 	fieldsToGroup.append('WEEKOFYEAR(date)')
 		
		spendings = db.query(
			"SELECT " + (', '.join(fieldsToSelect)) + "\
			FROM " + spending.getTableName() + " \
			WHERE " + where + "\
			GROUP BY " + (', '.join(fieldsToGroup))
		)
		
		return spendings
		
