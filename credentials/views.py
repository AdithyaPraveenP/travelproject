from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
def login(request):
    if request.method == 'POST':

        username = request.POST["username"]
        password = request.POST["password1"]
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,"invalid credentials")
            return redirect("logged")

    return render(request,'login.html')

def register(request):

    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = request.POST['username']
        email = request.POST["email"]

        # password = request.POST.get('password1')
        password = request.POST["password1"]
        password2 = request.POST["password2"]

        if password == password2:
            if User.objects.filter(username=user).exists():
                messages.info(request, "user name taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email taken")
                return redirect('register')
            else:
                userdata = User.objects.create_user(username=user, first_name=first_name, last_name=last_name,
                                                    email=email,
                                                    password=password)
                userdata.save()
                print("user created")
                messages.info(request, "user already created")
                return redirect('login')

        else:
            messages.info(request, "password is not matched")
            return redirect('register')


    return render(request,'register.html')

def logout(request):
    auth.logout(request)
    return render(request,'index.html')