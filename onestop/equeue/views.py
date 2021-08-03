# import json
# import urllib.request
# import urllib.parse
from django.conf import settings
# from django.contrib import messages
from django.contrib.auth.models import User
from django.views import generic
from .models import ServiceProvider, Service, ServiceEnrolment, QueuedCustomer, ServedCustomer, CancelledCustomer, CustomerReview
# from .forms import CommentForm, PostForm, CategoryForm
from django.shortcuts import render, get_object_or_404
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import CreateView
# from django.urls import reverse

# Create your views here.


def queues(request, pk, join_message=None):
    '''
    Generates a view for the current queue of any particular service enrolment. Pass in the service_enrolment (pk) based on the service clicked.

    '''
    context = {}
    # Return a queryset of customers queued up for the passed in service_enrolment
    current_service = ServiceEnrolment.objects.get(id=pk)
    current_queue = QueuedCustomer.objects.filter(
        service_id=pk).order_by('join_time') #A queryset of queuedCustomer instances filtered by the service_id
    queue_length = len(current_queue)>0
    queued_users = [customer.customer for customer in current_queue] # #A list of user objects in current_queue
    context['there_is_queue'] = queue_length
    context['current_queue'] = current_queue
    context['service'] = current_service.service
    context['service_enrolment'] = current_service
    context['service_provider'] = current_service.service_provider
    context['requirements'] = current_service.service_requirements
    context['queued_users'] = queued_users
    if request.method == "POST":
        current_user = request.user
        if current_user in queued_users:
            join_message = 'Duplicate'
            # join_message = 'Sorry, you\'re already queued for this service.'
        else:
            QueuedCustomer.objects.create(customer=current_user, service=current_service)
            join_message = "Success"
            # join_message = f'You\'ve been sucessfully added to the queue for {current_service.service} @ {current_service.service_provider.short_name}.'
    context['join_message'] = join_message
    return render(request, 'equeue/queues.html', context)

def exit_queue(request, pk):
    '''
    Retrieve an instance of QueuedCustomer where customer_id=current_user.id and service_id=pk and save it to a variable current_instance
    Insert in the CancelledCustomer table a new entry with queue_id and customer_id of the current_instance instance
    Delete the current_instance instance from the QueuedCustomer
    Return to and refresh the queue page.
    '''
    context = {}
    # current_user = request.user
    current_instance = QueuedCustomer.objects.filter(service_id=pk, customer_id=request.user.id).get() 
    CancelledCustomer.objects.create(queue_id=current_instance.id, customer_id=current_instance.customer.id, cancelled_by=request.user)
    current_instance.delete()


class ServiceEnrolmentList(generic.ListView):
    queryset = ServiceEnrolment.objects.all().order_by('service_provider')
    template_name = 'equeue/services.html'
    paginate_by = 10
