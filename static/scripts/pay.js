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
        make_pay_table_body(resp.payload)
      }else{
        var html="<tr align='center'><td colspan='9' class='w3-center w3-red'>No data to show.</td>";
        $("#pay_table_body").empty().html(html);
      }
    }
  });
}
function make_pay_table_body(data){
  if(data.length>0){
    html=""
    for(var i in data){
      var row_html=""
      var fields=data[i].fields;
      if(fields.hasOwnProperty("name"))
        row_html+='<td class="w3-center" data-filter="name">'+ fields.name+ '</td>';
      else
        row_html+='<td class="w3-center" data-filter="name"></td>';
      if(fields.hasOwnProperty("address"))
        row_html+='<td class="w3-center" data-filter="address">'+ fields.address+ '</td>';
      else
        row_html+='<td class="w3-center" data-filter="address"></td>';
      if(fields.hasOwnProperty("expiry_date"))
        row_html+='<td class="w3-center" data-filter="expiry">'+ fields.expiry_date+ '</td>';
      else
        row_html+='<td class="w3-center" data-filter="expiry"></td>';
      if(fields.hasOwnProperty("package"))
        row_html+='<td class="w3-center" data-filter="package">'+ fields.package+ '</td>';
      else
        row_html+='<td class="w3-center" data-filter="package"></td>';
      if(fields.hasOwnProperty("phone"))
        row_html+='<td class="w3-center" data-filter="phone">'+ fields.phone+ '</td>';
      else
        row_html+='<td class="w3-center" data-filter="phone"></td>';
      if(fields.hasOwnProperty("mobile"))
        row_html+='<td class="w3-center" data-filter="mobile">'+ fields.mobile+ '</td>';
      else
        row_html+='<td class="w3-center" data-filter="mobile"></td>';
      if(fields.hasOwnProperty("domain"))
        row_html+='<td class="w3-center" data-filter="domain">'+ fields.domain+ '</td>';
      else
        row_html+='<td class="w3-center" data-filter="domain"></td>';
      if(fields.hasOwnProperty("ip_count"))
        row_html+='<td class="w3-center" data-filter="ip">'+ fields.ip_count+ '</td>';
      else
        row_html+='<td class="w3-center" data-filter="ip"></td>';
      row_html+='<td class="w3-center"><button class="w3-btn w3-blue c3s-payment-btn" title="Pay" data-domain="'+ fields.domain+ '" data-user="'+ fields.ccid+ '"><i class="fa fa-plus-circle"></i></button></td>'
      row_html="<tr>"+ row_html+ "</tr>";
      html+=row_html;
    }
  }else{
    var html="<tr align='center'><td class='w3-center w3-red' colspan='9'>No data to show.</td>";
  }
  $("#pay_table_body").empty().html(html);
}
