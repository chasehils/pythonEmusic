from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    print("i am running sign up")
    if (request.method =="POST"):
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password != confirm_password:
            return HttpResponse('password is incorrect')
            # return render(request, 'auth/signup.html')
        
        try:
            if User.objects.get(username=email):
                return HttpResponse('email is already in use')
                # return render(request, 'auth/signup.html')

        except Exception as identifier:
            pass

        user = User.objects.create_user(email, email, password)
        user.save()
    return render(request, "signup.html")

def handlelogin(request):
    
    return render(request, "login.html")

def handlelogout(request):
    
    return redirect('/auth/login')
