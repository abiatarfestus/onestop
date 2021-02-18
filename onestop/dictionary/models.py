from django.db import models
from django.db.models import F  # For referencing fields on the same model
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
    objects = models.Manager()
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True), inherit=True)

    class Meta:
        abstract = True

# --------------------------------------------------------------------------------------------------------------


class EnglishWord(AuthAndTimeTracker):
    '''
    A model that adds and modifies English words in the database
    '''
    ABBREVIATION = 'Abbreviation'
    PROPER_NOUN = 'Proper'
    NORMAL = 'Normal'
    WORD_CASE = [
        (ABBREVIATION, 'Abbreviation'),
        (PROPER_NOUN, 'Proper'),
        (NORMAL, 'Normal'),
    ]
    word = models.CharField(unique=True, max_length=50)
    word_case = models.CharField(
        max_length=12,
        choices=WORD_CASE, default=NORMAL,
    )

    def __str__(self):
        return self.word

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dictionary:add-english', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.word_case == self.ABBREVIATION:
            self.word.strip().upper()
        elif self.word_case == self.PROPER_NOUN:
            self.word.capitalize()
        else:
            self.word.strip().lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.

# --------------------------------------------------------------------------------------------------------------


class OshindongaWord(AuthAndTimeTracker):
    '''
    A model that adds and modifies Oshindonga words in the database
    '''
    ABBREVIATION = 'Abbreviation'
    PROPER_NOUN = 'Proper'
    NORMAL = 'Normal'
    WORD_CASE = [
        (ABBREVIATION, 'Abbreviation'),
        (PROPER_NOUN, 'Proper'),
        (NORMAL, 'Normal'),
    ]
    #objects = models.Manager()
    english_word = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)
    word = models.CharField(unique=False, max_length=50)
    word_case = models.CharField(
        max_length=12,
        choices=WORD_CASE, default=NORMAL,
    )

    def __str__(self):
        return "%s | %s" % (self.english_word, self.word)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dictionary.views.OshindongaWordUpdate.as_view()', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.word_case == self.ABBREVIATION:
            self.word.strip().upper()
        elif self.word_case == self.PROPER_NOUN:
            self.word.strip().capitalize()
        else:
            self.word.strip().lower()
        super().save(*args, **kwargs)  # Call the "real" save() method.
# --------------------------------------------------------------------------------------------------------------


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
    #objects = models.Manager()
    word_pair = models.ForeignKey(OshindongaWord, on_delete=models.CASCADE)
    part_of_speech = models.CharField(
        max_length=5,
        choices=PART_OF_SPEECH_CHOICES,
    )
    variants = models.JSONField(blank=True)
    plural = models.JSONField(blank=True)
    tense = models.JSONField(blank=True)
    # english_word = models.CharField(max_length=50, editable=False, default=english_word_match)
    english_definition = models.TextField()
    oshindonga_definition = models.TextField()

    def __str__(self):
        return "%s (%s) [%s]" % (self.word_pair, self.part_of_speech, self.id)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dictionary.views.WordDefinitionUpdate.as_view()', args=[str(self.id)])

# --------------------------------------------------------------------------------------------------------------


class DefinitionExample(AuthAndTimeTracker):
    '''
    A model that adds and modifies exmples to word definitions.
    '''
    #objects = models.Manager()
    definition = models.ForeignKey(WordDefinition, on_delete=models.CASCADE)
    english_example = models.TextField()
    oshindonga_example = models.TextField()

    def __str__(self):
        return "%s" % (self.definition)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dictionary.views.DefinitionExampleUpdate.as_view()', args=[str(self.id)])

# --------------------------------------------------------------------------------------------------------------


class OshindongaIdiom(AuthAndTimeTracker):
    '''
    A model that adds and modifies idioms for Oshindonga words.
    '''
    #objects = models.Manager()
    oshindonga_word = models.ForeignKey(
        OshindongaWord, on_delete=models.CASCADE)
    oshindonga_idiom = models.TextField()

    def __str__(self):
        return "%s" % (self.oshindonga_word)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dictionary.views.OshindongaIdiomUpdate.as_view()', args=[str(self.id)])
