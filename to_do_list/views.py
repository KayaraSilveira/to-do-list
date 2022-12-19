# flake8: noqa
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from to_do_list.forms.list_tasks_form import ListTasksForm
from to_do_list.forms.task_form import TaskForm

from .models import ListTasks, Task


@login_required(login_url='accounts:login', redirect_field_name='next')
def list_tasks(request, list_pk=None):

    if list_pk is not None:
        list_tasks = ListTasks.objects.filter(pk=list_pk).first()

        if list_tasks.owner == request.user:
            owner = True
        elif request.user in list(list_tasks.members.all()):
            owner = False
        else:
            raise Http404

        tasks = Task.objects.filter(
            list_tasks__pk=list_pk).order_by('order_list')
        title = list_tasks.title

    else:
        owner = False
        tasks = Task.objects.filter(
            list_tasks__owner=request.user).order_by('order_home')
        title = 'Home'

    if request.session.get('hide'):
        tasks = tasks.filter(is_completed=False)

    return render(request, 'to_do_list/pages/list_tasks.html', context={
        'tasks': tasks,
        'title': title,
        'list_pk': list_pk,
        'owner': owner
    })


@login_required(login_url='accounts:login', redirect_field_name='next')
def task_hide(request):

    if request.session.get('hide'):
        request.session['hide'] = False
    else:
        request.session['hide'] = True

    list_pk = request.POST.get('list_pk')
    if list_pk != 'None':
        url = reverse('to_do_list:list', args=[list_pk])
    else:
        url = reverse('to_do_list:home')
    return redirect(url)


@login_required(login_url='accounts:login', redirect_field_name='next')
def task_completed(request, is_completed):

    task = Task.objects.filter(pk=request.POST.get('task_pk')).first()

    if task is None or (task.list_tasks.owner != request.user and request.user not in list(task.list_tasks.members.all())):
        raise Http404()

    list_pk = request.POST.get('list_pk')

    if is_completed == 'True':
        task.is_completed = False
    else:
        task.is_completed = True

    task.save()
    if list_pk != 'None':
        return redirect(reverse('to_do_list:list', args=[list_pk]))
    else:
        return redirect(reverse('to_do_list:home'))


@login_required(login_url='accounts:login', redirect_field_name='next')
def task_order(request):
    list_task_pk = request.POST.get('list_task_pk').split(',')

    list_pk = request.POST.get('list_pk')

    for i in range(1, len(list_task_pk)):
        task = Task.objects.filter(pk=int(list_task_pk[i])).first()
        if list_pk is not None:
            task.order_list = i
        else:
            task.order_home = i

        task.save()

    if list_pk is not None:
        return redirect(reverse('to_do_list:list', args=[list_pk]))
    else:
        return redirect(reverse('to_do_list:home'))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class ListAdd(View):
    def get_list_tasks(self, list_pk):

        list_tasks = ListTasks.objects.filter(
            owner=self.request.user, pk=list_pk,).first()

        if not list_tasks:
            raise Http404()

        return list_tasks

    def get_members_list(self, list_pk):
        list_tasks = self.get_list_tasks(list_pk)
        members_list = list_tasks.members.all()
        return members_list

    def render_list_add(self, title, list_pk, members_list):
        return render(
            self.request,
            'to_do_list/pages/list_add.html',
            context={
                'title': title,
                'list_pk': list_pk,
                'members_list': members_list
            }
        )

    def get(self, request, list_pk):
        list_tasks = self.get_list_tasks(list_pk)
        title = list_tasks.title
        members_list = self.get_members_list(list_pk)
        return self.render_list_add(title, list_pk, members_list)

    def post(self, request, list_pk):
        list_tasks = self.get_list_tasks(list_pk)
        username = request.POST.get('username')
        title = list_tasks.title
        members_list = self.get_members_list(list_pk)

        user = User.objects.filter(username=username).first()

        if user is None:
            messages.error(request, 'Nenhum usuário foi encontrado')
        elif user == request.user:
            messages.error(request, 'Você já é o dono desta lista')
        else:
            list_tasks.members.add(user)
            list_tasks.save()

        return self.render_list_add(title, list_pk, members_list)


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class ListRemove(ListAdd):
    def post(self, *args, **kwargs):
        list_pk = kwargs.get('list_pk')
        list_tasks = self.get_list_tasks(list_pk)
        username = self.request.POST.get('username')
        user = User.objects.filter(username=username).first()
        list_tasks.members.remove(user)
        list_tasks.save()
        return redirect(reverse('to_do_list:list_add', args=[list_pk]))


def list_leave(request, list_pk):
    list_tasks = ListTasks.objects.filter(pk=list_pk).first()

    if list_tasks is None:
        raise Http404()

    user = User.objects.filter(username=request.user).first()
    list_tasks.members.remove(user)
    list_tasks.save()

    return redirect(reverse('to_do_list:home'))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardListTask(View):
    def get_list_tasks(self, list_pk=None):
        list_tasks = None

        if list_pk is not None:
            list_tasks = ListTasks.objects.filter(
                owner=self.request.user,
                pk=list_pk,
            ).first()

            if not list_tasks:
                raise Http404()

        return list_tasks

    def render_list_tasks(self, form):
        return render(
            self.request,
            'to_do_list/pages/dashboard_list_tasks.html',
            context={
                'form': form,
            }
        )

    def get(self, request, list_pk=None):
        list_tasks = self.get_list_tasks(list_pk)
        form = ListTasksForm(instance=list_tasks)
        return self.render_list_tasks(form)

    def post(self, request, list_pk=None):
        list_tasks = self.get_list_tasks(list_pk)
        form = ListTasksForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=list_tasks,
        )

        if form.is_valid():
            list_tasks = form.save(commit=False)

            list_tasks.owner = request.user
            list_tasks.save()

            return redirect(
                reverse(
                    'to_do_list:list', args=(
                        list_tasks.pk,
                    )
                )
            )

        return self.render_list_tasks(form)


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardListTaskDelete(DashboardListTask):
    def post(self, *args, **kwargs):
        list_tasks = self.get_list_tasks(self.request.POST.get('list_pk'))
        list_tasks.delete()
        return redirect(reverse('to_do_list:home'))


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardTask(View):
    def get_task(self, task_pk=None):
        task = None
        if task_pk is not None:
            task = Task.objects.filter(pk=task_pk).first()

            if task is None or (task.list_tasks.owner != self.request.user and self.request.user not in list(task.list_tasks.members.all())):
                raise Http404()

        return task

    def render_task(self, form):
        return render(
            self.request,
            'to_do_list/pages/dashboard_task.html',
            context={
                'form': form,
            }
        )

    def get(self, request, task_pk=None):
        task = self.get_task(task_pk)
        list_selected = self.request.GET.get('list')
        form = TaskForm(instance=task, user=self.request.user,
                        list_selected=list_selected)
        return self.render_task(form)

    def post(self, request, task_pk=None):
        task = self.get_task(task_pk)
        form = TaskForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=task,
            user=self.request.user
        )

        if form.is_valid():
            task = form.save(commit=False)

            task.is_completed = task.is_completed or False
            task.save()

            return redirect(
                reverse(
                    'to_do_list:list', args=(
                        task.list_tasks.pk,
                    )
                )
            )

        return self.render_task(form)


@method_decorator(
    login_required(login_url='accounts:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardTaskDelete(DashboardTask):
    def post(self, *args, **kwargs):
        task = self.get_task(self.request.POST.get('task_pk'))
        list_pk = self.request.POST.get('list_pk')
        task.delete()
        if list_pk != 'None':
            return redirect(reverse('to_do_list:list', args=[list_pk]))
        else:
            return redirect(reverse('to_do_list:home'))
