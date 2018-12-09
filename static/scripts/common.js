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
