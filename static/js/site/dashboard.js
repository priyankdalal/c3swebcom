var total=0;
$(".check-new-user").click(function(){
  $("#domain_select_modal").modal();
});
$(".sync-user").click(function(){
  var confirm=window.confirm("Sync all existing users? Make sure its a very long running process...");
  if(confirm){
    sync_users();
  }
});
$(document).on("click","#s_u_d_i_btn",function(){
  var d_n=$("#s_u_d_i").val();
  check_new_users(d_n);
});
function check_new_users(domain){
  $("#domain_select_modal").modal("hide");
  $("#progress_bar").text("connecting...");
  $("#progress_modal").modal();
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
      $("#error_message").html(data.msg);
      $("#error_modal").modal();
      websock.close();
    }
    if(!!data.total){
      total=parseInt(data.total);
      $("#progress_modal").modal();
    }
    if(!!data.current){
      var p_c=(data.current*100)/total;
      p_c=parseFloat(p_c.toFixed(2))+ "%";
      $("#progress_bar").width(p_c).text(data.current+ "/"+ total);
    }
    if(!!data.end){
      $("#progress_modal").modal("hide");
      $("#result_response").html("Total Users : "+ data.total+ "<br>Inserted/Updated : "+ data.processed+ "<br>IP Inserted for : "+ data.ip+ "<br>Skipped : "+ data.skipped);
      $("#result_modal").modal();
      websock.close();
    }
  };
  websock.onopen=function(){
    websock.send(JSON.stringify({op:"sync_users",host:domain}));
  };
}
function sync_users(){
  var websock=new WebSocket(websoket_url);
  websock.onopen=function(){
    websock.send(JSON.stringify({op:"sync_all_users"}));
  };
  websock.onerror=function(err){
    websock.close();
    show_toast("Error occred while connecting to payment module. Please contact support.","danger");
  };
  websock.onmessage=function(e){
    var data=JSON.parse(e.data);
    /*if(!!data.error){
      $("#error_message").html(data.msg);
      $("#error_modal").modal();
      websock.close();
    }*/
    if(!!data.overall_total){
      overall_total=parseInt(data.overall_total);
      $("#dual_progress_modal").modal();
    }
    if(!!data.overall_progress){
      var p_c=(data.overall_progress*100)/overall_total;
      p_c=parseFloat(p_c.toFixed(2))+ "%";
      $("#progress_bar_1").width(p_c).text(data.overall_progress+ "/"+ overall_total);
    }
    if(!!data.step){
      $("#progress_bar_2").width(data.step+"%").text(data.msg);
    }
    if(!!data.end){
      $("#progress_bar_2").width("0%").text(data.msg);
    }
    if(!!data.terminate){
      $("#dual_progress_modal").modal("hide");
      $("#result_response").html("All users updated.");
      $("#result_modal").modal();
      websock.close();
    }
  };
}
$(document).ready(function(){
    drawMonthlyChart(monthlyChartData);
    drawYearlyChart(yearlyChartData);
    drawMonthlyPaymentWiseChart(dailyPaymentWiseData);
});
function drawMonthlyChart(monthlyData){
    var daywise=monthlyData.daywise,dayStaffWise = monthlyData.dayStaffWise;
    var days_arr=daywise.map(function(d){
        return d.day;
    });

    var dailyCtx = document.getElementById("dailyOrdersChart").getContext('2d');

    var chartOptions={
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true,
                    fontColor:'#fff'
                }
            }],
            xAxes: [{
                ticks: {
                    fontColor:'#fff'
                }
            }]
        },
        title:{
            fontColor:'rgb(200,30,40)'
        },
        legend:{
            labels:{
                fontColor:'#fff'
            }
        }
    };

    var datasets=[{
        label:"Total Orders",
        data:daywise.map(function(d){
            return d.count;
        }),
        borderWidth:2,
        backgroundColor:'rgba(233,233,233,0.45)',
        borderColor:'#fff',
        pointRadius:4
    }];
    for(var i in dayStaffWise){
        var data={};
        data['label']=i+ " orders";
        data['data']=days_arr.map(function(d){
            //debugger;
            var r=0;
            for(var j in dayStaffWise[i]){
                if(dayStaffWise[i][j].order_day==parseInt(d)){
                    r=dayStaffWise[i][j].order_count;
                    break;
                }
            }
            return r;
        });
        data['borderWidth']=1;
        data['backgroundColor']='rgba('+ Math.round(Math.random()*200)+ ','+ Math.round(Math.random()*200)+ ','+ Math.round(Math.random()*200)+ ',0.5)';
        //debugger;
        data['borderColor']='#fff';
        data['pointRadius']=3;
        datasets.push(data);
    }

    var montlyChart = new Chart(dailyCtx,{
        responsive:true,
        type:"line",
        data:{
            labels:daywise.map(function(d){
                return d.day;
            }),
            datasets:datasets.sort()
        },
        options:chartOptions
    });

}
function drawYearlyChart(yearlyData){
    var monthwise=yearlyData.monthwise;
    var monthlyCtx = document.getElementById("monthlyOrdersChart").getContext('2d');
    var chartOptions={
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true,
                    fontColor:'#fff'
                }
            }],
            xAxes: [{
                ticks: {
                    fontColor:'#fff'
                }
            }]
        },
        title:{
            fontColor:'rgb(200,30,40)'
        },
        legend:{
            labels:{
                fontColor:'#fff'
            }
        }
    };
    var monthlyChart = new Chart(monthlyCtx,{
        responsive:true,
        type:"line",
        data:{
            labels:monthwise.map(function(d){
                //return d.month;
                if(d.month=='1')
                    return "Jan";
                if(d.month=='2')
                    return "Feb";
                if(d.month=='3')
                    return "Mar";
                if(d.month=='4')
                    return "Apr";
                if(d.month=='5')
                    return "May";
                if(d.month=='6')
                    return "Jun";
                if(d.month=='7')
                    return "Jul";
                if(d.month=='8')
                    return "Aug";
                if(d.month=='9')
                    return "Sep";
                if(d.month=='10')
                    return "Oct";
                if(d.month=='11')
                    return "Nov";
                if(d.month=='12')
                    return "Dec";
            }),
            datasets:[{
                label:"Orders",
                data:monthwise.map(function(d){
                    return d.count;
                }),
                borderWidth:2,
                backgroundColor:'rgba(233,233,233,0.45)',
                borderColor:'#fff',
                pointRadius:8
            }]
        },
        options:chartOptions
    });
}
function drawMonthlyPaymentWiseChart(monthlyData){
    var monthlyObj = monthlyData.monthlyPaymentWiseData;
    var ctx = document.getElementById("dailyOrdersPaymentChart").getContext('2d');
    var datasets = [];
    for(var status in monthlyObj.chartData){
        var set={
            label: status+ " orders",
            data:monthlyObj.users.map(function(d){
                return monthlyObj.chartData[status][d];
            })
        }
        if(status == 'paid')
            set['backgroundColor'] = "darkseagreen";
        else
            set['backgroundColor'] = "indianred";
        datasets.push(set);
    }
    var options = {
        scales: {
            xAxes: [{
                stacked: true
            }],
            yAxes: [{
                stacked: true
            }]
        },
        title:{
            fontColor:'rgb(200,30,40)'
        },
        /*legend:{
            labels:{
                fontColor:'#fff'
            }
        }*/
    };
    var data = {
        labels: monthlyObj.users,
        datasets: datasets
    }
    var payementChart = new Chart(ctx,{
        type: 'bar',
        data: data,
        options: options
    });
}
