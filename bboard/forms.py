from django import forms
from .models import Bd


class BbForm(forms.ModelForm):
    class Meta:
        model = Bd
        fields = ['title', 'content', 'price', 'rubric']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'rubric': forms.Select(attrs={'class': 'form-control'})
        }
