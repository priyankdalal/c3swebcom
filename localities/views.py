from django.shortcuts import render,redirect

from .forms import addForm
from .models import Localities

# Create your views here.
def index(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3Swebcom - Localities",
        "user":request.session.get("user"),
        "localities":Localities.objects.all(),
    }
    return render(request,"localities/index.html",context)

def add(request):
    context={
        "title":"C3Swebcom - Localities : Add",
        "user":request.session.get("user"),
        "form":addForm()
    }
    return render(request,"localities/add.html",context)
    pass

def edit(request):
    pass

def delete(request):
    pass
