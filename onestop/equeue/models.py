from django.db import models
from django.conf import settings
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class ServiceProvider(models.Model):
    name = models.CharField(max_length=255, unique=True)
    street = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254, blank=True)
    website = models.CharField(max_length=255, blank=True)
    image = ResizedImageField(
        verbose_name='logo', upload_to='service_provider_logos', blank=True)
    join_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name