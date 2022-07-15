from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.utils.translation import gettext_lazy as _

class CyberstickAdminAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "class": 'form-control'
    }))    
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs=
        {"autocomplete": "current-password", 
        'class':'form-control',
        'placeholder':'Username'
        }),
    )
    
