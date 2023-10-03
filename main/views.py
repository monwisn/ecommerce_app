import folium
from django import template
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Template
from django.template.loader import get_template

from ecommerce_app import settings
from .forms import ContactForm, NewsletterUserForm
from .models import NewsletterUser


def home(request) -> HttpResponse:
    return render(request, 'main/home.html')


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
                                                                     headers={'Reply-To': "bartkram11@gmail.com"})
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
    return render(request, 'main/privacy_policy.html')


def register(request) -> HttpResponse:
    if request.method == 'POST':
        form: UserCreationForm = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your account has been successfully created.')
            # return redirect('main:home')
            return redirect('main:login')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def login_user(request) -> HttpResponse:
    if request.user.is_authenticated:
        messages.info(request, "You're already login!")
        return redirect('main:home')
    else:
        form: AuthenticationForm = AuthenticationForm()
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
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
    logout(request)
    messages.info(request, "You've been successfully logged out!")
    return redirect('main:home')
