from django import forms
from .models import Comment, Post, Category
from django_summernote.widgets import SummernoteWidget
#from django_summernote.fields import SummernoteTextFormField, SummernoteTextField


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'image', 'content')
        prepopulated_fields = {'slug': ('title',)}
        widgets = {'title': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2', }), 'category': forms.SelectMultiple(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'image': forms.FileInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'content': SummernoteWidget(
            attrs={'class': 'form-control form-control-lg mb-2', 'summernote': {'width': '100%'}})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {'name': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2', }), 'email': forms.EmailInput(
            attrs={'class': 'form-control form-control-lg mb-2'}), 'body': forms.Textarea(
            attrs={'class': 'form-control form-control-lg mb-2'})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        widgets = {'name': forms.TextInput(
            attrs={'class': 'form-control form-control-lg mb-2', })}
