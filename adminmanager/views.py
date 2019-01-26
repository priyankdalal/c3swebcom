from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from c3swebcom.conf_vars import VERSION
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
        "page":"adminusers",
        "adminusers":AdminUsers.objects.all(),
    }
    return render(request,"adminusers/index.html",contaxt)

def add(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom : Admin Users - Add",
        "page":"adminusers",
    }
    add_form=form.AddForm()
    if request.method=="POST":
        add_form=form.AddForm(request.POST)
        try:
            if add_form.is_valid():
                if add_form.cleaned_data['name']:
                    adminuser=AdminUsers(name=add_form.cleaned_data['name'])
                if add_form.cleaned_data['role']:
                    adminuser.role=add_form.cleaned_data['role']
                if add_form.cleaned_data['password_string']:
                    adminuser.password_string=add_form.cleaned_data['password_string']
                    newpass=adminuser.name+add_form.cleaned_data['password_string']
                    newpass=sha1(newpass.encode()).hexdigest()
                    adminuser.password=newpass
                adminuser.save()
                request.session["flash"]={"msg":"User added.","type":"success"}
                return redirect("/adminusers")
            pass
        except Exception as err:
            log.error("error occured: {}".format(str(err)),exc_info=True)
            request.session["flash"]={"msg":str(err.args[1]),"type":"danger"}

        #what if user exists
    context['form']=add_form
    return render(request,"adminusers/add.html",context)

def edit(request,id):
    if not request.session.get("user"):
        return redirect("/manager")
    if not id:
        return redirect('/adminusers')
    context={
        "title":"C3SWebcom : Admin Users - Edit",
        "page":"adminusers",
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
                    request.session["flash"]={"msg":"User updated.","type":"warning"}
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
def delete(request,id):
    if not request.session.get("user") and not id:
        return redirect("/manager")
    try:
        admin_user=AdminUsers.objects.get(pk=id)
        admin_user.delete()
        request.session["flash"]={"msg":"User deleted.","type":"warning"}
    except AdminUsers.DoesNotExist as err:
        log.error("Error:", exc_info=True)

    return redirect("/adminusers")
    pass
