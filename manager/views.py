from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse
from django.utils import timezone
from .forms import UserSearch, LoginForm
from c3swebcom import conf_vars
from adminmanager.models import AdminUsers
from .models import AdminManager
from users.models import CsUsers,IpTable
from domains.models import CsDomains
import logging
import subprocess,os
log=logging.getLogger(__name__)
import json
# Create your views here.
def index(request):
    context={
        "title":"C3SWebcom - Login",
    }
    if request.session.get("user"):
        return redirect("dashboard")
    if request.method=="POST":
        loginform=LoginForm(request.POST)
        if loginform.is_valid():
            status=AdminManager.validateAdminUser(loginform.cleaned_data['name'],loginform.cleaned_data['password'])
            if status==0:
                admin_user=AdminUsers.objects.get(name=loginform.cleaned_data['name'])
                request.session['user']=admin_user
                return redirect("dashboard")
            elif status==1:
                request.session["flash"]={"msg":"No user/password given.","type":"danger"}
            elif status==2:
                request.session["flash"]={"msg":"This user doesnot exists.","type":"danger"}
            elif status==3:
                request.session["flash"]={"msg":"User is currently disabled, Please contact admin.","type":"danger"}
            else:
                request.session["flash"]={"msg":"Internal error, Please contact administrator.","type":"danger"}
    loginform=LoginForm()
    context['form']=loginform
    return render(request,"manager/index.html",context)

def dashboard(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Dashboard",
        "page":"dashboard",
        "domains":CsDomains.objects.all(),
    }
    return render(request,"manager/dashboard.html",context)
def pay(request):
    if not request.session.get("user"):
        return redirect("/manager")
    user_list=CsUsers.objects.filter()
    if request.method=="GET":
        form=UserSearch(request.GET)
        try:
            if form.is_valid():
                if form.cleaned_data['name']:
                    user_list=user_list.filter(name__icontains=form.cleaned_data['name'])
                if form.cleaned_data['address']:
                    user_list=user_list.filter(address__icontains=form.cleaned_data['address'])
                if form.cleaned_data['expiry']:
                    user_list=user_list.filter(expiry_date=form.cleaned_data['expiry'])
                if form.cleaned_data['pacakge']:
                    user_list=user_list.filter(pacakge__icontains=form.cleaned_data['pacakge'])
                if form.cleaned_data['phone']:
                    user_list=user_list.filter(phone__icontains=form.cleaned_data['phone'])
                if form.cleaned_data['mobile']:
                    user_list=user_list.filter(mobile__icontains=form.cleaned_data['mobile'])
                if form.cleaned_data['domain']:
                    user_list=user_list.filter(domain__icontains=form.cleaned_data['domain'])
                if form.cleaned_data['ip']:
                    ips_ids=IpTable.objects.filter(ip__icontains=form.cleaned_data['ip']).values_list("user_id",flat=True)
                    ip_users=[(row) for row in ips_ids]
                    user_list=user_list.filter(id__in=ip_users)
            log.debug(user_list.query)
        except Exception as err:
            log.error("error occured: {}".format(str(err)))
        pass
    else:
        form=UserSearch()
    page=1
    if not "page" in request.GET:
        page=1
    else:
        page=request.GET.get("page")
    try:
        paginator=Paginator(list(user_list),conf_vars.PAGINATION_ITEMS)
        user_list=paginator.get_page(page)
    except Exception as err:
        log.debug(err)
    context={
        "title":"C3SWebcom - Pay",
        "page":"pay",
        "user_list":user_list,
        "form":form,
    }
    return render(request,"manager/pay.html",context)
def do_payment(request):
    if request.is_ajax():
        if request.method=="POST":
            if "user_id" in request.POST and request.POST['user_id'].strip():
                user=request.POST['user_id']
                log.debug("payment request for {}".format(user))
                user_data=CsUsers.objects.get(pk=request.POST.get("user_id"))
                if not user_data:
                    return JsonResponse({"error":True,"msg":"This user doesnot exists. Stopping"})
                ccid=user_data.ccid
                domain=user_data.domain
                log.info("ccid :{} and domain: {}".format(ccid,domain))
                order_params={
                    "user_id":user_data.id,
                    "initiator_id":1,
                    "plan":user_data.package,
                    "value":150,
                }
                order_id=AdminManager.create_order(order_params)
                if (not order_id) or order_id<1:
                    log.error("failed to create order, user id : {}".format(user))
                    return JsonResponse({"error":True,"msg":"Failed to create order. Stopping"})
                log.info("order id : {}".format(order_id))
                try:
                    process=subprocess.run(["python3",conf_vars.IPACCT_HANDLER,"-d{}".format(domain),"-umitul","-p{}".format(conf_vars.AUTH[domain]["mitul"]), "-odo_payment","-c{}".format(ccid)])
                except subprocess.CalledProcessError as err:
                    log.error("failed to call payment module")
                    return JsonResponse({"error":True,"msg":err})
                if process.returncode>0:
                    log.error("failed to do payment. error code: {}".format(process.returncode))
                    return JsonResponse({"error":True,"msg":"failed to complete payment","payload":process.returncode})
                AdminManager.update_order_status(order_id)
                log.info("payment completed for {}".format(user))
                return JsonResponse({"error":False,"msg":"done","payload":process.returncode})
            else:
                return JsonResponse({"error":True,"msg":"parameters required."})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    return JsonResponse({"error":True,"msg":"bad request"})
def create_order(request):
    if request.is_ajax():
        if request.method=="POST":
            if "user_id" in request.POST and request.POST['user_id'].strip():
                user=request.POST['user_id']
                log.debug("order request for {}".format(user))
                user_data=CsUsers.objects.get(pk=request.POST.get("user_id"))
                if not user_data:
                    return JsonResponse({"error":True,"msg":"This user doesnot exists. Stopping"})
                ccid=user_data.ccid
                domain=user_data.domain
                log.info("ccid :{} and domain: {}".format(ccid,domain))
                order_params={
                    "user_id":user_data.id,
                    "initiator_id":request.session.get("user").id,
                    "plan":user_data.package,
                    "value":150,
                }
                if request.POST.get("paid"):
                    order_params['paid']=request.POST.get("paid")
                    order_params['payment_date']=timezone.now()
                else:
                    order_params['paid']='0'
                order_id=AdminManager.create_order(order_params)
                if (not order_id) or order_id<1:
                    log.error("failed to create order, user id : {}".format(user))
                    return JsonResponse({"error":True,"msg":"Failed to create order. Stopping"})
                log.info("order id : {}".format(order_id))

                #AdminManager.update_order_status(order_id)
                return JsonResponse({"error":False,"msg":"done","payload":order_id})
            else:
                return JsonResponse({"error":True,"msg":"parameters required."})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    return JsonResponse({"error":True,"msg":"bad request"})
#NOTE this is obsolate for now
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
def sync_users(request):
    if request.is_ajax():
        if request.method=="POST":
            log.info("sending user sync command")
            domain="epay.globalnoc.in"
            try:
                process=subprocess.Popen(["python3",conf_vars.IPACCT_HANDLER,"-d{}".format(domain),"-umitul","-p{}".format(conf_vars.AUTH[domain]["mitul"]), "-osync_users"])
            except subprocess.CalledProcessError as err:
                log.error("failed to call user_sync module")
                return JsonResponse({"error":True,"msg":err})
            return JsonResponse({"error":False,"msg":"Request summitted."})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    else:
        return JsonResponse({"error":True,"msg":"bad request"})

def logout(request):
    if request.session.get("user"):
        del request.session['user']
    return redirect("/manager")
