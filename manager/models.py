from django.db import models
from hashlib import sha1
from orders.models import CsOrders
from adminmanager.models import AdminUsers
#create your models here
class AdminManager():

    def validateAdminUser(user,password):
        if not user.strip() or not password.strip():
            return 1
        try:
            admin_user=AdminUsers.objects.get(name=user)
        except AdminUsers.DoesNotExist:
            return 2
        if admin_user.enabled=="0":
            return 3
        en_pass=user+password
        en_pass=sha1(en_pass.encode()).hexdigest()
        if admin_user.password==en_pass:
            return 0
        return 4

    def create_order(params):
        order=CsOrders.objects.create()
        if "user_id" in params and params['user_id']>0:
            order.user_id=params['user_id']
        else:
            return 0
        if "initiator_id" in params:
            order.initiator_id=params['initiator_id']
        if "initiator_type" in params:
            order.initiator_type=params['initiator_type']
        if "plan" in params:
            order.plan=params['plan']
        if "value" in params:
            order.value=params['value']
        if "amount" in params:
            order.amount=params['amount']
        if "paid" in params:
            order.paid=params['paid']
            order.payment_date=params['payment_date']
        order.save()
        return order.id
    def update_order_status(id):
        order=CsOrders.objects.get(pk=id)
        order.status=1
        order.save()

class SummaryManger():
    def get_orders_summary():
        import datetime
        from orders.models import CsOrders
        from django.db.models import Count
        res={
            "all_time":{
                "total":0,
                "paid":0,
                "completed":0,},
            "monthly":{
                "total":0,
                "paid":0,
                "completed":0,},
            "today":{
                "total":0,
                "paid":0,
                "completed":0,},
        }
        total=CsOrders.objects.aggregate(total_count=Count('id'))
        if total:
            res['all_time']['total']=total['total_count']
        paid=CsOrders.objects.filter(paid="1").aggregate(paid_count=Count('id'))
        if paid:
            res['all_time']['paid']=paid['paid_count']
        completed=CsOrders.objects.filter(status="1").aggregate(completed_count=Count('id'))
        if completed:
            res['all_time']['completed']=completed['completed_count']
        today=datetime.date.today()
        month=today.month
        year=today.year
        total=CsOrders.objects.filter(initiated_at__month=month).filter(initiated_at__year=year).aggregate(total_count=Count('id'))
        print(total)
        if total:
            res['monthly']['total']=total['total_count']
        paid=CsOrders.objects.filter(paid="1").filter(initiated_at__month=month).filter(initiated_at__year=year).aggregate(paid_count=Count('id'))
        if paid:
            res['monthly']['paid']=paid['paid_count']
        completed=CsOrders.objects.filter(status="1").filter(initiated_at__month=month).filter(initiated_at__year=year).aggregate(completed_count=Count('id'))
        if completed:
            res['monthly']['completed']=completed['completed_count']
        total=CsOrders.objects.filter(initiated_at__date=today).aggregate(total_count=Count('id'))
        if total:
            res['today']['total']=total['total_count']
        paid=CsOrders.objects.filter(paid="1").filter(initiated_at__date=today).aggregate(paid_count=Count('id'))
        if paid:
            res['today']['paid']=paid['paid_count']
        completed=CsOrders.objects.filter(status="1").filter(initiated_at__date=today).aggregate(completed_count=Count('id'))
        if completed:
            res['today']['completed']=completed['completed_count']
        return res

    def get_chart_summary():
        import datetime
        from orders.models import CsOrders
        from django.db.models import Count
        res={}
        today=datetime.date.today()
        year=today.year
        month_wise = CsOrders.objects.filter(initiated_at__year=year).extra({"order_month":"MONTH(initiated_at)","order_year":"YEAR(initiated_at)"})
        month_wise = month_wise.values("order_month","order_year")
        month_wise = month_wise.annotate(order_count=Count('id'))
        month_chart_data=[]
        for d in month_wise:
            temp = {}
            temp['count'] = d['order_count']
            temp['month'] = "{}".format(d['order_month'])
            month_chart_data.append(temp)
        res['monthwise']=month_chart_data
        today=datetime.date.today()
        month=today.month
        day_wise = CsOrders.objects.filter(initiated_at__month=month).extra({"order_day":"DAY(initiated_at)","order_month":"MONTH(initiated_at)","order_year":"YEAR(initiated_at)"})
        day_wise = day_wise.values("order_day","order_month","order_year")
        day_wise = day_wise.annotate(order_count=Count('id'))
        day_chart_data=[]
        for d in day_wise:
            temp = {}
            temp['count'] = d['order_count']
            temp['day'] = "{}".format(d['order_day'])
            day_chart_data.append(temp)
        res['daywise']=day_chart_data
        print(res)
        return res
