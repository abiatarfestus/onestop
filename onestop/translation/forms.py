from django import forms

class TextForm(forms.Form):
    ENGLISH = "English"
    OSHINDONGA = "Oshindonga"
    INPUT_LANGUAGE = [
        (ENGLISH, "English"),
        (OSHINDONGA, "Oshindonga"),
    ]
    input_language = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "form-check form-check-inline", "type": "radio",}), choices=INPUT_LANGUAGE)

    input_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control", "rows": "10",
                "placeholder": "Enter Your Input Text Here...",
            }
        ),
    )