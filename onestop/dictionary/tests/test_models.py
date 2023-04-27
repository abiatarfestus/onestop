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
