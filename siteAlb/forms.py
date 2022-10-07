from django import forms
from .models import *

versions = {
    ("4.1", "plane-4.1"),
    ("3.9", "plane-3.9")
}

class versSim(forms.Form):
    vers_field = forms.ChoiceField(choices=versions, label="", widget=forms.RadioSelect)
    count_cont = forms.ChoiceField(choices=((1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")), label="", widget=forms.RadioSelect)