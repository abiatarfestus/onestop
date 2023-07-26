import sys
from datetime import datetime

# from django.contrib.auth.models import User
# from autodict import (
#     t_words,
#     u_words,
#     v_words,
#     w_z_words
# )
# from new_words_one import d_k_words
from dictionary.models import EnglishWord, OshindongaWord


def add_eng_words(words_dict):
    """Adds new English words to the dictionary from a python list"""
    print("STARTED:", datetime.now())
    words_list = [word for word in words_dict]
    count = 0
    for word in words_list:
        if word[0].isupper():
            try:
                new_word = EnglishWord(word=word, word_case="Proper Noun")
                new_word.save()
                count += 1
            except:
                print(sys.exc_info()[0], "occurred.")
        else:
            try:
                new_word = EnglishWord(word=word)
                new_word.save()
                count += 1
            except:
                print(sys.exc_info()[0], "occurred.")
    print(count, "English words were added)")
    print("ENDED:", datetime.now())
    return


def add_osh_words(words_dict):
    """Adds new Oshindonga words to the dictionary from a python dictionary"""
    print("STARTED:", datetime.now())
    words_list = [word for word in words_dict]
    count = 0
    for word in words_list:
        for osh_word in words_dict[word]:
            if word[0].isupper() or osh_word[0].isupper():
                try:
                    new_word = OshindongaWord(
                        english_word=EnglishWord.objects.get(word=word),
                        word=osh_word,
                        word_case="Proper Noun",
                    )
                    new_word.save()
                    count += 1
                except:
                    print(sys.exc_info()[0], "occurred.")
            else:
                try:
                    new_word = OshindongaWord(
                        english_word=EnglishWord.objects.get(word=word), word=osh_word
                    )
                    new_word.save()
                    count += 1
                except:
                    print(sys.exc_info()[0], "occurred.")
    print(count, "Oshindonga words were added)")
    print("ENDED:", datetime.now())
    return


# update = [
#     t_words,
#     u_words,
#     v_words,
#     w_z_words
# ]
# for obj in update:
#     add_eng_words(obj)
#     add_osh_words(obj)

# add_eng_words(d_k_words)
# add_osh_words(d_k_words)
