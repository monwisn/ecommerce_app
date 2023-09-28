from django.urls import path
from . import views


app_name: str = 'main'

urlpatterns: list = [
    path('', views.home, name='home'),
    path('location/', views.location, name='location'),
    path('contact/', views.contact, name='contact'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter-delete/', views.newsletter_delete, name='newsletter_delete'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
