from django import forms
from django.forms import ModelForm
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample


class SearchWordForm(forms.Form):
    ENGLISH = 'English'
    OSHINDONGA = 'Oshindonga'
    INPUT_LANGUAGE = [
        (ENGLISH, 'English'),
        (OSHINDONGA, 'Oshindonga'),
    ]
    input_language = forms.ChoiceField(widget=forms.Select(
        attrs={'class': "form-select form-select-lg", 'id': "inputGroupSelect01"}), choices=INPUT_LANGUAGE)
    search_word = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Search word'}), max_length=50)


class EnglishWordForm(ModelForm):
    class Meta:
        model = EnglishWord
        fields = '__all__'


class OshindongaWordForm(ModelForm):
    class Meta:
        model = OshindongaWord
        fields = '__all__'


class WordDefinitionForm(ModelForm):
    class Meta:
        model = WordDefinition
        fields = '__all__'
        widgets = {'part_of_speech': forms.Select(
            attrs={'onchange': 'displayPluralOrTense()'})}


class DefinitionExampleForm(ModelForm):
    class Meta:
        model = DefinitionExample
        fields = '__all__'
