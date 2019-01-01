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
$(document).on("click",".c3s-payment-go-btn",function(){
  var that=this;
  $(this).closest("td").find(".pay-actions").slideUp(200,function(){
      $(this).closest("td").find(".pay-select-order").slideDown(200);
  });
});
$(document).on("click",".payment-cancel",function(){
    var that=this;
    $(this).closest("td").find(".pay-select-order").slideUp(200,function(){
      $(this).closest("td").find(".pay-actions").slideDown(200);
  });
});
$(document).on("click",".c3s-payment-btn",function(){
  var that=this;
  $("#payment_confirmation").data("user_id",$(that).data("user_id"));
  $("#payment_modal").modal();
});
$(document).on("click","#payment_confirmation",function(){
  $("#payment_modal").modal("hide");
  $(".progressor").show();
  var user_id=$(this).data("user_id");
  create_order(user_id);
});
$(document).on("click",".c3s-update-btn",function(){
  var that=this;
  var user_id=$(that).data("user_id");
  update_user(user_id);
});
function update_user(id){
  if(!!id){
    var status='';
    var websock=new WebSocket(websoket_url);
    websock.onmessage=function(e){
      var data=JSON.parse(e.data);
      if(!!data.error){
        $("#progress_modal").modal("hide");
        $("#error_message").html(data.msg);
        $("#error_modal").modal();
        websock.close();
      }
      else{
        if(data.step=="90"){
          status=data.msg;
        }
        //total=parseInt(data.total);
        $("#progress_modal").modal();
        $("#progress_bar").width(data.step+"%").text(data.msg);
        if(!!data.end){
          setTimeout(function(){
            $("#progress_modal").modal("hide");
            $("#result_response").html(status);
            //$("#row_user_"+user_id).find("td[data-filter='expiry']").text(data.date);
            $("#result_modal").modal();
          },1500);
          websock.close();
        }
      }
    };
    websock.onerror=function(err){
      $("#progress_modal").modal("hide");
      $("#error_message").html("Error occured while connecting to payment module. Please contact support.");
      $("#error_modal").modal();
      websock.close();
    }
    websock.onopen=function(){
      websock.send(JSON.stringify({op:"upadete_user",payload:id+""}));
    };
  }else{
    $("#error_message").html("No/invalid user to update.");
    $("#error_modal").modal();
  }
}
function create_order(id){
  if (!!id){
    var payment_status=$("#select_paid_"+id).val();
    $.ajax({
      type:"POST",
      url:"create-order",
      data:{user_id:id,paid:payment_status,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
      timeout:10000,
      error:function(e){
        $("#error_message").html(e.statusText);
        $("#error_modal").modal();
        $(".progressor").hide();
        $(".payment-cancel").click();
      },
      success:function(resp){
        $(".progressor").hide();
        if (!resp.error & resp.payload>0){
          do_payment(id,resp.payload)
        }else{
          $("#error_message").html(resp.msg);
          $("#error_modal").modal();
          $(".payment-cancel").click();
        }
      }
    });
  }else{
    alert("failed");
  }
}
function do_payment(user_id,order_id){
  $(".payment-cancel").click();
  if(!!user_id && !!order_id){
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
        $("#progress_modal").modal("hide");
        $("#error_message").html(data.msg);
        $("#error_modal").modal();
        websock.close();
      }
      else{
        //total=parseInt(data.total);
        $("#progress_modal").modal();
        $("#progress_bar").width(data.step+"%").text(data.msg);
        if(!!data.end){
          $("#progress_bar").text(data.msg+ " next date: "+ data.date);
          setTimeout(function(){
            $("#progress_modal").modal("hide");
            $("#result_response").html("Next due date of user is : <strong>"+ data.date +"</strong>");
            $("#row_user_"+user_id).find("td[data-filter='expiry']").text(data.date);
            $("#result_modal").modal();
          },1500);
          websock.close();
        }
      }
    };
    websock.onopen=function(e){
      websock.send(JSON.stringify({op:"do_payment",payload:user_id+"",order_load:order_id+""}));
    };
  }else{
    $(".w3-modal").modal("hide");
    $("#error_message").text("js:payment:invalid request.");
    $("#error_modal").show();
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
          $("#pay_table_container_id").empty().html(rep_arr[1]);
        }
      }else{
        var html="<tr align='center'><td colspan='9' class='text-center text-red'>No data to show.</td>";
        $("#pay_table_body").empty().html(html);
      }
    }
  });
}
