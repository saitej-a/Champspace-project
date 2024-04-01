from django.urls import  path
from .views import *
urlpatterns=[
    path('',home,name='home'),
    path('login/',signin,name= 'signin'),
    path('signup/',signup,name='signup'),
    path('logout/',logoutpage, name="logout"),
    path('makepost/',newpost,name='newpost'),
    path('messages/',messages,name='messages'),
    path('messages/<str:pk>/',get_messages,name= "get_messages"),
    path('getmessage/<str:pk>/',get_message,name= "get_message"),
    path('send/',sendMessage,name ='send'),
    path('sendRequest/<str:pk>/',sendrequestPost,name='sendrequest'),
    path('getpostmessage/<str:pk>/',getpost_message,name='getpost_message'),
    path('ownposts/',ownposts,name='ownposts'),
    path('delete/<str:pk>/',deletepost,name='deletepost'),
    path('userprofile/<str:pk>/',viewProfile,name='viewProfile'),
    path('edituserprofile/',editProfile,name='editProfile')
    
]