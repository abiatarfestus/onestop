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
from dictionary.classes import HistoryRecord
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            """Begin reCAPTCHA validation"""
            recaptcha_response = request.POST.get("g-recaptcha-response")
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {
                "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                "response": recaptcha_response,
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            """ End reCAPTCHA validation """
            if result["success"]:
                user = form.save()
                login(request, user)
                subject = "Welcome to the community"
                message = f"Hi {user.first_name}, \n\nThank you for registering as a contributor. \nThe site is currently being tested; hence, your feedback at this stage will be of great importance. We cannot wait to see your contribution. \n\nRegards, \nFessy"
                email_from = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email, "abiatarfestus@outlook.com"]
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, "You have been registered successfully!")
                return redirect(reverse("index"))
            else:
                messages.error(request, "Invalid reCAPTCHA. Please try again.")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


# Update it here
contribution = HistoryRecord()


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("users:profile")  # Redirect back to profile page
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "user_contribution": contribution.get_user_contribution(request.user),
    }
    return render(request, "users/profile.html", context)


# Comment added on 15.03.2022 to test deployment update
