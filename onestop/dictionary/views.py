from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .search import SearchDefinition
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom
from .forms import SearchWordForm, EnglishWordForm, OshindongaWordForm, WordDefinitionForm, DefinitionExampleForm, OshindongaIdiomForm
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

class EnglishWordCreate(SuccessMessageMixin, CreateView):
    form_class = EnglishWordForm
    model = EnglishWord
    success_message = "The word '%(word)s' was successfully added to the dictionary. Thank you for your contribution!"


class OshindongaWordCreate(SuccessMessageMixin, CreateView):
    form_class = OshindongaWordForm
    model = OshindongaWord
    success_message = "Oshitya '%(word)s' osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"



class WordDefinitionCreate(SuccessMessageMixin, CreateView):
    form_class = WordDefinitionForm  # Uses the form class defined in forms.py which allows customization
    model = WordDefinition
    success_message = "Definition of '%(word_pair)s' was successfully added to the dictionary. Thank you for your contribution!"


class DefinitionExampleCreate(SuccessMessageMixin, CreateView):
    form_class = DefinitionExampleForm
    model = DefinitionExample
    success_message = "Example of '%(definition)s' usage was successfully added to the dictionary. Thank you for your contribution!"


class OshindongaIdiomCreate(SuccessMessageMixin, CreateView):
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    success_message = "Oshipopiwamayele osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"


# Update class-based views


class EnglishWordUpdate(SuccessMessageMixin, UpdateView):
    form_class = EnglishWordForm
    model = EnglishWord
    extra_context = {'operation': 'Update an existing English word'}
    success_message = "The word '%(word)s' was successfully updated. Thank you for your contribution!"


class OshindongaWordUpdate(SuccessMessageMixin, UpdateView):
    form_class = OshindongaWordForm
    model = OshindongaWord
    success_message = "Oshitya '%(word)s' osha lundululwa nawa. Tangi ku sho wa gandja!"


class WordDefinitionUpdate(SuccessMessageMixin, UpdateView):
    form_class = WordDefinitionForm  # Uses the form class defined in forms.py which allows customization
    model = WordDefinition
    success_message = "Definition of '%(word_pair)s' was successfully updated. Thank you for your contribution!"


class DefinitionExampleUpdate(SuccessMessageMixin, UpdateView):
    form_class = DefinitionExampleForm
    model = DefinitionExample
    success_message = "Example of '%(definition)s' usage was successfully updated. Thank you for your contribution!"


class OshindongaIdiomUpdate(SuccessMessageMixin, UpdateView):
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    success_message = "Oshipopiwamayele osha lundululwa nawa.Tangi ku sho wa gandja!"


# List View
# A template for displating List and Detail views dynamically
objects_view = 'dictionary/objects_view.html'


class EnglishWordListView(generic.ListView):
    model = EnglishWord
    template_name = objects_view

    # Override the default get_queryset()
    def get_queryset(self):
        return EnglishWord.objects.all().order_by('word')

    # Add additional context variables
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EnglishWordListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # Default context = englishword_list
        context['heading'] = 'List of English words in the dictionary'
        return context


class OshindongaWordListView(generic.ListView):
    model = OshindongaWord
    template_name = objects_view

    def get_queryset(self):
        return OshindongaWord.objects.all().order_by('word')

    def get_context_data(self, **kwargs):
        context = super(OshindongaWordListView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'List of Oshindonga words in the dictionary'
        return context


class OshindongaIdiomListView(generic.ListView):
    model = OshindongaIdiom
    template_name = objects_view

    def get_queryset(self):
        return OshindongaIdiom.objects.all().order_by('oshindonga_idiom')

    def get_context_data(self, **kwargs):
        context = super(OshindongaIdiomListView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'List of Oshindonga idioms in the dictionary'
        return context

# Detail View


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
        context = super(OshindongaWordDetailView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'Oshindonga word detail view'
        return context


class WordDefinitionDetailView(generic.DetailView):
    model = WordDefinition
    template_name = objects_view

    def get_context_data(self, **kwargs):
        context = super(WordDefinitionDetailView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'Word definition detail view'
        return context


class DefinitionExampleDetailView(generic.DetailView):
    model = DefinitionExample
    template_name = objects_view

    def get_context_data(self, **kwargs):
        context = super(DefinitionExampleDetailView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'Definition example detail view'
        return context


class OshindongaIdiomDetailView(generic.DetailView):
    model = OshindongaIdiom
    template_name = objects_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaIdiomDetailView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'Oshindonga idiom detail view'
        return context
