import copy
from urllib.parse import quote

import folium
from django import template
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import Template
from django.template.loader import get_template

from cart.cart import Cart
from ecommerce_app import settings
from store.forms import CustomerForm, ProfileImageForm
from store.models import Customer
from .forms import ContactForm, NewsletterUserForm, RegisterForm, EditRegisterForm, PasswordChangeUserForm
from .models import NewsletterUser


# def home(request) -> HttpResponse:
#     # return render(request, 'main/home.html')

def home(request) -> HttpResponse:
    # Check if the user has visited the page before
    if not request.session.get('visited_main_page', False):
        # Set the session variable to indicate that the user has visited the page
        request.session['visited_main_page'] = True
        # Render the main page with the privacy policy banner
        return render(request, 'main/home.html', {'show_privacy_policy_banner': True})
    else:
        # Check if the user has accepted the privacy policy
        if not request.session.get('accepted_privacy_policy', False):
            # Render the main page with the privacy policy banner
            return render(request, 'main/home.html', {'show_privacy_policy_banner': True})
        else:
            # Render the main page without the privacy policy banner
            return render(request, 'main/home.html', {'show_privacy_policy_banner': False})


def accept_privacy_policy(request):
    # Update the session variable to indicate that the user has accepted the privacy policy
    request.session['accepted_privacy_policy'] = True
    return redirect('main:home')


def about(request) -> HttpResponse:
    return render(request, 'main/about.html')


def location(request) -> HttpResponse:
    coordinates: list[float] = [54.337, 18.569]

    # Create the map
    map_location: folium.folium.Map = folium.Map(location=coordinates, zoom_start=13)
    # map_location: folium.folium.Map = folium.Map(location=coordinates,
    #                                              zoom_start=13,
    #                                              height='90%',
    #                                              width='90%',
    #                                              left='5%')

    # Add pin to map
    folium.Marker(location=[54.337, 18.569],
                  popup='Opening hours: 10:00-20:00 (Mon-Sat)',
                  tooltip='HauAria- Pet Concept Store',
                  icon=folium.Icon(color='purple', icon='star')
                  ).add_to(map_location)

    folium.Marker(location=[54.3398, 18.5686],
                  popup='Opening hours: 9:00-17:00 (Mon-Fri), 10:00-14:00 (Sat)',
                  tooltip='HauAria Office - Click here for more info',
                  icon=folium.Icon(color='darkpurple', icon='info-sign')
                  ).add_to(map_location)

    return render(request, 'main/location.html', {'map': map_location._repr_html_()})


def contact(request) -> HttpResponse:
    if request.method == 'POST':
        form: ContactForm = ContactForm(request.POST)
        if form.is_valid():
            subject: str = f'New request: {form.cleaned_data["subject"]}'
            plaintext: Template = template.loader.get_template('main/contact_email.txt')
            htmltemp: Template = template.loader.get_template('main/contact_email.html')
            body: dict[str] = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'subject': form.cleaned_data['subject'],
                'message': form.cleaned_data['message'],
            }
            from_email: str = form.cleaned_data['email']
            to_email: str = settings.EMAIL_HOST_USER
            text_content: Template = plaintext.render(body)
            html_content: Template = htmltemp.render(body)
            try:
                msg: EmailMultiAlternatives = EmailMultiAlternatives(subject, text_content, from_email, [to_email],
                                                                     headers={'Reply-To': "your-email@gmail.com"})
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, 'Your message has been send successfully.')
            return redirect('main:home')
        else:
            messages.info(request, 'You must confirm recaptcha.')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})


def newsletter_signup(request) -> HttpResponse:
    form: NewsletterUserForm = NewsletterUserForm()
    if request.method == 'POST':
        form = NewsletterUserForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email has been added successfully to our mailing list.')
            return redirect('main:home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
            form = NewsletterUserForm()
    return render(request, 'main/newsletter.html', {'form': form})


def newsletter_delete(request) -> HttpResponse:
    form: NewsletterUserForm = NewsletterUserForm()
    if request.method == 'POST':
        email = request.POST['email']
        try:
            subscriber = NewsletterUser.objects.get(email=email)
            subscriber.delete()
            messages.success(request, 'User successfully deleted from the newsletter.')
        except NewsletterUser.DoesNotExist:
            messages.warning(request, 'User does not exist in the newsletter.')

    return render(request, 'main/newsletter.html', {'form': form})


def privacy_policy(request) -> HttpResponse:
    recipient_email: str = "your-email@gmail.com"  # Replace with your actual recipient email address
    encoded_email: str = quote(recipient_email)
    link: str = f"https://mail.google.com/mail/?view=cm&to={encoded_email}"

    return render(request, 'main/privacy_policy.html', {'link': link})


def register(request) -> HttpResponse:
    if request.method == 'POST':
        form: RegisterForm = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your account has been successfully created.')
            return redirect('main:login')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})


def login_user(request) -> HttpResponse:
    if request.user.is_authenticated:
        messages.info(request, "You're already login!")
        return redirect('main:home')
    else:
        form: AuthenticationForm = AuthenticationForm()
        if request.method == 'POST':
            # form = AuthenticationForm(request, data=request.POST)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You've been successfully logged in as {username}!")
                return redirect('main:home')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'main/login.html', {'form': form})


def logout_user(request) -> HttpResponse:
    cart: dict = copy.deepcopy(Cart(request).cart)
    logout(request)
    # Save session cart even if user is logged out
    session = request.session
    session[settings.CART_SESSION_ID] = cart
    session.save()
    messages.info(request, "You've been successfully logged out!")
    return redirect('main:home')


def user_account(request) -> HttpResponse:
    if request.user.is_authenticated:
        current_user: User = User.objects.get(id=request.user.id)
        profile_user: Customer = Customer.objects.get(username_id=request.user.customer.username_id)
        if request.method == 'POST':
            register_form: EditRegisterForm = EditRegisterForm(data=request.POST or None, instance=current_user)
            delivery_form: CustomerForm = CustomerForm(request.POST or None, request.FILES or None, instance=current_user.customer)
            password_form: PasswordChangeUserForm = PasswordChangeUserForm(data=request.POST, user=request.user)
            profile_form: ProfileImageForm = ProfileImageForm(request.POST or None, request.FILES or None, instance=profile_user)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Your User account has been updated!')
            elif delivery_form.is_valid():
                delivery_form.save()
                messages.success(request, 'Your Customer information has been updated.')
            elif password_form.is_valid():
                password_form.save()
                messages.success(request, 'Your Password has been changed.')
                update_session_auth_hash(request, password_form.user)
            elif profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Your Image has been updated.')
            else:
                messages.error(request, 'Something went wrong. You may have entered incorrect data.')
                for error in list(password_form.errors.values()):
                    messages.error(request, error)
            return redirect('main:user_account')
        else:
            register_form = EditRegisterForm(instance=current_user)
            delivery_form = CustomerForm(instance=current_user.customer)
            password_form = PasswordChangeUserForm(user=request.user)
            profile_form = ProfileImageForm(instance=profile_user)
        return render(request, 'main/user_account.html', {
            'user': current_user,
            'register_form': register_form,
            'delivery_form': delivery_form,
            'password_form': password_form,
            'profile_form': profile_form,
        })
    else:
        messages.info(request, 'You have to log in first!')
    return redirect('main:login')


def clear_profile_picture(request) -> HttpResponse:
    if request.method == 'GET':
        image = Customer.objects.get(username_id=request.user.customer.username_id)
        if image.profile_image:
            image.profile_image.delete()
            image.save()
            messages.success(request, 'Your Image has been deleted.')
        else:
            messages.error(request, 'You can\'t delete default image.')
    return redirect('main:user_account')


def account_delete(request) -> HttpResponse:
    if request.user.is_authenticated:
        current_user: User = User.objects.get(id=request.user.id)
        if request.method == 'GET':
            current_user.delete()
            messages.info(request, 'Your user account has been permanently deleted.')
            return redirect('main:home')
        else:
            messages.info(request, 'Something went wrong.')
            redirect('main:user_account')
    else:
        messages.info(request, 'You have to log in first!')
    return redirect('main:login')


def toggle_theme(request) -> HttpResponse:
    if request.session.get('theme') == 'dark':
        request.session['theme']: str = 'light'
    else:
        request.session['theme']: str = 'dark'
    return redirect(request.META.get('HTTP_REFERER'))
