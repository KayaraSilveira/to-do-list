from django.contrib import admin

from .models import ListTasks, Task


class ListTasksAdmin(admin.ModelAdmin):
    ...


class TaskAdmin(admin.ModelAdmin):
    ...


admin.site.register(ListTasks, ListTasksAdmin)
admin.site.register(Task, TaskAdmin)
