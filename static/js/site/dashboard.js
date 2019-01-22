var total=0;
$(".check-new-user").click(function(){
  $("#domain_select_modal").modal();
});
$(".sync-user").click(function(){
  var confirm=window.confirm("Sync all existing users? Make sure its a very long running process...");
  if(confirm){
    sync_users();
  }
});
$(document).on("click","#s_u_d_i_btn",function(){
  var d_n=$("#s_u_d_i").val();
  check_new_users(d_n);
});
function check_new_users(domain){
  $("#domain_select_modal").modal("hide");
  $("#progress_bar").text("connecting...");
  $("#progress_modal").modal();
  var websock=new WebSocket(websoket_url);
  websock.onerror=function(err){
    $("#progress_modal").modal("hide");
    $("#error_message").html("Error occured while connecting to payment module. Please contact support.");
    $("#error_modal").modal();
    websock.close();
  }
  websock.onmessage=function(e){
    var data=JSON.parse(e.data);
    if(!!data.error){
      $("#error_message").html(data.msg);
      $("#error_modal").modal();
      websock.close();
    }
    if(!!data.total){
      total=parseInt(data.total);
      $("#progress_modal").modal();
    }
    if(!!data.current){
      var p_c=(data.current*100)/total;
      p_c=parseFloat(p_c.toFixed(2))+ "%";
      $("#progress_bar").width(p_c).text(data.current+ "/"+ total);
    }
    if(!!data.end){
      $("#progress_modal").modal("hide");
      $("#result_response").html("Total Users : "+ data.total+ "<br>Inserted/Updated : "+ data.processed+ "<br>IP Inserted for : "+ data.ip+ "<br>Skipped : "+ data.skipped);
      $("#result_modal").modal();
      websock.close();
    }
  };
  websock.onopen=function(){
    websock.send(JSON.stringify({op:"sync_users",host:domain}));
  };
}
function sync_users(){
  var websock=new WebSocket(websoket_url);
  websock.onopen=function(){
    websock.send(JSON.stringify({op:"sync_all_users"}));
  };
  websock.onerror=function(err){
    websock.close();
    show_toast("Error occred while connecting to payment module. Please contact support.","danger");
  };
  websock.onmessage=function(e){
    console.log(e);
    var data=JSON.parse(e.data);
    /*if(!!data.error){
      $("#error_message").html(data.msg);
      $("#error_modal").modal();
      websock.close();
    }*/
    if(!!data.overall_total){
      overall_total=parseInt(data.overall_total);
      $("#dual_progress_modal").modal();
    }
    if(!!data.overall_progress){
      var p_c=(data.overall_progress*100)/overall_total;
      p_c=parseFloat(p_c.toFixed(2))+ "%";
      $("#progress_bar_1").width(p_c).text(data.overall_progress+ "/"+ overall_total);
    }
    if(!!data.step){
      $("#progress_bar_2").width(data.step+"%").text(data.msg);
    }
    if(!!data.end){
      $("#progress_bar_2").width("0%").text(data.msg);
    }
    if(!!data.terminate){
      $("#dual_progress_modal").modal("hide");
      $("#result_response").html("All users updated.");
      $("#result_modal").modal();
      websock.close();
    }
  };
}