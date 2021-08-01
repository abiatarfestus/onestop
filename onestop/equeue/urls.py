from django.urls import path
from . import views

app_name = 'equeue'
urlpatterns = [
    # Pass in the pk of the service_enrolment
    path('queues/<int:pk>/', views.queues, name='queues'),
    path('queues/join-queue/<int:pk>/', views.join_queue, name='join-queue'),
    path('services/', views.ServiceEnrolmentList.as_view(), name='services'),
]
