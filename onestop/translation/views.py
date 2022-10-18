from django.shortcuts import render
from .forms import TextForm
from .translator import Translation


def translate_text(request):
    form = TextForm(request.GET)
    context = {"output_text": "Your translation will appear here...", "form": form}
    if request.method == "POST":
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
    return render(request, "translation/translation.html", context)
