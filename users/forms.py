from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
User=get_user_model()

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder' : 'Enter your Username'}),
        error_messages = {
            'required' : "Username can't be empty."
        }
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Enter your Email"}),
        error_messages={
            'required': "Email can't be empty.",
            'invalid': "Введите корректный email адрес."
        }
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Enter your Password"}),
        error_messages={
            'required': "Password can't be empty",
        }
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Enter Confirm Password"}),
        error_messages={
            'required': "Password can't be empty",
        }
    )
    phone_number = PhoneNumberField(
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your Phone Number"})
    )
    class Meta:
        model=User
        fields=["username","phone_number","email","password","confirm_password"]

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'}),
        error_messages={
            'required': "Username can't be empty."
        }
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Enter your Password"}),
        error_messages={
            'required': "Password can't be empty",
        }
    )
