from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from c3swebcom import conf_vars
from .models import CsPackages

# Create your views here.
def index(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Packages",
        "page":"packages",
        "package_list":CsPackages.objects.all()
    }
    return render(request,"packages/index.html",context)
def getPackage(request):
    if request.is_ajax():
        if request.method=="POST":
            if "id" in request.POST:
                try:
                    package_id=int(request.POST.get("id"))
                except ValueError as err:
                    return JsonResponse({"error":True,"msg":"Invalid package."})
                try:
                    package_data=CsPackages.objects.get(pk=package_id)
                    package={
                        "id":package_data.id,
                        "name":package_data.name,
                        "domain":package_data.domain.name,
                        "value":package_data.value,
                        "remote_id":package_data.remote_id,
                    }
                except CsPackages.DoesNotExist as err:
                    return JsonResponse({"error":True,"msg":"This package doesnot exists."})
                return JsonResponse({"error":False,"msg":"Success","payload":package})
            else:
                return JsonResponse({"error":True,"msg":"Invalid package."})
        else:
            return JsonResponse({"error":True,"msg":"bad request method."})
    else:
        return JsonResponse({"error":True,"msg":"Bad request."})

def updatePackage(request):
    if request.is_ajax():
        if request.method=="POST":
            if "id" in request.POST:
                try:
                    package_id=int(request.POST.get("id"))
                except ValueError as err:
                    return JsonResponse({"error":True,"msg":"Invalid package."})
                try:
                    package=CsPackages.objects.get(pk=package_id)
                    if "value" in request.POST:
                        package.value=request.POST.get("value")
                    package.save()
                except CsPackages.DoesNotExist as err:
                    return JsonResponse({"error":True,"msg":"This package doesnot exists."})
                return JsonResponse({"error":False,"msg":"Package updated successfully."})
            else:
                return JsonResponse({"error":True,"msg":"No package to update."})
        else:
            return JsonResponse({"error":True,"msg":"Bad request method"})
    else:
     return JsonResponse({"error":True,"msg":"Bad request"})
