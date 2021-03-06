/*!
 * jQuery UI Position 1.10.3
 * http://jqueryui.com
 *
 * Copyright 2013 jQuery Foundation and other contributors
 * Released under the MIT license.
 * http://jquery.org/license
 *
 * http://api.jqueryui.com/position/
 */
(function($,undefined){$.ui=$.ui||{};
var cachedScrollbarWidth,max=Math.max,abs=Math.abs,round=Math.round,rhorizontal=/left|center|right/,rvertical=/top|center|bottom/,roffset=/[\+\-]\d+(\.[\d]+)?%?/,rposition=/^\w+/,rpercent=/%$/,_position=$.fn.position;
function getOffsets(offsets,width,height){return[parseFloat(offsets[0])*(rpercent.test(offsets[0])?width/100:1),parseFloat(offsets[1])*(rpercent.test(offsets[1])?height/100:1)];
}function parseCss(element,property){return parseInt($.css(element,property),10)||0;
}function getDimensions(elem){var raw=elem[0];
if(raw.nodeType===9){return{width:elem.width(),height:elem.height(),offset:{top:0,left:0}};
}if($.isWindow(raw)){return{width:elem.width(),height:elem.height(),offset:{top:elem.scrollTop(),left:elem.scrollLeft()}};
}if(raw.preventDefault){return{width:0,height:0,offset:{top:raw.pageY,left:raw.pageX}};
}return{width:elem.outerWidth(),height:elem.outerHeight(),offset:elem.offset()};
}$.position={scrollbarWidth:function(){if(cachedScrollbarWidth!==undefined){return cachedScrollbarWidth;
}var w1,w2,div=$("<div style='display:block;width:50px;height:50px;overflow:hidden;'><div style='height:100px;width:auto;'></div></div>"),innerDiv=div.children()[0];
$("body").append(div);
w1=innerDiv.offsetWidth;
div.css("overflow","scroll");
w2=innerDiv.offsetWidth;
if(w1===w2){w2=div[0].clientWidth;
}div.remove();
return(cachedScrollbarWidth=w1-w2);
},getScrollInfo:function(within){var overflowX=within.isWindow?"":within.element.css("overflow-x"),overflowY=within.isWindow?"":within.element.css("overflow-y"),hasOverflowX=overflowX==="scroll"||(overflowX==="auto"&&within.width<within.element[0].scrollWidth),hasOverflowY=overflowY==="scroll"||(overflowY==="auto"&&within.height<within.element[0].scrollHeight);
return{width:hasOverflowY?$.position.scrollbarWidth():0,height:hasOverflowX?$.position.scrollbarWidth():0};
},getWithinInfo:function(element){var withinElement=$(element||window),isWindow=$.isWindow(withinElement[0]);
return{element:withinElement,isWindow:isWindow,offset:withinElement.offset()||{left:0,top:0},scrollLeft:withinElement.scrollLeft(),scrollTop:withinElement.scrollTop(),width:isWindow?withinElement.width():withinElement.outerWidth(),height:isWindow?withinElement.height():withinElement.outerHeight()};
}};
$.fn.position=function(options){if(!options||!options.of){return _position.apply(this,arguments);
}options=$.extend({},options);
var atOffset,targetWidth,targetHeight,targetOffset,basePosition,dimensions,target=$(options.of),within=$.position.getWithinInfo(options.within),scrollInfo=$.position.getScrollInfo(within),collision=(options.collision||"flip").split(" "),offsets={};
dimensions=getDimensions(target);
if(target[0].preventDefault){options.at="left top";
}targetWidth=dimensions.width;
targetHeight=dimensions.height;
targetOffset=dimensions.offset;
basePosition=$.extend({},targetOffset);
$.each(["my","at"],function(){var pos=(options[this]||"").split(" "),horizontalOffset,verticalOffset;
if(pos.length===1){pos=rhorizontal.test(pos[0])?pos.concat(["center"]):rvertical.test(pos[0])?["center"].concat(pos):["center","center"];
}pos[0]=rhorizontal.test(pos[0])?pos[0]:"center";
pos[1]=rvertical.test(pos[1])?pos[1]:"center";
horizontalOffset=roffset.exec(pos[0]);
verticalOffset=roffset.exec(pos[1]);
offsets[this]=[horizontalOffset?horizontalOffset[0]:0,verticalOffset?verticalOffset[0]:0];
options[this]=[rposition.exec(pos[0])[0],rposition.exec(pos[1])[0]];
});
if(collision.length===1){collision[1]=collision[0];
}if(options.at[0]==="right"){basePosition.left+=targetWidth;
}else{if(options.at[0]==="center"){basePosition.left+=targetWidth/2;
}}if(options.at[1]==="bottom"){basePosition.top+=targetHeight;
}else{if(options.at[1]==="center"){basePosition.top+=targetHeight/2;
}}atOffset=getOffsets(offsets.at,targetWidth,targetHeight);
basePosition.left+=atOffset[0];
basePosition.top+=atOffset[1];
return this.each(function(){var collisionPosition,using,elem=$(this),elemWidth=elem.outerWidth(),elemHeight=elem.outerHeight(),marginLeft=parseCss(this,"marginLeft"),marginTop=parseCss(this,"marginTop"),collisionWidth=elemWidth+marginLeft+parseCss(this,"marginRight")+scrollInfo.width,collisionHeight=elemHeight+marginTop+parseCss(this,"marginBottom")+scrollInfo.height,position=$.extend({},basePosition),myOffset=getOffsets(offsets.my,elem.outerWidth(),elem.outerHeight());
if(options.my[0]==="right"){position.left-=elemWidth;
}else{if(options.my[0]==="center"){position.left-=elemWidth/2;
}}if(options.my[1]==="bottom"){position.top-=elemHeight;
}else{if(options.my[1]==="center"){position.top-=elemHeight/2;
}}position.left+=myOffset[0];
position.top+=myOffset[1];
if(!$.support.offsetFractions){position.left=round(position.left);
position.top=round(position.top);
}collisionPosition={marginLeft:marginLeft,marginTop:marginTop};
$.each(["left","top"],function(i,dir){if($.ui.position[collision[i]]){$.ui.position[collision[i]][dir](position,{targetWidth:targetWidth,targetHeight:targetHeight,elemWidth:elemWidth,elemHeight:elemHeight,collisionPosition:collisionPosition,collisionWidth:collisionWidth,collisionHeight:collisionHeight,offset:[atOffset[0]+myOffset[0],atOffset[1]+myOffset[1]],my:options.my,at:options.at,within:within,elem:elem});
}});
if(options.using){using=function(props){var left=targetOffset.left-position.left,right=left+targetWidth-elemWidth,top=targetOffset.top-position.top,bottom=top+targetHeight-elemHeight,feedback={target:{element:target,left:targetOffset.left,top:targetOffset.top,width:targetWidth,height:targetHeight},element:{element:elem,left:position.left,top:position.top,width:elemWidth,height:elemHeight},horizontal:right<0?"left":left>0?"right":"center",vertical:bottom<0?"top":top>0?"bottom":"middle"};
if(targetWidth<elemWidth&&abs(left+right)<targetWidth){feedback.horizontal="center";
}if(targetHeight<elemHeight&&abs(top+bottom)<targetHeight){feedback.vertical="middle";
}if(max(abs(left),abs(right))>max(abs(top),abs(bottom))){feedback.important="horizontal";
}else{feedback.important="vertical";
}options.using.call(this,props,feedback);
};
}elem.offset($.extend(position,{using:using}));
});
};
$.ui.position={fit:{left:function(position,data){var within=data.within,withinOffset=within.isWindow?within.scrollLeft:within.offset.left,outerWidth=within.width,collisionPosLeft=position.left-data.collisionPosition.marginLeft,overLeft=withinOffset-collisionPosLeft,overRight=collisionPosLeft+data.collisionWidth-outerWidth-withinOffset,newOverRight;
if(data.collisionWidth>outerWidth){if(overLeft>0&&overRight<=0){newOverRight=position.left+overLeft+data.collisionWidth-outerWidth-withinOffset;
position.left+=overLeft-newOverRight;
}else{if(overRight>0&&overLeft<=0){position.left=withinOffset;
}else{if(overLeft>overRight){position.left=withinOffset+outerWidth-data.collisionWidth;
}else{position.left=withinOffset;
}}}}else{if(overLeft>0){position.left+=overLeft;
}else{if(overRight>0){position.left-=overRight;
}else{position.left=max(position.left-collisionPosLeft,position.left);
}}}},top:function(position,data){var within=data.within,withinOffset=within.isWindow?within.scrollTop:within.offset.top,outerHeight=data.within.height,collisionPosTop=position.top-data.collisionPosition.marginTop,overTop=withinOffset-collisionPosTop,overBottom=collisionPosTop+data.collisionHeight-outerHeight-withinOffset,newOverBottom;
if(data.collisionHeight>outerHeight){if(overTop>0&&overBottom<=0){newOverBottom=position.top+overTop+data.collisionHeight-outerHeight-withinOffset;
position.top+=overTop-newOverBottom;
}else{if(overBottom>0&&overTop<=0){position.top=withinOffset;
}else{if(overTop>overBottom){position.top=withinOffset+outerHeight-data.collisionHeight;
}else{position.top=withinOffset;
}}}}else{if(overTop>0){position.top+=overTop;
}else{if(overBottom>0){position.top-=overBottom;
}else{position.top=max(position.top-collisionPosTop,position.top);
}}}}},flip:{left:function(position,data){var within=data.within,withinOffset=within.offset.left+within.scrollLeft,outerWidth=within.width,offsetLeft=within.isWindow?within.scrollLeft:within.offset.left,collisionPosLeft=position.left-data.collisionPosition.marginLeft,overLeft=collisionPosLeft-offsetLeft,overRight=collisionPosLeft+data.collisionWidth-outerWidth-offsetLeft,myOffset=data.my[0]==="left"?-data.elemWidth:data.my[0]==="right"?data.elemWidth:0,atOffset=data.at[0]==="left"?data.targetWidth:data.at[0]==="right"?-data.targetWidth:0,offset=-2*data.offset[0],newOverRight,newOverLeft;
if(overLeft<0){newOverRight=position.left+myOffset+atOffset+offset+data.collisionWidth-outerWidth-withinOffset;
if(newOverRight<0||newOverRight<abs(overLeft)){position.left+=myOffset+atOffset+offset;
}}else{if(overRight>0){newOverLeft=position.left-data.collisionPosition.marginLeft+myOffset+atOffset+offset-offsetLeft;
if(newOverLeft>0||abs(newOverLeft)<overRight){position.left+=myOffset+atOffset+offset;
}}}},top:function(position,data){var within=data.within,withinOffset=within.offset.top+within.scrollTop,outerHeight=within.height,offsetTop=within.isWindow?within.scrollTop:within.offset.top,collisionPosTop=position.top-data.collisionPosition.marginTop,overTop=collisionPosTop-offsetTop,overBottom=collisionPosTop+data.collisionHeight-outerHeight-offsetTop,top=data.my[1]==="top",myOffset=top?-data.elemHeight:data.my[1]==="bottom"?data.elemHeight:0,atOffset=data.at[1]==="top"?data.targetHeight:data.at[1]==="bottom"?-data.targetHeight:0,offset=-2*data.offset[1],newOverTop,newOverBottom;
if(overTop<0){newOverBottom=position.top+myOffset+atOffset+offset+data.collisionHeight-outerHeight-withinOffset;
if((position.top+myOffset+atOffset+offset)>overTop&&(newOverBottom<0||newOverBottom<abs(overTop))){position.top+=myOffset+atOffset+offset;
}}else{if(overBottom>0){newOverTop=position.top-data.collisionPosition.marginTop+myOffset+atOffset+offset-offsetTop;
if((position.top+myOffset+atOffset+offset)>overBottom&&(newOverTop>0||abs(newOverTop)<overBottom)){position.top+=myOffset+atOffset+offset;
}}}}},flipfit:{left:function(){$.ui.position.flip.left.apply(this,arguments);
$.ui.position.fit.left.apply(this,arguments);
},top:function(){$.ui.position.flip.top.apply(this,arguments);
$.ui.position.fit.top.apply(this,arguments);
}}};
(function(){var testElement,testElementParent,testElementStyle,offsetLeft,i,body=document.getElementsByTagName("body")[0],div=document.createElement("div");
testElement=document.createElement(body?"div":"body");
testElementStyle={visibility:"hidden",width:0,height:0,border:0,margin:0,background:"none"};
if(body){$.extend(testElementStyle,{position:"absolute",left:"-1000px",top:"-1000px"});
}for(i in testElementStyle){testElement.style[i]=testElementStyle[i];
}testElement.appendChild(div);
testElementParent=body||document.documentElement;
testElementParent.insertBefore(testElement,testElementParent.firstChild);
div.style.cssText="position: absolute; left: 10.7432222px;";
offsetLeft=$(div).offset().left;
$.support.offsetFractions=offsetLeft>10&&offsetLeft<11;
testElement.innerHTML="";
testElementParent.removeChild(testElement);
})();
}(jQuery));
(function($){$.widget("ui.watchinput",{lastVal:"",timer:null,_create:function(){var self=this;
self.disable(false);
if(typeof document.activeElement!="unknown"&&document.activeElement==this.element[0]){setTimeout($.proxy(self._focus,self),0);
}},disable:function(isDisable){var self=this;
if(isDisable){clearInterval(this.timer);
this.element.unbind("blur",self._blur).unbind("focus",self._focus).unbind("keypress",self._keypress);
}else{this.lastVal=this.element.val();
this.element.bind("blur",$.proxy(self._blur,self)).bind("focus",$.proxy(self._focus,self)).bind("keypress",$.proxy(self._keypress,self));
}},_keypress:function(event){if(event.keyCode>=112&&event.keyCode<=123){return;
}this._watchAndFire(event);
},_blur:function(event){setTimeout($.proxy(this._watchAndFire,this),0);
clearInterval(this.timer);
},_focus:function(event){var self=this;
this.lastVal=this.element.val();
this.timer=setInterval($.proxy(self._watchAndFire,self),200);
},_watchAndFire:function(event){var self=this;
if(this.element.val()==this.lastVal){return false;
}this.lastVal=this.element.val();
setTimeout(function(){self._trigger("input",event,{value:self.element.val()});
},0);
return true;
}});
}(jQuery));
(function($,undefined){$.widget("ui.suggest",{options:{layerId:"suggestLayer",layerToggle:"",position:{my:"left top",at:"left bottom",collision:"none"},cookieDomain:"",cookieName:"",autofocus:true,disabled:false,maxLength:32},_create:function(){var self=this;
doc=this.element[0].ownerDocument;
var _cookie=$.cookie(this.options.cookieName);
this.options.disabled=(_cookie&&_cookie=="unuse")?true:false;
this.watch=new $.ui.watchinput;
this.watch.options={input:function(event,ui){if(self.options.disabled){return;
}self._input(event);
}};
this.watch.element=this.element;
this.watch._create();
this.element.attr({role:"textbox","aria-autocomplete":"list","aria-haspopup":"true"}).bind("keydown.suggest",function(event){var keyCode=$.ui.keyCode;
switch(event.keyCode){case keyCode.PAGE_UP:case keyCode.PAGE_DOWN:case keyCode.LEFT:case keyCode.RIGHT:break;
case keyCode.UP:self._move("previous",event);
break;
case keyCode.DOWN:self._move("next",event);
break;
case keyCode.ENTER:case keyCode.NUMPAD_ENTER:if(!self.menu.active){self._trigger("select",event,{item:{value:self.element.val(),term:self.term}});
}else{self._trigger("select",event,{item:self.menu.active.data("item.suggest")});
}event.stopPropagation();
break;
case keyCode.ESCAPE:self.element.val(self.term);
self.close(event);
break;
default:break;
}}).bind("blur.suggest",function(event){clearTimeout(self.searching);
self.closing=setTimeout(function(){self.close(event);
self._change(event);
},150);
}).bind("mousedown.suggest",function(){if(self.element.val().length>0){self.open();
}});
this._initSource();
this.response=function(){return self._response.apply(self,arguments);
};
this.menu=$("#"+this.options.layerId).mousedown(function(event){var menuElement=self.menu.element[0];
if(event.target===menuElement){setTimeout(function(){$(document).one("mousedown",function(event){if(event.target!==self.element[0]&&event.target!==menuElement&&!$.ui.contains(menuElement,event.target)){self.close();
}});
},1);
}setTimeout(function(){clearTimeout(self.closing);
},13);
}).suggestLayer({base:self.element.parent(),disabled:self.options.disabled,position:self.options.position,focus:function(event,ui){var item=ui.item.data("item.suggest");
if(false!==self._trigger("focus",null,{item:item})){if(/^key/.test(event.originalEvent.type)){self.watch.disable(true);
self.element.val(item.value);
self.watch.disable(false);
}}},selected:function(event,ui){var item=ui.item.data("item.suggest"),previous=self.previous;
if(self.element[0]!==doc.activeElement){self.element.focus();
self.previous=previous;
}if(false!==self._trigger("select",event,{item:item,term:self.term})){self.term=item.value;
self.watch.disable(true);
self.element.val(item.value);
self.watch.disable(false);
}self.close(event);
self.selectedItem=item;
},blur:function(event,ui){},enable:function(event,ui){self._disable(false,event);
},disable:function(event,ui){self._disable(true,event);
}}).zIndex(this.element.zIndex()+999).css({top:0,left:0}).hide().data("ui-suggestLayer");
var layerToggle=$(self.options.layerToggle);
layerToggle.mousedown(function(event){event.preventDefault();
if(!self.menu.element.is(":visible")){self.open();
}else{self.close();
}}).click(function(event){event.preventDefault();
});
if(this.options.autofocus){self._setAutoFocus();
}self._disable(self.options.disabled,null);
if($.fn.bgiframe){this.menu.element.bgiframe();
}},_setAutoFocus:function(){$(document).keydown($.proxy(function(event){var _target=event.target;
var cancelTag={INPUT:1,TEXTAREA:1,SELECT:1,EMBED:1,OBJECT:1};
var keyCode=$.ui.keyCode;
var code=event.keyCode;
var _name=_target.tagName?_target.tagName.toUpperCase():"";
if(!cancelTag[_name]||(event.ctrlKey&&code!==86)){if(code==224||code==116||event.metaKey||code===keyCode.BACKSPACE||(code>=keyCode.SPACE&&code<=keyCode.DOWN)||(code!=21&&code<keyCode.SPACE)||event.altKey){return;
}if(code===keyCode.SPACE&&event.shiftKey){window.scrollTo(0,0);
this.element.focus();
this.element.select();
event.preventDefault();
}else{if(_target!=this.element[0]){window.scrollTo(0,0);
this.element.focus();
this.element.select();
this._input(event);
}}}},this));
},_input:function(event){var self=this;
clearTimeout(self.searching);
self.searching=setTimeout(function(){if(self.term!=self.element.val()){self.selectedItem=null;
self.search(null,event);
}},self.options.delay);
},_disable:function(isDisable,event){$.cookie(this.options.cookieName,((isDisable)?"unuse":"use"),{expires:(new Date((new Date()).getTime()+21900*1000*60*60*24)),domain:this.options.domain});
this.options.disabled=isDisable;
this.element.attr("autocomplete",((isDisable)?"on":"off"));
if(!isDisable&&event){this.search(null,event);
}},_initSource:function(){var self=this,array,url;
if($.isArray(this.options.source)){array=this.options.source;
this.source=function(request,response){response($.ui.autocomplete.filter(array,request.term));
};
}else{if(typeof this.options.source==="string"){url=this.options.source;
this.source=function(request,response){if(self.xhr){self.xhr.abort();
}self.xhr=$.getJSON(url,request,function(data,status,xhr){if(xhr===self.xhr){response(data);
}self.xhr=null;
});
};
}else{this.source=this.options.source;
}}},search:function(value,event){value=value!=null?value:this.element.val();
this.term=this.element.val();
if(value.lengt_triggerh<this.options.minLength){return this.close(event);
}clearTimeout(this.closing);
if(this._trigger("search")===false){return;
}return this._search(value);
},_search:function(value){this.element.addClass("ui-autocomplete-loading");
this.source({term:value},this.response);
},_response:function(content){if(content.length){content=this._normalize(content);
this._suggest(content);
this._trigger("open");
}else{this.menu.ul.empty();
this.menu.deactivate();
this.menu.refresh();
if(this.element.val().length==0&&this.menu.element.is(":visible")){this.close();
}else{this.menu.show();
}}this.element.removeClass("ui-autocomplete-loading");
},close:function(event){clearTimeout(this.closing);
if(this.menu.element.is(":visible")){this.menu.hide();
this._trigger("close",event);
}},_change:function(event){if(this.previous!==this.element.val()){this._trigger("change",event,{item:this.selectedItem});
}},_normalize:function(items){if(items.length&&items[0].label&&items[0].value){return items;
}return $.map(items,function(item){if(typeof item==="string"){return{label:item,value:item};
}return{label:item[5],value:item[5],name:item[5],isMatch:item[6]=="1",id:item[2],count:item[3],officialFlag:(item[4]=="1")?true:false};
});
},_suggest:function(items){var ul=this.menu.ul.empty().zIndex(this.element.zIndex()+1),menuWidth,textWidth;
this._renderMenu(ul,items);
this.menu.deactivate();
this.menu.refresh();
this.open();
},open:function(){this.menu.show();
var ul=this.menu.ul;
menuWidth=ul.width("").outerWidth();
textWidth=$(this.options.layerSize).outerWidth();
ul.outerWidth(Math.max(menuWidth,textWidth));
},_renderMenu:function(ul,items){var self=this;
if(items.length>1||(items.length===1&&!items[0].isMatch)){$.each(items,function(index,item){self._renderItem(ul,item);
});
}var _elem=$('<li class="searchKeyword"><a title data-na="NC:searchword" href="" tabindex="-1"><em></em>で検索</a></li>');
_elem.data("item.suggest",{value:self.element.val(),term:self.element.val()}).find("EM").text(self.element.val());
ul.append(_elem);
},_renderItem:function(ul,item){var itemText=nj.cutStringByte(item.label,this.option("maxLength"),"…");
var _elem='<span class="mdSuggest01Txt"></span>';
return $("<li></li>").data("item.suggest",item).append('<a title="'+item.label+'" href="#">'+_elem+"</a>").find("SPAN.mdSuggest01Txt").text(itemText).end().appendTo(ul);
},_move:function(direction,event){if(this.menu.ul.is(":empty")){return;
}if(!this.menu.element.is(":visible")){if(/^next/.test(direction)){this.search(null,event);
}return;
}if(this.menu.last()&&/^next/.test(direction)){return;
}if(this.menu.first()&&/^previous/.test(direction)){this.element.val(this.term);
this.close();
return;
}this.menu[direction](event);
}});
}(jQuery));
(function($){$.widget("ui.suggestLayer",{options:{base:null,inner:"suggestDtl",listbox:"_resultBox1",messagebox1:"guideText",messagebox2:"guideText2",on:"suggestOn",off:"suggestOff",position:{my:"left top",at:"left bottom",collision:"none"},disabled:false},_create:function(){var self=this;
$("."+this.options.on,this.element).click(function(event){event.preventDefault();
event.stopPropagation();
self.options.disabled=false;
self._status();
self._trigger("enable",event,{});
});
$("."+this.options.off,this.element).click(function(event){event.preventDefault();
event.stopPropagation();
self.options.disabled=true;
self._status();
self._trigger("disable",event,{});
});
this.detail=$("."+this.options.inner,this.element);
this.ul=$("."+this.options.listbox,this.element);
this.ul.addClass("ui-menu ui-widget ui-widget-content ui-corner-all").attr({role:"listbox","aria-activedescendant":"ui-active-menuitem"}).click(function(event){if(!$(event.target).closest(".ui-menu-item a").length){return;
}event.preventDefault();
self.select(event);
});
this.refresh();
$(window).resize($.proxy(self._setPosition,self));
},refresh:function(){var self=this;
var items=this.ul.children("li:not(.ui-menu-item):has(a)").addClass("ui-menu-item").attr("role","menuitem").attr("data-na","NC:suggesttopic");
items.children("a").addClass("ui-corner-all").attr("tabindex",-1).mouseenter(function(event){self.activate(event,$(this).parent());
}).mouseleave(function(){self.deactivate();
});
this._status();
},activate:function(event,item){this.deactivate();
if(this.hasScroll()){var offset=item.offset().top-this.element.offset().top,scroll=this.element.attr("scrollTop"),elementHeight=this.element.height();
if(offset<0){this.element.attr("scrollTop",scroll+offset);
}else{if(offset>=elementHeight){this.element.attr("scrollTop",scroll+offset-elementHeight+item.height());
}}}this.active=item.eq(0).children("a").addClass("ui-state-hover").addClass("selected").attr("id","ui-active-menuitem").end();
this._trigger("focus",event,{item:item});
},deactivate:function(){if(!this.active){return;
}this.active.children("a").removeClass("ui-state-hover").removeClass("selected").removeAttr("id");
this._trigger("blur");
this.active=null;
},next:function(event){this.move("next",".ui-menu-item:first",event);
},previous:function(event){this.move("prev",".ui-menu-item:last",event);
},first:function(){return this.active&&!this.active.prevAll(".ui-menu-item").length;
},last:function(){return this.active&&!this.active.nextAll(".ui-menu-item").length;
},move:function(direction,edge,event){if(!this.active){this.activate(event,this.ul.children(edge));
return;
}var next=this.active[direction+"All"](".ui-menu-item").eq(0);
if(next.length){this.activate(event,next);
}else{this.activate(event,this.ul.children(edge));
}},hasScroll:function(){return this.element.height()<this.element.attr("scrollHeight");
},select:function(event){this._trigger("selected",event,{item:this.active});
},show:function(){this.element.show();
this._status();
this._setPosition();
},hide:function(){this.element.hide();
this.deactivate();
},_setPosition:function(){if(this.element.is(":visible")){this.element.position($.extend({of:this.options.base},this.options.position));
}},_status:function(){if(this.options.disabled){this.detail.removeClass("list").addClass("disable");
return;
}else{this.detail.removeClass("disable");
}this.detail[this.ul.is(":empty")?"removeClass":"addClass"]("list");
}});
}(jQuery));
(function($,undefined){$.widget("ui.njSuggest",$.ui.suggest,{options:{plusWidth:0},_create:function(){var suggestLayer='<!-- Suggest Layer --><div id="smartSearchLayer" data-na="NA:suggest" class="suggestLayer MdSuggest01" style="display:none"><!--NA:suggest--><div class="suggestDtl list"><ul class="_resultBox1"></ul></div><!-- / .MdSuggest01 --></div>';
$("body").append(suggestLayer);
var _super=new $.ui.suggest;
this._create=_super._create;
this._create();
this._setDisplay();
},_setDisplay:function(){this.element.focus($.proxy(function(e){this.element.parent().parent().addClass("ExSelected");
},this)).focusout($.proxy(function(e){if(this.element.val().length<1){this.element.parent().parent().removeClass("ExSelected");
}},this));
},open:function(){var ul=this.menu.ul;
if(ul.children().length>0){this.menu.show();
}var sEle=this.element.parent().parent();
var _top=sEle.outerHeight()+sEle.offset().top-1;
var _width=sEle.outerWidth()+this.option("plusWidth")-1;
$(this.menu.element).css({top:_top,width:_width,left:sEle.offset().left});
}});
}(jQuery));
nj.getPackage("nj.matome.suggest",(function(){var options={issuggest:true,params:{official:"1"}};
return{options:{},init:function(oOptions){var o=$.extend(this.options,options,oOptions);
if(o.issuggest){this._initSuggest(o.params);
}$("#searchForm").submit(function(e){return false;
});
},_initSuggest:function(oParams){var _this=this;
var _data_max_length=5;
var q=$("#q").njSuggest({layerId:"smartSearchLayer",layerToggle:".mdHeadSearch01Btn02",layerSize:".mdHeadSearch01InputInner",cookieDomain:"naver.jp",cookieName:"NaverSuggestUse",autofocus:false,plusWidth:$("#searchForm").find("input[type=button]").width(),source:function(request,response){var oData={q:fnMatome.trim(request.term,true)};
$.extend(true,oData,oParams);
$.ajax({url:_this.options.Url+"/ac",dataType:"jsonp",jsonp:"_callback",data:oData,success:function(json){var items=json.items;
if(items[0].length<1){response([]);
$("#smartSearchLayer").hide();
}else{_data=[];
var aItems=[];
aItems=items[0].concat(items[1]).slice(0,_data_max_length);
$.each(aItems,function(i,v){if(typeof v!=="undefined"&&v){if(i>=_data_max_length||!v[0]){return;
}var _aTempInfo=v[1].split("{naver}");
_data.push([$.trim(v[0]).replace("$","$$"),_aTempInfo[0],_aTempInfo[1],_aTempInfo[2],_aTempInfo[3],_aTempInfo[4],_aTempInfo[5]]);
}});
response(_data);
}}});
},select:function(event,ui){$("#q").val(ui.item.value);
event.stopPropagation();
var _keyword=fnMatome.trim(ui.item.value,true);
_this._search(_keyword);
return false;
}});
$("INPUT.mdHeadSearch01Btn01").click(function(e){var _keyword=fnMatome.trim($("#q").val(),true);
if(_keyword!==""){window.location.href="/search?q="+encodeURIComponent(_keyword);
}else{window.location.href=getNullQueryReferencePage();
}return false;
});
$(document).bind("click.matome_suggest",function(e){var isLayer=false;
$.each(["mdHeadSearch01Btn02","guideText02","mdHeadSearch01InputTxt"],function(){isLayer=$(e.target).hasClass(this)||isLayer;
});
if(!isLayer){$("#smartSearchLayer").hide();
}});
},_search:function(sKeyword){if(sKeyword===""){window.location.href=getNullQueryReferencePage();
}else{window.location.href="/search?q="+encodeURIComponent(sKeyword);
}}};
})());


/* @release 1382429670 */