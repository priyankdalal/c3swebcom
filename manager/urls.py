from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("pay",views.pay,name="pay"),
    path("logout",views.logout,name="logout"),
]