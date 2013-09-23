#!/usr/bin/env python

import pycurl

def getUserData():
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'http://0.0.0.0:8080/')
	c.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
	c.setopt(pycurl.VERBOSE, 0)
	c.setopt(pycurl.USERPWD, 'test1:test1')
	c.perform()
	
getUserData()