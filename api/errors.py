__all__ = ["getMessage",]

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
	111 : 'Password and its confirmation are not equal',
	112 : 'Wrong password',
	113 : 'New password and its confirmation are not equal',
	
	114 : 'Length of name of spending must be greater than 1 and less than 255',
	115 : 'Amount of spending must be float number',
}

def getMessage(code):
	return errors[code]