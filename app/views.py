from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import CustomUser,Postings
from django.contrib.auth import authenticate,login,logout
from .globalvars import globalvars
globalvar=globalvars()
def home(request):
    if request.user.is_authenticated:
        posts=Postings.objects.all().order_by('-createdTime')
        
        return render(request, 'index.html',{'posts':posts})
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
        
    return render(request,'post.html')
def messages(request):
    return render(request,'messages.html')