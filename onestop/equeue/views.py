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


def queues(request, pk, **kwargs):
    '''
    Generates a view for the current queue of any particular service enrolment. Pass in the service_enrolment (pk) based on the service clicked.

    '''
    context = {}
    # Return a queryset of customers queued up for the passed in service_enrolment
    current_service = ServiceEnrolment.objects.get(id=pk)
    current_queue = QueuedCustomer.objects.filter(
        service_id=pk).order_by('join_time')
    queue_length = len(current_queue)>0
    context['there_is_queue'] = queue_length
    context['current_queue'] = current_queue
    context['service'] = current_service.service
    context['service_provider'] = current_service.service_provider
    context['requirements'] = current_service.service_requirements
    return render(request, 'equeue/queues.html', context)

def join_queue(request, pk):
    context = {}
    current_user = request.user
    current_service = ServiceEnrolment.objects.get(id=pk)
    current_queue = QueuedCustomer.objects.filter(service_id=pk)
    for customer in current_queue:
        if customer.customer == current_user:
            join_message= 'Sorry, you\'re already queued for this service.'
            return queues(request=request, pk=pk, join_message=join_message)
        else:
            new_customer = QueuedCustomer.objects.create(customer=current_user, service=current_service)
            join_message= 'You\'ve been sucessfully entered on to this queue.'
    return queues(request=request, pk=pk, join_message=join_message)
    # https://book.pythontips.com/en/latest/args_and_kwargs.html


class ServiceEnrolmentList(generic.ListView):
    queryset = ServiceEnrolment.objects.all().order_by('service_provider')
    template_name = 'equeue/services.html'
    paginate_by = 10
