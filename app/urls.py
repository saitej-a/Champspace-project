from django.urls import  path
from .views import *
urlpatterns=[
    path('',home,name='home'),
    path('login/',signin,name= 'signin'),
    path('signup/',signup,name='signup'),
    path('logout/',logoutpage, name="logout"),
    path('makepost/',newpost,name='newpost'),
    path('messages/',messages,name='messages'),
    
]