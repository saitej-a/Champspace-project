from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q,F
# Create your models here.
class CustomUser(AbstractUser):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    skills = models.CharField(max_length=256, blank=True)  # Comma separated list of skills
    role = models.CharField(max_length=32, default='Fresher') 
    
    # You can also specify a custom manager for your user model, if needed
    # objects = CustomUserManager()
class Postings(models.Model):
    
    title = models.CharField(max_length=80)
    description = models.TextField()
    investment_needed=models.TextField()
    duration = models.TextField()
    skills=models.TextField()
    createdTime=models.DateTimeField(auto_now_add=True)
    creator=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="posting")

    def  __str__(self):
        return self.title
class Message(models.Model):
    sender = models.ForeignKey(CustomUser,related_name='sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser,related_name="receiver",on_delete=models.CASCADE)
    message = models.TextField()
    
    createdTime=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['sender','receiver'], name='unique_message'),models.CheckConstraint(check=~Q(sender=F('receiver')), name='sender_receiver_check')
        ]
        