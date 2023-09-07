from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator, generate_token

from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def signup(request):
    print("i am running sign up")
    if (request.method =="POST"):
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, 'Passwords do not match')
            return render(request, 'signup.html')
        
        try:
            if User.objects.get(username=email):
                # return HttpResponse('email is already in use')
                messages.info(request, 'Email is taken')
                return render(request, 'signup.html')

        except Exception as identifier:
            pass

        user = User.objects.create_user(email, email, password)
        user.is_active=False
        user.save()
        email_subject="Activate Your Account"
        message=render_to_string('activate.html', {
            'user': user,
            'domain': 'http://127.0.0.1:8000',
            'uid': urlsafe_base64_encode(user.pk.encode()),
            'token':generate_token.make_token(user)
        })

        # email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        # email_message.send()
        messages.succcess(request, f"Activate your Account by clicking the link in your email {message}")
        return redirect('/auth/login')
    return render(request, "signup.html")


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode() 
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user, token):
            user.is_active=True
            user.save()
            messages.info(request, "Account Activated Successfully")
            return redirect('auth/login')
        return render(request, 'auth/activatefail.html')


def handlelogin(request):
    
    return render(request, "login.html")

def handlelogout(request):
    
    return redirect('/auth/login')
