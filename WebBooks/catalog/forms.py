from django import forms
from datetime import date
from django.forms import ModelForm
from .models import Book
class AuthorsForm(forms.Form):
    first_name = forms.CharField(label="Ім'я автора")
    last_name=forms.CharField(label="Прізвище автора")
    date_of_birth=forms.DateField(label="Дата народження",
                                  initial=format(date.today()),
                                  widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    date_of_death = forms.DateField(label="Дата смерті",
                                    initial=format(date.today()),
                                    widget=forms.widgets.DateInput(attrs={'type': 'date'}))

class BookModelForm(ModelForm):
    class Meta:
        model = Book
        fields=['title','genre','language','author','summary','isbn']
