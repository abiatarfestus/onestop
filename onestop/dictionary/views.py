from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import SearchWordForm

# Create your views here.

def index(request):
    context = {}
    return render(request, 'dictionary/index.html', context)

# def search(request):
#     context = {}
#     return render(request, 'dictionary/search.html', context)

def search_word(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchWordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/search/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchWordForm()

    return render(request, 'dictionary/search.html', {'form': form})