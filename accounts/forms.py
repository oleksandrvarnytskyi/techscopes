from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Please input a valid email address.'
    )
    birth_date = forms.DateField(
        help_text='Not required. Format: YYYY-MM-DD'
    )
    country = forms.CharField(
        max_length=30,
        help_text='Not required. Not required. 30 characters or fewer'
    )
    city = forms.CharField(
        max_length=30,
        help_text='Not required. 30 characters or fewer'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'birth_date',
            'country',
            'city'
        )
