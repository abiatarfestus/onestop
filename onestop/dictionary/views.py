from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .classes import SearchDefinition
from .models import (
    EnglishWord,
    OshindongaWord,
    WordDefinition,
    DefinitionExample,
    OshindongaIdiom,
    OshindongaPhonetic,
)
from .forms import (
    EnglishWordForm,
    OshindongaWordForm,
    WordDefinitionForm,
    DefinitionExampleForm,
    OshindongaIdiomForm,
    OshindongaPhoneticForm,
)
from django.views import generic
from json import dumps
import random


english_words = EnglishWord.objects.order_by("-time_added")[:5]
oshindonga_words = OshindongaWord.objects.order_by("-time_added")[:5]
new_phonetics = OshindongaPhonetic.objects.order_by("-time_added")[:5]
random_unphonetised = OshindongaWord.objects.filter(word_phonetics_id=1).order_by("?")[
    :5
]
defined_words = WordDefinition.objects.order_by("-time_added")[:5]
exemplified_definitions = DefinitionExample.objects.order_by("-time_added")[:5]
oshindonga_idioms = OshindongaIdiom.objects.order_by("-time_added")[:10]

# Consider using


def get_untranslated_words():
    all_english = EnglishWord.objects.all()
    # Ids of all English words
    all_english_ids = [word.id for word in all_english]
    all_oshindonga = OshindongaWord.objects.all()
    # Ids of all English words translated
    all_translated_ids = [word.english_word_id for word in all_oshindonga]
    untranslated_ids = [i for i in all_english_ids if i not in all_translated_ids]
    random.shuffle(untranslated_ids)
    untranslated_words = []
    for i in untranslated_ids[:5]:
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
    for i in undefined_ids[:5]:
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
    for i in unexemplified_ids[:5]:
        unexemplified.append(WordDefinition.objects.get(id=i))
    return unexemplified


def search_word(request):
    # Create an instance of the SearchDefinition calss, passing in the request
    search_object = SearchDefinition(request)
    # Call the search_word() method of the created instance/object, which will kickstart the necessary queries
    search_object.search_word()
    # Pass the context of the object/instance and pass it to the context variable of this view
    context = search_object.context
    return render(request, "dictionary/search.html", context)


def search_suggested_word(request, pk):
    word_instance = get_object_or_404(EnglishWord, pk=pk)
    search_object = SearchDefinition(request)
    search_object.search_suggested(word_instance.id)
    context = search_object.context
    return render(request, "dictionary/search.html", context)


class EnglishWordCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_englishword"
    form_class = EnglishWordForm
    model = EnglishWord
    extra_context = {
        "operation": "Add a new English word",
        "newly_added_words": english_words,
    }
    success_message = "The word '%(word)s' was successfully added to the dictionary. Thank you for your contribution!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaPhoneticCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_oshindongaphonetic"
    form_class = OshindongaPhoneticForm
    model = OshindongaPhonetic
    extra_context = {
        "operation": "Gwedha mo omawi gOshindonga",
        "new_phonetics": new_phonetics,
        "random_unphonetised": random_unphonetised,
    }
    success_message = "Ewi lyoshitya '%(oshindonga_word)s' olya gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"
    # Add these to context: 'newly_added_phonetics': oshindonga_words, 'untranslated_words': get_untranslated_words

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaWordCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_oshindongaword"
    form_class = OshindongaWordForm
    model = OshindongaWord
    extra_context = {
        "operation": "Gwedha mo oshitya shOshindonga oshipe",
        "newly_added_words": oshindonga_words,
        "untranslated_words": get_untranslated_words,
    }
    success_message = (
        "Oshitya '%(word)s' osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"
    )

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class WordDefinitionCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    # Uses the form class defined in forms.py which allows customization
    permission_required = "dictionary.add_worddefinition"
    form_class = WordDefinitionForm
    model = WordDefinition
    extra_context = {
        "operation": "Add a new word definition",
        "newly_defined_words": defined_words,
        "undefined_words": get_undefined_words,
    }
    success_message = "Definition of '%(word_pair)s' was successfully added to the dictionary. Thank you for your contribution!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


# Converting definitions queryset into a dictionary of {id:(engDef,oshDef)} for passing to the context.
q = WordDefinition.objects.all()
queryset_dict = dumps(
    {
        q[i].id: (q[i].english_definition, q[i].oshindonga_definition)
        for i in range(len(q))
    }
)


class DefinitionExampleCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_definitionexample"
    form_class = DefinitionExampleForm
    model = DefinitionExample
    extra_context = {
        "operation": "Add a new definition example",
        "newly_added_examples": exemplified_definitions,
        "unexemplified_definitions": get_unexemplified,
        "definitions_dict": queryset_dict,
    }
    success_message = "Example of '%(definition)s' usage was successfully added to the dictionary. Thank you for your contribution!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaIdiomCreate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    permission_required = "dictionary.add_oshindongaidiom"
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    extra_context = {
        "operation": "Gwedha mo oshipopiwamayele oshipe",
        "newly_added_idioms": oshindonga_idioms,
        "random_idioms": OshindongaIdiom.objects.order_by("?")[:10],
    }
    success_message = (
        "Oshipopiwamayele osha gwedhwa mo nawa membwiitya. Tangi ku sho wa gandja!"
    )

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


# Update class-based views


class EnglishWordUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_englishword"
    form_class = EnglishWordForm
    model = EnglishWord
    extra_context = {
        "operation": "Update an existing English word",
        "newly_added_words": english_words,
    }
    success_message = (
        "The word '%(word)s' was successfully updated. Thank you for your contribution!"
    )

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaPhoneticUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_oshindongaphonetic"
    form_class = OshindongaPhoneticForm
    model = OshindongaPhonetic
    extra_context = {
        "operation": "Pukulula ewi lyoshitya shOshindonga li li mo nale",
        "new_phonetics": new_phonetics,
        "random_unphonetised": random_unphonetised,
    }
    success_message = "Ewi lyoshitya '%(oshindonga_word)s' olya lundululwa nawa. Tangi ku sho wa gandja!"
    # Add these to context: 'newly_added_words': oshindonga_words, 'untranslated_words': get_untranslated_words

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaWordUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_oshindongaword"
    form_class = OshindongaWordForm
    model = OshindongaWord
    extra_context = {
        "operation": "Pukulula oshitya shOshindonga shi li mo nale",
        "newly_added_words": oshindonga_words,
        "untranslated_words": get_untranslated_words,
    }
    success_message = "Oshitya '%(word)s' osha lundululwa nawa. Tangi ku sho wa gandja!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class WordDefinitionUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    # Uses the form class defined in forms.py which allows customization
    permission_required = "dictionary.change_worddefinition"
    form_class = WordDefinitionForm
    model = WordDefinition
    success_message = "Definition of '%(word_pair)s' was successfully updated. Thank you for your contribution!"
    # extra_context = {
    #     "operation": "Update an existing word definition",
    #     "newly_defined_words": defined_words,
    #     "undefined_words": get_undefined_words,
    # }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        synonyms = self.object.synonyms.all()
        context["synonym_list"] = [str(synonym.id) for synonym in synonyms]
        context["operation"] = "Update an existing word definition",
        context["newly_defined_words"] = defined_words,
        context["undefined_words"] = get_undefined_words,
        return context

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class DefinitionExampleUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_definitionexample"
    form_class = DefinitionExampleForm
    model = DefinitionExample
    extra_context = {
        "operation": "Update an existing definition example",
        "newly_added_examples": exemplified_definitions,
        "definitions_dict": queryset_dict,
    }
    success_message = "Example of '%(definition)s' usage was successfully updated. Thank you for your contribution!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


class OshindongaIdiomUpdate(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    permission_required = "dictionary.change_oshindongaidiom"
    form_class = OshindongaIdiomForm
    model = OshindongaIdiom
    extra_context = {"operation": "Pukulula oshipopiwamayele shi li monale"}
    success_message = "Oshipopiwamayele osha lundululwa nawa.Tangi ku sho wa gandja!"

    def handle_no_permission(self):
        """Redirect to custom access denied page if authenticated or login page if not"""
        if not self.request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        return redirect("access-denied")


# List View
# Templates for displaying List and Detail views
list_view = "dictionary/list_view.html"
detail_view = "dictionary/detail_view.html"


class EnglishWordListView(generic.ListView):
    paginate_by = 50
    model = EnglishWord
    template_name = list_view

    # Override the default get_queryset()
    def get_queryset(self):
        return EnglishWord.objects.all().order_by("word")

    # Add additional context variables
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(EnglishWordListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        # Default context = englishword_list
        context["heading"] = "List of English words in the dictionary"
        return context


class OshindongaPhoneticListView(generic.ListView):
    paginate_by = 50
    model = OshindongaPhonetic
    template_name = list_view

    def get_queryset(self):
        return OshindongaPhonetic.objects.all().order_by("oshindonga_word")

    def get_context_data(self, **kwargs):
        context = super(OshindongaPhoneticListView, self).get_context_data(**kwargs)
        context["heading"] = "List of Oshindonga phonetics in the dictionary"
        return context


class OshindongaWordListView(generic.ListView):
    paginate_by = 50
    model = OshindongaWord
    template_name = list_view

    def get_queryset(self):
        return OshindongaWord.objects.all().order_by("word")

    def get_context_data(self, **kwargs):
        context = super(OshindongaWordListView, self).get_context_data(**kwargs)
        context["heading"] = "List of Oshindonga words in the dictionary"
        return context


class OshindongaIdiomListView(generic.ListView):
    paginate_by = 10
    model = OshindongaIdiom
    template_name = list_view

    def get_queryset(self):
        return OshindongaIdiom.objects.all().order_by("oshindonga_idiom")

    def get_context_data(self, **kwargs):
        context = super(OshindongaIdiomListView, self).get_context_data(**kwargs)
        context["heading"] = "List of Oshindonga idioms in the dictionary"
        return context


# Detail View


class EnglishWordDetailView(generic.DetailView):
    model = EnglishWord
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(EnglishWordDetailView, self).get_context_data(**kwargs)
        context["heading"] = "English word detail view"
        return context


class OshindongaPhoneticDetailView(generic.DetailView):
    model = OshindongaPhonetic
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaPhoneticDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Oshindonga phonetic detail view"
        return context


class OshindongaWordDetailView(generic.DetailView):
    model = OshindongaWord
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaWordDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Oshindonga word detail view"
        return context


class WordDefinitionDetailView(generic.DetailView):
    model = WordDefinition
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(WordDefinitionDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Word definition detail view"
        return context


class DefinitionExampleDetailView(generic.DetailView):
    model = DefinitionExample
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(DefinitionExampleDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Definition example detail view"
        return context


class OshindongaIdiomDetailView(generic.DetailView):
    model = OshindongaIdiom
    template_name = detail_view

    def get_context_data(self, **kwargs):
        context = super(OshindongaIdiomDetailView, self).get_context_data(**kwargs)
        context["heading"] = "Oshindonga idiom detail view"
        return context
