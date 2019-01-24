from django.urls import path
from . import views
urlpatterns=[
    path("",views.index,name="index"),
    path("edit/<int:id>",views.edit,name="edit"),
    path("add",views.add,name="add-admin-user")
]
