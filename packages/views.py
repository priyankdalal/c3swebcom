from django.shortcuts import render
from c3swebcom import conf_vars
from .models import CsPackages

# Create your views here.
def index(request):
    if not request.session.get("user"):
        return redirect("/manager")
    context={
        "title":"C3SWebcom - Packages",
        "user":request.session.get("user"),
        "websocket":"{}:{}".format(conf_vars.WEBSOCKET_SERVER,conf_vars.WEBSOCKET_PORT),
        "package_list":CsPackages.objects.all()
    }
    return render(request,"packages/index.html",context)
