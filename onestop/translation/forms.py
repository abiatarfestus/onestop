from django import forms


class TextForm(forms.Form):
    ENGLISH = "English"
    OSHINDONGA = "Oshindonga"
    INPUT_LANGUAGE = [
        (ENGLISH, "English"),
        (OSHINDONGA, "Oshindonga"),
    ]
    input_language = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                "class": "form-check form-check-inline",
                "style": "margin-left:10px;",
                "type": "radio",
            }
        ),
        choices=INPUT_LANGUAGE,
    )

    input_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control auto-expand",
                "id": "inputTextarea",
                "rows": "3",
                "data-min-rows": "1",
                "placeholder": "Enter Your Input Text Here...",
            }
        ),
    )
