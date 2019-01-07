from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from c3swebcom import conf_vars
from django.db.utils import IntegrityError
from django.http import JsonResponse
from .models import CsOrders
from c3swebcom import conf_vars
from django.utils import timezone
import logging
log=logging.getLogger(__name__)

# Create your views here.
def index(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Orders",
        "user":request.session.get("user"),
        "websocket":"{}:{}".format(conf_vars.WEBSOCKET_SERVER,conf_vars.WEBSOCKET_PORT)
    }
    try:
        if request.session.get("user").role=="admin":
            order_list=CsOrders.objects.all()
        else:
            order_list=CsOrders.objects.filter(initiator_id=request.session.get("user").id)
    except Exception as err:
        log.error("error occured: {}".format(str(err)))
    if order_list:
        if not 'page' in request.GET:
            page=1
        else:
            page=request.GET.get('page')
        try:
            paginator=Paginator(order_list,conf_vars.PAGINATION_ITEMS)
            order_list=paginator.get_page(page)
        except Exception as err:
            log.error("error occured: {}".format(str(err)))
        context['order_list']=order_list

    return render(request,"orders/index.html",context)
def order_status_update(request):
    if not request.session.get("user"):
        return JsonResponse({"error":True,"msg":"unauthorized user"})
    if request.is_ajax():
        if request.method=="POST":
            try:
                order=CsOrders.objects.get(pk=request.POST.get("id"))
                if request.POST.get("key")=="paid":
                    order.paid=request.POST.get("value");
                    order.payment_date=timezone.now()
                elif request.POST.get("key")=="status":
                    order.status=request.POST.get("value");
                order.save()
            except CsOrders.DoesNotExist as err:
                return JsonResponse({"error":True,"msg":"order:{} does not exits".format(request.POST.get("id"))})
            except IntegrityError as err:
                return JsonResponse({"error":True,"msg":err.args[1]})
            except Exception as err:
                return JsonResponse({"error":True,"msg":str(err)})
            return JsonResponse({"error":False,"msg":"order:{} status updated".format(order.id)})
        else:
            return JsonResponse({"error":True,"msg":"bad request method"})
    else:
        return JsonResponse({"error":True,"msg":"bad request"})
