from .models import *
from django import forms


class Myform(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['search_keyword','username']