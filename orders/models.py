from django.db import models
from users.models import CsUsers

# Create your models here.
class CsOrders(models.Model):
    initiatorType=(("admin","admin"),("user","user"))
    user_id = models.IntegerField(blank=True, null=True)#models.ForeignKey(CsUsers, models.PROTECT,db_column='id')
    initiator_id = models.IntegerField(blank=True, null=True)
    initiator_type = models.CharField(max_length=5,choices=initiatorType,default="admin")
    plan = models.CharField(max_length=100, blank=True, null=True)
    value = models.FloatField(blank=True, null=True, default="0.00")
    amount = models.FloatField(blank=True, null=True, default="0.00")
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default="0")
    response = models.CharField(max_length=100, default="")

    class Meta:
        managed = False
        db_table = 'cs_orders'
        ordering = ('initiated_at',)
