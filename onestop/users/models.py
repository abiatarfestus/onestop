from PIL import Image
from django.db import models
from django.contrib.auth.models import User
from django_resized import ResizedImageField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = ResizedImageField(default='profile_pics/default.apng', size=[200, 200], upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

    # Override the save method of the model
    # def save(self, *args, **kwargs):
    #     super().save()
    #     img = Image.open(self.image.path) # Open image
    #     # print(f'IMAGE PATH: {self.image.path}')
    #     # print(f'IMAGE NAME: {self.image.name}')
        
    #     # resize image
    #     if img.height > 200 or img.width > 200:
    #         output_size = (200, 200)
    #         img.thumbnail(output_size) # Resize image
    #         img.save(self.image.path) # Save it again and override the larger image