from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .search import SearchEnglishDefinition
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample
from .forms import SearchWordForm, EnglishWordForm, OshindongaWordForm, WordDefinitionForm, DefinitionExampleForm

# Create your views here.


def index(request):
    context = {}
    return render(request, 'dictionary/index.html', context)

# def search(request):
#     context = {}
#     return render(request, 'dictionary/search.html', context)


def thankyou(request):
    context = {}
    return render(request, 'dictionary/thankyou.html', context)


# def search_word(request):
#     sub_request = request
#     print('Started here')
#     form = SearchWordForm(request.GET)
#     print(form)
#     print(form.is_valid())
#     if form.is_valid():
#         print('Passed here')
#         return SearchEnglishDefinition(sub_request, form.cleaned_data['search_word'])
#         # return render(request, 'dictionary/search.html', {'form': form})
#     else:
#         form = SearchWordForm()
#         return render(request, 'dictionary/search.html', {'form': form})


def add_english(request):
    if request.method == 'POST':
        form = EnglishWordForm(request.POST)
        if form.is_valid():
            new_word = form
            new_word.save()
            #context = {'success':'Word added successfully. Thanks for your contribution!'}
            return HttpResponseRedirect(reverse('dictionary:add-english'))
    else:
        form = EnglishWordForm()
    return render(request, 'dictionary/englishword_form.html/', {'form': form, 'operation': 'Add new English word'})


def add_oshindonga(request):
    if request.method == 'POST':
        form = OshindongaWordForm(request.POST)
        if form.is_valid():
            new_word = form
            new_word.save()
            return HttpResponseRedirect(reverse('dictionary:add-oshindonga'))
    else:
        form = OshindongaWordForm()
    return render(request, 'dictionary/add_oshindonga.html/', {'form': form})
    # context = {}
    # return render(request, 'dictionary/add_oshindonga.html', context)


def add_definition(request):
    if request.method == 'POST':
        form = WordDefinitionForm(request.POST)
        if form.is_valid():
            new_definition = form
            new_definition.save()
            return HttpResponseRedirect(reverse('dictionary:add-definition'))
    else:
        form = WordDefinitionForm()
    return render(request, 'dictionary/add_definition.html/', {'form': form})


def add_example(request):
    if request.method == 'POST':
        form = DefinitionExampleForm(request.POST)
        if form.is_valid():
            new_definition = form
            new_definition.save()
            return HttpResponseRedirect(reverse('dictionary:add_example'))
    else:
        form = DefinitionExampleForm()
    return render(request, 'dictionary/add_example.html/', {'form': form})


# TEST SEARCH FUNCTIONS
context = {'form': '', 'searched_word': 'Word not found',
           'definitions': '', 'examples': ''}


def search_examples(request, definitions_pks):
    '''
        Takes in a list of pks of found definitions and search if examples exist and return example objects.
    '''
    examples = []
    for definition_pk in definitions_pks:
        try:
            example = DefinitionExample.objects.get(
                definition_id=definition_pk)  # Return a definition example object
            examples.append(example)
        except DefinitionExample.DoesNotExist:
            # Rather than terminating if no definition found, continue search for the remaining word pairs' definitions
            examples.append('No example found')
    context['examples'] = examples
    return render(request, 'dictionary/search.html', context)


def search_definitions(request, word_pairs_pks):
    '''
        Takes in a list pks of word pairs and return a list of pks of all definitions found.
    '''
    sub_request3 = request
    definitions = []
    for pair_pk in word_pairs_pks:
        try:
            # Return a definitions of a word pair
            definition = WordDefinition.objects.filter(word_pair_id=pair_pk)
            definitions.append(definition)
        except WordDefinition.DoesNotExist:
            # Rather than terminating if no definition found, continue search for the remaining word pairs' definitions
            definitions.append('No definition found')
    context['definitions'] = definitions
    definitions_pks = [
        definition[0].id for definition in definitions]
    # return definitions_pks
    search_examples(sub_request3, definitions_pks)


def search_word_pairs(request, eng_word_pk):
    '''
        Using the English word pk (foreignkey id) search if for English|Oshindonga pairs and return a list of pks of all pair objects found.
    '''
    sub_request2 = request
    # Return a queryset of all word pairs with the searched word
    word_pairs = OshindongaWord.objects.filter(english_word_id=eng_word_pk)
    if word_pairs == []:
        context['searched_word'] = 'The word you searched is not yet translated into Oshindonga.'
        return render(request, 'dictionary/search.html', context)
    else:
        context['searched_word'] = word_pairs
        # Etract pk/id of each pair and save them in a list
        word_pairs_pks = [
            word_pair.id for word_pair in word_pairs]
        # return word_pairs_pks
        search_definitions(sub_request2, word_pairs_pks)


def search_word(request):
    '''
        Check if the searched English word exists in the English model. If found return its pk
    '''
    sub_request = request
    print('Started here')
    form = SearchWordForm(request.GET)
    context['form'] = form
    print(form)
    print(form.is_valid())
    if form.is_valid():
        print('Passed here')
        word = form.cleaned_data['search_word']
        try:
            # Search within English model, and if foud:
            eng_word = EnglishWord.objects.get(word=word)
            # Get the the id/pk of the word found to be used in Oshindonga model
            eng_word_pk = eng_word.id
        except EnglishWord.DoesNotExist:
            return render(request, 'dictionary/search.html', context)
        search_word_pairs(sub_request, eng_word_pk)
    return render(request, 'dictionary/search.html', context)

# GENERIC EDITING VIEWS: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy

# from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample

# class AuthorCreate(CreateView):
#     model = Author
#     fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
#     initial = {'date_of_death': '11/06/2020'}

# Update class-based views


class EnglishWordUpdate(UpdateView):
    model = EnglishWord
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
    extra_context = {'operation': 'Update an existing English word'}


class OshindongaWordUpdate(UpdateView):
    model = OshindongaWord
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class WordDefinitionUpdate(UpdateView):
    model = WordDefinition
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class DefinitionExampleUpdate(UpdateView):
    model = DefinitionExample
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'
# class AuthorDelete(DeleteView):
#     model = Author
#     success_url = reverse_lazy('authors')
