from django import forms
#Es una convención tener todos tus forms en un solo archivo
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead

User = get_user_model() #Especificamos nuestro propio modelo de usuario en vez de utilizar el de django

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead #Establecemos el modelo con el que estamos trabajando
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
        )

class LeadForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

