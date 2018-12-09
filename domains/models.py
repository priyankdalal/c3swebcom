from django.db import models

# Create your models here.
class CsDomains(models.Model):
    status_types=(("up","up"),("down","down"))
    name = models.CharField(max_length=100)
    url = models.CharField(unique=True,max_length=100, blank=False, null=False)
    auth_user = models.CharField(max_length=100, blank=True, null=True)
    auth_pass = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=4, choices=status_types, default="up")

    class Meta:
        managed = False
        db_table = 'cs_domains'
