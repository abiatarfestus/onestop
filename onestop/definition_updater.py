import sys
from datetime import datetime
from dictionary.models import OshindongaWord, WordDefinition
from pairs_extractor import word_pairs

def update_definitions(tagged_dict):
    print("STARTED:", datetime.now())
    key_list = list(tagged_dict.keys())
    count = 0
    for k in key_list[6:]:
        try:
            pair = OshindongaWord.objects.get(id=int(k))
            new_definition = WordDefinition(word_pair=pair, part_of_speech=tagged_dict.get(k)[-1])
            new_definition.save()
            count += 1
        except:
            print(sys.exc_info()[0], "occurred.")
    print(count, "Definitions were added)")
    print("ENDED:", datetime.now())
    return

update_definitions(word_pairs)