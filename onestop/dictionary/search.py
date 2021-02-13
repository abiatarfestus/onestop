from django.shortcuts import render
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample


class SearchEnglishDefinition():

    def __init__(self, request, word):
        self.request = request
        self.word = word
        self.context = {'searched_word': 'Word not found',
                        'definitions': '', 'examples': ''}

    def search_english(self):
        '''
            Check if the searched English word exists in the English model. If found return its pk
        '''
        try:
            # Search within English model, and if foud:
            self.eng_word = EnglishWord.objects.get(word=self.word)
            # Get the the id/pk of the word found to be used in Oshindonga model
            self.eng_word_pk = self.eng_word.id
        except EnglishWord.DoesNotExist:
            return render(self.request, 'dictionary/search.html', self.context)
        #return self.eng_word_pk
        self.search_word_pairs(self.eng_word_pk)

    def search_word_pairs(self, eng_word_pk):
        '''
            Using the English word pk (foreignkey id) search if for English|Oshindonga pairs and return a list of pks of all pair objects found.
        '''
        self.word_pairs = OshindongaWord.objects.filter(english_word_id=eng_word_pk)  # Return a queryset of all word pairs with the searched word
        if self.word_pairs == []:
            self.context['searched_word'] = 'The word you searched is not yet translated into Oshindonga.'
            return render(self.request, 'dictionary/search.html', self.context)
        else:
            self.context['searched_word'] = self.word_pairs
            # Etract pk/id of each pair and save them in a list
            self.word_pairs_pks = [
                self.word_pair.id for self.word_pair in self.word_pairs]
            #return self.word_pairs_pks
            self.search_word_pairs(self.word_pairs_pks)

    def search_definitions(self, word_pairs_pks):
        '''
            Takes in a list pks of word pairs and return a list of pks of all definitions found.
        '''
        self.definitions = []
        for self.pair_pk in self.word_pairs_pks:
            try:
                self.definition = WordDefinition.objects.get(word_pair_id=self.pair_pk)  # Return a definitions of a word pair
                self.definitions.append(self.definition)
            except WordDefinition.DoesNotExist:
                # Rather than terminating if no definition found, continue search for the remaining word pairs' definitions
                self.definitions.append('No definition found')
        self.context['definitions'] = self.definitions
        self.definitions_pks = [
            self.definition.id for self.definition in self.definitions]
        #return self.definitions_pks
        self.search_examples(self.definitions_pks)


    def search_examples(self, definitions_pks):
        '''
            Takes in a list of pks of found definitions and search if examples exist and return example objects.
        '''
        self.examples = []
        for self.definition_pk in self.definitions_pks:
            try:
                self.example = DefinitionExample.objects.get(definition_id=self.definition_pk)  # Return a definition example object
                self.examples.append(self.example)
            except DefinitionExample.DoesNotExist:
                # Rather than terminating if no definition found, continue search for the remaining word pairs' definitions
                self.examples.append('No example found')
        self.context['examples'] = self.examples
        return render(self.request, 'dictionary/search.html', self.context)

    


