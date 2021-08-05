# import json
# import urllib.request
# import urllib.parse
from django.conf import settings
# from django.contrib import messages
from django.contrib.auth.models import User
from django.views import generic
from .models import ServiceProvider, Service, ServiceEnrolment, ServantEnrolment, QueuedCustomer, ServedCustomer, CancelledCustomer, CustomerReview
# from .forms import CommentForm, PostForm, CategoryForm
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import CreateView
# from django.urls import reverse

# Create your views here.


def queues(request, pk, join_message=None):
    '''
    If request method is GET, generate a view for the current queue of the service enrolment of the passed in pk.
    If request method is POST, add the current user to the queue of the passed in service enrolment, if not already in queue.
    '''
    context = {}
    # Return a queryset of customers queued up for the passed in service_enrolment
    current_service_enrolment = ServiceEnrolment.objects.get(id=pk)
    current_queue = QueuedCustomer.objects.filter(
        service_enrolment_id=pk).order_by('join_time') #A queryset of queuedCustomer instances filtered by the service_id
    queue_length = len(current_queue)>0
    queued_users = [customer.customer for customer in current_queue] #A list of user objects in current_queue
    context['there_is_queue'] = queue_length
    context['current_queue'] = current_queue
    context['service'] = current_service_enrolment.service
    context['service_enrolment'] = current_service_enrolment
    context['service_provider'] = current_service_enrolment.service_provider
    context['requirements'] = current_service_enrolment.service_requirements
    context['queued_users'] = queued_users
    if request.method == "POST":
        if request.user in queued_users:
            join_message = 'Duplicate'
        else:
            QueuedCustomer.objects.create(customer=request.user, service_enrolment=current_service_enrolment)
            join_message = "Success"
    context['join_message'] = join_message
    return render(request, 'equeue/queues.html', context)

def exit_queue(request, pk):
    '''
    Retrieve an instance of QueuedCustomer where customer_id=current_user.id and service_id=pk and save it to a variable current_instance
    Insert in the CancelledCustomer table a new entry with queue_id and customer_id of the current_instance instance
    Delete the current_instance instance from the QueuedCustomer
    Return to and refresh the queue page.
    '''
    
    current_instance = QueuedCustomer.objects.filter(service_enrolment_id=pk, customer_id=request.user.id).get() 
    CancelledCustomer.objects.create(queue_id=current_instance.id, customer_id=current_instance.customer.id, cancelled_by=request.user)
    current_instance.delete()
    return redirect('equeue:queues', pk=pk)


def my_queues(request, pk):
    context = {}
    service_enrolment_ids = [] #A list to hold ids of the service_enrolments the current user/servant is assigned to
    servant_enrolments = ServantEnrolment.objects.filter(servant_id=pk)
    context['servant_enrolments'] = servant_enrolments
    for entry in servant_enrolments: #Loops through the servant_enrolments, extract the service_enrolment ids and add them to the list
        service_enrolment_ids.append(entry.service_enrolment_id)
    eligible_queue = QueuedCustomer.objects.filter(service_enrolment_id__in=service_enrolment_ids) #QueuedCustomer instances with service_enrolment assigned to the current servant
    eligible_queue_ids = []
    for entry in eligible_queue:
        eligible_queue_ids.append(entry.service_enrolment_id)
    context['eligible_queue_ids'] = eligible_queue_ids
    return render(request, 'equeue/my_queues.html', context)


def serve_customers(request):
    context = {'next_customer_message':None}
    return render(request, 'equeue/serve_customers.html', context)


def next_customer(request, pk):
    return redirect('equeue:serve-customers', pk=pk)


def cancel_customer(request, pk):
    return redirect('equeue:serve-customers', pk=pk)


class ServiceEnrolmentList(generic.ListView):
    queryset = ServiceEnrolment.objects.all().order_by('service_provider')
    template_name = 'equeue/services.html'
    paginate_by = 10
