#!/usr/bin/env python

import pycurl
import requests

def addSpending():
	
	postData =  'date=2013-09-23&spendingName=hhhh&amount=20&amountEncrypted='
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/spendings/')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, postData)
	c.setopt(pycurl.USERPWD, 'test1:test1')
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print


def getSpendings():
	
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/spendings?dateBegin=2013-09-23&dateEnd=2013-11-23')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.USERPWD, 'test1:test1')
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print
	
def getTopSpendings():
	
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/spendings/top')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.USERPWD, 'test13:1')
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print
	
	
def getSpendingAutocomplete():
	
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/spendings/autocomplete/?name=fddf')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.USERPWD, 'test13:1')
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print

def updateSpending():
	
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/spendings/8')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
	c.setopt(pycurl.CUSTOMREQUEST, "PATCH")
	c.setopt(pycurl.HTTPPOST, [('spendingNames', 'vvvv')])
	c.setopt(pycurl.USERPWD, 'test1:test1')
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print
		
def deleteSpending():
	
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/spendings/8')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
	c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
	c.setopt(pycurl.USERPWD, 'test1:test1')
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print
		
		
def getAuthUser():
	
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/auth-users/')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.USERPWD, 'test1:test1')
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print
	
	
def registerUser():
	postData =  'login=test11&name=hhhh&email=test7@ub.ua1&password=1&confirmPassword=&lang=ua&currency=&useEncryption=1'
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/users/')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, postData)
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print
	
def patchUser():
	
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/users/test13/')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.HTTPHEADER, ['Content-Type : application/x-www-form-urlencoded'])
	c.setopt(pycurl.CUSTOMREQUEST, "PATCH")
	c.setopt(pycurl.USERPWD, 'test13:123456')
	c.setopt(pycurl.HTTPPOST, [('name', 'name1'), ('password', '123456')])
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	
	print
	print
	
def getReportGroupBySpengingName():
	
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/reports/group-by-spending-name/?dateBegin=2013-09-23&dateEnd=2014-11-23')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.USERPWD, 'kufd:paralelepiped')
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print
	
def getReportAmountByPeriod():
	
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/v1/reports/amount-by-period/?period=month&dateBegin=2013-09-23&dateEnd=2014-11-23')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.USERPWD, 'kufd:paralelepiped')
	c.setopt(c.VERBOSE, True)
	c.perform()
	
	print
	print
		
#addSpending()	
getReportAmountByPeriod()




