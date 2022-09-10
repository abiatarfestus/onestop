from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
<<<<<<< HEAD
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
=======
    path(
        "activate/<uidb64>/<token>/", views.ActivateAccount.as_view(), name="activate"
    ),
>>>>>>> ffe87787d1f395e67cf9792d6212b81a8f2b0e17
]
