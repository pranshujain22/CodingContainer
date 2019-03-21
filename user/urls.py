from django.urls import path
from user import views


# TEMPLATE TAGGING
app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('containers', views.containers, name='containers'),
    path('images', views.images, name='images'),
    path('create', views.create_container, name='create_container'),
    path('getContainers', views.get_containers, name='get_containers'),
    path('deleteContainer', views.remove_container, name='remove_container'),
    path('openport', views.open_port, name='openPort'),
    path('initial_setup', views.initial_setup, name='initial_setup'),
    path('profile', views.profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),
    path('files', views.files, name='files'),
    path('editor', views.editor, name='editor'),
    path('directory', views.get_directory, name='directory'),
    path('edit_file', views.edit_file, name='edit_file'),
]
