from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


class RegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "email",
        ]


class UpdateBioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]

    bio = forms.CharField(widget=forms.Textarea(attrs={"rows": 4, "maxlength": 360}))
