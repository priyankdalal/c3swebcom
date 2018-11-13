from django.urls import path
from . import views
urlpatterns=[
    path("",views.index,name="index"),
    path("home",views.home,name="home"),
    path("recharge",views.recharge,name="recharge"),
    path("pre-process-payment",views.pre_process_payment,name="preProcessPayment"),
    path("logout",views.logout,name="logout"),
]
