from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core import serializers
from c3swebcom import conf_vars
from django.db.utils import IntegrityError
from .models import CsDomains
import logging
log=logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Create your views here.
def index(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Domains",
        "user":request.session.get("user"),
        "domains":CsDomains.objects.all(),
        "websocket":"{}:{}".format(conf_vars.WEBSOCKET_SERVER,conf_vars.WEBSOCKET_PORT)
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
            except CsDomains.DoesNotExist as err:
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
                return JsonResponse({"error":True,"msg":"domain exits"})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    else:
        return JsonResponse({"error":True,"msg":"bad request"})
def get_domain(request):
    if not request.session.get("user"):
        return JsonResponse({"error":True,"msg":"unauthorized user"})
    #user_list=CsUsers.objects.all()
    if request.is_ajax():
        if request.method=="POST":
            try:
                domain=CsDomains.objects.get(pk=request.POST.get("id"))
            except Exception as err:
                return JsonResponse({"error":True,"msg":err})
            return JsonResponse({"error":False,"payload":serializers.serialize("json",[domain,])})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    else:
        return JsonResponse({"error":True,"msg":"bad request"})

def save_domain(request):
    if not request.session.get("user"):
        return JsonResponse({"error":True,"msg":"unauthorized user"})
    if request.is_ajax():
        if request.method=="POST":
            try:
                has_change=False
                domain=CsDomains.objects.get(pk=request.POST.get("id"))
                if "nm" in request.POST and request.POST.get("nm"):
                    domain.name=request.POST.get("nm")
                    has_change=True
                if "url" in request.POST and request.POST.get("url"):
                    domain.url=request.POST.get("url")
                    has_change=True
                if "un" in request.POST and request.POST.get("un"):
                    domain.auth_user=request.POST.get("un")
                    has_change=True
                if "up" in request.POST and request.POST.get("up"):
                    domain.auth_pass=request.POST.get("up")
                    print(request.POST.get("up"))
                    has_change=True
                if "st" in request.POST and request.POST.get("st"):
                    domain.status=request.POST.get("st")
                    has_change=True
                if not has_change:
                    return JsonResponse({"error":True,"msg":"nothing to update"})
                domain.save()
            except CsDomains.DoesNotExist as err:
                return JsonResponse({"error":True,"msg":"{} does not exits".format(request.POST.get("url"))})
            except IntegrityError as err:
                return JsonResponse({"error":True,"msg":err.args[1]})
            except Exception as err:
                return JsonResponse({"error":True,"msg":str(err)})
            return JsonResponse({"error":False,"msg":"{} saved".format(domain.name)})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    else:
        return JsonResponse({"error":True,"msg":"bad request"})

def delete_domain(request):
    if not request.session.get("user"):
        return JsonResponse({"error":True,"msg":"unauthorized user"})
    #user_list=CsUsers.objects.all()
    if request.is_ajax():
        if request.method=="POST":
            try:
                domain=CsDomains.objects.get(pk=request.POST.get("id"))
                domain.delete()
            except CsDomains.DoesNotExist as err:
                    return JsonResponse({"error":True,"msg":"Domain does not exits"})
            except Exception as err:
                return JsonResponse({"error":True,"msg":err})
            return JsonResponse({"error":False,"msg":"{} deleted.".format(domain.url)})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    else:
        return JsonResponse({"error":True,"msg":"bad request"})
