from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("add",views.add,name="add-locality"),
    path("edit/<int:id>",views.edit,name="edit-locality"),
    path("delete/<int:id>",views.delete,name="delete-locality"),
]
