<<<<<<< HEAD
from django.test import TestCase

from dictionary.models import EnglishWord, OshindongaWord, OshindongaPhonetic


class OshindongaWordModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        EnglishWord.objects.create(word="TestWord", word_case="Normal")
        english_word = EnglishWord.objects.all()
        OshindongaPhonetic.objects.create(oshindonga_word="default", phonetics="defolt")
        word_phonetics = OshindongaPhonetic.objects.all()
        OshindongaWord.objects.create(
            english_word=english_word[0],
            word="oshitya",
            word_case="Abbreviation",
            word_phonetics=word_phonetics[0],
        )

    def test_word_case_label(self):
        oshindonga_word = OshindongaWord.objects.get(word="oshitya")
        field_label = oshindonga_word._meta.get_field("word_case").verbose_name
        self.assertEqual(field_label, "word case")

    def test_english_word_label(self):
        oshindonga_word = OshindongaWord.objects.get(word="oshitya")
        field_label = oshindonga_word._meta.get_field("english_word").verbose_name
        self.assertEqual(field_label, "english word")

    def test_word_label(self):
        oshindonga_word = OshindongaWord.objects.get(word="oshitya")
        field_label = oshindonga_word._meta.get_field("word").verbose_name
        self.assertEqual(field_label, "word")

    def test_word_phonetics_label(self):
        oshindonga_word = OshindongaWord.objects.get(word="oshitya")
        field_label = oshindonga_word._meta.get_field("word_phonetics").verbose_name
        self.assertEqual(field_label, "word phonetics")

    def test_word_max_length(self):
        oshindonga_word = OshindongaWord.objects.get(word="oshitya")
        max_length = oshindonga_word._meta.get_field("word").max_length
        self.assertEqual(max_length, 50)

    def test_object_name_is_english_word_pipe_oshindonga_word(self):
        oshindonga_word = OshindongaWord.objects.get(word="oshitya")
        expected_object_name = (
            f"{oshindonga_word.english_word} | {oshindonga_word.word}"
        )
        self.assertEqual(str(oshindonga_word), expected_object_name)

    def test_get_absolute_url(self):
        oshindonga_word = OshindongaWord.objects.get(word="oshitya")
        # This will also fail if the urlconf is not defined.
        self.assertEqual(
            oshindonga_word.get_absolute_url(),
            f"/dictionary/oshindonga-word/{oshindonga_word.id}",
        )
=======
from dictionary.models import EnglishWord

def test_new_english_word(new_english_word):
    # print(new_english_word.word)
    print(EnglishWord.objects.all().count())
    assert True

def test_new_oshindonga_word(new_oshindonga_word):
    print(new_oshindonga_word)
    assert True


    
# def test_word_case_label(new_english_word):
#     field_label = new_english_word._meta.get_field("word_case").verbose_name
#     assert field_label == "word case"

# def test_english_word_label():
#     oshindonga_word = OshindongaWord.objects.get(word="oshitya")
#     field_label = oshindonga_word._meta.get_field("english_word").verbose_name
#     assert(field_label, "english word")

# def test_word_label():
#     oshindonga_word = OshindongaWord.objects.get(word="oshitya")
#     field_label = oshindonga_word._meta.get_field("word").verbose_name
#     assert(field_label, "word")

# def test_word_phonetics_label():
#     oshindonga_word = OshindongaWord.objects.get(word="oshitya")
#     field_label = oshindonga_word._meta.get_field("word_phonetics").verbose_name
#     assert(field_label, "word phonetics")

# def test_word_max_length():
#     oshindonga_word = OshindongaWord.objects.get(word="oshitya")
#     max_length = oshindonga_word._meta.get_field("word").max_length
#     assert(max_length, 50)

# def test_object_name_is_english_word_pipe_oshindonga_word():
#     oshindonga_word = OshindongaWord.objects.get(word="oshitya")
#     expected_object_name = (
#         f"{oshindonga_word.english_word} | {oshindonga_word.word}"
#     )
#     assert(str(oshindonga_word), expected_object_name)

# def test_get_absolute_url():
#     oshindonga_word = OshindongaWord.objects.get(word="oshitya")
#     # This will also fail if the urlconf is not defined.
#     assert(
#         oshindonga_word.get_absolute_url(),
#         f"/dictionary/oshindonga-word/{oshindonga_word.id}",
#     )
>>>>>>> ffe87787d1f395e67cf9792d6212b81a8f2b0e17
