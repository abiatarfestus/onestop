from django.urls import path
from . import views

app_name = "translation"
urlpatterns = [
    path("translate/", views.translate_text, name="translate"),
<<<<<<< HEAD
]
=======
]
>>>>>>> ffe87787d1f395e67cf9792d6212b81a8f2b0e17
