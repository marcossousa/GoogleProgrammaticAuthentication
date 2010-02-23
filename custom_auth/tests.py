import os
import re

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import Site, RequestSite
from django.contrib.auth.models import User
from django.contrib.auth.tests.views import AuthViewsTestCase
from django.test import TestCase
from django.core import mail
from django.core.urlresolvers import reverse
from backend import GoogleAuthenticator

class GoogleLoginTest(AuthViewsTestCase):
	urls = 'django.contrib.auth.tests.urls'

	def test_login_with_fake_login(self):
		try:
			self.client.login(username="fake", password="123")
			# this login must not work
		except ValueError, e:
			self.assertEquals(e.message, "Your account was locked at Google. Please, login first at Gmail page before try again.")

			
	def test_login_with_wrong_pass(self):
		try:
			self.client.login(username="testes@marcossousa.com", password="wrong")
			# this login must not work
		except ValueError, e:
			self.assertEquals(e.message, "Please enter a correct username and password. Note that both fields are case-sensitive.")

	def test_login_with_unregistered_user(self):
		try:
			self.client.login(username="testes@marcossousa.com", password="123change")
			# this login must not work
		except ValueError, e:
			self.assertEquals(e.message, "Please enter with a registered Google account.")
			
	def test_register_default_user(self):
		auth = GoogleAuthenticator()
		user = auth.create_default_super_user("testes@marcossousa.com")
		self.assertEquals(user.first_name, "System")
		self.assertEquals(user.last_name, "Administrator")
		self.assertEquals(user.email, "testes@marcossousa.com")
		self.assertEquals(user.username, "testes")
	
	def test_success_login(self):
		try:
			auth = GoogleAuthenticator()
			user = auth.create_default_super_user("testes@marcossousa.com")
			self.client.login(username="testes@marcossousa.com", password="123change")
			# this login must not work
		except ValueError, e:
			self.assertEquals(e.message, "Please enter a correct username and password. Note that both fields are case-sensitive.")
	