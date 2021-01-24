from django import forms


class SearchWordForm(forms.Form):
    search_word = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg', 'placeholder': 'Search word'}), max_length=225)
