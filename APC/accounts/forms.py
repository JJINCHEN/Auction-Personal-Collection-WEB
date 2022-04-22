# coding:utf-8
from django import forms
from .models import UserProfile


# Login form
class LoginForm(forms.Form):
    # Judge user name submitted by user
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Username", "required": "required", "id": "user", "name": "username"}),
        max_length=50, error_messages={"required": "Username not null", })
    # Judge the password submitted by the user
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Passward", "required": "required", "id": "password", "name": "password"}),
        max_length=20, error_messages={"required": "Password cannot be empty", })


# Register form
class RegForm(forms.Form):
    # Judge user name submitted by user
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "User Name", "required": "required", }),
                               max_length=50, error_messages={"required": "The user name cannot be empty", })
    # Judge the email submitted by the user
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required", }),
                             max_length=50, error_messages={"required": "The mail cannot be empty", })
    # Judge the password submitted by the user
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required", }),
                               max_length=20, error_messages={"required": "The password cannot be empty", })
    # Judge the re-password submitted by the user
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password", "required": "required", }),
        max_length=20, error_messages={"required": "The Confirm password cannot be blank", })

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('All fields are required')
        elif self.cleaned_data['confirm_password'] != self.cleaned_data['password']:
            raise forms.ValidationError('Entered passwords differ')
        else:
            cleaned_data = super(RegForm, self).clean()
        username = self.cleaned_data['username']
        is_email_exist = UserProfile.objects.filter(email=username).exists()
        is_username_exist = UserProfile.objects.filter(username=username).exists()
        if is_username_exist or is_email_exist:
            raise forms.ValidationError(u"The account has been registered")

        return cleaned_data
