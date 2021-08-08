from django.urls import path
from . import views

app_name = 'equeue'
urlpatterns = [
    # Pass in the pk of the service_enrolment
    path('services/', views.ServiceEnrolmentList.as_view(), name='services'),
    path('queues/<int:pk>/', views.queues, name='queues'),
    path('queues/exit-queue/<int:pk>/', views.exit_queue, name='exit-queue'),
    path('queues/my-queues/<int:pk>/', views.my_queues, name='my-queues'),
    path('queues/serve-customers/<int:pk>/<int:current_customer>/', views.serve_customers, name='serve-customers'),
    path('queues/next-customer/<int:pk>/<int:last_served_id>/', views.next_customer, name='next-customer'),
    path('queues/cancel-customer/<int:pk>/', views.cancel_customer, name='cancel-customer'),
]
