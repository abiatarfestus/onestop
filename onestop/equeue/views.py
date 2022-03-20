# import json
# import urllib.request
# import urllib.parse
from django.utils import timezone
from django.conf import settings

# from django.contrib import messages
from django.contrib.auth.models import User
from django.views import generic
from .models import (
    ServiceProvider,
    Service,
    ServiceEnrolment,
    ServantEnrolment,
    QueuedCustomer,
    ServedCustomer,
    CancelledCustomer,
    CustomerReview,
)

# from .forms import CommentForm, PostForm, CategoryForm
from django.shortcuts import render, redirect, get_object_or_404
from .queue_management import Customer, Servant, Queue

# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import CreateView
# from django.urls import reverse

# Create your views here.


def queues(request, pk, join_message=None):
    queue = Queue(request)
    context = queue.form_queue(pk, join_message)
    return render(request, "equeue/queues.html", context)


def exit_queue(request, pk):
    customer = Customer(request)
    return customer.exit_queue(pk)


def join_queue(request, pk):
    customer = Customer(request)
    return customer.join_queue(pk)


def my_queues(request, pk):
    servant = Servant(request)
    context = servant.my_queues(pk)
    return render(request, "equeue/my_queues.html", context)


def serve_customers(request, pk, current_customer=0):
    servant = Servant(request)
    context = servant.serve_customers(pk, current_customer)
    return render(request, "equeue/serve_customers.html", context)


def next_customer(request, pk, last_served_id):
    servant = Servant(request)
    return servant.next_customer(pk, last_served_id)


def cancel_customer(request, pk):
    servant = Servant(request)
    return servant.cancel_customer(pk)


class ServiceEnrolmentList(generic.ListView):
    queryset = ServiceEnrolment.objects.all().order_by("service_provider")
    template_name = "equeue/services.html"
    paginate_by = 10
