$(document).on("click",".modal-close, .modal-cancel",function(){
  $(this).closest(".w3-modal").hide();
});
function show_error(msg){
  $("#error_message").empty().html(msg);
  $("#error_modal").show();
}
function hide_error(){
  $("#error_modal").hide();
}
function show_result(msg){
  $("#result_response").empty().html(msg);
  $("#result_modal").show();
}
function hide_result(){
  $("#result_modal").hide();
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
