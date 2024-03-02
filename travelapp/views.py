from django.http import HttpResponse


from django.shortcuts import render
from .models import place



# Create your views here.
def index(request):
    obj = place.objects.all()

    return render(request,'index.html',{'result':obj})
def demo(request):
    return render(request,'demo.html')

def about(request):
    return render(request,'about.html')
def call(request):
    name = "india"
    return render(request,'call.html',{'obj':name})
def form(request):
    return render(request,"form.html")
def addition(request):
    x = int(request.GET['num1'])
    y = int(request.GET['num2'])
    operation = request.GET['operation']
    if operation == 'add':
        add = x + y
        return render(request,"result.html",{"addition":add})

    elif operation == 'sub':
        sub = x - y
        return render(request, "result.html", {"substraction":sub})
    elif operation == 'mul':
        mult = x * y
        return render(request, "result.html", {"multiplication":mult})
    elif operation == 'div':
        div = x/y
        return render(request, "result.html", {"division":div})
    else:
        return HttpResponse("Invalid input")


