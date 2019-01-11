$(document).ready(function(){
  $('[data-toggle="tooltip"]').tooltip(); 
});
$(document).on("click",".order-update-btn",function(){
  $(this).closest("tr").addClass("edit-mode");
});
$(document).on("click",".order-submit-btn",function(){
  $(this).closest("tr").removeClass("edit-mode");
});
$(document).on("change",".order-status-select",function(){
  var o_id=$(this).data("id");
  $("#confirm_modal").find(".modal-ok").attr("onclick","do_order_update('"+ o_id+ "','status_')");
  $("#confirm_modal").modal();
});
$(document).on("change",".payment-status-select",function(){
  var o_id=$(this).data("id");
  $("#confirm_modal").find(".modal-ok").attr("onclick","do_order_update('"+ o_id+ "','payment_')");
  $("#confirm_modal").modal();
});
$("#order_update_confirmation").click(function(){
  var o_id=$(this).data("id");
  var val=$(this).data("val");
  $("#order_update_modal").hide();
  do_order_update(o_id,val);
});
function do_order_update(id,field){
  $("#confirm_modal").modal("hide");
  if(!!id && field){
    var data={
        id:id,
        csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content"),
        key:$("#"+ field+ id).attr("name"),
        value:$("#"+ field+ id).val(),
    };
    $.ajax({
      type:"POST",
      url:"do-order-status-update",
      data:data,
      timeout:10000,
      error:function(err){
        console.log(err)
        show_toast(err.statusText,"danger");
      },
      success:function(r){
        if(!!r.error){
          show_toast(r.msg);
        }else{
          show_toast(r.msg,"success");
          $("#tr_"+id).removeClass("edit-mode");
          if(data.value=="1"){
            $("#tr_"+id).removeClass("text-danger").addClass("text-success");
            $("#"+ field+ "td_"+ id).find(".status").text("Completed");
          }else{
            $("#tr_"+id).removeClass("text-success").addClass("text-danger");
            $("#"+ field+ "td_"+ id).find(".status").text("Pending");
          }
        }
      }
    });
  }else{
    alert("one or more input is empty");
  }
}
