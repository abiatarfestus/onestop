from django.db.models.signals import post_save #Import a post_save signal when a new English/Oshindonga word is added
from .models import EnglishWord, OshindongaWord, UnfoundWord
from django.dispatch import receiver # Import the receiver


@receiver(post_save, sender=EnglishWord) 
def update_unfound_english(sender, instance, created, **kwargs):
    if created:
        try:
            UnfoundWord.objects.filter(word=instance.word.lower(), language='English').update(added_to_dict = True)
        except:
            pass

@receiver(post_save, sender=OshindongaWord) 
def update_unfound_oshindonga(sender, instance, created, **kwargs):
    if created:
        try:
            UnfoundWord.objects.filter(word=instance.word.lower(), language='Oshindonga').update(added_to_dict = True)
        except:
            pass
