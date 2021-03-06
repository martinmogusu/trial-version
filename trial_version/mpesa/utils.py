'''
General utilities for the MPESA functions
'''

from .exceptions import *
from trial_version.models import AccessToken
import requests
import json
from django.utils import timezone
from decouple import config, UndefinedValueError
import os

def mpesa_config(key):
	'''
	Gets Mpesa configuration variable with the matching key, otherwise returns MpesaConfigurationException
	
	Arguments:
		key {str} -- The configuration key
	'''

	try:
		value = config(key)
	except UndefinedValueError:
		raise MpesaConfigurationException('Mpesa environment not configured properly - ' + key + ' not found')

	return value


def api_base_url():
	'''
	Gets the base URL depending on the development environment (sandbox or production)
	'''

	mpesa_environment = mpesa_config('MPESA_ENVIRONMENT')

	if mpesa_environment == 'sandbox':
		return 'https://sandbox.safaricom.co.ke/'
	elif mpesa_environment == 'production':
		return 'https://api.safaricom.co.ke/'
	else:
		raise MpesaConfigurationException('Mpesa environment not configured properly - MPESA_ENVIRONMENT should be sandbox or production')

def generate_access_token_request(consumer_key = None, consumer_secret = None):
	'''
	Makes call to OAuth API
	'''

	url = api_base_url() + 'oauth/v1/generate?grant_type=client_credentials'
	consumer_key = consumer_key if consumer_key is not None else mpesa_config('MPESA_CONSUMER_KEY') 
	consumer_secret = consumer_secret if consumer_secret is not None else mpesa_config('MPESA_CONSUMER_SECRET')
	r = requests.get(url, auth=(consumer_key, consumer_secret))
	return r

def generate_access_token():
	'''
	Parses OAuth response to generate access token, then updates database access token value
	'''

	r = generate_access_token_request()
	token = json.loads(r.text)['access_token']

	AccessToken.objects.all().delete()
	access_token = AccessToken.objects.create(token=token)

	return access_token

def mpesa_access_token():
	'''
	Generates access token if the current one has expired or if token is non-existent
	Otherwise returns existing access token
	'''

	# access_token = generate_access_token()

	access_token = AccessToken.objects.first()
	if access_token == None:
		# No access token found
		access_token = generate_access_token()
	else:
		delta = timezone.now() - access_token.created_at
		minutes = (delta.total_seconds()//60)%60
		if minutes > 50:
			# Access token expired
			access_token = generate_access_token()	
	
	return access_token.token

def format_phone_number(phone_number):
	'''
	Formats phone number into the format 2547XXXXXXXX
	'''

	if len(phone_number) < 9:
		raise IllegalPhoneNumberException('Phone number too short')
	else:
		return '254' + phone_number[-9:]
