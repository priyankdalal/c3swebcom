(function(w){
	function LorelPopup(){
		var id=new Date().getTime();
		return {
			getVersion:function(){
				return "1.0";
			},
			init:function(l){
				var tHtml="",cHtml="",aHtml="";
				if(l.title && l.title.length>0)
					tHtml=this.buildTitle(l.title);
				if(l.content && l.content.hasOwnProperty("align")){
					var a="flex-start";
					switch(l.content.align){
						case "center":
							a="center";
							break;
						case "right":
							a="flex-end";
							break;
					};
					if(l.content.msg.length>0)
					cHtml=this.buildContent(l.content.msg,a);
				}
				else{
					if(l.content.length>0)
					cHtml=this.buildContent(l.content,"flex-start");
				}
				aHtml=this.buildActions(l.actions);
				return this.buildStructure(tHtml, cHtml, aHtml);
			},
			buildStructure:function(t,c,a){
				var popup='<div class="lorel" id="lorel_popup_'+ id+ '">'
						+'<div class="lorel-container">';
				if(t.length>0)
					popup+='<div class="close" onclick="lorel.close('+ id+ ');"><bold>x</bold></div>'+t;
				popup+=c +a
						+'</div>'
					+'</div>';
				var elem=document.createElement("div");
				elem.id=id;
				document.body.appendChild(elem);
				elem.innerHTML=popup;
				return true;
			},
			buildTitle:function(o){
				return '<div class="title-bar"><span class="title">'+ o+ '</span></div>';
			},
			buildContent:function(d,a){
				return '<div class="contents" style="justify-content:'+ a+ ';">'+ d+ '</div>';
			},
			buildActions:function(a){
				var btns="<div class='actions'>";
				if(a.length>0){
					for(var i in a){
						var v="",t="class='btn-success' ";
						if(a[i].hasOwnProperty("value"))
							v=a[i].value;
						if(a[i].hasOwnProperty("type"))
							t="class='btn-"+ a[i].type+ "' ";
						if(a[i].hasOwnProperty("onclick"))
							t+="onclick='"+ a[i].onclick+ "'";

						btns+="<button value='"+ v+ "' "+ t+ ">"+ v+ "</button>";
					}
				}else{
					btns+="<button>ok</button>";
				}
				btns+="</div>"
				return btns;
			},
			close:function(){
				var elem=document.getElementById(id);
				elem.parentNode.removeChild(elem);
			},
			alert:function(m){
				this.init({content:{msg:m,align:"center"},actions:[{value:"Ok",onclick:"lorel.close()"}]});
			},
			confirm:function(m,callback){
				this.init({content:{msg:m,align:"center"},actions:[{value:"Yes",onclick:"lorel.response(this.value,"+ callback+ ")"},{value:"No",type:"cancel",onclick:"lorel.response(this.value,"+ callback+ ")"}]});
			},
			prompt:function(m,callback){
				var pmsg="<input class='lorel-input' type='text' id='lorel_prompt_text' autofocus/>"
				this.init({title:m,content:{msg:pmsg,align:"center"},actions:[{value:"Submit",onclick:"lorel.response(this.value,"+ callback+ ")"}]});
			},
			response:function(i,callback){
				if(!callback)
					return false;
				if(i.toLowerCase()=="yes")
					callback(true);
				else if(i.toLowerCase()=="submit"){
					callback(document.getElementById("lorel_prompt_text").value);
				}
				else
					callback(false);
				this.close();
			}
		};
	};
	w["lorel"]=new LorelPopup();
})(window);
