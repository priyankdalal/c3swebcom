from django.db import models
from domains.models import CsDomains

class CsPackages(models.Model):
    remote_id = models.IntegerField()
    name = models.CharField(max_length=100)
    value = models.FloatField()
    domain = models.ForeignKey(CsDomains, models.PROTECT)

    class Meta:
        managed = False
        db_table = 'cs_packages'

