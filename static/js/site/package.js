function PackageManager(opt){
    if(!opt && !opt.host && !opt.progressModel && !opt.errorModel && !opt.resultModel){
        console.log("cannot initialize package module.");
        return false;
    }
    this.websoket_url=opt.host;
    this.progressModel=opt.progressModel;
    this.errorModel=opt.errorModel;
    this.resultModel=opt.resultModel;
};
PackageManager.prototype.pingUrl=function(){
    var that=this;
    console.log(that.websoket_url);
};
PackageManager.prototype.syncAll=function(){
    if(!!this.websoket_url){
        var that=this;
        var websocket=new WebSocket(that.websoket_url);
        websocket.onerror=function(){
            that.progressModel.modal("hide");
            that.errorModel.find(".error-message").html("Error while connecting to Package Module. Please contact support.");
            that.errorModel.modal();
            websocket.close();
        };
        websocket.onopen=function(){
            websocket.send(JSON.stringify({op:"sync_packages"}));
        };
        websocket.onmessage=function(e){
            var data=JSON.parse(e.data);
            console.log(data);
            if(!!data.error){
                that.progressModel.modal("hide");;
                that.errorModel.find(".error-message").html(data.msg);
                that.errorModel.modal();
            }
            else{
                if(data.end){
                    that.progressModel.modal("hide");
                    show_toast(data.msg,"success");
                }else{
                    that.progressModel.find(".progress-bar-text").text(data.msg);
                    that.progressModel.modal();
                    that.progressModel.find("#progress_bar").width(data.step+"%").text(data.msg);
                }
            }
        };
    }
};
PackageManager.prototype.updatePackage=function(package_id,data,callback=null){
    var that=this;
    if(!!package_id){
        data['csrfmiddlewaretoken']=$("meta[name='csrf_token']").attr("content");
        data['id']=package_id;
        $.ajax({
            type:"POST",
            url:"update-package",
            data:data,
            timeout:10000,
            error:function(err){
                show_toast(err.statusText,"danger");
                if(!!callback){
                    callback(package_id);
                }
            },
            success:function(r){
                if(r.error){
                    show_toast(r.msg,"danger");
                }else{
                    $("#package_"+data['id']).find("td[data-filter='value']").html('<i class="fa fa-inr"></i>'+ data.value);
                    /*that.resultModel.find(".result-message").text(r.msg);
                    that.resultModel.modal();*/
                    show_toast(r.msg,"success");
                }
                if(!!callback){
                    callback(package_id);
                }
            }
        });
    }else{
        that.errorModel.find(".error-message").html("<i class='text-danger fa fa-exclamation-triangle'></i> Please select a package first.");
        that.errorModel.modal();
    }
};
PackageManager.prototype.fetchPackage=function(package_id,callback=null){
    var that=this;
    if(!!package_id){
        var data={id:package_id,csrfmiddlewaretoken:$("meta[name='csrf_token']").attr("content")};
        $.ajax({
            type:"POST",
            url:"get-package-data",
            data:data,
            error:function(err){
                that.errorModel.find(".error-message").html(err.statusText);
                that.errorModel.modal();
            },
            success:function(r){
                if(r.error){
                    that.errorModel.find(".error-message").html(r.msg);
                    that.errorModel.modal();
                }else{
                    console.log(r);
                    if(!!callback){
                        callback(r.payload);
                    }
                }
            }
        });
    }else{
        that.errorModel.find(".error-message").html("<i class='text-danger fa fa-exclamation-triangle'></i> Please select a package first.");
        that.errorModel.modal();
    }
};
$("#sync_package").click(function(){
    var pm= new PackageManager({
        host:websoket_url,
        progressModel:$("#progress_modal"),
        errorModel:$("#error_modal"),
        resultModel:$("#result_modal")
        });
    pm.syncAll();
});
$(document).on("click",".update-package",function(){
    var package_id=$(this).data("id");
    $(this).prop("disabled",true);
    if(!!package_id){
        var pm= new PackageManager({
            host:websoket_url,
            progressModel:$("#progress_modal"),
            errorModel:$("#error_modal"),
            resultModel:$("#result_modal")
        });
        pm.fetchPackage(package_id,showEditPackage);
    }else{
        $("#error_modal").find("#error_message").html("<i class='text-danger fa fa-exclamation-triangle'></i> Please select a package first.");
        $("#error_modal").modal();
    }
});
$(document).on("click","#update_package_btn",function(){
    var id=$(this).data("id");
    var value=$("#package_value").val();
    $("#edit_package_modal").modal("hide");
    if(!!id){
        var pm= new PackageManager({
            host:websoket_url,
            progressModel:$("#progress_modal"),
            errorModel:$("#error_modal"),
            resultModel:$("#result_modal")
        });
        pm.updatePackage(id,{value:value},postUpdate);
    }else{
        $("#error_modal").find("#error_message").html("<i class='text-danger fa fa-exclamation-triangle'></i> Please select a package first.");
        $("#error_modal").modal();
    }
});
function showEditPackage(package){
    if(!!package){
        $("#package_name").val(package.name);
        $("#package_domain").val(package.domain);
        $("#package_value").val(package.value);
        $("#update_package_btn").data("id",package.id);
        $("#edit_package_modal").modal();
    }else{
        show_error("No package data fetched");
    }
}
function postUpdate(id){
    $("#package_"+id).find(".update-package").prop("disabled",false);
}
