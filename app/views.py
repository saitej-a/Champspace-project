from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import CustomUser,Postings,Message,Chatbox,Appliedfor
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from .globalvars import globalvars
from django.http import JsonResponse,HttpResponse
from django.contrib import messages as msg
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
        posts=Postings.objects.all().order_by('-createdTime')
        return render(request,'admin/landingpage.html',{'posts':posts})

def signin(request):
    

    print(globalvar['status'])
    if  request.method == "POST":
        username = request.POST['name']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print('if')
            globalvar['status']=""
            login(request,user)
                
            return redirect('/')
        else:
            globalvar['status']=""
            print('else')
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
        posttype=request.POST['typeofpost']
        website=request.POST['website']
        location=request.POST['location']
        companyname=request.POST['company_name']
        post=Postings.objects.create(title=title,description=content,duration=deadline,skills=skills,investment_needed=invest,creator=request.user,typeofpost=posttype,location=location,company_name=companyname,website=website)
        post.save()
        return redirect('home')
        
    return render(request,'admin/postcreation.html')
def messages(request):
    if request.user.is_authenticated:
        chat_people=Chatbox.objects.filter(receiver=request.user) | Chatbox.objects.filter(sender=request.user)
        unique_people=[]
        for i in chat_people:
            if  not i in unique_people:
                unique_people.append(i)
        return render(request,'messages.html',{'chat_people':unique_people})
    else:
        return redirect('signin')
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
    if request.user.is_authenticated:

        post=Postings.objects.get(id=pk)
        appliedfor=Appliedfor.objects.filter(post=post)
        if not appliedfor:
            appliedfor=Appliedfor.objects.create(post=post)
            appliedfor.applicants.add(request.user)
            appliedfor.applied=True
            appliedfor.save()
            
            
            return redirect('home')
        else:
            try:
                appliedfor=appliedfor.objects.get(post=post)
                appliedfor.applicants.add(request.user)
                
                appliedfor.applied=True
                appliedfor.save()
                
                
                return redirect('home')
            except Exception:
                print('exception')
                appliedfor.applied=True
                
                return redirect('home')
    else:
        return redirect('signin')
        
        
        
def sendrequest(request,pk):
    
    if request.user.is_authenticated:
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
    else:
        return redirect('signin')
    
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

    
    skills=profile.skills
    skills_range=profile.skills_range.split(',')
    skills=skills.split(',')
    skills=list(zip(skills,skills_range))
    print(skills)
    links=profile.websitelinks.split(',')
    return render(request,'userprofile.html',{'profile':profile,'skills':skills,'ownweb':links[0],'second':links[1],'third':links[2],'forth':links[3],'fifth':links[4]})
def editProfile(request):
    if request.method== "POST":
        
        print(request.POST)
        user=CustomUser.objects.get(id=request.user.id)
        user.city=request.POST['city']
        user.last_name=request.POST['lname']
        user.websitelinks=','.join(request.POST.getlist('websites'))
        user.first_name=request.POST['fname']
        user.username=request.POST['username']
        user.experience=request.POST['experience']
        user.state=request.POST['state']
        user.zip_code=request.POST['zipcode']
        user.skills_range=','.join(request.POST.getlist('skillsrange'))
        user.skills=','.join(request.POST.getlist('skillslist'))
        user.role=request.POST.get('role')
        user.save()
        return redirect('editProfile')
    skills=request.user.skills
    skills_range=request.user.skills_range.split(',')
    skills=skills.split(',')
    skills=list(zip(skills,skills_range))
    print(skills)
    links=request.user.websitelinks.split(',')
    
    
    return render(request,'edituserprofile.html',{'skills':skills,'ownweb':links[0],'second':links[1],'third':links[2],'forth':links[3],'fifth':links[4]})
def viewpostdetails(request,pk):
    if request.user.is_authenticated:

        post=Postings.objects.get(id=pk)
        skills=post.skills.split(',')
        apply=Appliedfor.objects.filter(post=post,applicants=request.user)#applied=True
    else:
        post=Postings.objects.get(id=pk)
        skills=post.skills.split(',')
        apply=False
    return render(request,'admin/fullpage.html',{'post':post,'skills':skills,"apply":apply})
def search(request):
    if request.method=='GET':

        to=''
        q=request.GET['searchtag'] if request.GET['searchtag'] != None else ''
        if request.GET['dropdown'] == 'User':
            to='Users'
            searched=CustomUser.objects.filter(Q(username__icontains=q)|Q(first_name__icontains=q)|Q(last_name__icontains=q)|Q(city__icontains=q)|Q(state__icontains=q)|Q(zip_code__icontains=q)|Q(skills__icontains=q))
        else:
            to="Posts"
            searched=Postings.objects.filter(Q(title__icontains=q)| Q(typeofpost__icontains=q)|Q(location__icontains=q)|Q(company_name__icontains=q)|Q(skills__icontains=q))
        
        
        
    return render(request,'admin/search.html',{'searched':searched,'to':to})
def notloginsearch(request):
    if request.method=='GET':

        to=''
        q=request.GET['searchtag'] if request.GET['searchtag'] != None else ''
        if request.GET['dropdown'] == 'User':
            to='Users'
            searched=CustomUser.objects.filter(Q(username__icontains=q)|Q(first_name__icontains=q)|Q(last_name__icontains=q)|Q(city__icontains=q)|Q(state__icontains=q)|Q(zip_code__icontains=q)|Q(skills__icontains=q))
        else:
            to="Posts"
            searched=Postings.objects.filter(Q(title__icontains=q)| Q(typeofpost__icontains=q)|Q(location__icontains=q)|Q(company_name__icontains=q)|Q(skills__icontains=q))
        
    return render(request,'admin/searchednotlogin.html',{'searched':searched,'to':to})