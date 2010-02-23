import re
from django import http
from django.contrib.admin import actions
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.utils.functional import update_wrapper
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.decorators.cache import never_cache
from django.conf import settings

from django.contrib.admin import sites
from django.contrib import admin

class CustomAdminSite(sites.AdminSite):
    def login(self, request):
        """
        This is a override version of login to displays the login form for the given HttpRequest.
        It remove username validation to e-mail e catch ValueError from authenticate method. 		
        """
        from django.contrib.auth.models import User

        # If this isn't already the login page, display it.
        if not request.POST.has_key(sites.LOGIN_FORM_KEY):
            if request.POST:
                message = _("Please log in again, because your session has expired.")
            else:
                message = ""
            return self.display_login_form(request, message)

        # Check that the user accepts cookies.
        if not request.session.test_cookie_worked():
            message = _("Looks like your browser isn't configured to accept cookies. Please enable cookies, reload this page, and try again.")
            return self.display_login_form(request, message)
        else:
            request.session.delete_test_cookie()

        # Check the password.
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        try:
            user = authenticate(username=username, password=password)
        except ValueError, verr:
            return self.display_login_form(request, verr)
			
        if user is None:
            message = sites.ERROR_MESSAGE
            if username is not None and u'@' in username:
            	# Mistakenly entered e-mail address instead of username? Look it up.
            	try:
            		user = User.objects.get(email=username)
            	except (User.DoesNotExist, User.MultipleObjectsReturned):
            		message = _("Usernames cannot contain the '@' character.")
            else:
            	if user.check_password(password):
            		message = _("Your e-mail address is not your username."
            						" Try '%s' instead.") % user.username
            	else:
            		message = _("Usernames cannot contain the '@' character.")
            return self.display_login_form(request, message)

        # The user data is correct; log in the user in and continue.
        else:
            if user.is_active and user.is_staff:
                login(request, user)
                return http.HttpResponseRedirect(request.get_full_path())
            else:
                return self.display_login_form(request, sites.ERROR_MESSAGE)
    login = never_cache(login)