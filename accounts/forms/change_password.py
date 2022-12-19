from django import forms
from django.core.exceptions import ValidationError


class ChangePasswordForm(forms.Form):

    new_password = forms.CharField(
        label='Digite a nova senha',
        widget=forms.PasswordInput(),
        help_text='A senha precisa ter pelo menos 8 caracteres',
        error_messages={'required': 'Este campo não pode estar vazio'}
    )

    new_password_confirm = forms.CharField(
        label='Confirme a nova senha',
        widget=forms.PasswordInput(),
        help_text='Precisa ser igual a nova senha',
        error_messages={'required': 'Este campo não pode estar vazio'}
    )

    old_password = forms.CharField(
        label='Digite sua senha antiga',
        widget=forms.PasswordInput(),
        error_messages={'required': 'Este campo não pode estar vazio'}
    )

    def clean_new_password(self):
        data = self.cleaned_data.get('new_password')

        if len(data) < 8:
            raise ValidationError(
                'A senha é muito curta. Digite pelo menos 8 caracteres',
                code='min-length',
            )

        return data

    def clean(self):
        cleaned_data = super().clean()

        password = self.data.get('new_password')
        password_confirm = cleaned_data.get('new_password_confirm')

        if password != password_confirm:
            password_confirmation_error = ValidationError(
                'As senhas precisam ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'new_password': password_confirmation_error,
                'new_password_confirm': password_confirmation_error,
            })
