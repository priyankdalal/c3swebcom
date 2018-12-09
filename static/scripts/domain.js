$(document).on("click","#d_a_btn",function(){
  $("#domain_add_modal").show();
});
$(document).on("click","#d_a_s_btn",function(){
  add_domain();
});
function add_domain(){
  var nm=$("#n_d_n").val();
  var url=$("#n_d_u").val();
  var un=$("#n_d_un").val();
  var up=$("#n_d_up").val();
  var st=$("#n_d_st").val();
  if(!!nm && !!url && !!un && !!up){
    $.ajax({
      type:"POST",
      url:"add-domain",
      data:{nm:nm,url:url,un:un,up:up,st:st,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
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
          setTimeout(function(){window.location.reload();},3000);
        }
        console.log(r);
      }
    });
  }else{
    $("#d_a_e").empty().html("one or more input is empty");
  }
}
