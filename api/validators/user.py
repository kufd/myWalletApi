__all__ = ["post","patch",]

import re
import api.errors
from exception import *
from voluptuous import *
from collections import defaultdict
from api.user import *


def processValidationException(e):
	if 'required key not provided' in e.msg:
		raise InternalError(api.errors.getMessage(108) + '. Key: ' + str(e.path).replace("['", '"').replace("']", '"'), 108)
	raise InternalError(api.errors.getMessage(int(e.error_message)), e.error_message)

# ---------- valitate functions ---------
def validateLang(lang):
	if lang not in ('ua', 'en'):
		raise Invalid("103")
	else:
		return lang

def validateEmail(email, ignoreUser=None):
	pattern = '[\.\w]{1,}[@]\w+[.]\w+'
	user = User()
	
	if not re.match(pattern, email):
		raise Invalid("104")
	elif user.isEmailExists(email, ignoreUser):
		raise Invalid("110")
	else:
		return email
	
def validateUseEncryption(useEncryption):
	if useEncryption not in ('0', '1'):
		raise Invalid("107")
	else:
		return useEncryption
# ---------------------------------------- 


def patch(fields):
	
	# ---------- valitate functions ---------
	def validatePassword(password):
		user = User()
		if not user.getByLoginAndPassword(fields['login'], fields['password']):
			raise Invalid("112")
		else:
			return password
		
	def validateNewPassword(newPassword):
		
		if newPassword and newPassword != fields['confirmNewPassword']:
			raise Invalid("113")
		else:
			return newPassword
		
	def validateEmailCustom(email):
		return validateEmail(email, fields['login'])
	# ---------------------------------------- 
	
	try:
		schema = voluptuous.Schema(
			{
				Required('login'): voluptuous.All(
					unicode, 
					voluptuous.Length(min=4, max=50, msg='101')
				),
				'name': voluptuous.All(
					unicode, 
					voluptuous.Length(min=2, max=100, msg='102')
				),
				'lang': validateLang,
			 	'email': validateEmailCustom,
			 	'useEncryption': validateUseEncryption,
			 	Required('password'): voluptuous.All(
					unicode, 
					voluptuous.Length(min=1, msg='105'),
					validatePassword
				),
				'newPassword': validateNewPassword,
			}, 
			extra=True
		)

		schema(fields)
	except MultipleInvalid as e:
		processValidationException(e)


def post(fields):

	# ---------- valitate functions ---------- 
	def validatePassword(password):
		if password != fields['confirmPassword']:
			raise Invalid("111")
		else:
			return password
		
	def validateLogin(login):
		user = User()
		if user.isLoginExists(login):
			raise Invalid("109")
		else:
			return login
	# ---------------------------------------- 

	try:
		schema = voluptuous.Schema(
			{
				'login': voluptuous.All(
					unicode, 
					voluptuous.Length(min=4, max=50, msg='101'),
					validateLogin
				),
				'name': voluptuous.All(
					unicode, 
					voluptuous.Length(min=2, max=100, msg='102')
				),
				'lang': validateLang,
			 	'email': validateEmail,
			 	'confirmPassword': voluptuous.All(
					unicode, 
					voluptuous.Length(min=1, msg='106')
				),
				'password': voluptuous.All(
					unicode, 
					voluptuous.Length(min=1, msg='105'),
					validatePassword
				),
				'useEncryption': validateUseEncryption,
			}, 
			extra=True, 
			required=True
		)

		schema(fields)
	except MultipleInvalid as e:
		processValidationException(e)
		
