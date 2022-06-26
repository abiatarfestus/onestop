from django.urls import path
from . import views

app_name = "translation"
urlpatterns = [
    path("translate/", views.translate_text, name="translate"),
]
