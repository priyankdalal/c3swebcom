function DomainManager(opts){
    this.editDomainId=0;
    this.AddDomainErrorElement=(!!opts.AddDomainErrorElement)?opts.AddDomainErrorElement:"#add_domain_error";
    this.EditDomainErrorElement=(!!opts.EditDomainErrorElement)?opts.EditDomainErrorElement:"#edit_domain_error";
    this.AddDomainModal=(!!opts.AddDomainModal)?opts.AddDomainModal:"#add_domain_modal";
    this.EditDomainModal=(!!opts.EditDomainModal)?opts.EditDomainModal:"#edit_domain_modal";
}
DomainManager.prototype.AddDomain=function(opts){
    if(!opts.name){
        $(this.AddDomainErrorElement).show().find("span").empty().html("Name is empty");
        return false;
    }else if(!opts.url){
        $(this.AddDomainErrorElement).show().find("span").empty().html("Url is empty");
        return false;
    }else if(!opts.username){
        $(this.AddDomainErrorElement).show().find("span").empty().html("Username is empty");
        return false;
    }else if(!opts.userpass){
        $(this.AddDomainErrorElement).show().find("span").empty().html("Password is empty");
        return false;
    }else{
        if(!opts.st) opts.st="up";
        $(".progressor").show();
        $.ajax({
          type:"POST",
          url:"add-domain",
          data:{ nm:opts.name, url:opts.url, un:opts.username, up:opts.userpass, st:opts.st, csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
          timeout:10000,
          error:function(err){
            $(".progressor").hide();
            show_error(err.statusText);
          },
          success:function(r){
            $(".progressor").hide();
            if(!!r.error){
              show_error(r.msg);
            }else{
              show_result(r.msg);
              setTimeout(function(){window.location.reload();},3000);
            }
          }
        });
    }
};
DomainManager.prototype.SaveDomain=function(opts){
    if(!this.editDomainId){
        $(this.EditDomainErrorElement).show().find("span").empty().html("No/Invalid Domain");
        return false;
    }else if(!opts.name){
        $(this.EditDomainErrorElement).show().find("span").empty().html("Name is empty");
        return false;
    }else if(!opts.url){
        $(this.EditDomainErrorElement).show().find("span").empty().html("Url is empty");
        return false;
    }else if(!opts.username){
        $(this.EditDomainErrorElement).show().find("span").empty().html("Username is empty");
        return false;
    }else if(!opts.userpass){
        $(this.EditDomainErrorElement).show().find("span").empty().html("Password is empty");
        return false;
    }else if(!opts.st){
        $(this.EditDomainErrorElement).show().find("span").empty().html("Please select a status first.");
        return false;
    }else{
        var that=this;
        $(".progressor").show();
        $.ajax({
          type:"POST",
          url:"save-domain",
          data:{id:that.editDomainId,nm:opts.name,url:opts.url,un:opts.username,up:opts.userpass,st:opts.st,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
          timeout:10000,
          error:function(err){
            $(".progressor").hide();
            that.editDomainId=0
            $(that.EditDomainModal).modal("hide");
            show_error(err.statusText);
          },
          success:function(r){
            $(".progressor").hide();
            that.editDomainId=0;
            $(that.EditDomainModal).modal("hide");
            if(!!r.error){
              show_error(r.msg);
            }else{
              show_result(r.msg);
              setTimeout(function(){window.location.reload();},3000);
            }
          }
        });
    }
};
DomainManager.prototype.deleteDomain=function(id){
    if(!!id){
        $.ajax({
          type:"POST",
          url:"delete-domain",
          data:{id:id,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
          timeout:10000,
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
};
DomainManager.prototype.fetchDomainInfo=function(id){
    if(!!id){
        var that=this;
        $(".progressor").show();
        $.ajax({
          type:"POST",
          url:"get-domain",
          data:{id:id,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")},
          timeout:10000,
          error:function(err){
            $(".progressor").hide();
            show_error(err.statusText);
          },
          success:function(r){
            $(".progressor").hide();
            if(!!r.error){
              show_error(r.msg);
            }else{
              domain=JSON.parse(r.payload);
              that.showEditDomainModal(domain);
            }
          }
    });
    }else{
        show_error("Domain is required to edit");
    }
};
DomainManager.prototype.showEditDomainModal=function(data){
    $("#e_d_n",this.EditDomainModal).val(data[0].fields.name);
    $("#e_d_u",this.EditDomainModal).val(data[0].fields.url);
    $("#e_d_un",this.EditDomainModal).val(data[0].fields.auth_user);
    $("#e_d_up",this.EditDomainModal).val(data[0].fields.auth_pass);
    $("#e_d_st",this.EditDomainModal).val(data[0].fields.status);
    $(this.EditDomainModal).modal();
};
var dm=new DomainManager({
    AddDomainErrorElement:"#d_a_e",
    EditDomainErrorElement:"#d_e_e",
    AddDomainModal:"#domain_add_modal",
    EditDomainModal:"#domain_edit_modal"
});



$("#d_a_e,#d_e_e").hide();
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
  dm.editDomainId=d_id;
  dm.fetchDomainInfo(d_id);
});
$(document).on("click",".domain-delete",function(){
  var d_id=$(this).data("id");
  $(".modal-ok","#confirm_modal").attr("onclick","deleteDomain("+ d_id+ ")");
  $("#confirm_modal").modal();
});
function deleteDomain(id){
  dm.deleteDomain(id);
  $("#confirm_modal").modal("hide");
  $(".card[data-domain_id='"+ id+ "']").parent().remove();
}
function add_domain(){
  var nm=$("#n_d_n").val();
  var url=$("#n_d_u").val();
  var un=$("#n_d_un").val();
  var up=$("#n_d_up").val();
  var st=$("#n_d_st").val();
  dm.AddDomain({name:nm,url:url,username:un,userpass:up,st:st});
}
function save_domain(){
    var opts={
        name:$("#e_d_n","#domain_edit_modal").val(),
        url:$("#e_d_u","#domain_edit_modal").val(),
        username:$("#e_d_un","#domain_edit_modal").val(),
        userpass:$("#e_d_up","#domain_edit_modal").val(),
        st:$("#e_d_st","#domain_edit_modal").val()
    };
    dm.SaveDomain(opts);
}

