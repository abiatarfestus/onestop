# import json
# import urllib.request
# import urllib.parse
from django.utils import timezone
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

class Queue():
    def __init__(self, request):
        '''
        If request method is GET, generate a view for the current queue of the service enrolment of the passed in pk.
        If request method is POST, add the current user to the queue of the passed in service enrolment, if not already in queue.
        '''
        self.request = request
        self.queue_length = 0
        self.service_enrolment = None
        self.service_provider = None
        self.context = {}
        self.current_queue = []
        self.queued_users = []
    
    def form_queue(self, pk, join_message=None):
        self.service_enrolment = ServiceEnrolment.objects.get(id=pk)
        self.current_queue = QueuedCustomer.objects.filter(service_enrolment_id=pk).order_by('join_time')  # A queryset of queuedCustomer instances filtered by the service_id
        self.queue_length = len(self.current_queue)
        if self.queue_length > 0:
            # A list of user objects in current_queue
            self.queued_users = [customer.customer for customer in self.current_queue]
        self.context['queued_users'] = self.queued_users    
        self.context['there_is_queue'] = self.queue_length > 0
        self.context['current_queue'] = self.current_queue
        self.context['service'] = self.service_enrolment.service
        self.context['service_enrolment'] = self.service_enrolment
        self.context['service_provider'] = self.service_enrolment.service_provider
        self.context['requirements'] = self.service_enrolment.service_requirements
        if self.request.method == "POST":
            if self.request.user in self.queued_users:
                join_message = 'Duplicate'
            else:
                QueuedCustomer.objects.create(customer=self.request.user, service_enrolment=self.service_enrolment)
                join_message = "Success"
        self.context['join_message'] = join_message
        return self.context


class Customer():
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.queues_joined = None
        self.queued_instance = None
    
    def join_queue(self, pk, join_message=None):
        queue = Queue(self.request)
        queue.form_queue(pk=pk, join_message=join_message)
        return redirect('equeue:queues', pk=pk)

    def exit_queue(self, pk):
        '''
        Retrieve an instance of QueuedCustomer where customer_id=current_user.id and service_id=pk and save it to a variable current_instance
        Insert in the CancelledCustomer table a new entry with queue_id and customer_id of the current_instance instance
        Delete the current_instance instance from the QueuedCustomer
        Return to and refresh the queue page.
        '''

        self.queued_instance = QueuedCustomer.objects.filter(service_enrolment_id=pk, customer_id=self.request.user.id).get()
        CancelledCustomer.objects.create(service_enrolment_id=self.queued_instance.service_enrolment_id, customer_id=self.queued_instance.customer.id, cancelled_by=self.request.user)
        self.queued_instance.delete()
        return redirect('equeue:queues', pk=pk)

class Servant():
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.context = {}
        self.servant_enrolments = None
        self.service_enrolment = None
        self.eligible_queues = None
        self.eligible_queues_ids = {}
        self.current_queue = None
        self.queued_users = []
        self.queue_length = 0
        self.front_customer = None #Front QueuedCustomer instance
        self.front_customer_id = 0
        self.service_enrolment_ids = [] # A list to hold ids of the service_enrolments the current user/servant is assigned to

    def my_queues(self, pk):
        self.servant_enrolments = ServantEnrolment.objects.filter(servant_id=pk)
        self.context['servant_enrolments'] = self.servant_enrolments
        for entry in self.servant_enrolments:  # Loops through the servant_enrolments, extract the service_enrolment ids and add them to the list
            self.service_enrolment_ids.append(entry.service_enrolment_id)
        self.eligible_queues = QueuedCustomer.objects.filter(service_enrolment_id__in=self.service_enrolment_ids)
        for entry in self.eligible_queues:
            if entry.service_enrolment_id in self.eligible_queues_ids:
                self.eligible_queues_ids[entry.service_enrolment_id] += 1
            else:
                self.eligible_queues_ids[entry.service_enrolment_id] = 1
        self.context['eligible_queues_ids'] = self.eligible_queues_ids
        return self.context

    def serve_customers(self, pk, current_customer=0):
        '''
        Build the current_queue from QueuedCustomer using the service-enrolment id passed in as pk.
        If called as a redirect from nex_customer, use the current_customer value to get served_customer from ServedCustmer.
        Use served_customer.customer_id to determine the current_customer object from User.
        The last_served_id holds the current_customer value, to be passed to the template and used as an argument to the next call of next_customer.

        '''
        self.context = {'next_customer_message': None,
                'current_customer': current_customer, 'last_served_id':current_customer}
        if current_customer > 0:
            served_customer = ServedCustomer.objects.get(id=current_customer)
            self.context['current_customer'] = User.objects.get(id=served_customer.customer_id)
        self.service_enrolment = ServiceEnrolment.objects.get(id=pk)
        self.current_queue = QueuedCustomer.objects.filter(service_enrolment_id=pk).order_by('join_time')
        self.queue_length = len(self.current_queue)
        if self.queue_length > 0:
            self.queued_users = [customer.customer for customer in self.current_queue]
        self.context['queued_users'] = self.queued_users
        self.context['there_is_queue'] = self.queue_length
        self.context['current_queue'] = self.current_queue
        self.context['queue_length'] = self.queue_length
        self.context['service'] = self.service_enrolment.service
        self.context['service_enrolment'] = self.service_enrolment
        self.context['service_provider'] = self.service_enrolment.service_provider
        return self.context

    def next_customer(self, pk, last_served_id):
        '''
        Retrieve an instance of QueuedCunstomer with an id denoted by the pk parameter passed to the request.
        Save it in a variable front_customer (this is not a user, but a QueuedCustomer instance) and save it to the ServedCustomer table as a new entry with customer_id of the front_customer.
        The new entry to ServedCustomer should have an initial service_duration = 0 (default), to be updated when the customer is done with.
        Delete this record from the QueuedCustomer table (but not the instance itself since it should be passed to the re-direct function).
        Redirect to the serve-customer view, passing in the id of front_customer's ServedCustomer instance as current_customer.
        NB: current_customer in this function is the instance of ServedCustomr that has just been created, and its id is being passed to serve_customers.
        '''
        if last_served_id > 0: #When this is NOT the first custmer served
            last_served = ServedCustomer.objects.get(id=last_served_id)
            duration = timezone.now()-last_served.date_time_served
            seconds = int(duration.total_seconds())
            last_served.service_duration = seconds
            last_served.save()
        self.front_customer = QueuedCustomer.objects.get(id=pk)
        self.front_customer_id = self.front_customer.customer_id
        ServedCustomer.objects.create(customer_id=self.front_customer_id,
                                    service_enrolment_id=self.front_customer.service_enrolment_id, served_by=self.request.user)
        current_customer = ServedCustomer.objects.filter(
            customer_id=self.front_customer_id, service_enrolment_id=self.front_customer.service_enrolment_id, served_by=self.request.user).order_by('-date_time_served')
        served_id = current_customer[0].id
        QueuedCustomer.objects.filter(id=pk).delete()
        return redirect('equeue:serve-customers', pk=self.front_customer.service_enrolment_id, current_customer=served_id)


    def cancel_customer(self, pk):
        '''
        Retrieve an instance of QueuedCustomer where customer_id=current_user.id and service_id=pk and save it to a variable current_instance
        Insert in the CancelledCustomer table a new entry with queue_id and customer_id of the current_instance instance
        Delete the current_instance instance from the QueuedCustomer
        Return to and refresh the queue page.
        '''
        self.front_customer = QueuedCustomer.objects.get(id=pk)
        self.front_customer_id = self.front_customer.customer_id
        CancelledCustomer.objects.create(service_enrolment_id=self.front_customer.service_enrolment_id, customer_id=self.front_customer_id, cancelled_by=self.request.user)
        self.front_customer.delete()
        return redirect('equeue:serve-customers', pk=self.front_customer.service_enrolment_id, current_customer=0)








