# flake8: noqa
import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class ChangeProfileForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Nome de usuário',
            'email': 'E-mail',
        }
        help_texts = {
            'username': "Pode ter de 3 a 20 caracteres. São permitidos apenas letras, números, _ e .",
            'email': 'O E-mail precisa ser válido',
        }
        error_messages = {
            'username': {
                'unique': 'Este nome de usuário já está sendo utilizado',
                'required': 'Este campo não pode estar vazio',
            },
            'first_name': {
                'required': 'Este campo não pode estar vazio',
            },
            'last_name': {
                'required': 'Este campo não pode estar vazio',
            },
            'email': {
                'required': 'Este campo não pode estar vazio',
                'invalid': 'Digite um e-mail válido',
            },
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'required': 'required',
                'unique': 'False'
            }),
            'username': forms.TextInput(attrs={
                'required': 'required',
                'unique': 'False'
            })
        }

    def clean_username(self):
        data = self.cleaned_data.get('username')

        exists = User.objects.filter(username=data).exists()
        current = User.objects.filter(
            username=data, pk=self.instance.pk).exists()

        if exists and not current:
            raise ValidationError(
                'Este nome de usuário já está sendo utilizado', code='unique')

        if len(data) < 3:
            raise ValidationError(
                'O nome de usuário é muito curto. Digite no mínimo 3 caracteres',
                code='min-length',
            )
        elif len(data) > 20:
            raise ValidationError(
                'O nome de usuário é muito longo. Digite no maximo 20 caracteres',
                code='max-length',
            )

        for c in data:
            if re.search("[0-9]|[a-z]|[A-Z]|\.|\_", c) is None:
                raise ValidationError(
                    'Há caracteres não permitidos no username',
                    code='invalid',
                )

        return data

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name').strip()

        if len(data) < 1:
            raise ValidationError(
                'Este campo não pode estar vazio',
                code='required',
            )

        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name').strip()

        if len(data) < 1:
            raise ValidationError(
                'Este campo não pode estar vazio',
                code='required',
            )

        return data

    def clean_email(self):
        data = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=data).exists()
        current = User.objects.filter(email=data, pk=self.instance.pk).exists()

        if exists and not current:
            raise ValidationError(
                'Já existe uma conta vinculada a este E-mail', code='unique',
            )

        return data
