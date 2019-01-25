function show_error(msg){
  $("#error_message").empty().html(msg);
  $("#error_modal").modal();
}
function hide_error(){
  $("#error_modal").modal("hide");
}
function show_result(msg){
  $("#result_response").empty().html(msg);
  $("#result_modal").modal();
}
function hide_result(){
  $("#result_modal").modal("hide");
}
$(".input-helper").click(function(){
  var ty=$(this).data("for");
  var i_e=$(this).parent().find("input");
  if(ty=="visibility"){
    if(i_e.attr("type")=="password"){
      i_e.attr("type","text");
    }else{
      i_e.attr("type","password");
    }
  }
});
/*sidebar js***************************/
$(".close-sidebar").click(function(){
    window.localStorage.setItem("sidebar-open","0");
    $(".wrapper").addClass("hide-sidebar");
});
$(".open-sidebar").click(function(){
    window.localStorage.setItem("sidebar-open","1");
    $(".wrapper").removeClass("hide-sidebar");
});
if(!!window.localStorage.getItem("sidebar-open")){
    if(window.localStorage.getItem("sidebar-open")=="0")
        $(".wrapper").addClass("hide-sidebar");
}
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
$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip();
});
/*confirm js***********************************/
if($(".btn-confirm").length>0){
    $(".btn-confirm").click(function(){
        $(this).parent().attr("data-open","open");
    });
    $(".btn-cancel").click(function(){
        $(this).parent().attr("data-open","close");
    });
}
