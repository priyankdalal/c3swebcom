from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse
from django.core import serializers
from django.db.models import Q
from c3swebcom import conf_vars
import functools,operator
from .models import AdminUsers
from users.models import CsUsers
import logging
import subprocess,os
log=logging.getLogger(__name__)
import subprocess, json
# Create your views here.
def index(request):
    log.debug("current directory is: {}".format(os.getcwd()))
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
    #user_list=CsUsers.objects.all()
    user_list=CsUsers.objects.raw("select cs.id,cs.ccid,name,address,expiry_date,package,phone,mobile,domain,group_concat(ip.ip) as `ip` from cs_users cs inner join ip_table ip on cs.id=ip.user_id group by cs.id")
    page=1
    if not "page" in request.GET:
        page=1
    else:
        page=request.GET.get("page")
    try:
        paginator=Paginator(list(user_list),conf_vars.PAGINATION_ITEMS)
        user_list=paginator.get_page(page)
    except Exception as err:
        print(err)
    context={
        "title":"C3SWebcom - Pay",
        "user":request.session.get("user"),
        "user_list":user_list
    }
    return render(request,"manager/pay.html",context)
def do_payment(request):
    if request.is_ajax():
        if request.method=="POST":
            if "user_id" in request.POST and request.POST['user_id'].strip():
                user=request.POST['user_id']
                user_data=CsUsers.objects.get(pk=request.POST.get("user_id"))
                if not user_data:
                    return JsonResponse({"error":True,"msg":"This user doesnot exists. Stopping"})
                ccid=user_data.ccid
                domain=user_data.domain
                order_params={
                    "user_id":user_data.id,
                    "initiator_id":1,
                    "plan":user_data.package,
                    "value":150,
                }
                order_id=AdminUsers.create_order(order_params)
                if (not order_id) or order_id<1:
                    return JsonResponse({"error":True,"msg":"Failed to create order. Stopping"})
                try:
                    process=subprocess.run(["python3",conf_vars.IPACCT_HANDLER,"-d{}".format(domain),"-umitul","-p{}".format(conf_vars.AUTH[domain]["mitul"]), "-odo_payment","-c{}".format(ccid)])
                    '''with open("/tmp/stdoutjs.txt","w") outf:
                        outf.write(process.std)'''
                except subprocess.CalledProcessError as err:
                    return JsonResponse({"error":True,"msg":err})
                if process.returncode>0:
                    return JsonResponse({"error":True,"msg":"failed to complete payment","payload":process.returncode})
                AdminUsers.update_order_status(order_id)
                return JsonResponse({"error":False,"msg":"done","payload":process.returncode})
            else:
                return JsonResponse({"error":True,"msg":"parameters required."})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    return JsonResponse({"error":True,"msg":"bad request"})
def get_filter_users(request):
    if request.is_ajax():
        if request.method=="POST":
            try:
                if not "page" in request.POST:
                    page=1
                else:
                    page=request.POST.get("page")
                user_list=CsUsers.get_filtered_user_list(request.POST)
                if len(user_list)>conf_vars.PAGINATION_ITEMS:
                    paginator=Paginator(user_list,conf_vars.PAGINATION_ITEMS)
                    user_list=paginator.get_page(page)
                    context={
                        "user_list":user_list,
                        "request_user":request.POST,
                        "pagination":True
                    }
                else:
                    context={
                        "user_list":user_list,
                        "request_user":request.POST,
                        "pagination":False,
                    }
                return render(request,"manager/pay_filter.html",context)
            except Exception as err:
                print(err)
            else:
                return JsonResponse({"error":True,"msg":"internal error"})
            #return JsonResponse({"error":False,"msg":"done","payload":usr_dict})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    else:
        return JsonResponse({"error":True,"msg":"bad request"})

def logout(request):
    if request.session.get("user"):
        del request.session['user']
    return redirect("/manager")
