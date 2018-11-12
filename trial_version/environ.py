from decouple import config
import os

def get_environ(key):
	value = os.environ(key)
	return value
