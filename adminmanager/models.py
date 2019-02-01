from django.db import models

# Create your models here.
class AdminUsers(models.Model):
    name = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)
    password_string = models.CharField(max_length=100,default="1111")
    role = models.CharField(max_length=8, blank=False, choices=(("admin","Admin"),("operator","Operator")))
    enabled = models.CharField(default="1", max_length=1, blank=True, null=True, choices=(("1","Enabled"),("0","Disabled")))

    class Meta:
        managed = False
        db_table = 'admin_users'
