# flake8: noqa
import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class RegisterForm(ModelForm):

    password_confirm = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Digite a senha novamente',
        error_messages={'required': 'Este campo não pode estar vazio'},
        help_text='As senhas precisam ser iguais'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'first_name': 'Digite seu nome',
            'last_name': 'Digite seu sobrenome',
            'username': 'Crie um nome de usuário',
            'email': 'Digite seu e-mail',
            'password': 'Crie uma senha'
        }
        help_texts = {
            'username': "Pode ter de 3 a 20 caracteres. São permitidos apenas letras, números, _ e .",
            'email': 'O E-mail precisa ser válido',
            'password': 'A senha precisa ter pelo menos 8 caracteres',
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
            'password': {
                'required': 'Este campo não pode estar vazio',
            }
        }
        widgets = {
            'password': forms.PasswordInput(),
            'first_name': forms.TextInput(attrs={
                'required': 'required'
            }),
            'last_name': forms.TextInput(attrs={
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'required': 'required'
            }),
        }

    def clean_username(self):
        data = self.cleaned_data.get('username')

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

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if len(data) < 8:
            raise ValidationError(
                'A senha é muito curta. Digite pelo menos 8 caracteres',
                code='min-length',
            )

        return data

    def clean_email(self):
        data = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=data).exists()

        if exists:
            raise ValidationError(
                'Já existe uma conta vinculada a este E-mail', code='unique',
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = self.data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            password_confirmation_error = ValidationError(
                'As senhas precisam ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password_confirm': password_confirmation_error,
            })
