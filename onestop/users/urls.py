from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path(
        "activate/<uidb64>/<token>/", views.ActivateAccount.as_view(), name="activate"
    ),
]
