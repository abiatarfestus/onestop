import json
import urllib.request
import urllib.parse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
# from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.urls import reverse_lazy
from .classes import SearchDefinition
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom, OshindongaPhonetic
from .forms import EnglishWordForm, OshindongaWordForm, WordDefinitionForm, DefinitionExampleForm, OshindongaIdiomForm, ContributorCreationForm, OshindongaPhoneticForm
from django.views import generic
from json import dumps
import random


english_words = EnglishWord.objects.order_by('-time_added')[:10]
oshindonga_words = OshindongaWord.objects.order_by('-time_added')[:10]
new_phonetics = OshindongaPhonetic.objects.order_by('-time_added')[:10]
random_unphonetised = OshindongaWord.objects.filter(
    word_phonetics_id=1).order_by('?')[:10]
defined_words = WordDefinition.objects.order_by('-time_added')[:10]
exemplified_definitions = DefinitionExample.objects.order_by(
    '-time_added')[:10]
oshindonga_idioms = OshindongaIdiom.objects.order_by(
    '-time_added')[:10]

# Consider using


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


def register(request):
    if request.method == "POST":
        form = ContributorCreationForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            ''' End reCAPTCHA validation '''

            if result['success']:
                user = form.save()
                login(request, user)
                subject = 'Welcome to the community'
                message = f'Hi {user.username}, \n\nThank you for registering as a contributor. \nThe site is currently being tested; hence, your feedback at this stage will be of great importance. We cannot wait to see your contribution. \n\nRegards, \nFessy'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, 'abiatarfestus@outlook.com']
                send_mail(subject, message, email_from, recipient_list)
                messages.success(request, 'You have been registered successfully!')
                return redirect(reverse("index"))
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    else:
        form = ContributorCreationForm()
    return render(request, "registration/register.html", {"form": ContributorCreationForm})


def index(request):
    context = {}
    return render(request, 'onestop/index.html', context)


def under_construction(request):
    context = {}
    return render(request, 'onestop/under_construction.html', context)


def search_word(request):
    # Create an instance of the SearchDefinition calss, passing in the request
    search_object = SearchDefinition(request)
    # Call the search_word() method of the created instance/object, which will kickstart the necessary queries
    search_object.search_word()
    # Pass the context of the object/instance and pass it to the context variable of this view
    context = search_object.context
    return render(request, 'dictionary/search.html', context)


# class SearchSuggestedWord(FormView):
#     form_class = SearchWordForm
#     template_name = 'search.html'

#     def get_initial(self):
#         initial = super(SearchSuggestedWord, self).get_initial()
#         initial.update({'input_language': 'English', 'search_word': ''})
#         return initial
#     pass


def search_suggested_word(request, pk):
    word_instance = get_object_or_404(EnglishWord, pk=pk)
    search_object = SearchDefinition(request)
    search_object.search_suggested(word_instance.id)
    context = search_object.context
    return render(request, 'dictionary/search.html', context)

# Template class-based views


class HelpView(TemplateView):
    template_name = "onestop/help.html"

# GENERIC EDITING VIEWS: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy

# from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample

# class AuthorCreate(CreateView):
#     model = Author
#     fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
#     initial = {'date_of_death': '11/06/2020'}


class EnglishWordCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = EnglishWordForm
    model = EnglishWord
    extra_context = {'operation': 'Add a new English word',
                     'newly_added_words': english_words}
    success_message = "The word '%(word)s' was successfully added to the dictionary. Thank you for your contribution!"


class OshindongaPhoneticCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = OshindongaPhoneticForm
    model = OshindongaPhonetic
    extra_context = {'operation': 'Gwedha mo omawi gOshindonga',
                     'new_phonetics': new_phonetics, 'random_unphonetised': random_unphonetised}
    success_message = "Ewi lyoshitya '%(oshindonga_word)s' olya gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"
    # Add these to context: 'newly_added_phonetics': oshindonga_words, 'untranslated_words': get_untranslated_words


class OshindongaWordCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = OshindongaWordForm
    model = OshindongaWord
    extra_context = {'operation': 'Gwedha mo oshitya shOshindonga oshipe',
                     'newly_added_words': oshindonga_words, 'untranslated_words': get_untranslated_words}
    success_message = "Oshitya '%(word)s' osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"


class WordDefinitionCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    # Uses the form class defined in forms.py which allows customization
    form_class = WordDefinitionForm
    model = WordDefinition
    extra_context = {'operation': 'Add a new word definition',
                     'newly_defined_words': defined_words, 'undefined_words': get_undefined_words}
    success_message = "Definition of '%(word_pair)s' was successfully added to the dictionary. Thank you for your contribution!"


# Converting definitions queryset into a dictionary of {id:(engDef,oshDef)} for passing to the context.
q = WordDefinition.objects.all()
queryset_dict = dumps({q[i].id: (
    q[i].english_definition, q[i].oshindonga_definition) for i in range(len(q))})


class DefinitionExampleCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = DefinitionExampleForm
    model = DefinitionExample
    extra_context = {'operation': 'Add a new definition example',
                     'newly_added_examples': exemplified_definitions, 'unexemplified_definitions': get_unexemplified, 'definitions_dict': queryset_dict}
    success_message = "Example of '%(definition)s' usage was successfully added to the dictionary. Thank you for your contribution!"


class OshindongaIdiomCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    extra_context = {'operation': 'Gwedha mo oshipopiwamayele oshipe',
                     'newly_added_idioms': oshindonga_idioms, 'random_idioms': OshindongaIdiom.objects.order_by('?')[:10]}
    success_message = "Oshipopiwamayele osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"


# Update class-based views


class EnglishWordUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = EnglishWordForm
    model = EnglishWord
    extra_context = {'operation': 'Update an existing English word',
                     'newly_added_words': english_words}
    success_message = "The word '%(word)s' was successfully updated. Thank you for your contribution!"


class OshindongaPhoneticUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = OshindongaPhoneticForm
    model = OshindongaPhonetic
    extra_context = {
        'operation': 'Pukulula ewi lyoshitya shOshindonga li li mo nale', 'new_phonetics': new_phonetics, 'random_unphonetised': random_unphonetised}
    success_message = "Ewi lyoshitya '%(oshindonga_word)s' olya lundululwa nawa. Tangi ku sho wa gandja!"
    # Add these to context: 'newly_added_words': oshindonga_words, 'untranslated_words': get_untranslated_words


class OshindongaWordUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = OshindongaWordForm
    model = OshindongaWord
    extra_context = {
        'operation': 'Pukulula oshitya shOshindonga shi li mo nale',
                     'newly_added_words': oshindonga_words, 'untranslated_words': get_untranslated_words}
    success_message = "Oshitya '%(word)s' osha lundululwa nawa. Tangi ku sho wa gandja!"


class WordDefinitionUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    # Uses the form class defined in forms.py which allows customization
    form_class = WordDefinitionForm
    model = WordDefinition
    extra_context = {'operation': 'Update an existing word definition',
                     'newly_defined_words': defined_words, 'undefined_words': get_undefined_words}
    success_message = "Definition of '%(word_pair)s' was successfully updated. Thank you for your contribution!"


class DefinitionExampleUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = DefinitionExampleForm
    model = DefinitionExample
    extra_context = {'operation': 'Update an existing definition example',
                     'newly_added_examples': exemplified_definitions, 'definitions_dict': queryset_dict}
    success_message = "Example of '%(definition)s' usage was successfully updated. Thank you for your contribution!"


class OshindongaIdiomUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    extra_context = {'operation': 'Pukulula oshipopiwamayele shi li monale'}
    success_message = "Oshipopiwamayele osha lundululwa nawa.Tangi ku sho wa gandja!"


# List View
# Templates for displaying List and Detail views
list_view = 'dictionary/list_view.html'
detail_view = 'dictionary/detail_view.html'


class EnglishWordListView(generic.ListView):
    paginate_by = 50
    model = EnglishWord
    template_name = list_view

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


class OshindongaPhoneticListView(generic.ListView):
    paginate_by = 50
    model = OshindongaPhonetic
    template_name = list_view

    def get_queryset(self):
        return OshindongaPhonetic.objects.all().order_by('oshindonga_word')

    def get_context_data(self, **kwargs):
        context = super(OshindongaPhoneticListView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'List of Oshindonga phonetics in the dictionary'
        return context


class OshindongaWordListView(generic.ListView):
    paginate_by = 50
    model = OshindongaWord
    template_name = list_view

    def get_queryset(self):
        return OshindongaWord.objects.all().order_by('word')

    def get_context_data(self, **kwargs):
        context = super(OshindongaWordListView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'List of Oshindonga words in the dictionary'
        return context


class OshindongaIdiomListView(generic.ListView):
    paginate_by = 10
    model = OshindongaIdiom
    template_name = list_view

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
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(EnglishWordDetailView, self).get_context_data(**kwargs)
        context['heading'] = 'English word detail view'
        return context


class OshindongaPhoneticDetailView(generic.DetailView):
    model = OshindongaPhonetic
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaPhoneticDetailView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'Oshindonga phonetic detail view'
        return context


class OshindongaWordDetailView(generic.DetailView):
    model = OshindongaWord
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaWordDetailView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'Oshindonga word detail view'
        return context


class WordDefinitionDetailView(generic.DetailView):
    model = WordDefinition
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(WordDefinitionDetailView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'Word definition detail view'
        return context


class DefinitionExampleDetailView(generic.DetailView):
    model = DefinitionExample
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(DefinitionExampleDetailView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'Definition example detail view'
        return context


class OshindongaIdiomDetailView(generic.DetailView):
    model = OshindongaIdiom
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaIdiomDetailView,
                        self).get_context_data(**kwargs)
        context['heading'] = 'Oshindonga idiom detail view'
        return context
