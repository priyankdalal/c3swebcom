$(document).on("click","#delete_locality",function(){
    window.location.href="delete/"+$(this).data("locality");
});
$(document).on("click","#auto_assign",function(){
    var websocket=new WebSocket(websoket_url);
    websocket.onerror=function(err){
        show_toast("Failed to connect remote service.","danger");
        websocket.close();
    };
    websocket.onmessage=function(e){
        var data=JSON.parse(e.data);
        console.log(data);
        if(!!data.error){
            console.log(data.msg);
            show_toast(data.msg,"danger");
            websocket.close();
        }
        if(!!data.end){
            console.log(data.msg);
            show_toast(data.msg,"info");
            websocket.close();
        }
        if(!!data.payload){
            if(data.payload.state=="pr"){
                var top=$("#user_"+data.payload.user_id).offset().top;
                $(document).scrollTop(top-100);
                $("#user_"+data.payload.user_id).addClass("bg-warning");
                $(".assign-btn","#user_"+data.payload.user_id).prop("disabled",true);
            }else if(data.payload.state=="cp"){
                $(".assign-btn","#user_"+data.payload.user_id).prop("disabled",false);
                $(".user-locality","#user_"+data.payload.user_id).text(data.payload.locality);
            }else{
                $("#user_"+data.payload.user_id).removeClass("bg-warning");
                $(".assign-btn","#user_"+data.payload.user_id).prop("disabled",false);
            }
        }
    };
    websocket.onopen=function(){
        websocket.send(JSON.stringify({"op":"assign_users"}));
    };
});
