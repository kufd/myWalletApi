__all__ = ["post",]

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

def post(fields):

	try:
		schema = voluptuous.Schema(
			{
				'spendingName': voluptuous.All(
					unicode, 
					voluptuous.Length(min=1, max=255, msg='114')
				),
				'amount': voluptuous.All(
					float, 
					msg='115'
				),
			}, 
			extra=True, 
			required=True
		)

		schema(fields)
	except MultipleInvalid as e:
		processValidationException(e)
		
