import json
import urllib.request
import urllib.parse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
# from django.views.generic import TemplateView
# from django.views.generic.edit import CreateView, UpdateView
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# # from django.urls import reverse_lazy
# from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom, OshindongaPhonetic
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
# from django.views import generic
# from json import dumps
# import random

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''
            if result['success']:
                user = form.save()
                login(request, user)
                subject = 'Welcome to the community'
                message = f'Hi {user.username}, \n\nThank you for registering as a contributor. \nThe site is currently being tested; hence, your feedback at this stage will be of great importance. We cannot wait to see your contribution. \n\nRegards, \nFessy'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, 'abiatarfestus@outlook.com']
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, 'You have been registered successfully!')
                return redirect(reverse("index"))
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


# Update it here
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile) 
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # Redirect back to profile page
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)