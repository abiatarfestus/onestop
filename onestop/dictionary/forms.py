from django import forms
from django.forms import ModelForm
from .models import EnglishWord, OshindongaWord, WordDefinition, DefinitionExample


class SearchWordForm(forms.Form):
    search_word = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Search word'}), max_length=225)


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


class DefinitionExampleForm(ModelForm):
    class Meta:
        model = DefinitionExample
        fields = '__all__'