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
            'invalid': "Please enter a valid email address."
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
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Confirm your Password"}),
        error_messages={
            'required': "Password confirmation can't be empty",
        }
    )
    phone = PhoneNumberField(
        label="Phone Number",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your Phone Number (optional)"})
    )
    
    class Meta:
        model = User
        fields = ["username", "email", "phone"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username


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
