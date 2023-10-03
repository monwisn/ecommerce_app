from typing import List

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms

from .models import NewsletterUser


# Support Contact
class ContactForm(forms.Form):
    name: str = forms.CharField(label='Your Name', max_length=80)
    email: forms.EmailField = forms.EmailField(label='Your Email')
    subject: str = forms.CharField(max_length=150, label='Subject')
    message: str = forms.CharField(label='Your Message', widget=forms.Textarea, required=True, max_length=2500)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label='')


class NewsletterUserForm(forms.ModelForm):
    class Meta:
        model: NewsletterUser = NewsletterUser
        fields: List[str] = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('@')[1]
        if domain != 'gmail.com':
            raise forms.ValidationError('Only Gmail addresses are allowed.')
        return email
