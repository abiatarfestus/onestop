from django import forms


class SearchWordForm(forms.Form):
    search_word = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control-lg me-2'}), max_length=225)
