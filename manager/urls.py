from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("pay",views.pay,name="pay"),
    path("do-payment",views.do_payment,name="do_payment"),
    path("logout",views.logout,name="logout"),
]
