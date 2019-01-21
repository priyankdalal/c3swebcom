from django.urls import path
from . import views

urlpatterns=[
    path("",views.search,name="index"),
    #path("search",views.search, name="search"),
    path("do-order-status-update",views.order_status_update,name="do-order-status-update"),
    path("get-pdf",views.get_pdf,name="get-pdf"),
    path("get-csv",views.get_csv,name="get-csv"),
]
