from typing import List
from django import forms
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import Customer


# Customer Delivery Form
class CustomerForm(forms.ModelForm):
    first_name: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email: str = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}))
    phone: str = forms.CharField(
        widget=PhoneNumberInternationalFallbackWidget(attrs={'placeholder': '+48 XXX-XXX-XXX',
                                                             'class': 'form-control'}),
        max_length=15)
    street: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Street Name', 'class': 'form-control'}))
    address: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Building/Flat Number', 'class': 'form-control'}))
    postal_code: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'XX-XXX', 'class': 'form-control'}))
    city: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-control'}))
    additional_info: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Floor number, door code, etc.', 'class': 'form-control'}),
        required=False)
    dog_name: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your Dog name', 'class': 'form-control'}),
        required=False)
    instagram: str = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your ig name', 'class': 'form-control'}),
        max_length=50,
        required=False)

    class Meta:
        model: Customer = Customer
        fields: List[str] = ['first_name',
                             'last_name',
                             'email',
                             'phone',
                             'street',
                             'address',
                             'postal_code',
                             'city',
                             'additional_info',
                             'dog_name',
                             'instagram',
                             ]
