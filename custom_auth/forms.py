from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class GoogleUserCreationForm(forms.ModelForm):
	email = forms.RegexField(label=_("Email"), max_length=70, regex=r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)',
        help_text = _("Required. 70 characters or fewer following a valid e-mail format."),
        error_message = _("This value must contain a valid e-mail format."))

	def clean_email(self):
		email = self.cleaned_data["email"]
		try:
			username = email[:email.find("@")]
			User.objects.get(username=username)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError(_("A user with that e-mail already exists."))

		
	def save(self, commit=True):
		user = super(EleicoesUserCreationForm, self).save(commit=False)
		# dummy password
		user.set_password("none")
		# getting username from e-mail
		username = self.cleaned_data["email"]
		username = username[:username.find("@")]
		user.username=username
		if commit:
			user.save()
		return user
	
	class Meta:
		model = User
		fields = ("email",)
	
class GoogleUserChangeForm(forms.ModelForm):
	email = forms.RegexField(label=_("Email"), max_length=70, regex=r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)',
        help_text = _("Required. 70 characters or fewer following a valid e-mail format."),
        error_message = _("This value must contain a valid e-mail format."))
    
	class Meta:
		model = User