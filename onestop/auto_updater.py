import sys
from datetime import datetime
# from django.contrib.auth.models import User
from autodict import e_words, f_words, g_words, h_words, i_words, j_words, k_words, l_words, m_words, n_words, o_words, p_words
from dictionary.models import EnglishWord, OshindongaWord

def add_eng_words(words_dict):
    '''Adds new English words to the dictionary from a python list'''
    print("STARTED:", datetime.now())
    words_list = [word for word in words_dict]
    count = 0
    for word in words_list:
        if word[0].isupper():
            try:
                new_word = EnglishWord(word=word, word_case='Proper Noun')
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
    '''Adds new Oshindonga words to the dictionary from a python dictionary'''
    print("STARTED:", datetime.now())
    words_list = [word for word in words_dict]
    count = 0
    for word in words_list:
        for osh_word in words_dict[word]:
            if word[0].isupper() or osh_word[0].isupper():
                try:
                    new_word = OshindongaWord(english_word=EnglishWord.objects.get(word=word), word=osh_word, word_case='Proper Noun')
                    new_word.save()
                    count += 1
                except:
                    print(sys.exc_info()[0], "occurred.")
            else:
                try:
                    new_word = OshindongaWord(english_word=EnglishWord.objects.get(word=word), word=osh_word)
                    new_word.save()
                    count += 1
                except:
                    print(sys.exc_info()[0], "occurred.")
    print(count, "Oshindonga words were added)")
    print("ENDED:", datetime.now())
    return

update = [e_words, f_words, g_words, h_words, i_words, j_words, k_words, l_words, m_words, n_words, o_words, p_words]
for obj in update:
    add_eng_words(obj)
    add_osh_words(obj)
