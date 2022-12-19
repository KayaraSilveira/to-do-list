from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('change_password/', views.change_password_view,
         name='change_password'),
    path('change_password/send', views.change_password_send,
         name='change_password_send'),
    path('change_profile/', views.change_profile_view,
         name='change_profile'),
    path('change_profile/send', views.change_profile_send,
         name='change_profile_send'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout', views.logout_view, name='logout'),
    path('delete', views.delete_account, name='delete'),
    path('profile/<int:pk>/', views.ProfileDetail.as_view(), name='profile'),
]
