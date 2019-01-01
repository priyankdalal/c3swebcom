$(document).on("click",".order-update-btn",function(){
  $(this).closest("td").addClass("edit-mode");
});
$(document).on("click",".order-submit-btn",function(){
  $(this).closest("td").removeClass("edit-mode");
});
$(document).on("change",".order-status-select",function(){
  var o_id=$(this).data("id");
  var val=$(this).val();
  $("#confirm_modal").find(".modal-ok").attr("onclick","do_order_update('"+ o_id+ "','"+ val+ "')");
  $("#confirm_modal").modal();
});
$("#order_update_confirmation").click(function(){
  var o_id=$(this).data("id");
  var val=$(this).data("val");
  $("#order_update_modal").hide();
  do_order_update(o_id,val);
});
function do_order_update(id,val){
  $("#confirm_modal").modal("hide");
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
          if(val=="1"){
            $("#td_"+id).closest("tr").removeClass("text-danger").addClass("text-success");
            $("#td_"+id).find(".order-status").text("Completed");
          }else{
            $("#td_"+id).closest("tr").removeClass("text-success").addClass("text-danger");
            $("#td_"+id).find(".order-status").text("Pending");
          }
        }
      }
    });
  }else{
    alert("one or more input is empty");
  }
}
