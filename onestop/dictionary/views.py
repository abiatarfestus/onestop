from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {}
    return render(request, 'dictionary/index.html', context)

def search(request):
    context = {}
    return render(request, 'dictionary/search.html', context)