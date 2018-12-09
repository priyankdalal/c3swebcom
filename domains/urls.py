from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("add-domain",views.add_domain,name="add-domain"),
]
