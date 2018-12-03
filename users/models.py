from django.db import models
from django.db import connection
from c3swebcom.utils import dict_fetch_all
from hashlib import sha1
import logging

logger=logging.getLogger(__name__)

# Create your models here.
class CsUsers(models.Model):
    ccid = models.IntegerField()
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    ip_count = models.IntegerField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    package = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    domain = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cs_users'
        unique_together = (('ccid', 'domain'),)
        ordering = ['-id']
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
    def user_split(self,str1):
        return str1.split(",")
    def get_filtered_user_list(filters):
        with connection.cursor() as cursor:
            where=''
            if ("name" in filters and filters['name'].strip()):
                if where.strip():
                    where+=" and "
                where+="name like '%{}%'".format(filters['name'])
            if ("address" in filters and filters['address'].strip()):
                if where.strip():
                    where+=" and "
                where+="address like '%{}%'".format(filters['address'])
            if ("phone" in filters and filters['phone'].strip()):
                if where.strip():
                    where+=" and "
                where+="phone like '%{}%'".format(filters['phone'])
            if ("mobile" in filters and filters['mobile'].strip()):
                if where.strip():
                    where+=" and "
                where+="mobile like '%{}%'".format(filters['mobile'])
            if ("domain" in filters and filters['domain'].strip()):
                if where.strip():
                    where+=" and "
                where+="domain like '%{}%'".format(filters['domain'])
            if ("ip" in filters and filters['ip'].strip()):
                if where.strip():
                    where+=" and "
                where+="it.ip like '%{}%'".format(filters['ip'])
            try:
                r=cursor.execute("select cs.ccid,cs.name,cs.address,cs.expiry_date,cs.package,cs.phone,cs.mobile,cs.domain,group_concat(it.ip,' ') ip from cs_users cs inner join ip_table it on cs.id=it.user_id where {} group by cs.id".format(where))
                user_list=dict_fetch_all(cursor)
                return user_list
            except Exception as err:
                print(err)
                return false

class C3SPlans(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()

    class Meta:
        managed = False
        db_table = 'c3s_plans'

class IpTable(models.Model):
    user = models.ForeignKey(CsUsers,on_delete=models.CASCADE)
    ip = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ip_table'
    def get_tables():
        return IpTable.objects.all().select_related()
