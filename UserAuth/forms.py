from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150,widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username","style":"width:360px;margin-left:38%;"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password","style":"width:360px;margin-left:38%;"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm Password","style":"width:360px;margin-left:38%;"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Email","style":"width:360px;margin-left:38%;"}))

    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError(e.messages[0])

        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one capital letter.')

        if not any(char in '!@#$%^&*()-_+={}[]:;?/~' for char in password):
            raise ValidationError('Password must contain at least one special character.')

        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        if confirm_password != self.cleaned_data.get('password'):
            raise ValidationError('Passwords do not match.')
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email address already registered.')
        return email
