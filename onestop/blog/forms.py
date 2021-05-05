from django import forms
from .models import Comment, Post
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'author',  'content')
        widgets = {'title': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2',}), 'slug': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'author': forms.Select(
            attrs={'class': 'form-control form-control-lg mb-2'}),'content': SummernoteWidget(
            attrs={'class': 'form-control form-control-lg mb-2'})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {'name': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2',}), 'email': forms.EmailInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'body': forms.Textarea(
            attrs={'class': 'form-control form-control-lg mb-2'})}