function filterTable(filter,table,needle) {
    var td_list=table.find("td[data-filter='"+ filter+ "']");
    for(var td of td_list){
        if($(td).text().toLowerCase().indexOf(needle)>-1)
            $(td).parent().show();
        else
            $(td).parent().hide();
    }
}
$(".pay-filter").on("keyup",function(){
    var val=$(this).val();
    var table=$("#pay_table");
    if(!!val){
        var filter=$(this).attr("data-filter");
        filterTable(filter,table,val);
    }else{
        table.find("tr").show();
    }
});