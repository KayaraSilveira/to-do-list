from collections import defaultdict

from django import forms

from to_do_list.models import ListTasks


class ListTasksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

    title = forms.CharField(
        label=''
    )

    class Meta:
        model = ListTasks
        fields = ('title',)

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) > 20:
            self._my_errors['title'].append(
                'Título muito longo. O tamanho máximo é de 20 caracteres')

        return title
