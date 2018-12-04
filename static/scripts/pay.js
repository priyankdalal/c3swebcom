function filterTable(filter,table,needle) {
    var td_list=table.find("td[data-filter='"+ filter+ "']");
    for(var td of td_list){
        if($(td).text().toLowerCase().indexOf(needle)>-1)
            $(td).parent().show();
        else
            $(td).parent().hide();
    }
}
$(document).on("click",".filter-user-page",function(){
  var data={};
  data["page"]=$(this).data("page");
  $(".pay-filter").each(function(){
    if ($(this).val().trim())
      data[$(this).data("filter")]=$(this).val();
  });
  get_filtered_data(data);
});
$(document).on("keyup",".pay-filter",function(){
  var timer={};
  var val=$(this).val();
  var table=$("#pay_table");
  if(!!val){
      var filter=$(this).attr("data-filter");
      //filterTable(filter,table,val);
      if(!!timer)
        clearTimeout(timer);
      timer=setTimeout(function(){
        var data={};
        $(".pay-filter").each(function(){
          if ($(this).val().trim())
            data[$(this).data("filter")]=$(this).val();
        });
        get_filtered_data(data);
      },1500);
  }else{
      table.find("tr").show();
  }
});
$(document).on("click",".c3s-payment-btn",function(){
  var that=this;
  $("#payment_confirmation").data("user_id",$(that).data("user_id"));
  $("#payment_modal").show();
});
$(document).on("click","#payment_confirmation",function(){
  var user_id=$(this).data("user_id");
  do_payment(user_id);
});
function do_payment(id){
  if (!!id){
    $.ajax({
      type:"POST",
      url:"do-payment",
      data:{user_id:id,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
      error:function(e){
        console.log(e);
      },
      success:function(resp){
        console.log(resp);
        if (!resp.error & resp.payload==0){
          alert("done");
        }else{
          alert(resp.msg);
        }
      }
    });
  }else{
    alert("failed");
  }
}
function get_filtered_data(filters){
  filters['csrfmiddlewaretoken']=$("meta[name='csrf_token']").attr("content");
  $.ajax({
    type:"POST",
    url:"get-filtered-users",
    data:filters,
    success:function(resp){
      if(!resp.error){
        //make_pay_table_body(resp.payload)
        $("#pay_table_container_id").empty().html(resp)
      }else{
        var html="<tr align='center'><td colspan='9' class='w3-center w3-red'>No data to show.</td>";
        $("#pay_table_body").empty().html(html);
      }
    }
  });
}
