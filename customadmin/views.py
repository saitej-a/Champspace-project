from django.shortcuts import render,redirect
from django.contrib.auth import  authenticate, login
from django.contrib.auth.decorators import login_required
from app.models import *
from django.db.models import Count, Q

# Create your views here.
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST['name']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:
                
                login(request,user)
                return redirect( 'dashboard' )
                
            else:
                
                return redirect('admin_login')
        else :
            return render(request,'signin.html')
    
@login_required
def dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users=CustomUser.objects.annotate(post_count=Count('posting'),messages_count=Count('sender')).order_by('-date_joined')
        orderedusers=CustomUser.objects.all()
        messages=Message.objects.all()
        posts=Postings.objects.all()
    
        return render(request,"admin/index2.html",{'users':users,'messages':messages,'posts':posts,'ordered':orderedusers})
    else:
        return redirect('admin_login')
@login_required
def useradmin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users=CustomUser.objects.annotate(posts=Count('posting'),messagescount=Count('sender')).order_by("-date_joined")
        context= {'users':users}
        return render(request, "admin/useradmin.html",context)
    else:
        return redirect('admin_login')
@login_required
def updated(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method=="POST":
            username = request.POST['name']
            
            fname=request.POST['fname']
            lname=request.POST['lname']
            city=request.POST['city']
            state=request.POST['state']
            zipcode=request.POST['zipcode']
            skills=request.POST['skills']
            admin=request.POST.get('staff')
            user=CustomUser.objects.get(id=pk)
            user.username=username
            user.is_superuser= True if admin=='on' else False 
            user.first_name=fname
            user.last_name=lname
            user.skills=skills
            user.city=city
            user.state=state
            user.zip_code=zipcode
            user.save()
            return redirect('updateuser', pk) 
        else:
            user=CustomUser.objects.get(id=pk)
            return render(request,'admin/pages/create-account.html',{'user':user})
    else:
        return redirect('admin_login')

@login_required
def createuser(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method=="POST":
            username = request.POST['name']
            
            fname=request.POST['fname']
            password=request.POST['password']
            lname=request.POST['lname']
            city=request.POST['city']
            state=request.POST['state']
            zipcode=request.POST['zipcode']
            skills=request.POST['skills']
            admin=request.POST.get('staff')
            admin=True if admin=='on' else False 
            user=CustomUser.objects.create_user(username=username,password=password,city=city,first_name=fname,last_name=lname,state=state,zip_code=zipcode,skills=skills,is_superuser=admin)

            
            user.save()
            return redirect('admin_login') 
        else:
            
            return render(request,'admin/pages/createacc.html')
    else:
        return redirect('admin_login')
    
def deleteUser(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        user=CustomUser.objects.get(id=pk)
        user.delete()
        return redirect('userpage')  
    else:
        return redirect('admin_login')
def posts(request):
    if request.user.is_authenticated and request.user.is_superuser:
        print('before')
        postings=Postings.objects.all().order_by('-createdTime')
        print(postings)
        context={'postings':postings}
        return render(request,'admin/posts.html',context)
    else:
        return redirect('admin_login')
def delpost(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        post=Postings.objects.get(id=pk)
        post.delete()
        return redirect('posts')
    else:
        return redirect('admin_login')
def messagesdashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        msg=Message.objects.all().order_by('-createdTime')
        context = {'messages':msg}
        return render(request,'admin/adminmessages.html',context)

    else:
        return redirect('admin_login')
    
def delmessage(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        msg=Message.objects.get(id=pk)
        msg.delete()
        return redirect('messagedash')

    else:
        return redirect('admin_login')