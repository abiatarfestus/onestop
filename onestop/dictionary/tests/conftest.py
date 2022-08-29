import pytest

from pytest_factoryboy import register
from .factories import (
    UserFactory,
    DefinitionExampleFactory,
    EnglishWordFactory,
    OshindongaIdiomFactory,
    # OshindongaPhoneticFactory,
    OshindongaWordFactory,
    # UnfoundWordFactory,
    WordDefinitionFactory,
)

register(UserFactory)
register(DefinitionExampleFactory)
register(EnglishWordFactory)
register(OshindongaIdiomFactory)
register(OshindongaWordFactory)
register(WordDefinitionFactory)


@pytest.fixture
def new_english_word(db, english_word_factory):
    new_word = english_word_factory.create()
    # print(new_word.word)
    return new_word

@pytest.fixture
def new_oshindonga_word(db, oshindonga_word_factory):
    new_word = oshindonga_word_factory.create()
    # print(new_word.word)
    return new_word

@pytest.fixture
def new_word_definition(word_definition_factory):
    new_definition = word_definition_factory.build()
    return new_definition

@pytest.fixture
def new_definition_example(definition_example_factory):
    new_example = definition_example_factory.build()
    return new_example

@pytest.fixture
def new_oshindonga_idiom(oshindonga_idiom_factory):
    new_idiom = oshindonga_idiom_factory.build()
    return new_idiom
