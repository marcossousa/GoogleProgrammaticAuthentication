from django.contrib.auth.forms import AuthenticationForm
from django.contrib import admin
from sites import CustomAdminSite

# Change username size at login page
AuthenticationForm.base_fields['username'].max_length = 75

# This will override Django default AdminSite implementation
admin.site = CustomAdminSite()