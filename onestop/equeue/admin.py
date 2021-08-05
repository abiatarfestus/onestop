from django.contrib import admin
from .models import ServiceProvider, Service, ServiceEnrolment, ServantEnrolment, QueuedCustomer, ServedCustomer, CancelledCustomer, CustomerReview

# Register your models here.
admin.site.register(ServiceProvider)
admin.site.register(Service)
admin.site.register(ServiceEnrolment)
admin.site.register(ServantEnrolment)
admin.site.register(QueuedCustomer)
admin.site.register(ServedCustomer)
admin.site.register(CancelledCustomer)
admin.site.register(CustomerReview)
