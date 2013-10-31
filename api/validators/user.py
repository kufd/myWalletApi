from exception import *
from voluptuous import *
from collections import defaultdict

errors = {
	101 : 'Length of login must be greater than 5',
	102 : 'Length of name must be greater than 2',
	103 : 'Wrong lang code',
	104 : 'Wrong email',
	105 : 'Empty password',
	106 : 'Empty password confirmation',
	107 : 'Parameter useEncryption can be 1 or 0 only',
	108 : 'Required key not exists',
}

def post(fields):

	try:
		schema = voluptuous.Schema(
			{
				'login': voluptuous.All(
					unicode, 
					voluptuous.Length(min=5), 
					msg = '101'
				),
				'name': voluptuous.All(
					unicode, 
					voluptuous.Length(min=2),
					msg = '102'
				),
				'lang': voluptuous.All(
					unicode, 
					voluptuous.Length(min=2, max=2),
					msg = '103'
				),
			 	'email': voluptuous.All(
					unicode, 
					voluptuous.Length(min=5),
					msg = '104'
				),
				'password': voluptuous.All(
					unicode, 
					voluptuous.Length(min=1),
					msg = '105'
				),
				'confirmPassword': voluptuous.All(
					unicode, 
					voluptuous.Length(min=1),
					msg = '106'
				),
				'useEncryption': voluptuous.All(
					int, 
					voluptuous.Range(min=0, max=1),
					msg = '107'
				),
			}, 
			extra=True, 
			required=True
		)

		schema(fields)
	except MultipleInvalid as e:
		if 'required key not provided' in e.msg:
			raise InternalError(errors[int(108)] + '. Key: ' + str(e.path).replace("['", '"').replace("']", '"'), 108)
		raise InternalError(errors[int(e.error_message)], e.error_message)
		
