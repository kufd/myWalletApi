#!/usr/bin/env python

import pycurl

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
		
#addSpending()	
getAuthUser()




