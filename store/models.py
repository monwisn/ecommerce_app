from datetime import date, datetime
from typing import Union, Optional

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from .common import Timestamped


class Category(models.Model):
    name: str = models.CharField(max_length=60)

    class Meta:
        verbose_name_plural: str = 'categories'

    def get_absolute_url(self) -> str:
        return reverse('store:category', args=str(self.id))

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    first_name: str = models.CharField(max_length=60)
    last_name: str = models.CharField(max_length=80)
    phone: PhoneNumber = PhoneNumberField(max_length=15,
                                          region='PL',
                                          error_messages={
                                              'invalid': 'Please enter a valid phone number'
                                          })
    # phone: str = models.CharField(max_length=15)
    email: str = models.EmailField(max_length=80)
    password: str = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Product(Timestamped):
    name: str = models.CharField(max_length=100)
    price: float = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    brand: str = models.CharField(max_length=150)

    # Category type annotation: field is of type 'Union[Category, int]', which means that the field value can be either
    # an instance of the 'Category' model or an integer representing the primary key of the related category.
    category: Union[Category, int] = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

    # Description type annotation: field is of type 'Optional[str]', which means it can be either a string or 'None'.
    description: Optional[str] = models.CharField(max_length=500, default='', blank=True, null=True)

    # Image type annotation: it can accept either an instance of 'InMemoryUploadedFile'
    # (representing an uploaded image file) or a string (representing the path to an image file on the server).
    image: Union[InMemoryUploadedFile, str] = models.ImageField(upload_to='uploads/product/')

    # Add Sale Stuff
    is_sale: bool = models.BooleanField(default=False)
    sale_price: float = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def clean(self):
        is_sale: bool = self.is_sale
        if not is_sale:
            self.sale_price = self.price
        return super(Product, self).clean()

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    product: Union[Product, str] = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer: Union[Customer, str] = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity: int = models.IntegerField(default=1)
    address: str = models.CharField(max_length=150, default='')
    phone: str = models.CharField(max_length=20, default='')  # blank=True
    date: date = models.DateField(default=datetime.today)
    status: bool = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.product}'
