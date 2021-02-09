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
            return HttpResponseRedirect(reverse('dictionary:add_english'))
    else:
        form = EnglishWordForm()
    return render(request, 'dictionary/add_english.html/', {'form': form})


def add_oshindonga(request):
    if request.method == 'POST':
        form = OshindongaWordForm(request.POST)
        if form.is_valid():
            new_word = form
            new_word.save()
            return HttpResponseRedirect(reverse('dictionary:add_oshindonga'))
    else:
        form = OshindongaWordForm()
    return render(request, 'dictionary/add_oshindonga.html/', {'form': form})


def add_definition(request):
    if request.method == 'POST':
        form = WordDefinitionForm(request.POST)
        if form.is_valid():
            new_definition = form
            new_definition.save()
            return HttpResponseRedirect(reverse('dictionary:add_definition'))
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
