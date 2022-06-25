from django.shortcuts import render

# General views


def index(request):
    context = {}
    return render(request, "index.html", context)


def under_construction(request):
    context = {}
    return render(request, "onestop/under_construction.html", context)


def access_denied(request):
    context = {}
    return render(request, "onestop/access_denied.html", context)
