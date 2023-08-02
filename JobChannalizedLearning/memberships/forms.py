from .models import Membership
from django import forms

class Membership_form(forms.ModelForm):
    class Meta:
        model = Membership
        fields =['membership']