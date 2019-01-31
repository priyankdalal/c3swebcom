from django.db import models
from domains.models import CsDomains
from localities.models import CsLocalities

class CsPackages(models.Model):
    remote_id = models.IntegerField()
    name = models.CharField(max_length=100)
    value = models.FloatField()
    domain = models.ForeignKey(CsDomains, models.PROTECT)

    class Meta:
        managed = False
        db_table = 'cs_packages'
        unique_together = (('remote_id', 'domain'),)

class CsPriceMappings(models.Model):
    package = models.ForeignKey(CsPackages, models.DO_NOTHING, db_column='package')
    locality = models.ForeignKey(CsLocalities, models.DO_NOTHING, db_column='locality')
    price = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cs_price_mappings'
