from django.contrib import admin
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


# Register your models here.
@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceEnrolment)
class ServiceEnrolmentAdmin(admin.ModelAdmin):
    pass


@admin.register(ServantEnrolment)
class ServantEnrolmentAdmin(admin.ModelAdmin):
    pass


@admin.register(QueuedCustomer)
class QueuedCustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(ServedCustomer)
class ServedCustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(CancelledCustomer)
class CancelledCustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    pass


# admin.site.register(ServiceProvider)
# admin.site.register(Service)
# admin.site.register(ServiceEnrolment)
# admin.site.register(ServantEnrolment)
# admin.site.register(QueuedCustomer)
# admin.site.register(ServedCustomer)
# admin.site.register(CancelledCustomer)
# admin.site.register(CustomerReview)
