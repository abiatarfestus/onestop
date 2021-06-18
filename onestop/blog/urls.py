from . import views
from django.urls import path

app_name = 'blog'
urlpatterns = [
    path('post-list/', views.PostList.as_view(), name='post-list'),
    path('create-post/', views.PostCreate.as_view(), name='create-post'),
    path('create-category/', views.CategoryCreate.as_view(), name='create-category'),
    path('<int:pk>/', views.category_detail, name='category-detail'),
    path('<int:pk>/', views.category_detail, name='category-detail'),
    path('category-list/', views.CategoryList.as_view(), name='category-list'),
    # path('<slug:slug>/', views.post_detail, name='post-detail'), #Fix not to catch other urls
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
]
