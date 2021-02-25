from django.db import models
from django.db.models import F  # For referencing fields on the same model
from simple_history.models import HistoricalRecords


# Module level functions and variable

def variants_default():
    return ['']


def plural_default():
    return ['']


def tense_default():
    return {'present simple': '', 'present participle': '', 'past simple': '', 'past participle': ''}


class AuthAndTimeTracker(models.Model):
    '''
    An abstract base class for adding instance creation and modification time as well as modification history.
    To be inherited by all models.
    '''
    time_added = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

# --------------------------------------------------------------------------------------------------------------


class EnglishWord(AuthAndTimeTracker):
    '''
    A model that adds and modifies English words in the database
    '''
    ABBREVIATION = 'Abbreviation'
    PROPER_NOUN = 'Proper Noun'
    NORMAL = 'Normal'
    WORD_CASE = [
        (ABBREVIATION, 'Abbreviation'),
        (PROPER_NOUN, 'Proper Noun'),
        (NORMAL, 'Normal'),
    ]
    word = models.CharField(unique=True, max_length=50, error_messages={
                            'unique': 'The English word you entered already exists in the dictionary.'})
    word_case = models.CharField(
        max_length=12,
        choices=WORD_CASE, default=NORMAL, help_text='Indicate whether the word you are entering is a normal word, abbretiation or proper noun.'
    )

    def __str__(self):
        return self.word

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dictionary:english-word-detail', args=[str(self.id)])
        # return reverse('dictionary:english-create')


# --------------------------------------------------------------------------------------------------------------


class OshindongaWord(AuthAndTimeTracker):
    '''
    A model that adds and modifies Oshindonga words in the database
    '''
    ABBREVIATION = 'Abbreviation'
    PROPER_NOUN = 'Proper Noun'
    NORMAL = 'Normal'
    WORD_CASE = [
        (ABBREVIATION, 'Abbreviation'),
        (PROPER_NOUN, 'Proper Noun'),
        (NORMAL, 'Normal'),
    ]
    #objects = models.Manager()
    english_word = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)
    word = models.CharField(unique=False, max_length=50)
    word_case = models.CharField(
        max_length=12,
        choices=WORD_CASE, default=NORMAL, help_text='Ulika ngele oshitya wa shanga oshowala, efupipiko nenge oshityadhinalela.'
    )

    def __str__(self):
        return "%s | %s" % (self.english_word, self.word)

    def get_absolute_url(self):
        from django.urls import reverse
        # return reverse('dictionary:oshindonga-word-detail', args=[str(self.id)])
        return reverse('dictionary:oshindonga-create')

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
    SELECT = ''
    NOUN = 'Noun'
    PRONOUN = 'Pron.'
    VERB = 'Verb'
    ADJECTIVE = 'Adj.'
    ADVERB = 'Adv.'
    PREPOSITION = 'Prep.'
    CONJUNCTION = 'Conj.'
    INTERJECTION = 'Int.'
    PART_OF_SPEECH_CHOICES = [
        (SELECT, 'Select the part of speech of your definition'),
        (NOUN, 'Noun'),
        (PRONOUN, 'Pronoun'),
        (VERB, 'Verb'),
        (ADJECTIVE, 'Adjective'),
        (ADVERB, 'Adverb'),
        (PREPOSITION, 'Preposition'),
        (CONJUNCTION, 'Conjunction'),
        (INTERJECTION, 'Interjection'),
    ]

    word_pair = models.ForeignKey(OshindongaWord, on_delete=models.CASCADE)
    part_of_speech = models.CharField(
        max_length=5,
        choices=PART_OF_SPEECH_CHOICES,
    )
    variants = models.JSONField(default=variants_default)
    plural = models.JSONField(default=plural_default)
    tense = models.JSONField(default=tense_default)
    # english_word = models.CharField(max_length=50, editable=False, default=english_word_match)
    english_definition = models.CharField(max_length=255)
    oshindonga_definition = models.CharField(max_length=255)

    def __str__(self):
        return "%s (%s) [%s]" % (self.word_pair, self.part_of_speech, self.id)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dictionary:word-definition-detail', args=[str(self.id)])

# --------------------------------------------------------------------------------------------------------------


class DefinitionExample(AuthAndTimeTracker):
    '''
    A model that adds and modifies exmples to word definitions.
    '''
    #objects = models.Manager()
    definition = models.ForeignKey(
        WordDefinition, on_delete=models.CASCADE)
    english_example = models.CharField(max_length=255)
    oshindonga_example = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % (self.definition)

    def get_absolute_url(self):
        from django.urls import reverse
        # return reverse('dictionary:example-update', args=[str(self.id)])
        return reverse('dictionary:definition-example-detail', args=[str(self.id)])

# --------------------------------------------------------------------------------------------------------------


class OshindongaIdiom(AuthAndTimeTracker):
    '''
    A model that adds and modifies idioms for Oshindonga words.
    '''
    #objects = models.Manager()
    word_pair = models.ForeignKey(
        OshindongaWord, on_delete=models.CASCADE)
    oshindonga_idiom = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % (self.oshindonga_word)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('dictionary:oshindonga-idiom-detail', args=[str(self.id)])
