from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
