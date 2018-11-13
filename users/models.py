from django.db import models
from hashlib import sha1
import logging

logger=logging.getLogger(__name__)

# Create your models here.
class CsUsers(models.Model):
    ccid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    ip_count = models.IntegerField(blank=True, null=True)
    expiry_date = models.CharField(max_length=10, blank=True, null=True)
    package = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cs_users'
    def validateUser(user,password):
        if not user.strip() or not password.strip():
            return False   
        try:
            user_details=CsUsers.objects.get(ccid=user)
        except CsUsers.DoesNotExist:
            return False
        en_pass=user+password
        en_pass=sha1(en_pass.encode()).hexdigest()
        if user_details.password==en_pass:
            return True
        return False

class C3SPlans(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'c3s_plans'

