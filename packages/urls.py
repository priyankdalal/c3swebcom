from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("get-package-data",views.getPackage,name="get-package"),
    path("update-package",views.updatePackage,name="update-package"),
    path("price-map",views.priceMap,name="price-map"),
]
