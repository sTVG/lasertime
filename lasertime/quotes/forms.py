from django import forms
from .models import Material

class QuoteForm(forms.Form):
    svg_file = forms.FileField(label='Upload SVG File')
    material = forms.ModelChoiceField(queryset=Material.objects.all())
