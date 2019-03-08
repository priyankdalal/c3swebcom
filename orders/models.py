from django.db import models
from users.models import CsUsers
from adminmanager.models import AdminUsers

# Create your models here.
class CsOrders(models.Model):
    initiatorType=(("admin","admin"),("user","user"))
    paidTypes=(("Completed","1"),("Pending","0"))
    user = models.ForeignKey(CsUsers, models.PROTECT)
    initiator = models.ForeignKey(AdminUsers, models.PROTECT)
    initiator_type = models.CharField(max_length=5,choices=initiatorType,default="admin")
    plan = models.CharField(max_length=100, blank=True, null=True)
    value = models.FloatField(blank=True, null=True, default="0.00")
    amount = models.FloatField(blank=True, null=True, default="0.00")
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now=True)
    paid = models.CharField(max_length=1, choices=paidTypes, default="0")
    payment_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, default="0")
    response = models.CharField(max_length=100, default="")

    class Meta:
        managed = False
        db_table = 'cs_orders'
        #ordering = ('-initiated_at',)
