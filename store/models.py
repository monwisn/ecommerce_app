from datetime import date, datetime
from typing import Union, Optional, Any

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_save
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
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name: str = models.CharField(max_length=60)
    last_name: str = models.CharField(max_length=80)
    email: str = models.EmailField(max_length=80)
    phone: PhoneNumber = PhoneNumberField(max_length=15,
                                          region='PL',
                                          error_messages={
                                              'invalid': 'Please enter a valid phone number'
                                          })
    # phone: str = models.CharField(max_length=15)
    street: str = models.CharField(max_length=80)
    address: str = models.CharField(max_length=40)
    postal_code: str = models.CharField(max_length=6)  # postalcode contains 6 to 8 characters, 8 including spaces
    city: str = models.CharField(max_length=60)
    additional_info: str = models.TextField(max_length=250, blank=True)
    instagram: str = models.CharField(max_length=100, blank=True)
    dog_name: str = models.CharField(max_length=80, blank=True)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}: {self.id}'


def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Customer(username=instance)
        user_profile.save()


# does the same thing as a receiver
post_save.connect(create_profile, sender=User)


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
    favorites = models.ManyToManyField(User, through='FavoriteProduct', related_name='fav_product')

    # specify the 'through' parameter to use the 'FavoriteProduct' model as the intermediate model for
    # the many-to-many relationship.

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


# User Favorite Products
class FavoriteProduct(models.Model):
    user: Union[User, str] = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_fav')
    product: Union[Product, str] = models.ForeignKey(Product, on_delete=models.CASCADE)
    add_date: datetime = models.DateTimeField(auto_now_add=True)

    def clean(self) -> Any:
        # Check if the user has already added this product to their favorite list
        if FavoriteProduct.objects.filter(user=self.user, product=self.product).exists():
            raise ValidationError('This product is already in the favorite list.')
