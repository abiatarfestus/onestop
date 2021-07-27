# import json
# import urllib.request
# import urllib.parse
from django.conf import settings
# from django.contrib import messages
from django.views import generic
from .models import ServiceProvider, Service, ServiceEnrolment, QueuedCustomer, ServedCustomer, CancelledCustomer, CustomerReview
# from .forms import CommentForm, PostForm, CategoryForm
from django.shortcuts import render, get_object_or_404
# from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import CreateView
# from django.urls import reverse

# Create your views here.

def queues(request):
    context = {}
    return render(request, 'equeue/queues.html', context)

class ServiceEnrolmentList(generic.ListView):
    queryset = ServiceEnrolment.objects.all().order_by('service_provider')
    template_name = 'equeue/services.html'
    paginate_by = 10