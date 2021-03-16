from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .classes import SearchDefinition, HistoryRecord
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom
from .forms import SearchWordForm, EnglishWordForm, OshindongaWordForm, WordDefinitionForm, DefinitionExampleForm, OshindongaIdiomForm
from django.views import generic
import random


english_words = EnglishWord.objects.order_by('-time_added')[:10]
oshindonga_words = OshindongaWord.objects.order_by('-time_added')[:10]
defined_words = WordDefinition.objects.order_by('-time_added')[:10]
exemplified_definitions = DefinitionExample.objects.order_by(
    '-time_added')[:10]
oshindonga_idioms = OshindongaIdiom.objects.order_by(
    '-time_added')[:10]


def get_untranslated_words():
    all_english = EnglishWord.objects.all()
    # Ids of all English words
    all_english_ids = [word.id for word in all_english]
    all_oshindonga = OshindongaWord.objects.all()
    # Ids of all English words translated
    all_translated_ids = [word.english_word_id for word in all_oshindonga]
    untranslated_ids = [
        i for i in all_english_ids if i not in all_translated_ids]
    random.shuffle(untranslated_ids)
    untranslated_words = []
    for i in untranslated_ids[:10]:
        untranslated_words.append(EnglishWord.objects.get(id=i))
    return untranslated_words


def get_undefined_words():
    all_word_pairs = OshindongaWord.objects.all()
    word_pair_ids = [pair.id for pair in all_word_pairs]
    all_definitions = WordDefinition.objects.all()
    defined_ids = [definition.word_pair_id for definition in all_definitions]
    undefined_ids = [i for i in word_pair_ids if i not in defined_ids]
    random.shuffle(undefined_ids)
    undefined_word_pairs = []
    for i in undefined_ids[:10]:
        undefined_word_pairs.append(OshindongaWord.objects.get(id=i))
    return undefined_word_pairs


def get_unexemplified():
    all_definitions = WordDefinition.objects.all()
    definition_ids = [definition.id for definition in all_definitions]
    all_examples = DefinitionExample.objects.all()
    exemplified_ids = [example.definition_id for example in all_examples]
    unexemplified_ids = [i for i in definition_ids if i not in exemplified_ids]
    random.shuffle(unexemplified_ids)
    unexemplified = []
    for i in unexemplified_ids[:10]:
        unexemplified.append(WordDefinition.objects.get(id=i))
    return unexemplified


def index(request):
    context = {}
    return render(request, 'onestop/index.html', context)


def thankyou(request):
    context = {}
    return render(request, 'dictionary/thankyou.html', context)


def search_word(request):
    # Create an instance of the SearchDefinition calss, passing in the request
    search_object = SearchDefinition(request)
    # Call the search_word() method of the created instance/object, which will kickstart the necessary queries
    search_object.search_word()
    # Pass the context of the object/instance and pass it to the context variable of this view
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
    extra_context = {'operation': 'Add a new English word',
                     'newly_added_words': english_words}
    success_message = "The word '%(word)s' was successfully added to the dictionary. Thank you for your contribution!"


class OshindongaWordCreate(SuccessMessageMixin, CreateView):
    form_class = OshindongaWordForm
    model = OshindongaWord
    extra_context = {'operation': 'Gwedha mo oshitya shOshindonga oshipe',
                     'newly_added_words': oshindonga_words, 'untranslated_words': get_untranslated_words}
    success_message = "Oshitya '%(word)s' osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"


class WordDefinitionCreate(SuccessMessageMixin, CreateView):
    # Uses the form class defined in forms.py which allows customization
    form_class = WordDefinitionForm
    model = WordDefinition
    extra_context = {'operation': 'Add a new word definition',
                     'newly_defined_words': defined_words, 'undefined_words': get_undefined_words}
    success_message = "Definition of '%(word_pair)s' was successfully added to the dictionary. Thank you for your contribution!"


class DefinitionExampleCreate(SuccessMessageMixin, CreateView):
    form_class = DefinitionExampleForm
    model = DefinitionExample
    extra_context = {'operation': 'Add a new definition example',
                     'newly_added_examples': exemplified_definitions, 'unexemplified_definitions': get_unexemplified}
    success_message = "Example of '%(definition)s' usage was successfully added to the dictionary. Thank you for your contribution!"


class OshindongaIdiomCreate(SuccessMessageMixin, CreateView):
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    extra_context = {'operation': 'Gwedha mo oshipopiwamayele oshipe',
                     'newly_added_idioms': oshindonga_idioms}
    success_message = "Oshipopiwamayele osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"


# Update class-based views


class EnglishWordUpdate(SuccessMessageMixin, UpdateView):
    form_class = EnglishWordForm
    model = EnglishWord
    extra_context = {'operation': 'Update an existing English word',
                     'newly_added_words': english_words}
    success_message = "The word '%(word)s' was successfully updated. Thank you for your contribution!"


class OshindongaWordUpdate(SuccessMessageMixin, UpdateView):
    form_class = OshindongaWordForm
    model = OshindongaWord
    extra_context = {
        'operation': 'Pukulula oshitya shOshindonga shi li mo nale',
                     'newly_added_words': oshindonga_words, 'untranslated_words': get_untranslated_words}
    success_message = "Oshitya '%(word)s' osha lundululwa nawa. Tangi ku sho wa gandja!"


class WordDefinitionUpdate(SuccessMessageMixin, UpdateView):
    # Uses the form class defined in forms.py which allows customization
    form_class = WordDefinitionForm
    model = WordDefinition
    extra_context = {'operation': 'Update an existing word definition',
                     'newly_defined_words': defined_words, 'undefined_words': get_undefined_words}
    success_message = "Definition of '%(word_pair)s' was successfully updated. Thank you for your contribution!"


class DefinitionExampleUpdate(SuccessMessageMixin, UpdateView):
    form_class = DefinitionExampleForm
    model = DefinitionExample
    extra_context = {'operation': 'Update an existing definition example',
                     'newly_added_examples': exemplified_definitions}
    success_message = "Example of '%(definition)s' usage was successfully updated. Thank you for your contribution!"


class OshindongaIdiomUpdate(SuccessMessageMixin, UpdateView):
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    extra_context = {'operation': 'Pukulula oshipopiwamayele shi li monale'}
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
