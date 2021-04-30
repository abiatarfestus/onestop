from . import views
from django.urls import path

app_name = 'blog'
urlpatterns = [
    path('post-list/', views.PostList.as_view(), name='post-list'),
    path('<slug:slug>/', views.post_detail, name='post-detail'),
]