from django.db import models

# Create your models here.
class AdminUsers(models.Model):
    name = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_users'
