from django.contrib import admin

# Register your models here.
from .models import AdminUsers
#register admin user in admin site
admin.site.register(AdminUsers)
