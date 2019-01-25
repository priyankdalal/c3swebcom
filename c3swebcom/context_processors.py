from . import conf_vars
#insert version to response
def version_processor(request):
    return {"version":conf_vars.VERSION}

#insert user to response if login
def user_processor(request):
    print(request)
    if request.session:
        print(request.session.get("user"))
        if request.session.get("user") == None:
            return {"user":""}
        else:
            return {"user":request.session.get("user")}

#insert websocket url to response
def websocket_processor(request):
    return {"websocket":"{}:{}".format(conf_vars.WEBSOCKET_SERVER,conf_vars.WEBSOCKET_PORT)}
