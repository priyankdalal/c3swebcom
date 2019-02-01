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
