from . import views
from django.urls import path

app_name = 'blog'
urlpatterns = [
    path('post-list/', views.PostList.as_view(), name='post-list'),
    path('create-post/', views.PostCreate.as_view(), name='create-post'),
    path('<slug:slug>/', views.post_detail, name='post-detail'),
]