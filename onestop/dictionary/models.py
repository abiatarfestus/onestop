from django.db import models
from django.db.models import F  #For referencing fields on the same model
#from datetime import datetime
#from django.contrib.auth import get_user_model
#from audit_log.models.fields import CreatingUserField, CreatingSessionKeyField, LastUserField, LastSessionKeyField
# https://django-simple-history.readthedocs.io/en/latest/index.html
from simple_history.models import HistoricalRecords


# Create your models here.

class AuthAndTimeTracker(models.Model):
    '''
    An abstract base class for adding instance creation and modification time as well as modification history.
    To be inherited by all models.
    '''
    # (get_user_model(), null=True, on_delete=models.SET_NULL)
    #added_by = CreatingUserField()
    time_added = models.DateField(auto_now_add=True)
    # https://django-audit-log.readthedocs.io/en/latest/index.html
    #created_with_session_key = CreatingSessionKeyField()
    # (get_user_model(), null=True, on_delete=models.SET_NULL)
    #modified_by = LastUserField(on_delete=models.SET_NULL)
    time_modified = models.DateField(auto_now=True)
    #modified_with_session_key = LastSessionKeyField()

    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True), inherit=True)

    class Meta:
        abstract = True


class EnglishWord(AuthAndTimeTracker):
    '''
    A model that adds and modifies English words in the database
    '''
    word = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.word


class OshindongaWord(AuthAndTimeTracker):
    '''
    A model that adds and modifies Oshindonga words in the database
    '''
    word = models.CharField(unique=False, max_length=50)
    english_word = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)

    def __str__(self):
        return self.word

class WordDefinition(AuthAndTimeTracker):
    '''
    A model for the parts of speech/word catgories to be used to provid choices when adding dfinitions.
    '''
    NOUN = 'Noun'
    PRONOUN = 'Pron.'
    VERB = 'Verb'
    ADJECTIVE = 'Adj.'
    ADVERB = 'Adv.'
    PREPOSITION = 'Prep.'
    CONJUNCTION = 'Conj.'
    INTERJECTION = 'Int.'
    PART_OF_SPEECH_CHOICES = [
        (NOUN, 'Noun'),
        (PRONOUN, 'Pronoun'),
        (VERB, 'Verb'),
        (ADJECTIVE, 'Adjective'),
        (ADVERB, 'Adverb'),
        (PREPOSITION, 'Preposition'),
        (CONJUNCTION, 'Conjunction'),
        (INTERJECTION, 'Interjection'),
    ]

    # def english_word_match(self):
    #     return OshindongaWord.objects.filter(word=F('oshindonga_word')).english_word()

    part_of_speech = models.CharField(
        max_length=5,
        choices=PART_OF_SPEECH_CHOICES,
    )
    oshindonga_word = models.ForeignKey(OshindongaWord, on_delete=models.CASCADE)
    # english_word = models.CharField(max_length=50, editable=False, default=english_word_match)
    english_definition = models.TextField()
    oshindonga_definition = models.TextField()
