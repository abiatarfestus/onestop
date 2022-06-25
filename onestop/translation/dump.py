# nlp = spacy.load("en_core_web_trf")
# nlp.disable_pipe("parser")
# nlp.enable_pipe("senter")
# "Apple is looking at buying U.K. startup for $1 billion"

def process_text(self):
        '''Takes the source text and, depending on the source language, processes it with spaCy pipline to tokenize and tag it (convert it to Doc)
        Para: None
        Return: A list of keys in tagged_dict'''
        if self.src_language == "EN":
            nlp = spacy.load("en_core_web_sm", exclude=["ner", "parser", "lemmatizer"])
            doc = nlp(self.src_text)
            for token in doc:
                dict_item = {token.text: [token.pos_, token.tag_]}
                self.tagged_dict.update(dict_item)
            print(self.tagged_dict)
            tagged_words = self.tagged_dict.keys()
        else:
            tagged_words = self.tagged_dict.keys()
        return tagged_words

    def match_src_to_target(self, tagged_words):
        '''Takes tagged words and try to find matching words from the target language
        Para: Tagged words, list
        Return: A list of tuples of (source word, target word), defaults to -1 if no target word found'''
        word_pairs = []
        if self.src_language == "EN":
            for word in tagged_words:
                try:
                    current_word = OshindongaWord.objects.get(english_word=word)
                except IntegrityError:
                    current_word = -1
                finally:
                    word_pairs.append((word, current_word))
            print(word_pairs)
        else:
            pass
        return word_pairs

    def replace_src_with_target(self, word_pairs):
        '''Takes word pairs and update the tagged dictionary by  target language
        Para: Tagged words, list
        Return: A list of tuples of (source word, target word), defaults to -1 if no target word found'''
        for word_pair in word_pairs:
            if word_pair[1] != -1:
                self.tagged_dict.update({word_pair[0]:word_pair[1]})
        print(self.tagged_dict)

    def translate(self):
        tagged_words = self.process_text()
        word_pairs = self.match_src_to_target(tagged_words)
        self.replace_src_with_target(word_pairs)


print(f"\n \n \nInput text ************************************\n{txt}")