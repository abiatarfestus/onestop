from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs = {
            "class": "form-control form-control-lg mb-2",
            "placeholder": "Username",
        }
        self.fields["first_name"].widget.attrs = {
            "class": "form-control form-control-lg mb-2",
            "placeholder": "First Name",
        }
        self.fields["last_name"].widget.attrs = {
            "class": "form-control form-control-lg mb-2",
            "placeholder": "Last Name",
        }
        self.fields["email"].widget.attrs = {
            "class": "form-control form-control-lg mb-2",
            "placeholder": "Email address",
        }
        self.fields["password1"].widget.attrs = {
            "class": "form-control form-control-lg mb-2",
            "placeholder": "Password",
        }
        self.fields["password2"].widget.attrs = {
            "class": "form-control form-control-lg mb-2",
            "placeholder": "Confirm password",
        }


# Create a UserUpdateForm to update username and email
class UserUpdateForm(ModelForm):
    email = forms.EmailInput()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-lg mb-2",
                }
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            ),
        }


# Create a ProfileUpdateForm to update image


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "form-control form-control-lg mb-2"}
            )
        }
