function filterTable(filter,table,needle) {
    var td_list=table.find("td[data-filter='"+ filter+ "']");
    for(var td of td_list){
        if($(td).text().toLowerCase().indexOf(needle)>-1)
            $(td).parent().show();
        else
            $(td).parent().hide();
    }
}
var timer={};
$(".pay-filter").on("keyup",function(){
    var val=$(this).val();
    var table=$("#pay_table");
    if(!!val){
        var filter=$(this).attr("data-filter");
        filterTable(filter,table,val);
        if(!!timer)
          clearTimeout(timer);
        timer=setTimeout(function(){
          var data={};
          $(".pay-filter").each(function(){
            data[$(this).data("filter")]=$(this).val();
          });
          get_filtered_data(data);
        },1500);
    }else{
        table.find("tr").show();
    }
});
$(document).on("click",".c3s-payment-btn",function(){
  var domain=$(this).data("domain");
  var user=$(this).data("user");
  do_payment(user,domain);
});
function do_payment(user,domain){
  if (!!user && !!domain){
    $.ajax({
      type:"POST",
      url:"do-payment",
      data:{user:user,domain:domain,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
      error:function(e){
        console.log(e);
      },
      success:function(resp){
        console.log(resp)
        if (!resp.error & resp.payload==0){
          alert("done");
        }
      }
    });
  }else{
    alert("failed");
  }
}
function get_filtered_data(filters){
  alert("filtered data");
  filters['csrfmiddlewaretoken']=$("meta[name='csrf_token']").attr("content");
  $.ajax({
    type:"POST",
    url:"get-filtered-users",
    data:filters,
    success:function(resp){
      console.log(resp);
    }
  });
}
