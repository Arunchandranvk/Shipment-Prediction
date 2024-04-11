from django import forms
from .models import *


class FeedForm(forms.ModelForm):
    class Meta:
        model =Feedback
        exclude = ['user']

