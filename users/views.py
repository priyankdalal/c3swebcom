from django.shortcuts import render,redirect
import logging, os
from .models import CsUsers,C3SPlans

logger=logging.getLogger(__name__)
# Create your views here.
def index(request):
    contaxt={
        "title":"Welcome to C3SWebcom",
    }
    if request.session.get("user"):
        return redirect("home")
    if request.method=="POST":
        if "username" in request.POST and "password" in request.POST:
            request.session["login"]=False
            isUser=CsUsers.validateUser(request.POST['username'],request.POST['password'])
            if isUser==True:
                request.session['user']=request.POST['username']
                return redirect("home")
            else:
                contaxt['error']="invalid user/password"
        else:
            contaxt['error']="invalid request."
    #logger.error(dir(request))
    #logger.error(request.method)
    return render(request,"users/index.html",contaxt)

def home(request):
    contaxt={
        "user":request.session.get('user'),
    }
    return render(request,"users/home.html",contaxt)

def recharge(request):
    if not request.session.get("user"):
        return redirect("/users")
    contaxt={
        "user":request.session.get("user"),
        "plans":C3SPlans.objects.all()
    }
    return render(request,"users/recharge.html",contaxt)

def pre_process_payment(request):
    if not request.session.get("user"):
        return redirect("/users")
    return render(request, "users/preprocess.html")

def logout(request):
    del request.session["user"]
    return redirect('/users')
    
