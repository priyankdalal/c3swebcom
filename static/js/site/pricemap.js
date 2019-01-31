function drag(e){
    e.dataTransfer.setData("text",e.target.id);
}
function drop(e){
    if(e.target.tagName=="SELECT"){
        var src=$("#"+e.dataTransfer.getData("text"));
        var text=src.text();
        var value=src.data("id");
        var target=$(e.target);
        target.append("<option value='"+ value+ "'>"+ text+ "</option>");
        target.removeClass("drop-effect");
        target.contents().filter("option").removeClass("drop-effect");
        if(target.data("type")=="package"){
            var package_collection=$("#package_collection").val();
            if(!!package_collection){
                package_collection+=","+value;
            }else{
                package_collection=value;
            }
            $("#package_collection").val(package_collection);
        }
        if(target.data("type")=="locality"){
            var locality_collection=$("#locality_collection").val();
            if(!!locality_collection){
                locality_collection+=","+value;
            }else{
                locality_collection=value;
            }
            $("#locality_collection").val(locality_collection);
        }
    }
};
function allowdrag(e){
    if(e.target.tagName=="SELECT"){
        console.log(e);
        e.dataTransfer.dropEffect = "copy";
        var target=$(e.target);
        target.addClass("drop-effect");
        e.preventDefault();
    }
}
