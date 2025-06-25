from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Stuff, Rating
from captcha.fields import CaptchaField


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
    captcha = CaptchaField()

    class Meta:
        model = Rating
        fields = ['stars', 'comment', 'captcha']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Залиште свій коментар'})
        }


class FeedBackForm(forms.Form):
    subject = forms.CharField(
        max_length=200,
        label='Topic',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    from_email = forms.EmailField(
        label = 'Your Email',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    message = forms.CharField(
        label='Повідомлення',
        widget=forms.TextInput(attrs={'class': 'form-control', 'rows': 5})
    )