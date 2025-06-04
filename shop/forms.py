from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Stuff, Rating


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255,
        required=True,
        help_text="Це обов'язкове поле. Введіть дійсну пошту."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class StuffForm(forms.ModelForm):
    class Meta:
        model = Stuff
        fields = ['stuff_name', 'stuff_desc', 'price', 'image']

        widgets = {
            'stuff_name': forms.TextInput(attrs={'class': 'form-control'}),
            'stuff_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Залиште свій коментар'})
        }