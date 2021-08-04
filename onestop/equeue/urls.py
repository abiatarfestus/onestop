from django.urls import path
from . import views

app_name = 'equeue'
urlpatterns = [
    # Pass in the pk of the service_enrolment
    path('queues/<int:pk>/', views.queues, name='queues'),
    path('queues/exit-queue/<int:pk>/', views.exit_queue, name='exit-queue'),
    path('services/', views.ServiceEnrolmentList.as_view(), name='services'),
]
