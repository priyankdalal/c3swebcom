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
$(document).on("keyup",".pay-filter",function(e){
  var val=$(this).val();
  var table=$("#pay_table");
  if(!!val && e.keyCode==13){
      var filter=$(this).attr("data-filter");
      //filterTable(filter,table,val);
      var data={};
      $(".pay-filter").each(function(){
        if ($(this).val().trim())
          data[$(this).data("filter")]=$(this).val();
      });
      get_filtered_data(data);
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
  //do_payment(user_id);
  var websock=new WebSocket("ws://localhost:8180");
  websock.onmessage=function(e){
    var data=JSON.parse(e.data);
    console.log(data);
    if(!!data.error){
      $("#progress_modal").hide();
      $("#payment_modal").hide();
      $("#error_message").html(data.msg);
      $("#error_modal").show();
      websock.close();
    }
    else{
      //total=parseInt(data.total);
      $("#progress_modal").show();
      $("#progress_bar").width(data.step+"%");
      $("#progress_bar_text").text(data.msg);
      if(!!data.end){
        $("#progress_bar_text").text(data.msg+ " next date: "+ data.date);
        setTimeout(function(){
          $("#progress_modal").hide();
          $("#payment_modal").hide();
          $("#result_response").html("Next due date of user is : <strong>"+ data.date +"</strong>");
          $("#row_user_"+user_id).find("tr[data-filter='expiry']").text(date.date);
          $("#result_modal").show();
        },1500);
        websock.close();
      }
    }
  };
  websock.onopen=function(){
    websock.send(JSON.stringify({op:"do_payment",host:"epay.globalnoc.in",payload:user_id+""}));
  };
});
function do_payment(id){
  if (!!id){
    $.ajax({
      type:"POST",
      url:"do-payment",
      data:{user_id:id,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
      timeout:10000,
      error:function(e){
        $("#payment_modal").hide();
        $("#payment_error").html(e.statusText);
        $("#error_modal").show();
      },
      success:function(resp){
        if (!resp.error & resp.payload==0){
          alert("done");
        }else{
          $("#payment_error").html(resp.msg);
          $("#error_modal").show();
        }
        $("#payment_modal").hide();
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
        rep_arr=resp.split("<!--resp-breaker-->");
        $("#pay_table tbody").empty().html(rep_arr[0]);
        if (rep_arr.length>1){
          $(".pagination").empty().html(rep_arr[1]);
        }
      }else{
        var html="<tr align='center'><td colspan='9' class='w3-center w3-red'>No data to show.</td>";
        $("#pay_table_body").empty().html(html);
      }
    }
  });
}
