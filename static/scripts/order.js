$(document).on("click",".order-update-btn",function(){
  $(this).closest("td").addClass("edit-mode");
});
$(document).on("click",".order-submit-btn",function(){
  $(this).closest("td").removeClass("edit-mode");
});
$(document).on("change",".order-status-select",function(){
  var o_id=$(this).data("id");
  var val=$(this).val();
  $("#order_update_confirmation").data("id",o_id).data("val",val);
  $("#order_update_modal").show();
});
$("#order_update_confirmation").click(function(){
  var o_id=$(this).data("id");
  var val=$(this).data("val");
  $("#order_update_modal").hide();
  do_order_update(o_id,val);
});
function do_order_update(id,val){
  if(!!id && !!val ){
    $.ajax({
      type:"POST",
      url:"do-order-status-update",
      data:{id:id,status:val,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
      timeout:10000,
      error:function(err){
        console.log(err)
        show_error(err.statusText);
      },
      success:function(r){
        if(!!r.error){
          show_error(r.msg);
        }else{
          show_result(r.msg);
          $("#td_"+id).removeClass("edit-mode");
          if(!!val){
            $("#td_"+id).closest("tr").removeClass("w3-red").addClass("w3-green");
          }else{
            $("#td_"+id).closest("tr").removeClass("w3-green").addClass("w3-red");
          }
        }
      }
    });
  }else{
    alert("one or more input is empty");
  }
}
