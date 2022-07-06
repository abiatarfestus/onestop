english_words = EnglishWord.objects.order_by("-time_added")[:5]
oshindonga_words = OshindongaWord.objects.order_by("-time_added")[:5]
new_phonetics = OshindongaPhonetic.objects.order_by("-time_added")[:5]
random_unphonetised = OshindongaWord.objects.filter(word_phonetics_id=1).order_by("?")[
    :5
]


def get_undefined_words():
    all_word_pairs = OshindongaWord.objects.all()
    word_pair_ids = [pair.id for pair in all_word_pairs]
    all_definitions = WordDefinition.objects.all()
    defined_ids = [definition.word_pair_id for definition in all_definitions]
    undefined_ids = [i for i in word_pair_ids if i not in defined_ids]
    random.shuffle(undefined_ids)
    undefined_word_pairs = []
    for i in undefined_ids[:5]:
        undefined_word_pairs.append(OshindongaWord.objects.get(id=i))
    return undefined_word_pairs
