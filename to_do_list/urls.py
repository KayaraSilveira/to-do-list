from django.urls import path

from . import views

app_name = 'to_do_list'

urlpatterns = [
    path('', views.list_tasks, name='home'),
    path('list/new', views.DashboardListTask.as_view(), name='list_new'),
    path('list/edit/<int:list_pk>',
         views.DashboardListTask.as_view(), name='list_edit'),
    path('list/add/<int:list_pk>', views.ListAdd.as_view(), name='list_add'),
    path('list/remove/<int:list_pk>',
         views.ListRemove.as_view(), name='list_remove'),
    path('list/delete',
         views.DashboardListTaskDelete.as_view(), name='list_delete'),
    path('list/<int:list_pk>', views.list_tasks, name='list'),
    path('list/leave/<int:list_pk>', views.list_leave, name='list_leave'),
    path('task/order', views.task_order, name="task_order"),
    path('task/hide', views.task_hide, name="task_hide"),
    path('task/new/',
         views.DashboardTask.as_view(), name='task_new'),
    path('task/new/<int:list>',
         views.DashboardTask.as_view(), name='task_new'),
    path('task/edit/<int:task_pk>',
         views.DashboardTask.as_view(), name='task_edit'),
    path('task/delete',
         views.DashboardTaskDelete.as_view(), name='task_delete'),
    path('task/completed/<str:is_completed>',
         views.task_completed, name="task_completed"),

]
