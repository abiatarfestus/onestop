from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .search import SearchDefinition
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom
from .forms import SearchWordForm
from django import forms
from django.views import generic

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

#List View
objects_view = 'dictionary/objects_view.html' #A template for displating List and Detail views dynamically
class EnglishWordListView(generic.ListView):
    model = EnglishWord
    template_name = objects_view

    #Override the default get_queryset()
    def get_queryset(self):
        return EnglishWord.objects.all().order_by('word')

    #Add additional context variables
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EnglishWordListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['heading'] = 'List of English words in the dictionary' #Default context = englishword_list
        return context


class OshindongaWordListView(generic.ListView):
    model = OshindongaWord
    template_name = objects_view

    def get_queryset(self):
        return OshindongaWord.objects.all().order_by('word')

    def get_context_data(self, **kwargs):
        context = super(OshindongaWordListView, self).get_context_data(**kwargs)
        context['heading'] = 'List of Oshindonga words in the dictionary'
        return context


class OshindongaIdiomListView(generic.ListView):
    model = OshindongaIdiom
    template_name = objects_view

    def get_queryset(self):
        return OshindongaIdiom.objects.all().order_by('oshindonga_idiom')

    def get_context_data(self, **kwargs):
        context = super(OshindongaIdiomListView, self).get_context_data(**kwargs)
        context['heading'] = 'List of Oshindonga idioms in the dictionary'
        return context

#Detail View

class EnglishWordDetailView(generic.DetailView):
    model = EnglishWord
    template_name = objects_view

    def get_context_data(self, **kwargs):
        context = super(EnglishWordDetailView, self).get_context_data(**kwargs)
        context['heading'] = 'English word detail view'
        return context


class OshindongaWordDetailView(generic.DetailView):
    model = OshindongaWord
    template_name = objects_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaWordDetailView, self).get_context_data(**kwargs)
        context['heading'] = 'Oshindonga word detail view'
        return context


class OshindongaIdiomDetailView(generic.DetailView):
    model = OshindongaIdiom
    template_name = objects_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaIdiomDetailView, self).get_context_data(**kwargs)
        context['heading'] = 'Oshindonga idiom detail view'
        return context

