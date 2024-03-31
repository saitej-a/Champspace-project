from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import CustomUser,Postings,Message,Chatbox,Appliedfor
from django.contrib.auth import authenticate,login,logout
from .globalvars import globalvars
from django.http import JsonResponse,HttpResponse
import json 
globalvar=globalvars()
def home(request):
    if request.user.is_authenticated:
        posts=Postings.objects.all().order_by('-createdTime')
        applied_status=[]
        for i in posts:
            applied = Appliedfor.objects.filter(post=i,applied=True).exists()
            applied_status.append(applied)
        post=zip(posts,applied_status)


        return render(request, 'admin/base123.html',{'posts':post})
    else:
        return render(request,'landingpage.html')

def signin(request):
    

    print(globalvar['status'])
    if  request.method == "POST":
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            globalvar['status']=""
            login(request,user)
                
            return redirect('/')
        else:
            globalvar['status']=""
            return render(request,'signin.html',{'error':'Username or Password is incorrect'})
    return render(request,'signin.html',{"status":globalvar['status']})
def signup(request):
    print(globalvar['status'])
    if request.method == "POST":
        username = request.POST['name']
        password=request.POST['password']
        fname=request.POST['fname']
        lname=request.POST['lname']
        city=request.POST['city']
        state=request.POST['state']
        zipcode=request.POST['zipcode']
        # experience=request.POST['experience']
         # Check if user already exists
        if CustomUser.objects.filter(username=username).exists() :
            context={'message':'Username Already Taken or Try with Another Username'}
            return render(request,"registration.html",context)
        else :
            user=CustomUser.objects.create_user(username=username,first_name=fname,last_name=lname,password=password)
            user.city=city
            user.state=state
            user.zip_code=zipcode
            user.save()
            globalvar['status']="Account Created  Successfully! Please Login"
            return redirect('signin')
    return render(request,"registration.html")
def logoutpage(request):
    logout(request)
    return redirect('home')
def newpost(request):
    if request.method=='POST':
        title=request.POST['projectTitle']
        content=request.POST['projectDescription']
        invest=request.POST['investmentNeeded']
        deadline=request.POST['timeline']
        skills=request.POST['desiredSkills']
        post=Postings.objects.create(title=title,description=content,duration=deadline,skills=skills,investment_needed=invest,creator=request.user)
        post.save()
        return redirect('home')
        
    return render(request,'admin/postcreation.html')
def messages(request):
    chat_people=Chatbox.objects.filter(receiver=request.user) | Chatbox.objects.filter(sender=request.user)
    unique_people=[]
    for i in chat_people:
        if  not i in unique_people:
            unique_people.append(i)
    return render(request,'messages.html',{'chat_people':unique_people})
def get_messages(request,pk):
    
    

    chat_people=Chatbox.objects.filter(receiver=request.user) | Chatbox.objects.filter(sender=request.user)
    unique_people=[]
    for i in chat_people:
        if  not i in unique_people:
            unique_people.append(i)
    
    messages_set=Message.objects.filter(contact=pk).order_by('createdTime')
    
    return render(request,'get_messages.html',{'chat_people':unique_people,'messages_set':messages_set,'pk':pk,})

def get_message(request,pk):
    
    messages = Message.objects.filter(contact=pk).order_by('createdTime')
    messages= list(messages.values())
    
    return JsonResponse({'messages': messages})
def sendMessage(request):
    contact=request.POST.get("chat")
    # receiver=request.POST.get('receiver')
    
    
    message=request.POST.get("body")
    chatbox =Chatbox.objects.get(id=contact)

    if chatbox != None:
        if chatbox.sender == request.user :
            print('if')
            receiver=chatbox.receiver
            
            
        else:
            print('else')
            receiver=chatbox.sender
            
            
            
        print("contact:",contact,"receiver",receiver)
        message=Message.objects.create(sender=request.user,receiver=receiver,message=message,contact=chatbox)
        message.save()
        return HttpResponse("success")
    else:
        chatbox=Chatbox.objects.create(sender=request.user,receiver=receiver)
        chatbox.save()
        message=Message.objects.create(sender=request.user,receiver=receiver,message=message,contact=chatbox)
        message.save()
        return HttpResponse("success")
def sendrequestPost(request,pk):

    post=Postings.objects.get(id=pk)
    appliedfor=Appliedfor.objects.filter(post=post)
    if not appliedfor:
        appliedfor=Appliedfor.objects.create(post=post)
        appliedfor.applicants.add(request.user)
        appliedfor.applied=True
        appliedfor.save()
        print('if')
        
        return redirect('home')
    else:
        try:
            appliedfor=appliedfor.objects.get(post=post)
            appliedfor.applicants.add(request.user)
            appliedfor.save()
            appliedfor.applied=True
            print('try')
            
            return redirect('home')
        except Exception:
            print('exception')
            appliedfor.applied=True
            
            return redirect('home')
        
        
        
def sendrequest(request,pk):
    
    
    post_creator=CustomUser.objects.get(id=pk)
    print('before')
    chatbox=Chatbox.objects.filter(sender=request.user,receiver=post_creator) or Chatbox.objects.filter(sender=post_creator,receiver=request.user)
    unique=[]
    for i in chatbox:
        if  not i in unique:
            unique.append(i)
    print('after')
    print("chatbox",unique)
    if not unique:
        print('if')
        chatbox=Chatbox.objects.create(sender=request.user,receiver=post_creator)
        return redirect('get_messages',pk=chatbox.id)
    else:
        print('else')
        return redirect('getpost_message',pk=chatbox[0].id)
    
def getpost_message(request,pk):
    chat_people=Chatbox.objects.filter(receiver=request.user) | Chatbox.objects.filter(sender=request.user)
    unique_people=[]
    for i in chat_people:
        if  not i in unique_people:
            unique_people.append(i)
    
    messages_set=Message.objects.filter(contact=pk).order_by('createdTime')
    
    
    

    
    return render(request,'get_messages.html',{'chat_people':unique_people,'messages_set':messages_set,'pk':pk})
def ownposts(request):
    post=Postings.objects.filter(creator=request.user).order_by('-createdTime')
    return render(request,'admin/ownpost.html',{'posts':post})
def deletepost(request,pk):
    post=Postings.objects.get(id=pk)
    post.delete()
    return redirect('ownposts')
def viewProfile(request,pk):
    profile=CustomUser.objects.get(id=pk)
    posts = Postings.objects.filter(creator=profile)
    profile_skills=profile.skills.split(',')
    return render(request,'userprofile.html',{'profile':profile,'posts':posts,'skills':profile_skills})