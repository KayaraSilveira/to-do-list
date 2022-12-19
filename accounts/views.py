# flake8: noqa
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView

from to_do_list.models import ListTasks

from .forms import (ChangePasswordForm, ChangeProfileForm, LoginForm,
                    RegisterForm)


def register_view(request):

    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    return render(request, 'accounts/pages/register.html', {
        'form': form,
    })


def register_create(request):

    if not request.POST:
        raise Http404

    POST = request.POST

    request.session['register_form_data'] = POST

    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        del (request.session['register_form_data'])
        return redirect('accounts:login')

    return redirect('accounts:register')


def login_view(request):

    login_form_data = request.session.get('login_form_data')
    form = LoginForm(login_form_data)

    return render(request, 'accounts/pages/login.html', {
        'form': form,
    })


def login_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST

    request.session['login_form_data'] = POST

    form = LoginForm(POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            login(request, authenticated_user)
            if request.session.get('login_form_data') is not None:
                del (request.session['login_form_data'])
            return redirect(reverse('to_do_list:home'))

        else:
            messages.error(request, 'Senha ou usuário inválido')

    return redirect(reverse('accounts:login'))


@login_required(login_url='accounts:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return Http404

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('to_do_list:home'))

    logout(request)
    return redirect(reverse('accounts:login'))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class ProfileDetail(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'accounts/pages/profile.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(pk=self.request.user.pk)
        return qs


@login_required(login_url='accounts:login', redirect_field_name='next')
def change_password_view(request):

    change_password_form_data = request.session.get(
        'change_password_form_data')
    form = ChangePasswordForm(change_password_form_data)

    if change_password_form_data is not None:
        del (request.session['change_password_form_data'])

    return render(request, 'accounts/pages/change-password.html', {
        'form': form,
    })


@login_required(login_url='accounts:login', redirect_field_name='next')
def change_password_send(request):
    if not request.POST:
        raise Http404

    POST = request.POST

    request.session['change_password_form_data'] = POST

    form = ChangePasswordForm(POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=request.user.username,
            password=form.cleaned_data.get('old_password', ''),
        )

        if authenticated_user is not None:
            new_password = form.cleaned_data.get('new_password', '')
            request.user.set_password(new_password)
            request.user.save()

            if request.session.get('change_password_form_data') is not None:
                del (request.session['change_password_form_data'])

            messages.success(
                request, 'Senha alterada com sucesso. Faça login com sua nova senha.')

        else:
            messages.error(
                request, 'Erro ao alterar senha: a senha antiga não está correta.')

    return redirect(reverse('accounts:change_password'))


@login_required(login_url='accounts:login', redirect_field_name='next')
def change_profile_view(request):
    profile = User.objects.get(pk=request.user.pk)
    change_profile_form_data = request.session.get('change_profile_form_data')

    if change_profile_form_data is not None:
        del (request.session['change_profile_form_data'])

    form = ChangeProfileForm(instance=profile, data=change_profile_form_data)
    return render(request, 'accounts/pages/change-profile.html', {
        'form': form,
    })


@login_required(login_url='accounts:login', redirect_field_name='next')
def change_profile_send(request):
    if not request.POST:
        raise Http404

    profile = User.objects.get(pk=request.user.pk)

    POST = request.POST

    request.session['change_profile_form_data'] = POST

    form = ChangeProfileForm(POST, instance=profile)

    if form.is_valid():
        form.save()
        messages.success(request, 'Perfil editado com sucesso')
        del (request.session['change_profile_form_data'])

    return redirect(reverse('accounts:change_profile'))


@login_required(login_url='accounts:login', redirect_field_name='next')
def delete_account(request):

    if not request.POST:
        raise Http404

    account = User.objects.get(pk=request.user.pk)
    account.delete()

    messages.error(request, 'Sua conta foi excluída permanentemente')

    return redirect(reverse('accounts:login'))
