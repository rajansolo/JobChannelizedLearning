from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from user_account.models import User


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    user_choices = [
        ('STUDENT', 'Student'),
        ('MENTOR', 'Mentor'),
    ]
    user_role = forms.ChoiceField(choices=user_choices,widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ("email", "user_role", "username", "password1", "password2")


class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username","password")

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            user_password = self.cleaned_data['password']
            if not authenticate(username=username,password=user_password):
                raise forms.ValidationError("Username Or Password is incorrect.")
