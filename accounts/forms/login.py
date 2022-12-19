from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(
        label='Digite seu nome de usuário',
        error_messages={'required': 'Este campo não pode estar vazio'}
    )
    password = forms.CharField(
        label='Digite sua senha',
        widget=forms.PasswordInput(),
        error_messages={'required': 'Este campo não pode estar vazio'}
    )
