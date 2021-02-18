from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .search import SearchDefinition
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom
from .forms import SearchWordForm
from django import forms

# Create your views here.


def index(request):
    context = {}
    return render(request, 'dictionary/index.html', context)


def thankyou(request):
    context = {}
    return render(request, 'dictionary/thankyou.html', context)


def search_word(request):
    search_object = SearchDefinition(request)
    search_object.search_word()
    context = search_object.context
    return render(request, 'dictionary/search.html', context)


# def add_english(request):
#     if request.method == 'POST':
#         form = EnglishWordForm(request.POST)
#         if form.is_valid():
#             new_word = form
#             new_word.save()
#             return HttpResponseRedirect(reverse('dictionary:add-english'))
#     else:
#         form = EnglishWordForm()
#     return render(request, 'dictionary/add_english.html/', {'form': form, 'operation': 'Add new English word'})


# def add_oshindonga(request):
#     if request.method == 'POST':
#         form = OshindongaWordForm(request.POST)
#         if form.is_valid():
#             new_word = form
#             new_word.save()
#             return HttpResponseRedirect(reverse('dictionary:add-oshindonga'))
#     else:
#         form = OshindongaWordForm()
#     return render(request, 'dictionary/add_oshindonga.html/', {'form': form})


# def add_definition(request):
#     if request.method == 'POST':
#         form = WordDefinitionForm(request.POST)
#         if form.is_valid():
#             new_definition = form
#             new_definition.save()
#             return HttpResponseRedirect(reverse('dictionary:add-definition'))
#     else:
#         form = WordDefinitionForm()
#     return render(request, 'dictionary/add_definition.html/', {'form': form})


# def add_example(request):
#     if request.method == 'POST':
#         form = DefinitionExampleForm(request.POST)
#         if form.is_valid():
#             new_definition = form
#             new_definition.save()
#             return HttpResponseRedirect(reverse('dictionary:add_example'))
#     else:
#         form = DefinitionExampleForm()
#     return render(request, 'dictionary/add_example.html/', {'form': form})

# GENERIC EDITING VIEWS: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy

# from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample

# class AuthorCreate(CreateView):
#     model = Author
#     fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
#     initial = {'date_of_death': '11/06/2020'}

class EnglishWordCreate(CreateView):
    model = EnglishWord
    # Not recommended (potential security issue if more fields added)
    fields = '__all__'


class OshindongaWordCreate(CreateView):
    model = OshindongaWord
    fields = '__all__'


class WordDefinitionCreate(CreateView):
    model = WordDefinition
    fields = '__all__'
    widgets = {'part_of_speech': forms.Select(
        attrs={'onchange': 'displayPluralOrTense()'})}


class DefinitionExampleCreate(CreateView):
    model = DefinitionExample
    fields = '__all__'


class OshindongaIdiomCreate(CreateView):
    model = OshindongaIdiom
    fields = '__all__'

# Update class-based views


class EnglishWordUpdate(UpdateView):
    model = EnglishWord
    fields = '__all__'
    extra_context = {'operation': 'Update an existing English word'}


class OshindongaWordUpdate(UpdateView):
    model = OshindongaWord
    fields = '__all__'


class WordDefinitionUpdate(UpdateView):
    model = WordDefinition
    fields = '__all__'


class DefinitionExampleUpdate(UpdateView):
    model = DefinitionExample
    fields = '__all__'


class OshindongaIdiomUpdate(UpdateView):
    model = OshindongaIdiom
    fields = '__all__'
