from django.shortcuts import render
from .forms import SearchWordForm
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample


class SearchDefinition():
    '''
        Searches for a word and returns its definition and example if found, otherwise returns no word, 
        translation, definition or example found.
    '''

    def __init__(self, request):
        self.request = request
        self.context = {'form': '', 'searched_word': '',
                        'definitions': '', 'examples': '', 'suggested_searches': EnglishWord.objects.order_by('?')[:10],
                        'history':''}
        # Note: order_by('?') queries may be expensive and slow, depending on the database backend you’re using

    def search_examples(self, definitions_pks):
        '''
            Takes in a list of pks of found definitions and search if examples exist and return example objects.
        '''
        self.example_querysets = []
        for self.definition_pk in self.definitions_pks:
            self.example_queryset = DefinitionExample.objects.filter(
                definition_id=self.definition_pk)
            # If no definition found, an empty queryset is appended
            self. example_querysets.append(self.example_queryset)
        self.example_objects = []
        self.no_example_found = 'No example found'
        for self.example_queryset in self.example_querysets:
            if len(self.example_queryset) > 0:  # If it's not an empty querset
                # Loop through the queryset to extract objects
                for i in range(len(self.example_queryset)):
                    self.example_objects.append(self.example_queryset[i])
            else:
                self.example_objects.append(self.no_example_found)
        self.context['examples'] = self.example_objects
        return render(self.request, 'dictionary/search.html', self.context)

    def search_definitions(self, word_pairs_pks):
        '''
            Takes in a list pks of word pairs and return a list of pks of all definitions found.
        '''
        self.definition_querysets = []
        for self.pair_pk in self.word_pairs_pks:
            self.definition_queryset = WordDefinition.objects.filter(
                word_pair_id=self.pair_pk)
            # If no definition found, an empty queryset is appended
            self.definition_querysets.append(self.definition_queryset)
        self.definition_objects = []
        self.no_definition_found = 'No definition found'
        for self.definition_queryset in self.definition_querysets:
            if len(self.definition_queryset) > 0:  # If it's not an empty queryset
                for self.i in range(len(self.definition_queryset)):
                    self.definition_objects.append(
                        self.definition_queryset[self.i])
            else:
                self.definition_objects.append(self.no_definition_found)
        self.context['definitions'] = self.definition_objects
        self.definitions_pks = []
        for self.i in range(len(self.definition_objects)):
            if self.definition_objects[self.i] != self.no_definition_found:
                self.definitions_pks.append(self.definition_objects[self.i].id)
        self.search_examples(self.definitions_pks)

    def search_word_pairs(self, eng_word_pk):
        '''
            Using the English word pk (foreignkey id) search if for English|Oshindonga pairs and return a list of pks of all pair objects found.
        '''
        # Return a queryset of all word pairs with the searched word
        self.word_pairs = OshindongaWord.objects.filter(
            english_word_id=self.eng_word_pk)
        if len(self.word_pairs) == 0:
            self.context['searched_word'] = [
                'The word you searched is not yet translated into Oshindonga.']
            return render(self.request, 'dictionary/search.html', self.context)
        else:
            self.context['searched_word'] = self.word_pairs
            # Extract pk/id of each pair and save them in a list
            self.word_pairs_pks = [
                self.word_pair.id for self.word_pair in self.word_pairs]
            self.search_definitions(self.word_pairs_pks)

    def search_word(self):
        '''
            Check if the searched English word exists in the English model. If found return its pk
        '''
        # Reset context variables when visiting for the first time or refreshing the page
        self.context['searched_word'] = ''
        self.context['definitions'] = ''
        self.context['examples'] = ''
        self.form = SearchWordForm(self.request.GET)
        self.context['form'] = self.form
        if self.form.is_valid():
            self.word = self.form.cleaned_data['search_word']
            self.language = self.form.cleaned_data['input_language']
            if self.language == 'English':
                try:
                    # Search within English model, and if foud:
                    self.eng_word = EnglishWord.objects.get(word=self.word)
                    # Get the the id/pk of the word found to be used in Oshindonga model
                    self.eng_word_pk = self.eng_word.id
                except EnglishWord.DoesNotExist:
                    self.context['searched_word'] = [
                        'The word you searched was not found.']
                    return render(self.request, 'dictionary/search.html', self.context)
                self.search_word_pairs(self.eng_word_pk)
                return render(self.request, 'dictionary/search.html', self.context)
            else:
                self.word_pairs = OshindongaWord.objects.filter(
                    word=self.word)  # Search in OshindongaWord using the word
                if len(self.word_pairs) == 0:
                    self.context['searched_word'] = [
                        'Oshitya shi wa kongo ina shi monika.']
                    return render(self.request, 'dictionary/search.html', self.context)
                else:
                    self.context['searched_word'] = self.word_pairs
                    # Extract pk/id of each pair and save them in a list
                    self.word_pairs_pks = [
                        self.word_pair.id for self.word_pair in self.word_pairs]
                    self.search_definitions(self.word_pairs_pks)
        else:
            return render(self.request, 'dictionary/search.html', self.context)
