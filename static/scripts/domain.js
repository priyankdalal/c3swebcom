$(document).on("click","#d_a_btn",function(){
  $("#domain_add_modal").show();
});
$(document).on("click","#d_a_s_btn",function(){
  add_domain();
});
$(document).on("click","#d_e_s_btn",function(){
  save_domain();
});
$(document).on("click",".domain-edit",function(){
  var d_id=$(this).data("id");
  console.log(d_id);
  $("#d_e_s_btn").data("id",d_id);
  fetch_domain_info(d_id);
});
$(document).on("click",".domain-delete",function(){
  var d_id=$(this).data("id");
  lorel.args.push(d_id);
  lorel.confirm("Are you sure?",lorel_delete);
  //delete_domain(d_id);
});
function lorel_delete(r){
  if(!!r){
    delete_domain(lorel.args.pop());
  }
}
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
      }
    });
  }else{
    $("#d_a_e").empty().html("one or more input is empty");
  }
}
function save_domain(){
  var nm=$("#e_d_n").val();
  var url=$("#e_d_u").val();
  var un=$("#e_d_un").val();
  var up=$("#e_d_up").val();
  var st=$("#e_d_st").val();
  id=$("#d_e_s_btn").data("id");
  console.log(un);
  if(!!nm && !!url && !!un && !!up){
    $.ajax({
      type:"POST",
      url:"save-domain",
      data:{id:id,nm:nm,url:url,un:un,up:up,st:st,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
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
      }
    });
  }else{
    $("#d_a_e").empty().html("one or more input is empty");
  }
}
function fetch_domain_info(id){
  if(!!id){
    $.ajax({
      type:"POST",
      url:"get-domain",
      data:{id:id,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
      timeout:1000,
      error:function(err){
        console.log(err)
        show_error(err.statusText);
      },
      success:function(r){
        if(!!r.error){
          show_error(r.msg);
        }else{
          domain=JSON.parse(r.payload);
          create_edit_dialog(domain);
        }
      }
    });
  }else{
    show_error("Domain is required to edit");
  }
}
function delete_domain(id){
  if(!!id){
    $.ajax({
      type:"POST",
      url:"delete-domain",
      data:{id:id,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
      timeout:1000,
      error:function(err){
        show_error(err.statusText);
      },
      success:function(r){
        if(!!r.error){
          show_error(r.msg);
        }else{
          $("#domain_card_"+id).remove();
          show_result(r.msg);
        }
      }
    });
  }else{
    show_error("Domain is required to edit");
  }
}
function create_edit_dialog(data){
  $("#e_d_n").val(data[0].fields.name);
  $("#e_d_u").val(data[0].fields.url);
  $("#e_d_un").val(data[0].fields.auth_user);
  $("#e_d_up").val(data[0].fields.auth_pass);
  $("#e_d_st").val(data[0].fields.status);
  $("#domain_edit_modal").show();
}
