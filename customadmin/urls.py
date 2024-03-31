from django.urls import  path
from .views import *
urlpatterns=[
    
    path('',admin_login,name='admin_login'),
    path('dashboard/',dashboard,name="dashboard"),
    path('users/',useradmin,name='userpage'),
    path('users/<str:pk>/',updated,name='updateuser'),
    path('users/delete/<str:pk>/',deleteUser,name="deleteuser"),
    path('posts/',posts,name='posts'),
    path('posts/<str:pk>/',delpost,name='delpost')
]