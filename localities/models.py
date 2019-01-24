from django.db import models

# Create your models here.
class Localities(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'localities'
