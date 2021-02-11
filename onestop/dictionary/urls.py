from django.urls import path
from dictionary import views

app_name = 'dictionary'
urlpatterns = [
    path('', views.index, name="index"),
    path('search', views.search_word, name='search'),
    path('add_english', views.add_english, name='add-english'),
    path('add_oshindonga', views.add_oshindonga, name='add-oshindonga'),
    path('add_definition', views.add_definition, name='add-definition'),
    path('add_example', views.add_example, name='add-example'),
    path('thankyou', views.thankyou, name='thankyou'),
    path('english-word/<int:pk>/update/', views.EnglishWordUpdate.as_view(), name='english-word-update'),
    path('oshindonga-word/<int:pk>/update/', views.OshindongaWordUpdate.as_view(), name='oshindonga-word-update'),
    path('definition/<int:pk>/update/', views.WordDefinitionUpdate.as_view(), name='word-definition-update'),
    path('example/<int:pk>/update/', views.DefinitionExampleUpdate.as_view(), name='definition-example-update'),
]
