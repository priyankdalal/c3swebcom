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
PackageManager.prototype.syncAll=function(domain){
    if(!!this.websoket_url && !!domain){
        var that=this;
        var websocket=new WebSocket(that.websoket_url);
        websocket.onerror=function(){
            that.progressModel.hide();
            that.errorModel.find(".error-message").html("Error while connecting to Package Module. Please contact support.");
            that.errorModel.show();
            websocket.close();
        };
        websocket.onopen=function(){
            websocket.send(JSON.stringify({op:"sync_packages",host:domain}));
        };
        websocket.onmessage=function(e){
            var data=JSON.parse(e.data);
            console.log(data);
            if(!!data.error){
                that.progressModel.hide();
                that.errorModel.find(".error-message").html(data.msg);
                that.errorModel.show();
            }
            else{
                if(data.end){
                    that.progressModel.hide();
                    that.resultModel.find(".result-message").text(data.msg);
                    that.resultModel.show();
                }else{
                    that.progressModel.find(".progress-bar-text").text(data.msg);
                    that.progressModel.show();
                    that.progressModel.find(".progress-bar").width(data.step+"%");
                }
            }
        };
    }
};
$("#sync_package").click(function(){
    var pm= new PackageManager({
        host:"ws://localhost:8180",
        progressModel:$("#progress_modal"),
        errorModel:$("#error_modal"),
        resultModel:$("#result_modal")
        });
    pm.syncAll("epay.globalnoc.in");
});
