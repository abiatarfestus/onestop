import random

import factory
from dictionary.models import (
    DefinitionExample,
    EnglishWord,
    OshindongaIdiom,
    OshindongaPhonetic,
    OshindongaWord,
    UnfoundWord,
    WordDefinition,
)
from django.contrib.auth.models import User
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()


class EnglishWordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EnglishWord

    word = fake.word()


# class OshindongaPhoneticFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = OshindongaPhonetic

#     oshindonga_word =
#     pronunciation =


class OshindongaWordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OshindongaWord

    english_word = factory.SubFactory(EnglishWordFactory)
    word = "oshitya"


class WordDefinitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WordDefinition

    word_pair = factory.SubFactory(OshindongaWordFactory)
    part_of_speech = random.choice(
        [
            "CC",
            "CD",
            "DT",
            "EX",
            "FW",
            "IN",
            "JJ",
            "JJR",
            "JJS",
            "LS",
            "MD",
            "NN",
            "NNS",
            "NNP",
            "NNPS",
            "PDT",
            "POS",
            "PRP",
            "PRP$",
            "RB",
            "RBR",
            "RBS",
            "RP",
            "TO",
            "UH",
            "VB",
            "VBD",
            "VBG",
            "VBN",
            "VBP",
            "VBZ",
            "WDT",
            "WP",
            "WP$",
            "WRB",
        ]
    )
    english_definition = fake.sentence()
    oshindonga_definition = fake.sentence()


class DefinitionExampleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DefinitionExample

    definition = factory.SubFactory(WordDefinitionFactory)
    english_example = fake.sentence()
    oshindonga_example = fake.sentence()


class OshindongaIdiomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OshindongaIdiom

    word_pair = factory.SubFactory(OshindongaWordFactory)
    oshindonga_idiom = fake.word()
    meaning = fake.sentence()


# class UnfoundWordFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = UnfoundWord

#     word =
#     language =
#     time_searched =
#     search_count =
#     added_to_dict =
