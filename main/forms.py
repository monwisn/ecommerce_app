from typing import List, Optional

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User

from .models import NewsletterUser


# Support Contact
class ContactForm(forms.Form):
    name: str = forms.CharField(label='Your Name', max_length=80)
    email: forms.EmailField = forms.EmailField(label='Your Email')
    subject: str = forms.CharField(max_length=150, label='Subject')
    message: str = forms.CharField(label='Your Message', widget=forms.Textarea, required=True, max_length=2500)
    captcha: ReCaptchaField = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')


class NewsletterUserForm(forms.ModelForm):
    class Meta:
        model: NewsletterUser = NewsletterUser
        fields: List[str] = ['email']

    def clean_email(self) -> Optional[str]:
        email: str = self.cleaned_data['email']
        domain: str = email.split('@')[1]
        if domain != 'gmail.com':
            raise forms.ValidationError('Only Gmail addresses are allowed.')
        return email


# Custom RegisterForm
class RegisterForm(UserCreationForm):
    username: str = forms.CharField(max_length=80,
                                    required=True,
                                    help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    email: forms.EmailField = forms.EmailField(max_length=100)
    first_name: str = forms.CharField(max_length=60)
    last_name: str = forms.CharField(max_length=100)

    class Meta:
        model: User = User
        fields: List[str] = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self) -> Optional[str]:
        email: str = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


# Edit RegisterForm
class EditRegisterForm(forms.ModelForm):
    username: str = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), max_length=60)
    email: str = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter Your Email', 'class': 'form-control'}), max_length=100)
    first_name: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your Name', 'class': 'form-control'}), max_length=60)
    last_name: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter Your Surname', 'class': 'form-control'}), max_length=100)

    class Meta:
        model: User = User
        # model = get_user_model()
        fields: List[str] = ['username', 'email', 'first_name', 'last_name']


# Change Password
class PasswordChangeUserForm(SetPasswordForm):
    new_password1: str = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        label='New Password *')
    new_password2: str = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password *')

    class Meta:
        model: User = User
        fields: List[str] = ['new_password1', 'new_password2']
