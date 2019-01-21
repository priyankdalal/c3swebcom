from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from c3swebcom import conf_vars
from django.db.utils import IntegrityError
from django.http import JsonResponse,HttpResponse
from .models import CsOrders
from .forms import SearchForm
from c3swebcom import conf_vars
from django.utils import timezone
import datetime
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
def search(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Orders/search",
        "user":request.session.get("user"),
        "request":request,
        "websocket":"{}:{}".format(conf_vars.WEBSOCKET_SERVER,conf_vars.WEBSOCKET_PORT)
    }  
    if request.method=="GET":
        form=SearchForm(request.GET)
        try:
            if request.session.get("user").role=="admin":
                order_list=CsOrders.objects.filter()
            else:
                order_list=CsOrders.objects.filter(initiator_id=request.session.get("user").id)
            if form.is_valid():
                if form.cleaned_data['name']:
                    order_list=order_list.filter(user__name__icontains=form.cleaned_data['name'])
                if form.cleaned_data['address']:
                    order_list=order_list.filter(user__address__icontains=form.cleaned_data['address'])
                if form.cleaned_data['payment_date']:
                    order_list=order_list.filter(payment_date__contains=datetime.datetime.strptime(form.cleaned_data['payment_date'],'%Y-%m-%d').date());
                if form.cleaned_data['start_date']:
                    order_list=order_list.filter(initiated_at__gte=form.cleaned_data['start_date'])
                if form.cleaned_data['end_date']:
                    order_list=order_list.filter(initiated_at__lte=form.cleaned_data['end_date'])
                if form.cleaned_data['order_by']:
                    order_list=order_list.filter(initiator_id=form.cleaned_data['order_by'])                 
                if form.cleaned_data['is_paid']:
                    order_list=order_list.filter(paid=form.cleaned_data['is_paid'])
                if form.cleaned_data['status']:
                    order_list=order_list.filter(status=form.cleaned_data['status'])
                context['valid']="valid : {}".format(form.cleaned_data['is_paid'])
        except Exception as err:
            log.error("error occured: {}".format(str(err))) 
    else:
        form=SearchForm()
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
    context['form']=form
    return render(request,"orders/search.html",context)
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

def get_pdf(request):
    from .render import Render    
    orders=CsOrders.objects.all()
    today=timezone.now()
    params={
        'today':today,
        'orders':orders,
        'request':request
        }
    return render(request,'orders/pdf.html',params)
    #return Render.render("orders/pdf.html",params)
    
def get_csv(request):
    import csv
    from django.utils.encoding import smart_str
    form=SearchForm(request.GET)
    try:
        if request.session.get("user").role=="admin":
            order_list=CsOrders.objects.filter()
        else:
            order_list=CsOrders.objects.filter(initiator_id=request.session.get("user").id)
        if form.is_valid():
            if form.cleaned_data['name']:
                order_list=order_list.filter(user__name__icontains=form.cleaned_data['name'])
            if form.cleaned_data['address']:
                order_list=order_list.filter(user__address__icontains=form.cleaned_data['address'])
            if form.cleaned_data['payment_date']:
                order_list=order_list.filter(payment_date__contains=datetime.datetime.strptime(form.cleaned_data['payment_date'],'%Y-%m-%d').date());
            if form.cleaned_data['start_date']:
                order_list=order_list.filter(initiated_at__gte=form.cleaned_data['start_date'])
            if form.cleaned_data['end_date']:
                order_list=order_list.filter(initiated_at__lte=form.cleaned_data['end_date'])
            if form.cleaned_data['order_by']:
                order_list=order_list.filter(initiator_id=form.cleaned_data['order_by'])                 
            if form.cleaned_data['is_paid']:
                order_list=order_list.filter(paid=form.cleaned_data['is_paid'])
            if form.cleaned_data['status']:
                order_list=order_list.filter(status=form.cleaned_data['status'])
            context['valid']="valid : {}".format(form.cleaned_data['is_paid'])
    except Exception as err:
        log.error("error occured: {}".format(str(err)))
    today=timezone.now()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders-{}.csv'.format(today)
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        "Orders Report - {}".format(today),
        ])
    writer.writerow([
        smart_str(u"S.no"),
        smart_str(u"Name"),
        smart_str(u"Address"),
        smart_str(u"Completed By"),
        smart_str(u"Started At"),
        smart_str(u"Completed At"),
        smart_str(u"Payment Date"),
        smart_str(u"Payment Status"),
        smart_str(u"Recharge Status"),
    ])
    count=1
    for order in order_list:
        row=[]
        row.append(count)
        if not order.user:
            row.append("")
            row.append("")
        else:
            row.append(order.user.name)
            row.append(order.user.address)  
        if order.initiator_type=="admin":
            row.append(order.initiator.name)
        else:
            row.append("self")
        row.append(order.initiated_at)
        row.append(order.completed_at)
        row.append(order.payment_date)
        if order.paid == "1":
            row.append("Completed")
        else:
            row.append("Pending")
        if order.status == "1":
            row.append("Completed")
        else:
            row.append("Pending")  
        count+=1
        writer.writerow(row)
    return response
