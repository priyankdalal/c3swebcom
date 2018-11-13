from django.db import models
from hashlib import sha1
#create your models here
class AdminUsers(models.Model):
    name = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'admin_users'
    
    def validateAdminUser(user,password):
        if not user.strip() or not password.strip():
            return False
        try:
            admin_user=AdminUsers.objects.get(name=user)
        except AdminUsers.DoesNotExist:
            return False
        print(admin_user)
        en_pass=user+password
        en_pass=sha1(en_pass.encode()).hexdigest()
        if admin_user.password==en_pass:
            return True
        return False
