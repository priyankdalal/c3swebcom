var total=0;
$(".sync-user").click(function(){
  $("#domain_select_modal").modal();
});
$(document).on("click","#s_u_d_i_btn",function(){
  var d_n=$("#s_u_d_i").val();
  sync_users(d_n);
});
function sync_users(domain){
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