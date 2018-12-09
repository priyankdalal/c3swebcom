from django.shortcuts import render
from django.http import JsonResponse
from .models import CsDomains
import logging
log=logging.getLogger(__name__)

# Create your views here.
def index(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Domains",
        "user":request.session.get("user"),
        "domains":CsDomains.objects.all()
    }
    return render(request,"domains/index.html",context)
def add_domain(request):
    if not request.session.get("user"):
        return JsonResponse({"error":True,"msg":"unauthorized user"})
    #user_list=CsUsers.objects.all()
    if request.is_ajax():
        if request.method=="POST":
            try:
                old=CsDomains.objects.get(url=request.POST.get("url"))
            except Exception as err:
                print("there")
                err=str(err)
                if err.find("does not exist")>-1:
                    domain=CsDomains.objects.create()
                    domain.name=request.POST.get("nm")
                    domain.url=request.POST.get("url")
                    domain.auth_user=request.POST.get("un")
                    domain.auth_pass=request.POST.get("up")
                    domain.save()
                    if domain.id>0:
                        return JsonResponse({"error":False,"msg":"domain added"})
                    else:
                        return JsonResponse({"error":True,"msg":"Failed to add domain"})
                else:
                    return JsonResponse({"error":True,"msg":err})
            else:
                return JsonResponse({"error":True,"msg":"domain exits"})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    else:
        return JsonResponse({"error":True,"msg":"bad request"})
