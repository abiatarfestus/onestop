from django.shortcuts import render
from .forms import TextForm
from .translator import Translation


def translate_text(request):
    form = TextForm(request.GET)
    context = {"output_text": "Your translation will appear here...", "form": form}
<<<<<<< HEAD
    if request.method == 'POST':
=======
    if request.method == "POST":
>>>>>>> ffe87787d1f395e67cf9792d6212b81a8f2b0e17
        form = TextForm(data=request.POST)
        if form.is_valid():
            input_language = form.cleaned_data["input_language"]
            input_text = form.cleaned_data["input_text"]
            translation = Translation(input_language, input_text)
            translation = translation.translate()
            context["output_text"] = translation
            context["form"] = form
    else:
        text_form = TextForm()
<<<<<<< HEAD
    return render(request, "translation/translation.html", context)
=======
    return render(request, "translation/translation.html", context)
>>>>>>> ffe87787d1f395e67cf9792d6212b81a8f2b0e17
