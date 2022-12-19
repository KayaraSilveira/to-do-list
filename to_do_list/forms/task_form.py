# flake8: noqa
from collections import defaultdict

from django import forms
from django.db.models import Q

from to_do_list.models import ListTasks, Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get('list_selected', False) or kwargs.get('list_selected', False) == None:
            list_selected = kwargs.pop('list_selected')
        else:
            list_selected = None
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['list_tasks'] = forms.ModelChoiceField(
            queryset=ListTasks.objects.filter(
                Q(owner=user) | Q(members__in=[user])
            ),
            label='Lista da Tarefa',
            initial=list_selected
        )

        self._my_errors = defaultdict(list)

    title = forms.CharField(
        label='Tarefa'
    )

    class Meta:
        model = Task
        fields = ('title', 'list_tasks')

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) > 200:
            self._my_errors['title'].append(
                'Texto muito longo, por favor digite menos de 200 caracteres')

        return title
