from django.urls import path
from . import views


app_name: str = 'main'

urlpatterns: list = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('account/', views.user_account, name='user_account'),
    path('account-delete/', views.account_delete, name='account_delete'),
    path('contact/', views.contact, name='contact'),
    path('clear-image/', views.clear_profile_picture, name='clear_image'),
    path('location/', views.location, name='location'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
    path('newsletter-delete/', views.newsletter_delete, name='newsletter_delete'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('register/', views.register, name='register'),
    path('toggle-theme/', views.toggle_theme, name='toggle-theme'),
]
