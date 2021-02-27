from django import forms
from django.forms import ModelForm
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample, OshindongaIdiom


class SearchWordForm(forms.Form):
    ENGLISH = 'English'
    OSHINDONGA = 'Oshindonga'
    INPUT_LANGUAGE = [
        (ENGLISH, 'English'),
        (OSHINDONGA, 'Oshindonga'),
    ]
    input_language = forms.ChoiceField(widget=forms.Select(
        attrs={'class': "form-select form-select-lg", 'id': "inputGroupSelect01", 'style':'max-width:21%;'}), choices=INPUT_LANGUAGE)
    search_word = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Search word'}), max_length=50)


class EnglishWordForm(ModelForm):
    class Meta:
        model = EnglishWord
        # Not recommended (potential security issue if more fields added)
        fields = '__all__'
        widgets = {'word': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2', 'placeholder': 'Enter an English word'}), 'word_case': forms.Select(
            attrs={'class': 'form-select form-select-lg mb-2'})}

    def clean(self):
        cleaned_data = super().clean()
        word_case = cleaned_data.get('word_case')
        word = cleaned_data.get('word')
        if word_case == 'Abbreviation':
            self.cleaned_data['word'] = word.strip().upper()
        elif word_case == 'Proper Noun':
            self.cleaned_data['word'] = word.strip().capitalize()
        else:
            self.cleaned_data['word'] = word.strip().lower()


class OshindongaWordForm(ModelForm):
    english_word = forms.ModelChoiceField(
        queryset=EnglishWord.objects.all().order_by('word'), empty_label='Select the English word',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-2'}))

    class Meta:
        model = OshindongaWord
        fields = '__all__'
        widgets = {'word': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2', 'placeholder': 'Shanga oshitya shOshindonga'}), 'word_case': forms.Select(
            attrs={'class': 'form-select form-select-lg mb-2'})}
    
    def clean(self):
        cleaned_data = super().clean()
        word_case = cleaned_data.get('word_case')
        word = cleaned_data.get('word')
        if word_case == 'Abbreviation':
            self.cleaned_data['word'] = word.strip().upper()
        elif word_case == 'Proper Noun':
            self.cleaned_data['word'] = word.strip().capitalize()
        else:
            self.cleaned_data['word'] = word.strip().lower()

class WordDefinitionForm(ModelForm):
    word_pair = forms.ModelChoiceField(
        queryset=OshindongaWord.objects.all().order_by('word'), empty_label='Select a word pair to define',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-2'}))

    class Meta:
        model = WordDefinition
        fields = '__all__'
        widgets = {'part_of_speech': forms.Select(
            attrs={'class': 'form-select form-select-lg mb-2', 'onchange': 'displayPluralOrTense()'}), 'synonym1': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'synonym2': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'synonym3': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'synonym4': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'simple_present': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'present_participle': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'simple_past': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'past_participle': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'plural1': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'plural2': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'english_definition': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2', 'placeholder': 'Enter the English definition here...'}), 'oshindonga_definition': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2', 'placeholder': 'Shanga efatululo mOshindonga mpaka...'})}


class DefinitionExampleForm(ModelForm):
    definition = forms.ModelChoiceField(
        queryset=WordDefinition.objects.all().order_by('word_pair'), empty_label='Select a definition to exemplify',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-2'}))

    class Meta:
        model = DefinitionExample
        fields = '__all__'
        widgets = {'english_example': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'oshindonga_example': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'})}


class OshindongaIdiomForm(ModelForm):
    word_pair = forms.ModelChoiceField(
        queryset=OshindongaWord.objects.all().order_by('word'), empty_label='Select the word pair',
        widget=forms.Select(attrs={'class': 'form-select form-select-lg mb-2'}))

    class Meta:
        model = OshindongaIdiom
        fields = '__all__'
        widgets = {'oshindonga_idiom': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'})}
