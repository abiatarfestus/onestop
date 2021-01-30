from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class English(models.Model):
    word = models.CharField(unique=True, max_length=50)
    added_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.SET_NULL)
    word_history = models.CharField(editable=False, blank=True, default='') 

    # Create a method for generating word history upon update
    # def history_generator(self):
    #     return ''