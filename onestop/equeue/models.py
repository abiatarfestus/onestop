from django.db import models
# from django.conf import settings
# from django.urls import reverse
# from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from django_resized import ResizedImageField


class ServiceProvider(models.Model):
    '''
    A model for reating service providers
    '''
    SELECT = ''
    PRIVATE = 'Noun [C]'
    PUBLIC = 'Noun [U]'
    PARASTATAL = 'Noun [U]'
    ENTITY_TYPE_CHOICES = [
        (SELECT, 'Select the part of speech of your definition'),
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
        (PARASTATAL, 'Parastatal'), ]

    ACTIVE = 1
    INACTIVE = 0
    STATUS = (
        (0, "Inactive"),
        (1, "Active")
    )

    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=20)
    entity_type = models.CharField(
        max_length=10,  choices=ENTITY_TYPE_CHOICES,)
    street = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=254, blank=True)
    website = models.CharField(max_length=255, blank=True)
    image = ResizedImageField(
        verbose_name='logo', upload_to='service_provider_logos', quality=100, size=[50, 50], blank=True)
    join_date = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    '''
    A model for creating types of services.

    '''
    SELECT = ''
    HAIR_AND_BEAUTY = 'Hair and Beauty'
    MISCELLANEOUS = 'Miscellaneous'
    MUNICIPAL = 'Local Authority'
    HEALTH = 'Health and Wellness'
    FINANCE = 'Banking and Finance'
    SERVICE_CATEGORY_CHOICES = [
        (SELECT, 'Select the part service category'),
        (HAIR_AND_BEAUTY, 'Hair and Beauty'),
        (MISCELLANEOUS, 'Miscellaneous'),
        (MUNICIPAL, 'Local Authority'),
        (HEALTH, 'Health and Wellness'),
        (FINANCE, 'Banking and Finance')]

    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=20, default=MISCELLANEOUS, choices=SERVICE_CATEGORY_CHOICES,)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ServiceEnrolment(models.Model):
    '''
    A model for enrolling service providers to services

    '''
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE)

    class Meta:
        ordering = ['service_provider']
        constraints = [models.UniqueConstraint(
            fields=['service', 'service_provider'], name='unique_enrolment')]

    def __str__(self):
        return f'{self.service_provider}: {self.service}'


class QueuedCustomer(models.Model):
    '''
    A model for creating service queues of customers
    '''
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    # position =
    service = models.ForeignKey(ServiceEnrolment, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        constraints = [models.UniqueConstraint(
            fields=['service', 'customer'], name='unique_queuer')]

    def __str__(self):
        return f'{self.customer}>> {self.service}'


class ServedCustomer(models.Model):
    '''
    A model for recording served customers
    '''
    customer_id = models.IntegerField()
    service_enrolment_id = models.IntegerField()
    date_time_served = models.DateTimeField(auto_now_add=True)
    # Number of minutes the customer spent with the server
    service_duration = models.IntegerField()
    # The server/User signed in
    server = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.server}>> {self.date_time_served}'


class CancelledCustomer(models.Model):
    '''
    A model for recording cancelled customers
    '''
    queue_id = models.IntegerField()
    customer_id = models.IntegerField()
    date_time_cancelled = models.DateTimeField(auto_now_add=True)
    # The server/customer signed in
    cancelled_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.cancelled_by}>> {self.date_time_cancelled}'


class CustomerReview(models.Model):
    '''
    A model for recording customer reviews
    '''

    SELECT = ''
    EXCELLENT = 3
    GOOD = 2
    POOR = 1
    REVIEW_CHOICES = [
        (SELECT, 'Select the part service category'),
        (EXCELLENT, 'Excellent'),
        (GOOD, 'Good'),
        (POOR, 'Poor'), ]
    service_reviewed = models.OneToOneField(
        ServedCustomer, on_delete=models.CASCADE)
    friendliness = models.IntegerField(choices=REVIEW_CHOICES)
    knowledge = models.IntegerField(choices=REVIEW_CHOICES)
    pace = models.IntegerField(choices=REVIEW_CHOICES)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.service_reviewed}>> Friendliness [{self.friendliness}] knowledge [{self.knowledge}] pace[{self.pace}]'
