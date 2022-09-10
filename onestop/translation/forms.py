from django import forms

<<<<<<< HEAD
=======

>>>>>>> ffe87787d1f395e67cf9792d6212b81a8f2b0e17
class TextForm(forms.Form):
    ENGLISH = "English"
    OSHINDONGA = "Oshindonga"
    INPUT_LANGUAGE = [
        (ENGLISH, "English"),
        (OSHINDONGA, "Oshindonga"),
    ]
    input_language = forms.ChoiceField(
<<<<<<< HEAD
        widget=forms.RadioSelect(attrs={"class": "form-check form-check-inline", "type": "radio",}), choices=INPUT_LANGUAGE)
=======
        widget=forms.RadioSelect(
            attrs={
                "class": "form-check form-check-inline",
                "style": "margin-left:10px;",
                "type": "radio",
            }
        ),
        choices=INPUT_LANGUAGE,
    )
>>>>>>> ffe87787d1f395e67cf9792d6212b81a8f2b0e17

    input_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
<<<<<<< HEAD
                "class": "form-control", "rows": "10",
                "placeholder": "Enter Your Input Text Here...",
            }
        ),
    )
=======
                "class": "form-control auto-expand",
                "id": "inputTextarea",
                "rows": "3",
                "data-min-rows": "1",
                "placeholder": "Enter Your Input Text Here...",
            }
        ),
    )
>>>>>>> ffe87787d1f395e67cf9792d6212b81a8f2b0e17
