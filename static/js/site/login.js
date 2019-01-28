/*toast js**************************/
function show_toast(msg="",type){
    var toast=document.getElementById("toast");
    var msg_e=toast.getElementsByClassName("toast-msg")[0];
    var icon_e=toast.getElementsByClassName("icon")[0];
    msg_e.innerHTML=msg;
    if(!!type){
        toast.classList.add("bg-"+type);
        switch(type){
            case "success":
                icon_e.getElementsByClassName('material-icons')[0].innerText="done";
                break;
            case "danger":
                icon_e.getElementsByClassName('material-icons')[0].innerText="clear";
                break;
            case "warning":
                icon_e.getElementsByClassName('material-icons')[0].innerText="report_problem";
                break;
            case "info":
                icon_e.getElementsByClassName('material-icons')[0].innerText="info";
                break;
        }
    }
    toast.classList.add("show");
    setTimeout(function(){
        toast.classList.remove("show");
        if(!!type){
            toast.classList.remove("bg-"+type);
        }
    },5000);
}
function show_notification_from_json(msg_obj){
    if(!!msg_obj){
        msg_obj=$('<textarea />').html(msg_obj).text();
        console.log(msg_obj);
        msg_obj=JSON.parse(msg_obj);
        show_toast(msg_obj.msg,msg_obj.type);
    }
}
$(document).ready(function(){
  show_notification_from_json(flash);
});
