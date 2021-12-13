import sys
from datetime import datetime
# from django.contrib.auth.models import User
import auto_updater
from dictionary.models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom

def add_eng_words(words_list):
    '''Adds new English words to the dictionary from a python list'''
    print("STARTED:", datetime.now())
    count = 0
    for word in words_list:
        try:
            # word = word.strip()
            new_word = EnglishWord(word=word)
            new_word.save()
            count += 1
        except:
            print(sys.exc_info()[0], "occurred.")
    print(count, "English words were added)")
    print("ENDED:", datetime.now())
    return

def add_osh_words(words_dict, words_list):
    '''Adds new Oshindonga words to the dictionary from a python dictionary'''
    print("STARTED:", datetime.now())
    english_queryset = EnglishWord.objects.all()
    english_words = [word.word for word in english_queryset]
    count = 0
    for word in words_list:
        if word in english_words:
            for osh_word in words_dict[word]:
                try:
                    new_word = OshindongaWord(english_word=word, word=osh_word)
                    new_word.save()
                    count += 1
                except:
                    print(sys.exc_info()[0], "occurred.")
    print(count, "Oshindonga words were added)")
    print("ENDED:", datetime.now())
    return