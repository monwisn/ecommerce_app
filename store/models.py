from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Union, Optional, Any

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.forms import ImageField
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from .common import Timestamped


class Category(models.Model):
    name: str = models.CharField(max_length=60)
    slug: str = models.SlugField(max_length=120)

    class Meta:
        verbose_name_plural: str = 'categories'

    def get_absolute_url(self) -> str:
        return reverse('store:category', args=str(self.id))

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    username: User = models.OneToOneField(User, on_delete=models.CASCADE)
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
    profile_image: ImageField = models.ImageField(upload_to='uploads/profile_image/', blank=True, null=True)

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
    price: Decimal = models.DecimalField(default=0, decimal_places=2, max_digits=6)
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
    sale_price: Decimal = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    favorites = models.ManyToManyField(User, through='FavoriteProduct', related_name='fav_product')
    quantity: int = models.IntegerField(default=0)

    # specify the 'through' parameter to use the 'FavoriteProduct' model as the intermediate model for
    # the many-to-many relationship.

    def clean(self):
        is_sale: bool = self.is_sale
        if not is_sale:
            self.sale_price = self.price
        return super(Product, self).clean()

    def __str__(self) -> str:
        return self.name

    # save() method takes care of either inserting or updating an existing record depending on
    # whether the object already exists in the database
    # args and kwargs are positional/keyword arguments that can be passed into the save method when it's called
    def save(self, *args, **kwargs):
        # customization: any code placed before the super is going to be performed before we save the data
        if self.id:
            existing = Product.objects.get(id=self.id)
            if existing.image != self.image:
                existing.image.delete(save=False)
                # this deletes the image and replaces it with a new one in the 'upload_to/product/' file

        super(Product, self).save(*args, **kwargs)  # basic setup for saving into this model


class Order(Timestamped):
    product: Union[Product, str] = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer: Union[Customer, str] = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity: int = models.IntegerField(default=1)
    address: str = models.CharField(max_length=150, default='')
    phone: str = models.CharField(max_length=20, default='')  # blank=True
    date: date = models.DateField(default=datetime.today)
    status: bool = models.BooleanField(default=False)  # paid/unpaid order

    class Meta:
        ordering: tuple[str] = ('-created',)

    def __str__(self) -> str:
        return f'Order: {self.id}'


# User Favorite Products
class FavoriteProduct(models.Model):
    user: Union[User, str] = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_fav')
    product: Union[Product, str] = models.ForeignKey(Product, on_delete=models.CASCADE)
    add_date: datetime = models.DateTimeField(auto_now_add=True)

    def clean(self) -> Any:
        # Check if the user has already added this product to their favorite list
        if FavoriteProduct.objects.filter(user=self.user, product=self.product).exists():
            raise ValidationError('This product is already in the favorite list.')


format_time: str = "%Y-%m-%d %H:%M:%S"


# Cart Products Discount
class DiscountCoupon(Timestamped):
    code: str = models.CharField(max_length=30, unique=True, blank=True)
    valid_from: datetime = models.DateTimeField(default=datetime.now, blank=True)
    valid_to: datetime = models.DateTimeField(default=datetime.now() + timedelta(days=7))
    discount: int = models.IntegerField(default=10, validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active: bool = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        if self.valid_from.strftime(format_time) < datetime.today().strftime(format_time) < self.valid_to.strftime(
                format_time):
            self.is_active = True
        else:
            self.is_active = False
        super().save(*args, **kwargs)
