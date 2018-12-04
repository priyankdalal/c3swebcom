from django.db import models
from hashlib import sha1
from orders.models import CsOrders
#create your models here
class AdminUsers(models.Model):
    name = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_users'

    def validateAdminUser(user,password):
        if not user.strip() or not password.strip():
            return False
        try:
            admin_user=AdminUsers.objects.get(name=user)
        except AdminUsers.DoesNotExist:
            return False
        print(admin_user)
        en_pass=user+password
        en_pass=sha1(en_pass.encode()).hexdigest()
        if admin_user.password==en_pass:
            return True
        return False

    def create_order(params):
        order=CsOrders.objects.create()
        if "user_id" in params and params['user_id']>0:
            order.user_id=params['user_id']
        else:
            return 0
        if "initiator_id" in params:
            order.initiator_id=params['initiator_id']
        if "initiator_type" in params:
            order.initiator_id=params['initiator_type']
        if "plan" in params:
            order.initiator_id=params['plan']
        if "value" in params:
            order.initiator_id=params['value']
        if "amount" in params:
            order.initiator_id=params['amount']
        return order.id
    def update_order_status(id):
        order=CsOrders.objects.get(pk=id)
        order.status=1
        order.save()
