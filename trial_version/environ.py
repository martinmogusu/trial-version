from decouple import config

def get_environ(key):
	value = config(key)
	return value
