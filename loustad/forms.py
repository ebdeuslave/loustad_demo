from django import forms
from .models import VDemo


class Vform(forms.ModelForm):
    class Meta:
        model = VDemo
        exclude = ('response', )

