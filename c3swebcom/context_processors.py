import json
import html
from . import conf_vars
#insert version to response
def version_processor(request):
    return {"version":conf_vars.VERSION}

#insert user to response if login
def user_processor(request):
    if request.session:
        if request.session.get("user") == None:
            return {"user":""}
        else:
            return {"user":request.session.get("user")}

#insert websocket url to response
def websocket_processor(request):
    return {"websocket":"{}:{}".format(conf_vars.WEBSOCKET_SERVER,conf_vars.WEBSOCKET_PORT)}

def flash_processor(request):
    print(request.session.get("flash"))
    if request.session:
        print(request.session)
        if request.session.get("flash"):
            flash=request.session.get("flash")
            del request.session['flash']
            return {"flash":html.unescape(json.dumps(flash))}
        else:
            return {"flash":""}
