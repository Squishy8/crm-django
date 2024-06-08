from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm #Ya existe un form para crear usuarios

User = get_user_model()

class AgentModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name'
        )
        #Este form crearía un nuevo usuario, no un nuevo agente