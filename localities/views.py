from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from .forms import addForm,editForm
from .models import Localities
import logging
log=logging.getLogger(__name__)
# Create your views here.
def index(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Localities",
        "page":"localities",
        "localities":Localities.objects.all(),
    }
    print(Localities.objects.all())
    return render(request,"localities/index.html",context)

def add(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Localities : Add",
        "page":"localities",
    }
    add_form=addForm()
    if request.method=="POST":
        add_form=addForm(request.POST)
        if add_form.is_valid():
            if add_form.cleaned_data['name']:
                locality=Localities(name=add_form.cleaned_data['name'])
            if add_form.cleaned_data['code']:
                locality.code=add_form.cleaned_data['code']
            locality.save()
            request.session["flash"]={"msg":"Locality added.","type":"success"}
            return redirect("/localities")
    context['form']=add_form
    return render(request,"localities/add.html",context)
    pass

def edit(request,id):
    if not request.session.get("user"):
        return redirect("/manager")
    if not id:
        return redirect("/localities")
    context={
        "title":"C3SWebcom - Localities : Edit",
        "page":"localities",
    }
    if request.method=="POST":
        edit_form=editForm(request.POST)
        if edit_form.is_valid():
            if edit_form.cleaned_data['id']:
                locality=Localities.objects.get(pk=edit_form.cleaned_data['id'])
            if edit_form.cleaned_data['name']:
                locality.name=edit_form.cleaned_data['name']
            if edit_form.cleaned_data['code']:
                locality.code=edit_form.cleaned_data['code']
            locality.save()
            request.session["flash"]={"msg":"Locality updated.","type":"info"}
            return redirect("/localities")
    try:
        locality=Localities.objects.get(pk=id)
        edit_form=editForm(model_to_dict(locality))
        context['form']=edit_form
    except Localities.DoesNotExist as err:
        log.error("Error:", exc_info=True)
        request.session["flash"]={"msg":err.args[0],"type":"danger"}
    return render(request,"localities/edit.html",context)

def delete(request,id):
    if not request.session.get("user") and not id:
        return redirect("/manager")
    try:
        locality=Localities.objects.get(pk=id)
        locality.delete()
        request.session["flash"]={"msg":"Locality deleted.","type":"info"}
    except Localities.DoesNotExist as err:
        log.error("Error:", exc_info=True)
        request.session["flash"]={"msg":err.args[0],"type":"danger"}

    return redirect("/localities")
    pass
