from __future__ import unicode_literals
from django.urls import reverse
from django.test import TestCase
from trial_version.environ import *
from trial_version.mpesa.utils import *

class EnvironTestCase(TestCase):

	def test_environ(self):
		value = mpesa_config('TEST_CREDENTIAL')
		self.assertEqual(value, '12345')

	def test_oauth_correct_credentials(self):
		'''
		Test correct credentials sent to oauth endpoint
		'''

		r = generate_access_token_request()
		self.assertEqual(r.status_code, 200)

	def test_oauth_wrong_credentials(self):
		'''
		Test wrong credentials sent to OAuth endpoint
		'''

		consumer_key = 'wrong_consumer_key'
		consumer_secret = 'wrong_consumer_secret'
		r = generate_access_token_request(consumer_key, consumer_secret)
		self.assertEqual(r.status_code, 400) # Unauthorized

	def test_access_token_valid(self):
		'''
		Test that access token is never older than 50 minutes	
		'''

		token = generate_access_token()
		delta = timezone.now() - token.created_at
		minutes = (delta.total_seconds()//60)%60
		self.assertLessEqual(minutes, 50)