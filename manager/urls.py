from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("pay",views.pay,name="pay"),
    path("do-payment",views.do_payment,name="do_payment"),
    path("create-order",views.create_order,name="create_order"),
    path("get-filtered-users",views.get_filter_users,name="get_filtered_data"),
    path("sync-users",views.sync_users,name="sync_users"),
    path("logout",views.logout,name="logout"),
]
