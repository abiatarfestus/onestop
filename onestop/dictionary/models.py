from django.db import models
from django.urls import reverse
from django.db.models import F  # For referencing fields on the same model
from simple_history.models import HistoricalRecords


# Module level functions and variable


def variants_default():
    return [""]


def plural_default():
    return [""]


def tense_default():
    return {
        "present simple": "",
        "present participle": "",
        "past simple": "",
        "past participle": "",
    }


def get_phonetics_default():
    return OshindongaPhonetic.objects.get(id=1)


class AuthAndTimeTracker(models.Model):
    """
    An abstract base class for adding instance creation and modification time as well as modification history.
    To be inherited by all models.
    """

    time_added = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


# --------------------------------------------------------------------------------------------------------------


class EnglishWord(AuthAndTimeTracker):
    """
    A model that adds and modifies English words in the database
    """

    ABBREVIATION = "Abbreviation"
    PROPER_NOUN = "Proper Noun"
    NORMAL = "Normal"
    WORD_CASE = [
        (ABBREVIATION, "Abbreviation"),
        (PROPER_NOUN, "Proper Noun"),
        (NORMAL, "Normal"),
    ]
    word = models.CharField(
        unique=True,
        max_length=50,
        error_messages={
            "unique": "The English word you entered already exists in the dictionary."
        },
    )
    word_case = models.CharField(
        max_length=12,
        choices=WORD_CASE,
        default=NORMAL,
        help_text="Indicate whether the word you are entering is a normal word, abbretiation or proper noun.",
    )

    def __str__(self):
        return self.word

    def get_absolute_url(self):
        # from django.urls import reverse
        return reverse("dictionary:english-word-detail", args=[str(self.id)])
        # return reverse('dictionary:english-create')


# --------------------------------------------------------------------------------------------------------------


class OshindongaPhonetic(AuthAndTimeTracker):
    """
    A model that adds and modifies Oshindonga word phonetic characteristics in the database
    """

    # objects = models.Manager()
    oshindonga_word = models.CharField(max_length=50, null=False, blank=False)
    pronunciation = models.FileField(
        upload_to="pronunciations", blank=True
    )  # Takes pronunciation audio
    # Takes phonetic transcription
    phonetics = models.CharField(
        max_length=255, blank=True, verbose_name="Phonetic trascription"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "oshindonga_word",
                    "phonetics",
                ],
                name="unique_phonetics",
            )
        ]

    def __str__(self):
        return "%s | %s" % (self.oshindonga_word, self.phonetics)

    def get_absolute_url(self):
        # from django.urls import reverse
        # url pattern/template not yet implemented
        return reverse("dictionary:oshindonga-phonetic-detail", args=[str(self.id)])
        # return reverse('dictionary:oshindonga-create')


# ---------------------------------------------------------------------------------------------------------------


class OshindongaWord(AuthAndTimeTracker):
    """
    A model that adds and modifies Oshindonga words in the database
    """

    ABBREVIATION = "Abbreviation"
    PROPER_NOUN = "Proper Noun"
    NORMAL = "Normal"
    WORD_CASE = [
        (ABBREVIATION, "Abbreviation"),
        (PROPER_NOUN, "Proper Noun"),
        (NORMAL, "Normal"),
    ]
    # objects = models.Manager()
    english_word = models.ForeignKey(EnglishWord, on_delete=models.CASCADE)
    word = models.CharField(unique=False, max_length=50)
    word_case = models.CharField(
        max_length=12,
        choices=WORD_CASE,
        default=NORMAL,
        help_text="Ulika ngele oshitya wa shanga oshowala, efupipiko nenge oshityadhinalela.",
    )
    word_phonetics = models.ForeignKey(
        OshindongaPhonetic,
        null=True,
        on_delete=models.SET_NULL,
        default=get_phonetics_default,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["english_word", "word", "word_case"], name="unique_word_pair"
            )
        ]

    def __str__(self):
        return f"{self.english_word} | {self.word}"

    def get_absolute_url(self):
        # from django.urls import reverse
        return reverse("dictionary:oshindonga-word-detail", args=[str(self.id)])
        # return reverse('dictionary:oshindonga-create')


# --------------------------------------------------------------------------------------------------------------


class WordDefinition(AuthAndTimeTracker):
    """
    A model for the parts of speech/word catgories to be used to provid choices when adding dfinitions.
    """
    PART_OF_SPEECH_CHOICES = [
        ("", "Select the part of speech of your definition"),
        ("CC", "Coordinating conjunction"),
        ("CD", "Cardinal digit"),
        ("DT", "Determiner"),
        ("EX", "Existential there [e.g., there is]"),
        ("FW", "Foreign word"),
        ("IN", "Preposition/Subordinating conjunction"),
        ("JJ", "Adjective"),
        ("JJR", "Adjective, comparative"),
        ("JJS", "Adjective, superlative"),
        ("LS", "List marker"),
        ("MD", "Modal"),
        ("NN", "Noun, singular"),
        ("NNS", "Noun, plural"),
        ("NNP", "Proper noun, singular"),
        ("NNPS", "Proper noun, plural"),
        ("PDT", "Predeterminer"),
        ("POS", "Possessive ending [e.g., parent's]"),
        ("PRP", "Personal pronoun"),
        ("PRP$", "Possessive pronoun"),
        ("RB", "Adverb"),
        ("RBR", "Adverb, comparative"),
        ("RBS", "Adverb, superlative"),
        ("RP", "Particle [e.g., come in/up/over]"),
        ("TO", "To [e.g., to + verb]"),
        ("UH", "Interjection"),
        ("VB", "Verb, base form"),
        ("VBD", "Verb, past tense"),
        ("VBG", "Verb, gerund/present participle"),
        ("VBN", "Verb, past participle"),
        ("VBP", "Verb, sing. present, non-3d"),
        ("VBZ", "Verb, 3rd person sing. Present"),
        ("WDT", "Wh-determiner [e.g., which]"),
        ("WP", "Wh-pronoun [e.g., who, what]"),
        ("WP$", "Possessive wh-pronoun [e.g., whose]"),
        ("WRB", "Wh-abverb where [e.g., when]"),
    ]

    word_pair = models.ForeignKey(
        OshindongaWord, on_delete=models.CASCADE, related_name="definitions"
    )
    part_of_speech = models.CharField(
        max_length=25,
        choices=PART_OF_SPEECH_CHOICES,
    )
    synonyms = models.ManyToManyField(
        OshindongaWord, blank=True, related_name="synonyms"
    )
    simple_present = models.CharField(max_length=50, blank=True)
    present_participle = models.CharField(max_length=50, blank=True)
    simple_past = models.CharField(max_length=50, blank=True)
    past_participle = models.CharField(max_length=50, blank=True)
    plurals = models.ManyToManyField(
        OshindongaWord, blank=True, related_name="plurals"
    )
    english_definition = models.CharField(max_length=255, blank=True)
    oshindonga_definition = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.word_pair}: {self.part_of_speech} {[self.id]}"

    def get_absolute_url(self):
        # from django.urls import reverse
        return reverse("dictionary:word-definition-detail", args=[str(self.id)])


# --------------------------------------------------------------------------------------------------------------


class DefinitionExample(AuthAndTimeTracker):
    """
    A model that adds and modifies exmples to word definitions.
    """

    definition = models.ForeignKey(WordDefinition, on_delete=models.CASCADE)
    english_example = models.CharField(max_length=255)
    oshindonga_example = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % (self.definition)

    def get_absolute_url(self):
        # from django.urls import reverse
        # return reverse('dictionary:example-update', args=[str(self.id)])
        return reverse("dictionary:definition-example-detail", args=[str(self.id)])


# --------------------------------------------------------------------------------------------------------------


class OshindongaIdiom(AuthAndTimeTracker):
    """
    A model that adds and modifies idioms for Oshindonga words.
    """

    word_pair = models.ForeignKey(OshindongaWord, on_delete=models.CASCADE)
    oshindonga_idiom = models.CharField(max_length=255)
    meaning = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "%s" % (self.word_pair)

    def get_absolute_url(self):
        # from django.urls import reverse
        return reverse("dictionary:oshindonga-idiom-detail", args=[str(self.id)])


class UnfoundWord(models.Model):
    """
    A model that records words that were searched, but no found in the dictionary.
    """

    word = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    time_searched = models.DateTimeField(auto_now_add=True)
    search_count = models.IntegerField(default=1)
    added_to_dict = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["word", "language"], name="unique_unfound_word"
            )
        ]

    def __str__(self):
        return f"{self.word}: {self.language}"

    # def get_absolute_url(self):
    # from django.urls import reverse
    # return reverse('dictionary:example-update', args=[str(self.id)])
    # return reverse('dictionary:definition-example-detail', args=[str(self.id)])
