"""
URL configuration for Active_Board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path

from users.views import add_position, add_task_for_user, add_teg, add_user, delete_user, edit_user, home, login, logout, register, update_task_status, user_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home", home,name="home"),
    path('add_user/',add_user,name="add_user"),
    path('delete_user/<int:id>/',delete_user,name="delete_user"),
    path('edit_user/<int:id>/',edit_user,name="edit_user"),
    path('user/user_status/<int:id>/',user_status,name="user_status"),
    path('user/update_status/<int:task_id>/',update_task_status,name="update_status"),
    path("user/add_task/",add_task_for_user,name="add_task"),
    path('register/',register,name="register"),
    path('',login,name='login'),
    path('logout/',logout,name='logout'),
    path('add_teg/',add_teg,name="add_teg"),    
    path('add_position/',add_position,name="add_position"),   
]
