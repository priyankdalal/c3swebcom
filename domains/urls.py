from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("add-domain",views.add_domain,name="add-domain"),
    path("get-domain",views.get_domain,name="get-domain"),
    path("save-domain",views.save_domain,name="save-domain"),
    path("delete-domain",views.delete_domain,name="delete-domain"),
]
