from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import ugettext as _
import gdata.contacts
import gdata.contacts.service

class GoogleAuthenticator(ModelBackend):
	def __init__(self):
		"""Constructor responsible to initialize Google Contacts Authentication Service."""
		self.google_service = gdata.contacts.service.ContactsService()
		
	def authenticate(self, username=None, password=None):
		user = None
		
		if self.call_google_programmatic_login(username, password):
			try:
				user = User.objects.get(email=username)
			except User.DoesNotExist:
				# crate default user if he doens't exists
				totalUsers = User.objects.count()
				if totalUsers == 0:
					user = self.create_default_super_user(username)
				if user is None:		
					raise ValueError(_("Please enter with a registered Google account."))
			return user
		return None
	
	def call_google_programmatic_login(self, google_account=None, password=None):
		""" Authenticate using a Google Account	"""
		try:
			self.google_service.email = google_account
			self.google_service.password = password
			self.google_service.source = 'GoogleProgrammaticApp'
			self.google_service.ProgrammaticLogin()
			return True
		except gdata.service.BadAuthentication:
			raise ValueError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
		except gdata.service.CaptchaRequired:
			raise ValueError(_("Your account was locked at Google. Please, login first at Gmail page before try again."))
		
		return False
			
	def create_default_super_user(self, email=None):
		username = email[:email.find("@")]
		user = User.objects.create_user(username, email, 'None')
		user.email=email
		user.first_name="System"
		user.last_name="Administrator"
		user.is_staff = True
		user.is_active = True
		user.is_superuser = True
		user.save()
		return user

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None