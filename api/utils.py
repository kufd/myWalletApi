import web
import json
import decimal
import datetime

''' Class  CustomJsonEncoder'''
class CustomJsonEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, decimal.Decimal):
			return float(obj)
		elif isinstance(obj, web.utils.IterBetter):
			return list(obj)
		elif isinstance(obj, web.utils.Storage):
			return dict(obj)
		elif isinstance(obj, datetime.date):
			return obj.isoformat()
		# Let the base class default method raise the TypeError
		return json.JSONEncoder.default(self, obj)