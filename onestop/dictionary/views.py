from django.shortcuts import render
#from django.http import HttpResponse
import datetime

# Create your views here.

def index(request):
    now = datetime.datetime.now()
    context = {'time': now}
    return render(request, 'dictionary/index.html', context)