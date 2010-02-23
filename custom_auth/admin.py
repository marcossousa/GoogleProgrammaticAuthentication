from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from GoogleProgrammaticAuthentication.custom_auth.forms import GoogleUserCreationForm, GoogleUserChangeForm
from django.utils.translation import ugettext, ugettext_lazy as _

class GoogleUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    form = GoogleUserChangeForm
    add_form = GoogleUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'email')

admin.site.unregister(User)
admin.site.register(User, GoogleUserAdmin)
