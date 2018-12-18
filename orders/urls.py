from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("do-order-status-update",views.order_status_update,name="do-order-status-update"),
]
