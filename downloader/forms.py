
from django import forms

class YouTubeLinkForm(forms.Form):
    link = forms.URLField(label='Link do YouTube', max_length=200)