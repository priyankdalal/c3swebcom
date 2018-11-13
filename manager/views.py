from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import AdminUsers
from users.models import CsUsers

# Create your views here.
def index(request):
    context={
        "title":"C3SWebcom - Login"
    }
    if request.session.get("user"):
        return redirect("dashboard")
    if request.method=="POST":
        if "username" in request.POST and "password" in request.POST:
            isUser=AdminUsers.validateAdminUser(request.POST['username'],request.POST['password'])
            if isUser==True:
                request.session['user']=request.POST['username']
                return redirect("dashboard")
            else:
                context["error"]="invalid user/password."
        else:
            context['error']="invalid request."
    return render(request,"manager/index.html",context)

def dashboard(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Dashboard",
        "user":request.session.get("user")
    }
    return render(request,"manager/dashboard.html",context)
def pay(request):
    if not request.session.get("user"):
        return redirect("/manager")
    user_list=CsUsers.objects.all()
    print(user_list[1])
    context={
        "title":"C3SWebcom - Pay",
        "user":request.session.get("user"),
        "user_list":user_list
    }
    return render(request,"manager/pay.html",context)
def logout(request):
    if request.session.get("user"):
        del request.session['user']
    return redirect("/manager")
    
