from django.urls import path
from dictionary import views

app_name = 'dictionary'
urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search_word, name='search'),
    path('add_english', views.add_english, name='add_english'),
    path('add_oshindonga', views.add_oshindonga, name='add_oshindonga'),
    path('add_definition', views.add_definition, name='add_definition')
]
