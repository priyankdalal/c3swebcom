var total=0;
$(".sync-user").click(function(){
  $("#domain_select_modal").show();
});
$(document).on("click","#s_u_d_i_btn",function(){
  var d_n=$("#s_u_d_i").val();
  sync_users(d_n);
});
function sync_users(domain){
  $("#domain_select_modal").hide();
  var websock=new WebSocket("ws://localhost:8180");
  websock.onmessage=function(e){
    var data=JSON.parse(e.data);
    console.log(data);
    if(!!data.error){
      $("#error_message").html(data.msg);
      $("#error_modal").show();
      websock.close();
    }
    if(!!data.total){
      total=parseInt(data.total);
      $("#progress_modal").show();
    }
    if(!!data.current){
      var p_c=(data.current*100)/total;
      p_c=parseFloat(p_c.toFixed(2))+ "%";
      $("#progress_bar").width(p_c);
      $("#progress_bar_text").text(data.current+ "/"+ total);
    }
    if(!!data.end){
      $("#progress_modal").hide();
      $("#result_response").html("Total Users : "+ data.total+ "<br>Inserted/Updated : "+ data.processed+ "<br>Skipped : "+ data.skipped);
      $("#result_modal").show();
      websock.close();
    }
  };
  websock.onopen=function(){
    websock.send(JSON.stringify({op:"sync_users",host:domain}));
  };
}
