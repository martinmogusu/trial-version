from __future__ import unicode_literals
from django.urls import reverse
from django.test import TestCase
from trial_version.environ import *

class EnvironTestCase(TestCase):

	def test_environ(self):
		val = get_environ('TEST_CREDENTIAL')
		self.assertEqual(val, '12345')