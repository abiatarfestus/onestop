from .models import Comment
from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {'name': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2',}), 'email': forms.EmailInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'body': forms.Textarea(
            attrs={'class': 'form-control form-control-lg mb-2'})}