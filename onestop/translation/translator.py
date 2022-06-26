import spacy
from dictionary.models import EnglishWord, OshindongaWord


class Translation:
    def __init__(self, src_lang, src_text):
        self.src_language = src_lang
        self.src_text = src_text
        self.tagged_src_tokens = []

    def process_src_text(self):
        """Takes the source text and processes it with spaCy pipline to tokenize and tag it (convert it to Doc)
        Para: None
        Return: None"""
        if self.src_language == "English":
            nlp = spacy.load("en_core_web_sm", exclude=["ner", "parser", "lemmatizer"])
            doc = nlp(self.src_text)
            for token in doc:
                current_token = [token.text, token.pos_, token.tag_]
                self.tagged_src_tokens.append(current_token)
            # print(self.tagged_src_tokens)
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
                    match_found = OshindongaWord.objects.filter(
                        english_word_id=EnglishWord.objects.get(word=src_token[0])
                    )
                    if len(match_found) > 0:
                        target_word = match_found[0].word
                    else:
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
        return translated_string

    def translate(self):
        self.process_src_text()
        word_pairs = self.match_src_to_target()
        self.replace_src_with_target(word_pairs)
        output_text = self.process_target_text()
        print("Output text ***************************************")
        print(output_text)
        return output_text


# new_translation = Translation("English", "Apple is looking at buying U.K. startup for $1 billion")
txt = "No part of this book may be reproduced in any written, electronic, recording, or photocopying without written permission of the author. The exception would be in the case of brief quotations embodied in the critical articles or reviews and pages where permission is specifically granted by the author."
