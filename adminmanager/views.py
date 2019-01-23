from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from hashlib import sha1
from .models import AdminUsers
from . import form
import logging
log=logging.getLogger(__name__)
# Create your views here.
def index(request):
    if not request.session.get("user"):
        return redirect("/manager")
    contaxt={
        "title":"C3SWebcom : Admin Users",
        "user":request.session.get("user"),
        "adminusers":AdminUsers.objects.all(),
    }
    return render(request,"adminusers/index.html",contaxt)

def edit(request,id):
    if not request.session.get("user"):
        return redirect("/manager")
    if not id:
        return redirect('/adminusers')
    context={
        "title":"C3SWebcom : Admin Users - Edit",
        "user":request.session.get("user"),
    }
    adminuser=AdminUsers.objects.get(pk=id)
    edit_form=form.EditForm(model_to_dict(adminuser))
    if request.method=="POST":
        edForm=form.EditForm(request.POST)
        try:
            if edForm.is_valid():
                if edForm.cleaned_data['id'] and edForm.cleaned_data['id'] == str(id):
                    adminuser=AdminUsers.objects.get(pk=id)
                    if edForm.cleaned_data['name']:
                        adminuser.name=edForm.cleaned_data['name']
                    if edForm.cleaned_data['role']:
                        adminuser.role=edForm.cleaned_data['role']
                    if edForm.cleaned_data['password_changed'] and edForm.cleaned_data['password_changed']=="1":
                        adminuser.password_string=edForm.cleaned_data['password_string']
                        newpass=adminuser.name+edForm.cleaned_data['password_string']
                        newpass=sha1(newpass.encode()).hexdigest()
                        adminuser.password=newpass
                    adminuser.save()
                    return redirect("/adminusers")
                else:
                    return redirect("/adminusers")
            else:
                adminuser=AdminUsers.objects.get(pk=id)
                edit_form=form.EditForm(model_to_dict(adminuser))
        except Exception as err:
            log.error("error occured: {}".format(str(err)))
    context['adminuser']=adminuser
    context['form']=edit_form
    return render(request,"adminusers/edit.html",context)
