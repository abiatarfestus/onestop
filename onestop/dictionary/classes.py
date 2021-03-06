from django.shortcuts import render
from .forms import SearchWordForm
from django.contrib.auth.models import User
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom


class HistoryRecord():
    '''Queries the history model of the datatbase and returns query sets of each model
    '''

    def __init__(self):
        # A queryset of all history entries from EnglishWord (historicalenglishword) database
        self.english = []
        # A queryset of all history entries from OshindongaWord (historicaloshindongaword) database
        self.oshindonga = []
        # A queryset of all history entries from WordDefinition (historicalenglisworddefinition) database
        self.definition = []
        # A queryset of all history entries from DefinitionExample (historicaldefinitionexample) database
        self.example = []
        # A queryset of all history entries from OshindongaIdiom (historicalenglishwordoshindongaidiom) database
        self.idiom = []
        self.usernames = []  # Holds all usernames from all history entries
        self.unique_usernames = set()  # Holds unique usernames (set) from the usernames list

    def reset_history(self):
        self.english = []
        self.oshindonga = []
        self.definition = []
        self.example = []
        self.idiom = []
        self.usernames = []
        self.unique_usernames = set()
        return

    def english_history(self):
        # Holds user ids of historical_users (created/modifiers)
        self.english = EnglishWord.history.all()
        self.user_ids = []
        for queryset in self.english:  # Loops through the querysets and take the user id if it's not null/none
            if queryset.history_user_id != None:  # Appends the the user id to user_ids list
                self.user_ids.append(queryset.history_user_id)
        for user_id in self.user_ids:  # Loops through user ids and matches them to users to obtain usernames
            # Holds querysets of users from the User model
            user = User.objects.get(id=user_id)
            # Appends the username to the usernames list
            self.usernames.append(user.username)
        # Updates the unique_usernames set with usernames
        self.unique_usernames.update(self.usernames)
        return self.english  # Returns a a queryset of EnglishWord historical objects/records

    def oshindonga_history(self):
        self.oshindonga = OshindongaWord.history.all()
        self.user_ids = []
        for queryset in self.oshindonga:
            if queryset.history_user_id != None:
                self.user_ids.append(queryset.history_user_id)
        for user_id in self.user_ids:
            user = User.objects.get(id=user_id)
            self.usernames.append(user.username)
        self.unique_usernames.update(self.usernames)
        return self.oshindonga

    def definition_history(self):
        self.definition = WordDefinition.history.all()
        self.user_ids = []
        for queryset in self.definition:
            if queryset.history_user_id != None:
                self.user_ids.append(queryset.history_user_id)
        for user_id in self.user_ids:
            user = User.objects.get(id=user_id)
            self.usernames.append(user.username)
        self.unique_usernames.update(self.usernames)
        return self.definition

    def example_history(self):
        self.example = DefinitionExample.history.all()
        self.user_ids = []
        for queryset in self.example:
            if queryset.history_user_id != None:
                self.user_ids.append(queryset.history_user_id)
        for user_id in self.user_ids:
            user = User.objects.get(id=user_id)
            self.usernames.append(user.username)
        self.unique_usernames.update(self.usernames)
        return self.example

    def idiom_history(self):
        self.idiom = OshindongaIdiom.history.all()
        self.user_ids = []
        for queryset in self.idiom:
            if queryset.history_user_id != None:
                self.user_ids.append(queryset.history_user_id)
        for user_id in self.user_ids:
            user = User.objects.get(id=user_id)
            self.usernames.append(user.username)
        self.unique_usernames.update(self.usernames)
        return self.idiom

    def get_contributors(self, num=None):
        self.reset_history()
        self.english_history()
        self.oshindonga_history()
        self.definition_history()
        self.example_history()
        self.idiom_history()
        contributors = []
        for username in self.unique_usernames:
            contributors.append((self.usernames.count(username), username))

        def getKey(item):
            return item[0]
        contributors.sort(key=getKey, reverse=True)
        top_contributors = contributors[:num]
        return top_contributors


class SearchDefinition():
    '''
        Searches for a word and returns its definition and example if found, otherwise returns no word, 
        translation, definition or example found.
    '''

    def __init__(self, request):
        self.request = request
        self.history = HistoryRecord()
        self.context = {'form': '', 'searched_word': '',
                        'definitions': '', 'examples': '', 'suggested_searches': EnglishWord.objects.order_by('?')[:10],
                        'top_contributors': self.history.get_contributors(10)}
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
