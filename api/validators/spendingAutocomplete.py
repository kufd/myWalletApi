__all__ = ["get",]

import api.errors
from exception import *
from voluptuous import *

def processValidationException(e):
	if 'required key not provided' in e.msg:
		raise InternalError(api.errors.getMessage(108) + '. Key: ' + str(e.path).replace("['", '"').replace("']", '"'), 108)
	raise InternalError(api.errors.getMessage(int(e.error_message)), e.error_message)

def get(fields):

	try:
		schema = voluptuous.Schema(
			{
				'name': voluptuous.All(
					unicode, 
					voluptuous.Length(min=2, max=255, msg='117')
				)
			}, 
			extra=True, 
			required=True
		)

		schema(fields)
	except MultipleInvalid as e:
		processValidationException(e)
		
