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
    # print(f'PK: {pk}')
    context['servant_enrolments'] = servant_enrolments
    for entry in servant_enrolments: #Loops through the servant_enrolments, extract the service_enrolment ids and add them to the list
        service_enrolment_ids.append(entry.service_enrolment_id)
        # print(f'SERVICE_ENROLMENT_IDs: {service_enrolment_ids}')
    eligible_queue = QueuedCustomer.objects.filter(service_enrolment_id__in=service_enrolment_ids) #QueuedCustomer instances with service_enrolment assigned to the current servant
    # eligible_queue_ids = []
    # for entry in eligible_queue:
    #     eligible_queue_ids.append(entry.service_enrolment_id)
    #     print(f'ELIGIBLE_QUEUE_IDs: {eligible_queue_ids}')

    eligible_queue_ids = {}
    for entry in eligible_queue:
        if entry.service_enrolment_id in eligible_queue_ids:
            eligible_queue_ids[entry.service_enrolment_id] +=1
        else:
            eligible_queue_ids[entry.service_enrolment_id] =1
        # print(f'ELIGIBLE_QUEUE_IDs: {eligible_queue_ids}')
    context['eligible_queue_ids'] = eligible_queue_ids
    return render(request, 'equeue/my_queues.html', context)


def serve_customers(request, pk, current_customer=0):
    context = {'next_customer_message':None, 'current_customer':current_customer}
    current_service_enrolment = ServiceEnrolment.objects.get(id=pk)
    current_queue = QueuedCustomer.objects.filter(
        service_enrolment_id=pk).order_by('join_time') #A queryset of queuedCustomer instances filtered by the service_id
    queue_length = len(current_queue)>0
    if queue_length:
        queued_users = [customer.customer for customer in current_queue] #A list of user objects in current_queue
        context['queued_users'] = queued_users
    context['there_is_queue'] = queue_length
    context['current_queue'] = current_queue
    context['service'] = current_service_enrolment.service
    context['service_enrolment'] = current_service_enrolment
    context['service_provider'] = current_service_enrolment.service_provider
    # context['requirements'] = current_service_enrolment.service_requirements
    # if request.method == "POST":
    #     if request.user in queued_users:
    #         join_message = 'Duplicate'
    #     else:
    #         QueuedCustomer.objects.create(customer=request.user, service_enrolment=current_service_enrolment)
    #         join_message = "Success"
    # context['join_message'] = join_message
    return render(request, 'equeue/serve_customers.html', context)


def next_customer(request, pk):
    '''
    Retrieve an instance of QueuedCunstomer with an id denoted by the pk parameter passed to the request.
    Save it in a variable front_customer (this is not a user, but a QueuedCustomer instance) and save it to the ServedCustomer table as a new entry with customer_id of the front_customer.
    The new entry to ServedCustomer should have an initial service_duration = 0 (default), to be updated when the customer is done with.
    Delete this record from the QueuedCustomer table (but not the instance itself since it should be passed to the re-direct function).
    Redirect to the serve-customer view, passing in the front_customer as current_customer)
    '''
    
    front_customer = QueuedCustomer.objects.get(id=pk)
    ServedCustomer.objects.create(customer_id=front_customer.customer_id, service_enrolment_id=front_customer.service_enrolment_id, served_by=request.user)
    front_customer_id = front_customer.customer_id
    QueuedCustomer.objects.filter(id=pk).delete()
    return redirect('equeue:serve-customers', pk=front_customer.service_enrolment_id, current_customer=front_customer_id)


def cancel_customer(request, pk):
    return redirect('equeue:serve-customers', pk=pk)


class ServiceEnrolmentList(generic.ListView):
    queryset = ServiceEnrolment.objects.all().order_by('service_provider')
    template_name = 'equeue/services.html'
    paginate_by = 10
