from django.db.models.signals import (
    post_save,
)  # Import a post_save signal when a user is created
from django.contrib.auth.models import (
    User,
)  # Import the built-in User model, which is a sender
from django.dispatch import receiver  # Import the receiver
from .models import Customer


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)
        # print("CUSTOMER CREATION SIGNAL EXECUTED")


@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    try:
        instance.customer.save()
        # print("CUSTOMER SAVE SIGNAL EXECUTED")
    except Exception as e:
        print(e)


# Test yml update
