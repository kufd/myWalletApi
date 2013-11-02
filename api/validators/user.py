__all__ = ["post",]

import re
from exception import *
from voluptuous import *
from collections import defaultdict
from api.user import *

errors = {
	101 : 'Length of login must be greater than 5 and less than 50',
	102 : 'Length of name must be greater than 2 and less than 100',
	103 : 'Wrong lang code. Allowed: en, ua',
	104 : 'Wrong email',
	105 : 'Empty password',
	106 : 'Empty password confirmation',
	107 : 'Parameter useEncryption can be 1 or 0 only',
	108 : 'Required key not exists',
	109 : 'This login exists yet',
	110 : 'This email exists yet',
	111 : 'Password and its confirmation are not equal' ,
}


	


def post(fields):

	# ---------- valitate functions ---------- 
	def validatePassword(password):
		if password != fields['confirmPassword']:
			raise Invalid("111")
		else:
			return password
		
	def validateEmail(email):
		pattern = '[\.\w]{1,}[@]\w+[.]\w+'
		user = User()
	
		if not re.match(pattern, email):
			raise Invalid("104")
		elif user.isEmailExists(email):
			raise Invalid("110")
		else:
			return email
	
	def validateLogin(login):
		user = User()
		if user.isLoginExists(login):
			raise Invalid("109")
		else:
			return login
	
	def validateLang(lang):
		if lang not in ('ua', 'en'):
			raise Invalid("103")
		else:
			return lang
		
	def validateUseEncryption(useEncryption):
		if useEncryption not in ('0', '1'):
			raise Invalid("107")
		else:
			return useEncryption
	# ---------------------------------------- 

	try:
		schema = voluptuous.Schema(
			{
				'login': voluptuous.All(
					unicode, 
					voluptuous.Length(min=5, max=50, msg='101'),
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
		if 'required key not provided' in e.msg:
			raise InternalError(errors[108] + '. Key: ' + str(e.path).replace("['", '"').replace("']", '"'), 108)
		raise InternalError(errors[int(e.error_message)], e.error_message)
		
