from django.contrib import admin

# Register your models here.
from .models import CustomUser,Postings,Message,Chatbox,Appliedfor
admin.site.register(CustomUser)
admin.site.register(Postings)
admin.site.register(Message)
admin.site.register(Chatbox)
admin.site.register(Appliedfor)