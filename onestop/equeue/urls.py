from django.urls import path
from . import views

app_name = 'equeue'
urlpatterns = [
#     path('', views.index, name="index"),
    path('queues/', views.queues, name='queues'),
    # path('search/<int:pk>', views.search_suggested_word, name='search-suggested-word'),
    # #Create Views
    # path('english/create/',
    #      views.EnglishWordCreate.as_view(), name='english-create'),
    #      #Update Views
    # path('english/<int:pk>/update/',
    #      views.EnglishWordUpdate.as_view(), name='english-update'),
         #List Views
     path('services/',
         views.ServiceEnrolmentList.as_view(), name='services'),
         #Detail Views
    #  path('english-word/<int:pk>',
    #      views.EnglishWordDetailView.as_view(), name='english-word-detail'),
]