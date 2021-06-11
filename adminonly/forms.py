from django import forms

from main.models import Movies, Series, Titles, Genres
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_staff'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Enter last name'}),
            'email': forms.TextInput(attrs={'class': 'form-control',  'placeholder': 'Enter valid email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
            'is_staff': forms.CheckboxInput()
        }


class MoviesForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = [
            'title',
            'language',
            'video'
        ]
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'})
        }


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = [
            'title',
            'episode',
            'season',
            'language',
            'video'
        ]
        widgets = {
            'title': forms.Select(attrs={'class': 'form-control'}),
            'episode': forms.NumberInput(attrs={'class': 'form-control'}),
            'season': forms.NumberInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'})
        }


class TitleForm(forms.ModelForm):
    class Meta:
        model = Titles
        fields = [
            'title',
            'thumbnail',
            'genre',
            'description',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter New Title'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'genre': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description Here'}),
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genres
        fields = [
            'genre'
        ]
        widgets = {
            'genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter genre'})
        }
