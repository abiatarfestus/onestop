import json
from datetime import datetime
from lexicon import lexicon
from dictionary.models import OshindongaWord


def check_osh_words(word_list):
    """Check if an Oshindonga word already exists in the database, if not add it to the new lexicon list"""
    print("STARTED:", datetime.now())
    count = 0
    new_lexicon = []
    print("Going through word list...")
    for word in word_list:
        osh_word = OshindongaWord.objects.filter(word=word.lower())
        if len(osh_word) == 0:
            new_lexicon.append(word)
        else:
            count +=1
    with open('new_lexicon.txt', 'w') as dest_file:
        print('STARTED Writing to Json File')
        json.dump(new_lexicon, dest_file, indent='')
    print("ENDED:", datetime.now())
    print(f"TOTAL Words Discarded: {count}")
    return

def normalise_words(word_list):
    """Lower case words and add them to a set to remove dulicates"""
    print("Going through word list...")
    new_lexicon = set(word.lower() for word in word_list)
    with open('new_lexicon.txt', 'w') as dest_file:
        print('STARTED Writing to Json File')
        json.dump(sorted(list(new_lexicon)), dest_file, indent='')
    return

# check_osh_words(lexicon)
normalise_words(lexicon)