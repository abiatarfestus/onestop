from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

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


def search_word(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchWordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/search/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchWordForm()

    return render(request, 'dictionary/search.html', {'form': form})


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


# GENERIC EDITING VIEWS: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample

# class AuthorCreate(CreateView):
#     model = Author
#     fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
#     initial = {'date_of_death': '11/06/2020'}

# Update class-based views

class EnglishWordUpdate(UpdateView):
    model = EnglishWord
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    extra_context={'operation': 'Update an existing English word'}

class OshindongaWordUpdate(UpdateView):
    model = OshindongaWord
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class WordDefinitionUpdate(UpdateView):
    model = WordDefinition
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class DefinitionExampleUpdate(UpdateView):
    model = DefinitionExample
    fields = '__all__' # Not recommended (potential security issue if more fields added)
# class AuthorDelete(DeleteView):
#     model = Author
#     success_url = reverse_lazy('authors')