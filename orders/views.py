from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import CsOrders
from c3swebcom import conf_vars
import logging
log=logging.getLogger(__name__)

# Create your views here.
def index(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Orders",
    }
    try:
        order_list=CsOrders.objects.all()
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
