from django.db.models import Q
from string import punctuation

# from onestop.dictionary.models import WordDefinition
import spacy
from dictionary.models import EnglishWord, OshindongaWord, WordDefinition


class Translation:
    punctuation = [
        ".",
        ",",
        ":",
        "?",
        ";",
        "!",
        ")",
        "]",
        "}",
        '"',
    ]

    def __init__(self, src_lang, src_text):
        self.src_language = src_lang
        self.src_text = src_text
        self.tagged_src_tokens = []
        if src_lang == "English":
            self.nonexist = ["the", "a", "an"]
        else:
            self.nonexist = []

    def process_src_text(self):
        """Takes the source text and processes it with spaCy pipline to tokenize and tag it (convert it to Doc)
        Para: None
        Return: None"""
        if self.src_language == "English":
            nlp = spacy.load("en_core_web_sm", exclude=["ner", "lemmatizer"])
            doc = nlp(self.src_text)
            for token in doc:
                current_token = [token.text, token.pos_, token.tag_]
                self.tagged_src_tokens.append(current_token)
            print("Before: ", self.tagged_src_tokens)
            for token in self.tagged_src_tokens:
                if token[0].lower() in self.nonexist:
                    self.tagged_src_tokens.remove(token)
            print("After: ", self.tagged_src_tokens)
        else:
            pass
        return

    def match_src_to_target(self):
        """Loops through tagged words and try to find matching words from the target language
        Para: None
        Return: A list of tuples of (source word, target word), defaults to -1 if no target word found"""
        word_pairs = []
        if self.src_language == "English":
            for src_token in self.tagged_src_tokens:
                target_word = -1
                try:
                    # A queryset of all pairs, where the english_word matches the current token
                    matched_word_pairs = OshindongaWord.objects.filter(
                        english_word_id=EnglishWord.objects.get(word=src_token[0])
                    )

                    # if len(matched_word_pairs) > 0:
                    if matched_word_pairs:
                        # print(f"MATCH FOUND: {matched_word_pairs}")
                        #  A list of pks of the matched word pairs
                        matched_word_pairs_id = [pair.id for pair in matched_word_pairs]
                        # pairs_with_matched_pos = [pair for pair in matched_word_pairs]
                        # A queryset of definitions with the POS matching the current token
                        definitions_with_matched_pos = WordDefinition.objects.filter(
                            Q(word_pair_id__in=matched_word_pairs_id)
                            & Q(part_of_speech=src_token[1])
                        ).select_related("word_pair")
                        # print(f"DEFINITIONS: {definitions_with_matched_pos}")
                        # Oshindonga word from the first definition in the queryset
                        target_word = definitions_with_matched_pos[0].word_pair.word
                    else:
                        # print("NO MATCH FOUND")
                        target_word = -1
                    # print(f'MATCH_FOUND: {match_found}')
                except Exception:
                    pass
                finally:
                    word_pairs.append((src_token[0], target_word))
            # print(word_pairs)
        else:
            pass
        return word_pairs

    def replace_src_with_target(self, word_pairs):
        """Loops through word pairs and update the tagged tokens with target language
        Para: word_pairs, list
        Return: None"""
        for i in range(len(word_pairs) - 1):
            if word_pairs[i][1] != -1:
                self.tagged_src_tokens[i][0] = word_pairs[i][1]
        # print(self.tagged_src_tokens)
        return

    def process_target_text(self):
        translated_list = [token[0] for token in self.tagged_src_tokens]
        translated_string = " ".join(translated_list)
        for punct in punctuation:
            if f" {punct}" in translated_string:
                translated_string = translated_string.replace(f" {punct}", f"{punct}")
        return translated_string

    def translate(self):
        self.process_src_text()
        word_pairs = self.match_src_to_target()
        self.replace_src_with_target(word_pairs)
        output_text = self.process_target_text()
        # print("Output text ***************************************")
        # print("\n\n")
        return output_text


# new_translation = Translation("English", "Apple is looking at buying U.K. startup for $1 billion")
txt = "No part of this book may be reproduced in any written, electronic, recording, or photocopying without written permission of the author. The exception would be in the case of brief quotations embodied in the critical articles or reviews and pages where permission is specifically granted by the author."
