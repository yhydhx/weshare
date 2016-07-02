//SYSLIB
//ver 20130721.01
//last modified: scientihark
var SYSLIB_base=function(){
	var $this=this;
	//SYSLIB Base Utils
	//Namespace
	this.namespaces={};
	this.namespace=function(ns){
		//##########################
		//U:$ns=sys.namespace("namespacename.namespacename");
		//R:namespaces,if it's empty return empty function;
		//##########################
		var $ns=ns.split(".");
		var opns=$this.namespaces[$ns[0]];
		if(typeof(opns) != 'function'){
            $this.namespaces[$ns[0]]=function(){};
			opns=$this.namespaces[$ns[0]];
		}
		for(var $i=1;$i<$ns.length;$i++){
			if(typeof(opns[$ns[$i]]) != 'function'){
            	opns[$ns[$i]]=function(){};
			}
			opns=opns[$ns[$i]];
		}
		return opns;
	}
	this.setnamespace=function(ns,func){
		var $ns=ns.split(".");
		var opns=$this.namespaces[$ns[0]];
		if(typeof(opns) != 'function'){
            $this.namespaces[$ns[0]]=function(){};
			opns=$this.namespaces[$ns[0]];
		}
		for(var $i=1;$i<$ns.length;$i++){
			if(typeof(opns[$ns[$i]]) != 'function'){
            	opns[$ns[$i]]=function(){};
			}
			opns=opns[$ns[$i]];
		}
		opns=new func.constructor();
	}
	//include
	this.included={};
	this.includePath='';
	this.include=function(file) {
        var files = typeof file == "string" ? [file]:file;
        for (var i = 0; i < files.length; i++) {
			var $ttp=files[i].split("#");
			if($ttp[1]=="!"){
				//If use name#! the file will be loaded agai
				$this.included[$this.includePath+$ttp[0]]=0;
			}
			//check if already included.
			if(!$this.included[$this.includePath+$ttp[0]]){
				var name = $ttp[0].replace(/^\s|\s$/g, "");
				var att = name.split('.');
				var ext = att[att.length - 1].toLowerCase();
				var isCSS = ext == "css";
				var tag = isCSS ? "link" : "script";
				var $newnode=document.createElement(tag);
				var link = $this.includePath + name;
				if(isCSS){
					$newnode.setAttribute("rel","stylesheet");
					$newnode.setAttribute("href",link);
				}else{
					$newnode.setAttribute("src",link);
				}
				document.body.appendChild($newnode);
				$this.included[$this.includePath+$ttp[0]]=1;
			}
        }
	};
	this.exclude=function removejscssfile(filename, filetype){
		 var targetelement=(filetype=="js")? "script" : (filetype=="css")? "link" : "none" //determine element type to create nodelist from
		 var targetattr=(filetype=="js")? "src" : (filetype=="css")? "href" : "none" //determine corresponding attribute to test for
		 var allsuspects=document.getElementsByTagName(targetelement)
		 for (var i=allsuspects.length; i>=0; i--){ //search backwards within nodelist for matching elements to remove
		  		if (allsuspects[i] && allsuspects[i].getAttribute(targetattr)!=null && allsuspects[i].getAttribute(targetattr).indexOf(filename)!=-1)
		   			allsuspects[i].parentNode.removeChild(allsuspects[i]) //remove element by calling parentNode.removeChild()
		 }
	}
	this.baseurl=(window.location.href).split("#")[0];
}
var SYSLIB=new SYSLIB_base();
var SYSLIB_utils=SYSLIB.namespace("syslib.utils");
SYSLIB_utils.errors={};
SYSLIB_utils.error=function(errorMessage, errorUrl, errorLine) {
	var id=SYSLIB_base64.encode(errorMessage+errorUrl+errorLine);
	if(SYSLIB_utils.errors[id]){
		SYSLIB_utils.errors[id].repeat++;
	}else{
		var uscreen={
			x:screen.availWidth,
			y:screen.availHeight,
			color:screen.colorDepth,
			pixel:screen.pixelDepth
		}
		SYSLIB_utils.errors[id]={repeat:0,data:errorMessage,path:errorUrl,line:errorLine,dom:(document.documentElement.innerHTML),screen:uscreen,sysvar:$SYSVARS};
	}
	return true;
}
window.onerror = SYSLIB_utils.error;
//DOM

var SYSLIB_dom=SYSLIB.namespace("syslib.dom");
SYSLIB_dom.domcache={
	allnodes:[],
	byid:{},
	byclass:{},
	bytag:{},
	byattr:{}
};
SYSLIB_dom.freshdomcache=function(){
	SYSLIB_dom.domcache={
		allnodes:[],
		byid:{},
		byclass:{},
		bytag:{},
		byattr:{}
	}
	SYSLIB_dom.findall(document.body);
}
SYSLIB_dom.findall=function(father){
	if(father.tagName){
		var $list=father.childNodes;
		SYSLIB_dom.domcache.allnodes.push(father);
		if($list){
			if($list.length>0){
				var $i=0;
				for($i=0;$i<$list.length;$i++){
					SYSLIB_dom.findall($list[$i]);
				}
			}else{
				SYSLIB_dom.findall($list);
			}
		}
	}
}
//DOM.find
SYSLIB_dom.find=function(ipt,from){
	this.findthis=function(ipt,from){
		var $query=ipt.split("#"),$nodes=0;
		
		if($query[1]){
			if(!from){
				$nodes=(SYSLIB_dom.domcache.byid[$query[1]])?SYSLIB_dom.domcache.byid[$query[1]]:document.getElementById($query[1]);
				$nodes=($nodes)?$nodes:0;
				if($nodes){
					SYSLIB_dom.domcache.byid[$query[1]]=$nodes;
				}
				return $nodes;
			}else{
				var $nodesn=[];
				for(var $uu=0;$uu<from.length;$uu++){
					$nodes=from[$uu];
					if($nodes.id&&$nodes.id==$query[1]){
						$nodesn.push($nodes);
					}
				}
				return $nodesn;
			}
		}
		$query=ipt.split(".");
		if($query[1]){
			if(!from){
				$nodes=(SYSLIB_dom.domcache.byclass[$query[1]])?SYSLIB_dom.domcache.byclass[$query[1]]:document.getElementsByClassName($query[1]);
				$nodes=($nodes)?$nodes:0;
				if($nodes){
					SYSLIB_dom.domcache.byclass[$query[1]]=$nodes;
				}
				return $nodes;
			}else{
				var $nodesn=[];
				for(var $uu=0;$uu<from.length;$uu++){
					$nodes=from[$uu];
					if($nodes.className&&$nodes.className==$query[1]){
						$nodesn.push($nodes);
					}
				}
				return $nodesn;
			}
		}
		$query=ipt.split("<");
		if($query[1]){
			$query=$query[1].split(">");
			if(!from){
				$nodes=(SYSLIB_dom.domcache.bytag[$query[0]])?SYSLIB_dom.domcache.bytag[$query[0]]:document.getElementsByTagName($query[0]);
				$nodes=($nodes)?$nodes:0;
				if($nodes){
					SYSLIB_dom.domcache.bytag[$query[0]]=$nodes;
				}
				return $nodes;
			}else{
				var $nodesn=[];
				for(var $uu=0;$uu<from.length;$uu++){
					$nodes=from[$uu];
					if($nodes.tagName&&(($nodes.tagName).toUpperCase())==(($query[0]).toUpperCase())){
						$nodesn.push($nodes);
					}
				}
				return $nodesn;
			}
		}
		$query=ipt.split("=");
		if($query[1]){
			$query[1]=$query[1].split("]")[0];
			$query[0]=$query[0].split("[")[1];
			if(!from){
				if(SYSLIB_dom.domcache.byattr[$query[0]]){
					$nodes=SYSLIB_dom.domcache.byattr[$query[0]];
				}else{
					if(!SYSLIB_dom.domcache.allnodes||SYSLIB_dom.domcache.allnodes.length==0){
						SYSLIB_dom.freshdomcache();
					}
					for(var $k=0;$k<SYSLIB_dom.domcache.allnodes.length;$k++){
						var $yy=SYSLIB_dom.domcache.allnodes[$k];
						if($yy.getAttribute($query[0])&&$yy.getAttribute($query[0])==$query[1]){
							if(!$nodes){
								$nodes=[];
							}
							$nodes.push($yy);
						}
					}
				}
				//$nodes=(SYSLIB_dom.domcache.bytag[$query[1]])?SYSLIB_dom.domcache.byclass[$query]:document.getElementsByClassName($query);
				$nodes=($nodes)?$nodes:0;
				if($nodes){
					SYSLIB_dom.domcache.byattr[$query[0]]=$nodes;
				}
				return $nodes;
			}else{
				var $nodesn=[];
				for(var $uu=0;$uu<from.length;$uu++){
					$nodes=from[$uu];
					if($nodes.getAttribute&&$nodes.getAttribute($query[0])&&$nodes.getAttribute($query[0])==($query[1])){
						$nodesn.push($nodes);
					}
				}
				return $nodesn;
			}
		}
	}
	//##########################
	//U:$dom=dom.find("bellow");
	//#id or .class or <tag> or [attr=val] mutil arg must use &&.
	//E.G. "<div>&&.ffg&&[type=ll]"
	//Do not support RE FOR NOW !
	//R:dom node(s) or 0;
	//##########################
	var $i=0,$j=0;
	if(!from){
		var $k=0;
	}else{
		var $k=from;
	}
	if(ipt.indexOf("&&")>0){
		$j=ipt.split("&&");
		for($i=0;$i<$j.length;$i++){
			$k=this.findthis($j[$i],$k);
			if(!$k){
				return 0;
			}
		}
		return $k;
	}else{
		return this.findthis(ipt,$k);
	}
}
SYSLIB_dom.search=function(ipt,from){
	this.searchthis=function(ipt,from){
		var $query=ipt.split("#"),$nodes=0;
		if(!from){
			var from=SYSLIB_dom.domcache.allnodes;	
		}
		if($query[1]){
			var $nodesn=[];
			for(var $uu=0;$uu<from.length;$uu++){
				$nodes=from[$uu];
				if($nodes.id&&($nodes.id).match($query[1])){
					$nodesn.push($nodes);
				}
			}
			return $nodesn;
		}
		$query=ipt.split(".");
		if($query[1]){
			var $nodesn=[];
			for(var $uu=0;$uu<from.length;$uu++){
				$nodes=from[$uu];
				if($nodes.className&&($nodes.className).match($query[1])){
					$nodesn.push($nodes);
				}
			}
			return $nodesn;
		}
		$query=ipt.split("<");
		if($query[1]){
			$query=$query[1].split(">");
			var $nodesn=[];
			for(var $uu=0;$uu<from.length;$uu++){
				$nodes=from[$uu];
				if($nodes.tagName&&(($nodes.tagName).toUpperCase()).match($query[0])){
					$nodesn.push($nodes);
				}
			}
			return $nodesn;
		}
		$query=ipt.split("=");
		if($query[1]){
			$query[1]=$query[1].split("]")[0];
			$query[0]=$query[0].split("[")[1];
			var $nodesn=[];
			for(var $uu=0;$uu<from.length;$uu++){
				$nodes=from[$uu];
				if($nodes.getAttribute&&$nodes.getAttribute($query[0])&&($nodes.getAttribute($query[0])).match($query[1])){
					$nodesn.push($nodes);
				}
			}
			return $nodesn;
		}
	}
	//##########################
	//U:$dom=dom.search("bellow");
	//#id or .class or <tag> or [attr=val] mutil arg must use &&.
	//id / class / tag / val is in RE
	//Only support RE FOR NOW !
	//R:dom node(s) or 0;
	//##########################
	var $i=0,$j=0;
	if(!from){
		var $k=0;
		if(!SYSLIB_dom.domcache.allnodes||SYSLIB_dom.domcache.allnodes.length==0){
			SYSLIB_dom.freshdomcache();
		}
	}else{
		var $k=from;
	}
	if(ipt.indexOf("&&")>0){
		$j=ipt.split("&&");
		for($i=0;$i<$j.length;$i++){
			$k=this.searchthis($j[$i],$k);
			if(!$k){
				return 0;
			}
		}
		return $k;
	}else{
		return this.searchthis(ipt,$k);
	}
}
//dom.searchcontent
SYSLIB_dom.searchcontent=function(ipt,from){
	if(!from){
			if(!SYSLIB_dom.domcache.allnodes||SYSLIB_dom.domcache.allnodes.length==0){
				SYSLIB_dom.freshdomcache();
			}
			var from=SYSLIB_dom.domcache.allnodes;	
	}
	var $nodesn=[];
	for(var $uu=0;$uu<from.length;$uu++){
		$nodes=from[$uu];
		if($nodes.innerHTML&&($nodes.innerHTML).match(ipt)){
			$nodesn.push($nodes);
		}
	}
	return $nodesn;
}
//dom.class
SYSLIB_dom.class=function(domnodes){
	if(!domnodes){
			return;
	}
	var $this={};
	$this.domnode=domnodes;
	if(!$this.domnode.length){
		$this.domnode=[$this.domnode];
	}
	$this.has=function(ipt){
		var $hasclass=true;
		var ipt=ipt.split(" ");
		for(var $i=0;$i<$this.domnode.length;$i++){
			var domnode=$this.domnode[$i];
			var $thisclassName=(domnode.className).split(" ");
			if(!SYSLIB_math.has($thisclassName,ipt)){
				$hasclass=false;
			}
		}
		return true;
	}
	$this.get=function(ipt){
		var $nodesclasslist=[];
		for(var $i=0;$i<$this.domnode.length;$i++){
			var domnode=$this.domnode[$i];
			var $thisclassName=(domnode.className).split(" ")||"";
			for(var $j=0;$j<$thisclassName.length;$j++){
				if($nodesclasslist.indexOf($thisclassName[$j])<0){
					if($thisclassName[$j]!=""){
						$nodesclasslist.push($thisclassName[$j]);
					}
				}
			}
		}
		return $nodesclasslist;
	}
	$this.add=function(ipt){
		var ipt=ipt.split(" ");
		for(var $i=0;$i<$this.domnode.length;$i++){
			var domnode=$this.domnode[$i];
			var $thisclassName=(domnode.className).split(" ");
			$thisclassName=($thisclassName!="")?$thisclassName:[];
			for(var $j=0;$j<ipt.length;$j++){
				if(!SYSLIB_math.has($thisclassName,[ipt[$j]])){
					if($thisclassName.length){
						$thisclassName.push(ipt[$j]);
					}else{
						$thisclassName=[ipt[$j]];
					}
				}
			}
			domnode.className=$thisclassName.join(" ");
		}
		
	}
	$this.remove=function(ipt){
		var ipt=ipt.split(" ");
		for(var $i=0;$i<$this.domnode.length;$i++){
			var domnode=$this.domnode[$i];
			var $thisclassName=(domnode.className).split(" ")||"";
			for(var $j=0;$j<ipt.length&&$thisclassName;$j++){
				if(SYSLIB_math.has($thisclassName,[ipt[$j]])){
					$thisclassName.splice($thisclassName.indexOf(ipt[$j]),1);
				}
			}
			domnode.className=$thisclassName.join(" ");
		}
	}
	$this.replace=function(ipt,to){
		var ipt=ipt.split(" ");
		var to=to.split(" ");
		for(var $i=0;$i<$this.domnode.length;$i++){
			var domnode=$this.domnode[$i];
			var $thisclassName=(domnode.className).split(" ");
			$thisclassName=($thisclassName!="")?$thisclassName:[];
			if($thisclassName!=[]){
				var $hasipt=1;
				for(var $j=0;$j<ipt.length;$j++){
					if(!SYSLIB_math.has($thisclassName,[ipt[$j]])){
						$hasipt=0;
					}
				}
				if($hasipt){
					for(var $j=0;$j<ipt.length;$j++){
						if($thisclassName.indexOf(ipt[$j])>=0){
							$thisclassName.splice($thisclassName.indexOf(ipt[$j]),1);
						}
					}
					for(var $j=0;$j<to.length;$j++){
						if($thisclassName.indexOf(to[$j])<0){
							if($thisclassName.length){
								$thisclassName.push(to[$j]);
							}else{
								$thisclassName=[to[$j]];
							}
						}
					}
					domnode.className=$thisclassName.join(" ");
				}
			}
		}
	}
	return $this;
}
//dom.searchcontent
SYSLIB_dom.checkFather=function(that,e){
	var parent = e.relatedTarget;
         try {
            while ( parent && parent !== that ) {
                parent = parent.parentNode; 
            }
            return (parent !== that);
        } catch(e) { }
}
//STYLE
var SYSLIB_style=SYSLIB.namespace("syslib.style");
SYSLIB_style.globalposition= function(node) {
            var $d = node,$c={x:0,y:0};
            for (; null != $d ;) {
                $c.x += $d.offsetLeft;
                $c.y += $d.offsetTop;
                $d = $d.offsetParent
            }
            return $c
};
//MATH
var SYSLIB_math=SYSLIB.namespace("syslib.math");
SYSLIB_math.sqrsumall= function(num) {
            var $opt =0;
            for (var $i =1;$i<num;$i++) {
               $opt =$opt+($i*$i);
            }
            return $opt
};
SYSLIB_math.funcsumall= function(num,func) {
            var $opt =0;
            for (var $i =1;$i<num;$i++) {
               $opt =$opt+func($i);
            }
            return $opt
};
SYSLIB_math.has= function($a,$b) {
            var $has=0;
			$a=($a.length)?$a:[$a];
			$b=($b.length)?$b:[$b];
			for(var $j=0;$j<$a.length;$j++){
				for(var $k=0;$k<$b.length;$k++){
					if($a[$j]==$b[$k]){
						$has++;
					}
				}
			}
            return ($has>=$b.length)
};
SYSLIB_math.rand= function(min,max,length) {
		var $rand=min+(Math.random() * (max-min));
		if(length){
			if(length>0){
				$rand=($rand.toString()).split(".");
				$rand[1]=$rand[1].substr(0,length);
				$rand=$rand.join(".");
				return parseFloat($rand);
			}else{
				return $rand;
			}
		}else{
            return Math.floor($rand);
		}
};
//ANIMATION
var SYSLIB_ani=SYSLIB.namespace("syslib.animation");
SYSLIB_ani.bind=function(node){
	var $this=this;
	this.node=node;
	this.x=parseInt(this.node.style.left);
	this.y=parseInt(this.node.style.top);
	this.nowx=this.x;
	this.nowy=this.y;
	this.destx=this.x;
	this.desty=this.y;
	this.delx=0;
	this.dely=0;
	this.func=0;
	this.dur=500;
	this.delay=0;
	this.isani=0;
	this.timekick=50;
	this.callback=0;
	this.pcallback=0;
	this.counter=0;
	this.pointscounter=0;
	this.plist=0;
	this.allkick=0;
	this.fulldelx=0;
	this.fulldely=0;
	this.moveto=function(newx,newy,func,dur,delay,timekick,callback){
		$this.destx=newx;
		$this.desty=newy;
		if(callback){
			$this.callback=callback;
		}
		if(dur){
			$this.dur=dur;
		}
		if(delay){
			$this.delay=delay;
		}
		if(timekick){
			$this.timekick=timekick;
		}
		if(typeof(func)=="function"){
			$this.func=func;
		}else{
			$this.func=$this.funcs[func];
		}
		if(!func){
			return;
			//##########################
			//TODO
			//DATE:20130319
			//BY:scientihark
			//TO:Anyone
			//##########
			//1.ADD SysBuger DEV report
			//##########################
		}
		$this.isani=1;
		$this.counter=0;
		$this.fulldelx=$this.destx-$this.x;
		$this.fulldely=$this.desty-$this.y;
		var $tt=$this.moving;
		setTimeout($tt,$this.delay)
	}
	this.moving=function(){
		$this.func();
		$this.nowx+=$this.delx;
		$this.nowy+=$this.dely;
		$this.node.style.left=$this.nowx+"px";
		$this.node.style.top=$this.nowy+"px";
		if((($this.nowx-$this.destx)*$this.delx>=0)&&(($this.nowy-$this.desty)*$this.dely>=0)){
			$this.x=parseInt($this.node.style.left);
			$this.y=parseInt($this.node.style.top);
			if($this.callback){
				$this.callback();
			}
			$this.isani=0;
		}else{
			
			var $tt=$this.moving;
			setTimeout($tt,$this.timekick)
		}
	}
	this.movetopoints=function(plist,func,delay,timekick,callback){
		var $tt=$this.movetopoints;
		if($this.pointscounter==0){
			$this.plist=plist;
			if(callback){
				$this.pcallback=callback;
			}
			if(delay){
				$this.delay=delay;
			}
			if(timekick){
				$this.timekick=timekick;
			}
			if(typeof(func)=="function"){
				$this.func=func;
			}else{
				$this.func=$this.funcs[func];
			}
			if(!func){
				return;
				//##########################
				//TODO
				//DATE:20130319
				//BY:scientihark
				//TO:Anyone
				//##########
				//1.ADD SysBuger DEV report
				//##########################
			}
			
		}
		if($this.pointscounter>=$this.plist.length){
			if($this.pcallback){
				$this.pcallback();
			}
			$this.pointscounter=0;
			$this.plist=0;
			return;
		}
		var newx=$this.plist[$this.pointscounter][0];
		var newy=$this.plist[$this.pointscounter][1];
		var func=$this.plist[$this.pointscounter][2];
		var dur=$this.plist[$this.pointscounter][3];
		var delay=$this.plist[$this.pointscounter][4];
		func=(func)?func:$this.func;
		$this.pointscounter++;
		$this.moveto(newx,newy,func,dur,delay,$this.timekick,$tt)
	}
	this.funcs={
		"Linear":function(){
			if(!$this.allkick){
				$this.allkick=$this.dur/$this.timekick;
			}
			$this.delx=$this.fulldelx/$this.allkick;
			$this.dely=$this.fulldely/$this.allkick;
		},
		"easeIn":function(){
			if(!$this.allkick){
				$this.allkick=$this.dur/$this.timekick;
				$this.allkick=SYSLIB_math.sqrsumall($this.allkick);
			}
			$this.counter++;
			$this.delx=($this.fulldelx/$this.allkick)*($this.counter*$this.counter);
			$this.dely=($this.fulldely/$this.allkick)*($this.counter*$this.counter);
		},
		"easeOut":function(){
			if(!$this.allkick){
				$this.allkick=$this.dur/$this.timekick;
				$this.counter=$this.allkick;
				$this.allkick=SYSLIB_math.sqrsumall($this.allkick);
			}
			$this.counter--;
			$this.delx=($this.fulldelx/$this.allkick)*($this.counter*$this.counter);
			$this.dely=($this.fulldely/$this.allkick)*($this.counter*$this.counter);
		},
		"easeInOut":function(){
			if(!$this.allkick){
				$this.allkick=$this.dur/$this.timekick;
				$this.counter=$this.allkick/2;
				$this.allkick=SYSLIB_math.sqrsumall($this.allkick);
			}
			$this.counter--;
			$this.delx=($this.fulldelx/$this.allkick)*($this.counter*$this.counter);
			$this.dely=($this.fulldely/$this.allkick)*($this.counter*$this.counter);
		}
	};
}
//Model
var SYSLIB_model=SYSLIB.namespace("syslib.model");
SYSLIB_model.t=function(name){
	return SYSLIB_model.list[name];
};
SYSLIB_model.list={};
SYSLIB_model.add=function(name,html,required,initfunc,attrs,father,formats){
	if(SYSLIB_model.list[name]){
		////////////////////////
		//##########################
		//TODO
		//DATE:20130326
		//BY:scientihark
		//TO:Anyone
		//##########
		//1.ADD SysBuger DEV report
		//##########################
		return;
	}
	if(required){
		if(required.p){
			SYSLIB.includePath=required.p;
		}else{
			SYSLIB.includePath='';
		}
		SYSLIB.include(required.f);
	}
	if(!father){
		father=document.getElementById('sys_main_playground');
	}
	var $model=SYSLIB_model.build(name,html,initfunc,attrs,father,formats);
	SYSLIB_model.list[name]=$model;
}
SYSLIB_model.draw=function(name,ipts){
	SYSLIB_model.list[name].draw(ipts);
}
SYSLIB_model.setstatue=function(name,statue){
	SYSLIB_model.list[name].setstatue(statue);
}
SYSLIB_model.jump_to=function(mod,statue,setdata){
	if(SYS_hide_all_mod){
		SYS_hide_all_mod();
	}
	if(setdata){
		var tmp;
		for(tmp in setdata){
			var ii=tmp+"=\'"+setdata[tmp]+"\'";
			eval(ii);
		}
	}
	setTimeout(function(){
		_m(mod).to(statue);
	},600);
}
SYSLIB_model.build=function(name,html,initfunc,attrs,father,formats){
	var $this={};
	$this.html=html;
	$this.father=father;
	$this.id="SYS_MD_"+name;
	$this.node=document.createElement("div");
	
	$this.node.innerHTML=SYSLIB_base64.mutilstring(html,formats);
	$this.node.id=$this.id;
	$this.statues={};
	$this.name=name;
	$this.statue="";
	$this.laststatue="";
	$this.formats=formats;
	SYSLIB_ui.parse_scroll_nodes();
	if(initfunc){
			$this.initfunc=initfunc;
	}
	$this.rebuild=function(){
		$this.statue="";
		$this.laststatue="";
		$this.node.innerHTML=SYSLIB_base64.mutilstring($this.html,$this.formats);
		SYSLIB_ui.parse_scroll_nodes();
		SYSLIB_dom.freshdomcache();
		if($this.initfunc){
			$this.initfunc();
		}
	}
	$this.to=function(stname){
		var ty=SYSLIB_model.list[$this.name].statues[stname];
		if(!ty){
			return;
		}
		if(ty.file){
			SYSLIB_model.list[$this.name].statues[stname]=0;
			SYSLIB.includePath=ty.file.p;
			if(ty.file.p){
					SYSLIB.includePath=ty.file.p;
			}else{
					SYSLIB.includePath='';
			}
			if(ty.file.loadingani&&ty.file.loadingani.start){
				ty.file.loadingani.start();
			}
			var $stname=stname;
			SYSLIB.include(ty.file.f);
			var checkt=0;
			var tt=function check_loadok(a,b,c){
				if(SYSLIB_model.list[a.name].statues[b]){
					if(c.file.loadingani&&c.file.loadingani.ok){
						c.file.loadingani.ok();
					}
					var $a=a;
					setTimeout(function(){$a.to($stname);},2000)
					clearInterval(checkt);
					return;
				}
				console.log('nothis');
			};
			var $stname=stname;
			checkt=setInterval(function(){tt($this,$stname,ty);},500);
			
			return;
		}
		SYSLIB_model.list[$this.name].statues[stname]();
		SYSLIB_ui.parse_scroll_nodes();
		$this.statue=stname;
		if(stname!="hide"){
			$this.laststatue=stname;
		}
	}
	$this.addstatue=function(stname,stfunc,required,delyloadme){
		if(SYSLIB_model.list[$this.name].statues[stname]){
			//////////////////////
			//##########################
			//TODO
			//DATE:20130326
			//BY:scientihark
			//TO:Anyone
			//##########
			//1.ADD SysBuger DEV report
			//##########################
			return;
		}
		if(delyloadme){
			SYSLIB_model.list[$this.name].statues[stname]={file:delyloadme};
		}else{
			SYSLIB_model.list[$this.name].statues[stname]=stfunc;
			if(required){
				if(required.p){
					SYSLIB.includePath=required.p;
				}else{
					SYSLIB.includePath='';
				}
				SYSLIB.include(required.f);
			}
		}
		
	}
	if(attrs){
		for(var $attr in attrs){
			$this.node.setAttribute($attr,attrs[$attr]);
		}
	}
	father.appendChild($this.node);
	if($this.initfunc){
			$this.initfunc();
	}
	return $this;
}
//Model
var SYSLIB_codepresser=SYSLIB.namespace("syslib.codepresser");
SYSLIB_codepresser.decompress=function(ipt,cb,magiccode){
	var d=new Image;
	var $callbc=cb||function(){};
	d.onload=function(){
		var b=this.width,
			c=this.height;
		var a=document.createElement("canvas").getContext("2d");
		a.width=b;
		a.height=c;
		a.drawImage(this,0,0);
		b=a.getImageData(0,0,b,c).data;
		//console.log(b);
		$c="";
		for(a=0;a<b.length-4;a+=4){
			var $e=b[a];
			$c+=String.fromCharCode($e);
			$e=b[a+1];
			$c+=String.fromCharCode($e);
			$e=b[a+2];
			$c+=String.fromCharCode($e);
		}
		//eval(c);
		var $concode=$c;
		//console.log($c);
		var $out=[];
		for(var $i=0;$i<$concode.length;$i++){
			if($i&&$i%magiccode!=0){
				$out.push($concode[$i]);
			}
		}
		//console.log($out);
		$out=unescape(SYSLIB_base64.decode(SYSLIB_base64.utf16to8($out.join(""))));
		//console.log($out);
		$callbc($out);
	};
	d.src=ipt;
}
SYSLIB_codepresser.compress=function(code,magiccode){
		if(!magiccode){
			return;
		}
		var $concode=SYSLIB_base64.encode(SYSLIB_base64.utf8to16(escape(code)));
		console.log($concode);
		var $out=[];
		for(var $i=0;$i<$concode.length;$i++){
			$out.push($concode[$i]);
			if($i&&$i%magiccode==0){
				$out.push("s");
			}
		}
		$out=$out.join("");
		console.log($out);
		var a=document.createElement("canvas");
		document.body.appendChild(a);
		var e=a.getContext("2d");
		var tw=1024,th=parseInt($out.length/tw)+1;
		a.width=tw;
		a.height=th;
		b=e.getImageData(0,0,tw,th);
		var c=0,$i=0;
		for(c=0;c<b.data.length-4;c+=4,$i+=3){
			if($i<$out.length-3){
				b.data[c]=(typeof($out[$i])=="string")?$out[$i].charCodeAt(0):$out[$i];
				b.data[c+1]=(typeof($out[$i+1])=="string")?$out[$i+1].charCodeAt(0):$out[$i+1];
				b.data[c+2]=(typeof($out[$i+2])=="string")?$out[$i+2].charCodeAt(0):$out[$i+2];
				b.data[c+3]=255;
			}else{
				b.data[c]=0;
				b.data[c+1]=0;
				b.data[c+2]=0;
				b.data[c+3]=255;
			}
		}
		e.putImageData(b, 0, 0);
		//console.log(b);
		window.open(a.toDataURL('image/png'),"uu");
		document.body.removeChild(a);
}
var SYSLIB_base64=SYSLIB.namespace("syslib.base64");
SYSLIB_base64.EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
SYSLIB_base64.DecodeChars = new Array(
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
     -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
     52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,
     -1,   0,   1,   2,   3,   4,   5,   6,   7,   8,   9, 10, 11, 12, 13, 14,
     15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,
     -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
     41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);
SYSLIB_base64.decode=function(str) {
     var c1, c2, c3, c4;
     var i, len, out;

     len = str.length;
     i = 0;
     out = "";
     while(i < len) {
         // c1 
         do {
             c1 = SYSLIB_base64.DecodeChars[str.charCodeAt(i++) & 0xff];
         } while(i < len && c1 == -1);
         if(c1 == -1)
             break;

         // c2
         do {
             c2 = SYSLIB_base64.DecodeChars[str.charCodeAt(i++) & 0xff];
         } while(i < len && c2 == -1);
         if(c2 == -1)
             break;

         out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));

         // c3
         do {
             c3 = str.charCodeAt(i++) & 0xff;
             if(c3 == 61)
                 return out;
             c3 = SYSLIB_base64.DecodeChars[c3];
         } while(i < len && c3 == -1);
         if(c3 == -1)
             break;

         out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));

         // c4
         do {
             c4 = str.charCodeAt(i++) & 0xff;
             if(c4 == 61)
                 return out;
             c4 = SYSLIB_base64.DecodeChars[c4];
         } while(i < len && c4 == -1);
         if(c4 == -1)
             break;
         out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
     }
     return out;
}
SYSLIB_base64.encode=function(str) {
     var out, i, len;
     var c1, c2, c3;

     len = str.length;
     i = 0;
     out = "";
     while(i < len) {
         c1 = str.charCodeAt(i++) & 0xff;
         if(i == len)
         {
             out += SYSLIB_base64.EncodeChars.charAt(c1 >> 2);
             out += SYSLIB_base64.EncodeChars.charAt((c1 & 0x3) << 4);
             out += "==";
             break;
         }
         c2 = str.charCodeAt(i++);
         if(i == len)
         {
             out += SYSLIB_base64.EncodeChars.charAt(c1 >> 2);
             out += SYSLIB_base64.EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
             out += SYSLIB_base64.EncodeChars.charAt((c2 & 0xF) << 2);
             out += "=";
             break;
         }
         c3 = str.charCodeAt(i++);
         out += SYSLIB_base64.EncodeChars.charAt(c1 >> 2);
         out += SYSLIB_base64.EncodeChars.charAt(((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4));
         out += SYSLIB_base64.EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >>6));
         out += SYSLIB_base64.EncodeChars.charAt(c3 & 0x3F);
     }
     return out;
}

SYSLIB_base64.utf8to16=function(str) {
     var out, i, len, c;
     var char2, char3;

     out = "";
     len = str.length;
     i = 0;
     while(i < len) {
         c = str.charCodeAt(i++);
         switch(c >> 4)
         { 
           case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
             // 0xxxxxxx
             out += str.charAt(i-1);
             break;
           case 12: case 13:
             // 110x xxxx    10xx xxxx
             char2 = str.charCodeAt(i++);
             out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
             break;
           case 14:
             // 1110 xxxx   10xx xxxx   10xx xxxx
             char2 = str.charCodeAt(i++);
             char3 = str.charCodeAt(i++);
             out += String.fromCharCode(((c & 0x0F) << 12) |
                                            ((char2 & 0x3F) << 6) |
                                            ((char3 & 0x3F) << 0));
             break;
         }
     }

     return out;
}

SYSLIB_base64.utf16to8=function(str) {
     var out, i, len, c;

     out = "";
     len = str.length;
     for(i = 0; i < len; i++) {
         c = str.charCodeAt(i);
         if ((c >= 0x0001) && (c <= 0x007F)) {
             out += str.charAt(i);
         } else if (c > 0x07FF) {
             out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
             out += String.fromCharCode(0x80 | ((c >>   6) & 0x3F));
             out += String.fromCharCode(0x80 | ((c >>   0) & 0x3F));
         } else {
             out += String.fromCharCode(0xC0 | ((c >>   6) & 0x1F));
             out += String.fromCharCode(0x80 | ((c >>   0) & 0x3F));
         }
     }
     return out;
}
SYSLIB_base64.mutilstring=function(f,vals){　
    var rhtml=f.toString().replace(/^[^\/]+\/\*!?\s?/, '').replace(/\*\/[^\/]+$/, '');
	
		rhtml=rhtml.replace(/\%\$([0-9])*\%/g, function(match) {
			var r=match.replace(/\%/g,'');
			r=parseInt(r.replace(/\$/g,''));
			if(r&&vals&&typeof(vals[r-1])!=="undefined"){
				return vals[r-1];
			}
        	return match;
			
    	});
		rhtml=rhtml.replace(/\%\#([^\%]*)\%/g, function(match) {
			var r=match.replace(/\%/g,'');
			r=r.replace(/\#/g,'');
			if(r&&$SYS_LAN&&typeof($SYS_LAN[r])!=="undefined"){
				return $SYS_LAN[r];
			}
        	return match;
			
    	});
		
	return rhtml;
}
var SYSLIB_error=SYSLIB.namespace("syslib.error");
SYSLIB_error.getstring=function(errcode,$erript){
	if(SYSLIB_error.list[errcode]){
		var $tys=SYSLIB_error.list[errcode];
		if($erript){
			if(!$erript.length){
				$erript=[$erript];
			}
			for(var $i=0;$i<$erript.length;$i++){
				$tys=$tys.replace(new RegExp("%s"+$i,"gm"),$erript[$i]);
			}
		}
		return $tys;
	}
}
//SYSLIB.includePath="js/js/base/";
//SYSLIB.include("error.code.js");
//DOM
var SYSLIB_vilade=SYSLIB.namespace("syslib.vilade");
SYSLIB_vilade.viladelist={
	"email":function(ipt){
		// contributed by Scott Gonzalez: http://projects.scottsplayground.com/email_address_validation/
		return /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i.test(ipt);
	},
	"url":function(ipt){
		// contributed by Scott Gonzalez: http://projects.scottsplayground.com/iri/
		return /^(https?|s?ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(ipt);
	},
	"date":function(ipt){
		return !/Invalid|NaN/.test(new Date(ipt).toString());
	},
	"dateISO":function(ipt){
		
		return /^\d{4}[\/\-]\d{1,2}[\/\-]\d{1,2}$/.test(ipt);
	},
	"number":function(ipt){
		
		return /^-?(?:\d+|\d{1,3}(?:,\d{3})+)?(?:\.\d+)?$/.test(ipt);
	},
	"digits":function(ipt){
		
		return /^\d+$/.test(ipt);
	},
	"letterswithbasicpunc":function(ipt){
		
		return /^[a-z\-.,()'"\s]+$/i.test(ipt);
	},
	"alpha+numer":function(ipt){
		
		return /^\w+$/i.test(ipt);
	},
	"lettersonly":function(ipt){
		
		return /^[a-z]+$/i.test(ipt);
	},
	"nowhitespace":function(ipt){
		
		return /^\S+$/i.test(ipt);
	},
	"int":function(ipt){
		
		return /^-?\d+$/.test(ipt);
	},
	"+int":function(ipt){
		
		return /^[0-9]*[1-9][0-9]*$/.test(ipt);
	},
	"0+int":function(ipt){
		
		return /^\d+$/.test(ipt);
	},
	"0-int":function(ipt){
		
		return /^((-\d+)|(0+))$/.test(ipt);
	},
	"-int":function(ipt){
		
		return /^-[0-9]*[1-9][0-9]*$/.test(ipt);
	},
	"0+float":function(ipt){
		
		return /^\d+(\.\d+)?$/.test(ipt);
	},
	"+float":function(ipt){
		
		return /^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$/.test(ipt);
	},
	"0-float":function(ipt){
		
		return /^((-\d+(\.\d+)?)|(0+(\.0+)?))$/.test(ipt);
	},
	"-float":function(ipt){
		
		return /^(-(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*)))$/.test(ipt);
	},
	"float":function(ipt){
		
		return /^(-?\d+)(\.\d+)?$/.test(ipt);
	},
	"alpha":function(ipt){
		
		return /^[A-Za-z]+$/.test(ipt);
	},
	"ualpha":function(ipt){
		
		return /^[A-Z]+$/.test(ipt);
	},
	"lalpha":function(ipt){
		
		return /^[a-z]+$/.test(ipt);
	},
	"chinesemobile":function(ipt){
		
		return /^1[3|4|5|8][0-9]\d{4,8}$/.test(ipt);
	},
	"chineseid":function(idcard){
		var area={11:"北京",12:"天津",13:"河北",14:"山西",15:"内蒙古",21:"辽宁",22:"吉林",23:"黑龙江",31:"上海",32:"江苏",33:"浙江",34:"安徽",35:"福建",36:"江西",37:"山东",41:"河南",42:"湖北",43:"湖南",44:"广东",45:"广西",46:"海南",50:"重庆",51:"四川",52:"贵州",53:"云南",54:"西藏",61:"陕西",62:"甘肃",63:"青海",64:"宁夏",65:"新疆",71:"台湾",81:"香港",82:"澳门",91:"国外"}
		var idcard,Y,JYM;
		var S,M;
		var idcard_array = new Array();
		idcard_array = idcard.split("");
		//地区检验
		if(area[parseInt(idcard.substr(0,2))]==null){
			return false;//"身份证地区非法!"
		}
		//身份号码位数及格式检验
		switch(idcard.length){
			case 15:
				  if ( (parseInt(idcard.substr(6,2))+1900) % 4 == 0 || ((parseInt(idcard.substr(6,2))+1900) % 100 == 0 && (parseInt(idcard.substr(6,2))+1900) % 4 == 0 )){
					  ereg=/^[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$/;//测试出生日期的合法性
				  } else {
					  ereg=/^[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$/;//测试出生日期的合法性
				  }
				  if(ereg.test(idcard)) {
					  return true;
				  }else{
					  return false;//"身份证号码出生日期超出范围或含有非法字符!",
				  }
				  break;
			case 18:
				  //18位身份号码检测
				  //出生日期的合法性检查
				  //闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
				  //平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
				  if ( parseInt(idcard.substr(6,4)) % 4 == 0 || (parseInt(idcard.substr(6,4)) % 100 == 0 && parseInt(idcard.substr(6,4))%4 == 0 )){
				  		ereg=/^[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$/;//闰年出生日期的合法性正则表达式
				  } else {
				  		ereg=/^[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$/;//平年出生日期的合法性正则表达式
				  }
				  if(ereg.test(idcard)){//测试出生日期的合法性
				  		//计算校验位
						S = (parseInt(idcard_array[0]) + parseInt(idcard_array[10])) * 7
						+ (parseInt(idcard_array[1]) + parseInt(idcard_array[11])) * 9
						+ (parseInt(idcard_array[2]) + parseInt(idcard_array[12])) * 10
						+ (parseInt(idcard_array[3]) + parseInt(idcard_array[13])) * 5
						+ (parseInt(idcard_array[4]) + parseInt(idcard_array[14])) * 8
						+ (parseInt(idcard_array[5]) + parseInt(idcard_array[15])) * 4
						+ (parseInt(idcard_array[6]) + parseInt(idcard_array[16])) * 2
						+ parseInt(idcard_array[7]) * 1
						+ parseInt(idcard_array[8]) * 6
						+ parseInt(idcard_array[9]) * 3 ;
						Y = S % 11;
						M = "F";
						JYM = "10X98765432";
						M = JYM.substr(Y,1);//判断校验位
						if(M == idcard_array[17]) {
							return true;
						}else{
							return false;//"身份证号码校验错误!",
						}
				  }else{
					  return false;//"身份证号码出生日期超出范围或含有非法字符!",
				  }
				  break;
		default:
			return false;// "身份证号码位数不对!",
			break;
		}
		
	},
	"sysupass":function(ipt){
		
		return /^[0-9a-zA-Z\!\?\@\#\$\%\^\&\*\(\)\[\]\{\}\|\\]{6,64}$/.test(ipt);
	},
	"systag":function(ipt){
		
		return /^[0-9a-zA-Z\u4e00-\u9fa5]{1,64}$/.test(ipt);
	},
	"sysitemname":function(ipt){
		
		return /^[\S]{4,24}$/.test(ipt);
	},
	"chineseonly":function(ipt){
		return /^[\u4e00-\u9fa5]{1,}$/.test(ipt);
	},
	"sysuname":function(ipt){
		return /^[0-9a-zA-Z\u4e00-\u9fa5\_]{3,12}$/.test(ipt);
	}
}
SYSLIB_vilade.vilade=function(ipt,rule){
	if(SYSLIB_vilade.viladelist[rule]){
		return SYSLIB_vilade.viladelist[rule](ipt);
	}
}
//UI
var SYSLIB_ui=SYSLIB.namespace("syslib.ui");
SYSLIB_ui.checkbox=function(father,id,attrs,uis,captions,w,h,initalstatue,onclick,onhover,onblur,ondisable,onenable,onon,onoff){
	this.node=document.createElement("div");
	if(attrs){
		for(var $attr in attrs){
			this,node.setAttritube($attr,attrs[$attr]);
		}
	}
	var $this=this;
	this.id=id;
	this.node.id=id;
	this.initalstatue=initalstatue||0;
	this.on=0;
	this.statue=this.initalstatue;
	if(w){
		this.node.style.width=this.w+"px";
	}
	if(h){
		this.node.style.height=this.h+"px";
	}
	if(onon){
		this.onon=onon;
	}else{
		this.onon=function(){};
	}
	if(onoff){
		this.onoff=onoff;
	}else{
		this.onoff=function(){};
	}
	if(onclick){
		this.onclick=onclick;
	}else{
		this.onclick=function(){};
	}
	if(onhover){
		this.onhover=onhover;
	}else{
		this.onhover=function(){};
	}
	if(onblur){
		this.onblur=onblur;
	}else{
		this.onblur=function(){};
	}
	if(onclick){
		this.ondisable=ondisable;
	}else{
		this.ondisable=function(){};
	}
	if(onclick){
		this.onenable=onenable;
	}else{
		this.onenable=function(){};
	}
	this.captions=captions||["右边是复选框","","On"];
	
	this.node.style.overflow="hidden";
	if(!uis){
		var uis="blue";
	}
	this.ui=uis;
	this.uilist={
		"blue":[
			function(){
				$this.node.style.backgroundColor="#ddd";
				$this.node.style.minWidth="150px";
				$this.node.style.display="inline-block";
				$this.node.style.fontSize="18px";
				$this.node.style.border="solid 1px #666";
				$this.node.style.borderRadius="4px";
				_f("#"+$this.id+"_node").style.minWidth="50px";
				_f("#"+$this.id+"_node").style.display="inline-block";
				_f("#"+$this.id+"_node").style.padding="3px 10px 3px 10px";
				_f("#"+$this.id+"_node").style.textAlign="center";
				_f("#"+$this.id+"_node").style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.borderRadius="4px";
				_f("#"+$this.id+"_node").style.setProperty("-webkit-transition","all .5s ease-in-out");
				_f("#"+$this.id+"_node").style.setProperty("-moz-transition","all .5s ease-in-out");
				_f("#"+$this.id+"_node").style.setProperty("-ms-transition","all .5s ease-in-out");
				_f("#"+$this.id+"_node").style.setProperty("-o-transition","all .5s ease-in-out");
				_f("#"+$this.id+"_node").style.setProperty("transition","all .5s ease-in-out");
			},
			function(){
				$this.node.style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.backgroundColor="#eee";
				_f("#"+$this.id+"_node").style.color="#666";
				_f("#"+$this.id+"_node").style.border="solid 1px #666";
			},
			function(){
				$this.node.style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.backgroundColor="#eee";
				_f("#"+$this.id+"_node").style.color="#666";
				_f("#"+$this.id+"_node").style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.marginLeft="0px";
			},
			function(){
				$this.node.style.border="solid 1px rgb(43, 141, 233)";
				_f("#"+$this.id+"_node").style.backgroundColor="rgb(43, 141, 233)";
				_f("#"+$this.id+"_node").style.color="#eee";
				_f("#"+$this.id+"_node").style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.marginLeft="80px";
			},
			function(){
				
			},
			function(){
				
			}
		],
		"cos":[
			function(){
				
			},
			function(){
				
			},
			function(){
				
			},
			function(){
				
			},
			function(){
				
			}
		]
	}
	this.disable=function(){
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_hover","SYSLIB_UI_switch_disable");
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_click","SYSLIB_UI_switch_disable");
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_blur","SYSLIB_UI_switch_disable");
		$this.statue=-1;
		$this.node.innerHTML=$this.captions[0];
		this.ondisable();
		$this.uilist[$this.ui][$this.statue+2]();
	}
	this.enable=function(){
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_disable","SYSLIB_UI_switch_normal");
		$this.statue=$this.on;
		$this.onenable();
		$this.uilist[$this.ui][$this.on+2]();
	}
	this.hover=function(){
		if($this.statue==0||$this.statue==1){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_normal","SYSLIB_UI_switch_hover");
			$this.statue=2;
			$this.onhover();
			$this.uilist[$this.ui][$this.statue+2]();
		}
	}
	this.blur=function(){
		if($this.statue==2){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_hover","SYSLIB_UI_switch_blur");
			$this.statue=$this.on;
			$this.onblur();
			$this.uilist[$this.ui][$this.on+2]();
			setTimeout(function(){if($this.statue==1||$this.statue==0){$this.uilist[$this.ui][$this.on+2]();SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_blur","SYSLIB_UI_switch_normal");}},1000);
		}
	}
	this.click=function(){
		if($this.statue==2||$this.statue==1||$this.statue==0){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_hover","SYSLIB_UI_switch_click");
			$this.statue=3;
			$this.onclick();
			$this.uilist[$this.ui][$this.statue+2]();
		}
	}
	this.unclick=function(){
		if($this.statue==3){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_click","SYSLIB_UI_switch_hover");
			$this.on=($this.on==0)?1:0;
			$this.statue=$this.on;
			if($this.on==0){
				SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_on","SYSLIB_UI_switch_off");
			}else{
				SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_off","SYSLIB_UI_switch_on");
			}
			_f("#"+$this.id+"_node").innerHTML=$this.captions[1+$this.on];
			$this.uilist[$this.ui][$this.on+2]();
		}
	}
	this.node.innerHTML="<div id=\""+this.id+"_node\">"+($this.captions[1+$this.on])+"</div>";
	var uu=(["disable","normal","normal","hover","click"])[$this.statue+1];
	var uu2=(["on","off"])[$this.on];
	SYSLIB_dom.class($this.node).add("SYSLIB_UI_switch_"+uu);
	SYSLIB_dom.class($this.node).add("SYSLIB_UI_switch_"+uu2);
	father.appendChild(this.node);
	this.uilist[$this.ui][0]();
	this.uilist[$this.ui][this.statue+2]();
	this.node.addEventListener("mouseover",$this.hover,false);
	this.node.addEventListener("mouseout",$this.blur,false);
	this.node.addEventListener("mousedown",$this.click,false);
	this.node.addEventListener("mouseup",$this.unclick,false);
	return this;
}
SYSLIB_ui.bottom=function(father,id,attrs,uis,captions,w,h,initalstatue,onclick,onhover,onblur,ondisable,onenable){
	this.node=document.createElement("div");
	if(attrs){
		for(var $attr in attrs){
			this,node.setAttritube($attr,attrs[$attr]);
		}
	}
	var $this=this;
	this.id=id;
	this.node.id=id;
	this.initalstatue=initalstatue||0;
	this.statue=this.initalstatue;
	if(w){
		this.node.style.width=this.w+"px";
	}
	if(h){
		this.node.style.height=this.h+"px";
	}
	if(onclick){
		this.onclick=onclick;
	}else{
		this.onclick=function(){};
	}
	if(onhover){
		this.onhover=onhover;
	}else{
		this.onhover=function(){};
	}
	if(onblur){
		this.onblur=onblur;
	}else{
		this.onblur=function(){};
	}
	if(onclick){
		this.ondisable=ondisable;
	}else{
		this.ondisable=function(){};
	}
	if(onclick){
		this.onenable=onenable;
	}else{
		this.onenable=function(){};
	}
	this.captions=captions||["我被禁用了","我是按钮","鼠标在我上面","鼠标移出我","我被点击了"];
	
	this.node.style.overflow="hidden";
	if(!uis){
		var uis="blue";
	}
	this.ui=uis;
	this.uilist={
		"blue":[
			function(){
				$this.node.style.minWidth="100px";
				$this.node.style.display="inline-block";
				$this.node.style.padding="3px 10px 3px 10px";
				$this.node.style.textAlign="center";
				$this.node.style.fontSize="18px";
				$this.node.style.border="solid 1px #0BAAFF";
				$this.node.style.borderRadius="5px";
			},
			function(){
				$this.node.style.backgroundColor="#ddd";
				$this.node.style.color="#666";
				$this.node.style.border="solid 1px #0BAAFF";
			},
			function(){
				$this.node.style.backgroundColor="rgb(45,180,255)";
				$this.node.style.color="#eee";
				$this.node.style.border="solid 1px #0BAAFF";
			},
			function(){
				$this.node.style.backgroundColor="#0BAAFF";
				$this.node.style.color="#eee";
				$this.node.style.border="solid 1px #0BAAFF";
			},
			function(){
				$this.node.style.backgroundColor="rgb(45,180,255)";
				$this.node.style.color="#eee";
				$this.node.style.border="solid 1px #0BAAFF";
			}
		],
		"orange":[
			function(){
				$this.node.style.minWidth="100px";
				$this.node.style.display="inline-block";
				$this.node.style.padding="3px 10px 3px 10px";
				$this.node.style.textAlign="center";
				$this.node.style.fontSize="18px";
				$this.node.style.border="solid 1px #444";
				$this.node.style.borderRadius="5px";
			},
			function(){
				$this.node.style.backgroundColor="#ddd";
				$this.node.style.color="#666";
				$this.node.style.border="solid 1px #666";
			},
			function(){
				$this.node.style.backgroundColor="rgb(255,140,0)";
				$this.node.style.color="#eee";
				$this.node.style.border="solid 1px #EA8100";
			},
			function(){
				$this.node.style.backgroundColor="#EA8100";
				$this.node.style.color="#eee";
				$this.node.style.border="solid 1px #EA8100";
			},
			function(){
				$this.node.style.backgroundColor="rgb(103, 177, 247)";
				$this.node.style.color="#eee";
				$this.node.style.border="solid 1px #EA8100";
			}
		],
		"green":[
			function(){
				$this.node.style.minWidth="100px";
				$this.node.style.display="inline-block";
				$this.node.style.padding="3px 10px 3px 10px";
				$this.node.style.textAlign="center";
				$this.node.style.fontSize="18px";
				$this.node.style.border="solid 1px #444";
				$this.node.style.borderRadius="5px";
			},
			function(){
				$this.node.style.backgroundColor="#ddd";
				$this.node.style.color="#666";
				$this.node.style.border="solid 1px #666";
			},
			function(){
				$this.node.style.backgroundColor="#8FC41F";
				$this.node.style.color="#eee";
				$this.node.style.border="solid 1px #84B61C";
			},
			function(){
				$this.node.style.backgroundColor="#84B61C";
				$this.node.style.color="#eee";
				$this.node.style.border="solid 1px #84B61C";
			},
			function(){
				$this.node.style.backgroundColor="#8FC41F";
				$this.node.style.color="#eee";
				$this.node.style.border="solid 1px #84B61C";
			}
		],
		"cos":[
			function(){
				
			},
			function(){
				
			},
			function(){
				
			},
			function(){
				
			},
			function(){
				
			}
		]
	}
	this.disable=function(){
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_hover","SYSLIB_UI_bottom_disable");
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_click","SYSLIB_UI_bottom_disable");
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_blur","SYSLIB_UI_bottom_disable");
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_normal","SYSLIB_UI_bottom_disable");
		$this.statue=-1;
		$this.node.innerHTML=$this.captions[0];
		this.ondisable();
		$this.uilist[$this.ui][$this.statue+2]();
	}
	this.enable=function(){
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_disable","SYSLIB_UI_bottom_normal");
		$this.statue=0;
		$this.node.innerHTML=$this.captions[1];
		$this.onenable();
		$this.uilist[$this.ui][$this.statue+2]();
	}
	this.hover=function(){
		if($this.statue==0){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_normal","SYSLIB_UI_bottom_hover");
			$this.statue=1;
			$this.node.innerHTML=$this.captions[2];
			$this.onhover();
			$this.uilist[$this.ui][$this.statue+2]();
		}
	}
	this.blur=function(){
		if($this.statue==1){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_hover","SYSLIB_UI_bottom_blur");
			$this.statue=0;
			$this.node.innerHTML=$this.captions[3];
			$this.onblur();
			$this.uilist[$this.ui][$this.statue+2]();
			setTimeout(function(){if($this.statue==0){$this.uilist[uis][$this.statue]();SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_blur","SYSLIB_UI_bottom_normal");$this.node.innerHTML=$this.captions[1];}},1000);
		}
	}
	this.click=function(){
		if($this.statue==1){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_hover","SYSLIB_UI_bottom_click");
			$this.statue=2;
			$this.node.innerHTML=$this.captions[4];
			$this.onclick();
			setTimeout(function(){
				$this.unclick();
			},1000);
			$this.uilist[$this.ui][$this.statue+2]();
		}
	}
	this.unclick=function(){
		if($this.statue==2){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_bottom_click","SYSLIB_UI_bottom_hover");
			$this.statue=1;
			$this.node.innerHTML=$this.captions[2];
			$this.uilist[$this.ui][$this.statue+2]();
		}
	}
	this.uilist[$this.ui][0]();
	this.uilist[$this.ui][this.statue+2]();
	this.node.innerHTML=$this.captions[$this.statue+1];
	var uu=(["disable","normal","hover","click"])[$this.statue+1];
	SYSLIB_dom.class($this.node).add("SYSLIB_UI_bottom_"+uu);
	father.appendChild(this.node);
	this.node.addEventListener("mouseover",$this.hover,false);
	this.node.addEventListener("mouseout",$this.blur,false);
	this.node.addEventListener("mousedown",$this.click,false);
	this.node.addEventListener("mouseup",$this.unclick,false);
	return this;
}
SYSLIB_ui.switch=function(father,id,attrs,uis,captions,w,h,initalstatue,onclick,onhover,onblur,ondisable,onenable,onon,onoff){
	this.node=document.createElement("div");
	if(attrs){
		for(var $attr in attrs){
			this,node.setAttritube($attr,attrs[$attr]);
		}
	}
	var $this=this;
	this.id=id;
	this.node.id=id;
	this.initalstatue=initalstatue||0;
	this.on=0;
	this.statue=this.initalstatue;
	if(w){
		this.node.style.width=this.w+"px";
	}
	if(h){
		this.node.style.height=this.h+"px";
	}
	if(onon){
		this.onon=onon;
	}else{
		this.onon=function(){};
	}
	if(onoff){
		this.onoff=onoff;
	}else{
		this.onoff=function(){};
	}
	if(onclick){
		this.onclick=onclick;
	}else{
		this.onclick=function(){};
	}
	if(onhover){
		this.onhover=onhover;
	}else{
		this.onhover=function(){};
	}
	if(onblur){
		this.onblur=onblur;
	}else{
		this.onblur=function(){};
	}
	if(onclick){
		this.ondisable=ondisable;
	}else{
		this.ondisable=function(){};
	}
	if(onclick){
		this.onenable=onenable;
	}else{
		this.onenable=function(){};
	}
	this.captions=captions||["右边是个开关","Off","On"];
	
	this.node.style.overflow="hidden";
	if(!uis){
		var uis="blue";
	}
	this.ui=uis;
	this.uilist={
		"blue":[
			function(){
				$this.node.style.backgroundColor="#ddd";
				$this.node.style.minWidth="150px";
				$this.node.style.display="inline-block";
				$this.node.style.fontSize="18px";
				$this.node.style.border="solid 1px #666";
				$this.node.style.borderRadius="4px";
				_f("#"+$this.id+"_node").style.minWidth="50px";
				_f("#"+$this.id+"_node").style.display="inline-block";
				_f("#"+$this.id+"_node").style.padding="3px 10px 3px 10px";
				_f("#"+$this.id+"_node").style.textAlign="center";
				_f("#"+$this.id+"_node").style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.borderRadius="4px";
				_f("#"+$this.id+"_node").style.setProperty("-webkit-transition","all .5s ease-in-out");
				_f("#"+$this.id+"_node").style.setProperty("-moz-transition","all .5s ease-in-out");
				_f("#"+$this.id+"_node").style.setProperty("-ms-transition","all .5s ease-in-out");
				_f("#"+$this.id+"_node").style.setProperty("-o-transition","all .5s ease-in-out");
				_f("#"+$this.id+"_node").style.setProperty("transition","all .5s ease-in-out");
			},
			function(){
				$this.node.style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.backgroundColor="#eee";
				_f("#"+$this.id+"_node").style.color="#666";
				_f("#"+$this.id+"_node").style.border="solid 1px #666";
			},
			function(){
				$this.node.style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.backgroundColor="#eee";
				_f("#"+$this.id+"_node").style.color="#666";
				_f("#"+$this.id+"_node").style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.marginLeft="0px";
			},
			function(){
				$this.node.style.border="solid 1px rgb(43, 141, 233)";
				_f("#"+$this.id+"_node").style.backgroundColor="rgb(43, 141, 233)";
				_f("#"+$this.id+"_node").style.color="#eee";
				_f("#"+$this.id+"_node").style.border="solid 1px #666";
				_f("#"+$this.id+"_node").style.marginLeft="80px";
			},
			function(){
				
			},
			function(){
				
			}
		],
		"cos":[
			function(){
				
			},
			function(){
				
			},
			function(){
				
			},
			function(){
				
			},
			function(){
				
			}
		]
	}
	this.disable=function(){
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_hover","SYSLIB_UI_switch_disable");
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_click","SYSLIB_UI_switch_disable");
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_blur","SYSLIB_UI_switch_disable");
		$this.statue=-1;
		$this.node.innerHTML=$this.captions[0];
		this.ondisable();
		$this.uilist[$this.ui][$this.statue+2]();
	}
	this.enable=function(){
		SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_disable","SYSLIB_UI_switch_normal");
		$this.statue=$this.on;
		$this.onenable();
		$this.uilist[$this.ui][$this.on+2]();
	}
	this.hover=function(){
		if($this.statue==0||$this.statue==1){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_normal","SYSLIB_UI_switch_hover");
			$this.statue=2;
			$this.onhover();
			$this.uilist[$this.ui][$this.statue+2]();
		}
	}
	this.blur=function(){
		if($this.statue==2){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_hover","SYSLIB_UI_switch_blur");
			$this.statue=$this.on;
			$this.onblur();
			$this.uilist[$this.ui][$this.on+2]();
			setTimeout(function(){if($this.statue==1||$this.statue==0){$this.uilist[$this.ui][$this.on+2]();SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_blur","SYSLIB_UI_switch_normal");}},1000);
		}
	}
	this.click=function(){
		if($this.statue==2||$this.statue==1||$this.statue==0){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_hover","SYSLIB_UI_switch_click");
			$this.statue=3;
			$this.onclick();
			$this.uilist[$this.ui][$this.statue+2]();
		}
	}
	this.unclick=function(){
		if($this.statue==3){
			SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_click","SYSLIB_UI_switch_hover");
			$this.on=($this.on==0)?1:0;
			$this.statue=$this.on;
			if($this.on==0){
				SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_on","SYSLIB_UI_switch_off");
			}else{
				SYSLIB_dom.class($this.node).replace("SYSLIB_UI_switch_off","SYSLIB_UI_switch_on");
			}
			_f("#"+$this.id+"_node").innerHTML=$this.captions[1+$this.on];
			$this.uilist[$this.ui][$this.on+2]();
		}
	}
	this.node.innerHTML="<div id=\""+this.id+"_node\">"+($this.captions[1+$this.on])+"</div>";
	var uu=(["disable","normal","normal","hover","click"])[$this.statue+1];
	var uu2=(["on","off"])[$this.on];
	SYSLIB_dom.class($this.node).add("SYSLIB_UI_switch_"+uu);
	SYSLIB_dom.class($this.node).add("SYSLIB_UI_switch_"+uu2);
	father.appendChild(this.node);
	this.uilist[$this.ui][0]();
	this.uilist[$this.ui][this.statue+2]();
	this.node.addEventListener("mouseover",$this.hover,false);
	this.node.addEventListener("mouseout",$this.blur,false);
	this.node.addEventListener("mousedown",$this.click,false);
	this.node.addEventListener("mouseup",$this.unclick,false);
	return this;
}
SYSLIB_ui.pbar=function(father,id,attrs,uis,max,min,w,h,outputval){
	this.node=document.createElement("div");
	if(attrs){
		for(var $attr in attrs){
			this,node.setAttritube($attr,attrs[$attr]);
		}
	}
	var $this=this;
	this.min=min||0;
	this.max=max||100;
	this.w=w||300;
	this.h=h||20;
	this.val=0;
	this.id=id;
	this.node.id=id;
	this.node.style.width=this.w+"px";
	this.node.style.height=this.h+"px";
	this.node.style.position="absolute";
	this.node.style.overflow="hidden";
	this.outputval=outputval||function(){};
	if(!uis){
		uis="blue";
	}
	this.uilist={
		"blue":function(){
			$this.backnodes=document.createElement("div");
			$this.backnodes.style.width=($this.w-20)+"px";
			$this.backnodes.style.marginLeft="10px";
			$this.backnodes.style.height=($this.h-10)+"px";
			$this.backnodes.style.marginTop="5px";
			$this.backnodes.style.border="solid 2px rgba(43, 141, 233,0.8)";
			$this.backnodes.style.borderRadius="5px";
			$this.backnodes.style.cursor="pointer";
			$this.backnodes.style.position="absolute";
			$this.midnodes=document.createElement("div");
			$this.midnodes.style.width=$this.initalval+"px";
			$this.midnodes.style.marginLeft="14px";
			$this.midnodes.style.height=($this.h-14)+"px";
			$this.midnodes.style.marginTop="9px";
			$this.midnodes.style.backgroundColor="rgb(68, 159, 245)";
			$this.midnodes.style.borderRadius="3px";
			$this.midnodes.style.cursor="pointer";
			$this.midnodes.style.position="absolute";
			$this.topnodes=document.createElement("div");
			$this.topnodes.style.width="40px";
			$this.topnodes.style.top="9px";
			$this.topnodes.style.borderRadius="100px";
			$this.topnodes.style.marginLeft=(12+$this.initalval-38)+"px";
			$this.topnodes.style.height=($this.h-14)+"px";
			$this.topnodes.style.marginTop="0px";
			$this.topnodes.style.boxShadow="0 0 5px 1px rgba(103, 177, 247,0.3)";
			$this.topnodes.style.setProperty("background","-webkit-linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.setProperty("background","-moz-linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.setProperty("background","-ms-linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.setProperty("background","-o-linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.setProperty("background","linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.cursor="pointer";
			$this.topnodes.style.position="absolute";
		}
		,"black":function(){
			$this.backnodes=document.createElement("div");
			$this.backnodes.style.width=($this.w-20)+"px";
			$this.backnodes.style.marginLeft="10px";
			$this.backnodes.style.height=($this.h-10)+"px";
			$this.backnodes.style.marginTop="5px";
			$this.backnodes.style.border="solid 2px rgba(0, 0, 0,0.1)";
			$this.backnodes.style.borderRadius="5px";
			$this.backnodes.style.cursor="pointer";
			$this.backnodes.style.position="absolute";
			$this.midnodes=document.createElement("div");
			$this.midnodes.style.width=$this.initalval+"px";
			$this.midnodes.style.marginLeft="14px";
			$this.midnodes.style.height=($this.h-14)+"px";
			$this.midnodes.style.marginTop="9px";
			$this.midnodes.style.backgroundColor="#999";
			$this.midnodes.style.borderRadius="3px";
			$this.midnodes.style.cursor="pointer";
			$this.midnodes.style.position="absolute";
			$this.topnodes=document.createElement("div");
			$this.topnodes.style.width="40px";
			$this.topnodes.style.top="9px";
			$this.topnodes.style.borderRadius="100px";
			$this.topnodes.style.marginLeft=(12+$this.initalval-38)+"px";
			$this.topnodes.style.height=($this.h-14)+"px";
			$this.topnodes.style.marginTop="0px";
			$this.topnodes.style.boxShadow="0 0 5px 1px rgba(0, 0, 0,0.3)";
			$this.topnodes.style.setProperty("background","-webkit-linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.setProperty("background","-moz-linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.setProperty("background","-ms-linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.setProperty("background","-o-linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.setProperty("background","linear-gradient(left, rgba(255,255,255,0), rgba(255,255,255,0.7))");
			$this.topnodes.style.cursor="pointer";
			$this.topnodes.style.position="absolute";
		}
		,"white":function(){
			$this.backnodes=document.createElement("div");
			$this.backnodes.style.width=($this.w-20)+"px";
			$this.backnodes.style.marginLeft="10px";
			$this.backnodes.style.height=($this.h-10)+"px";
			$this.backnodes.style.marginTop="5px";
			$this.backnodes.style.border="solid 2px rgba(255,255,255,0.8)";
			$this.backnodes.style.borderRadius="5px";
			$this.backnodes.style.cursor="pointer";
			$this.backnodes.style.position="absolute";
			$this.midnodes=document.createElement("div");
			$this.midnodes.style.width=$this.initalval+"px";
			$this.midnodes.style.marginLeft="14px";
			$this.midnodes.style.height=($this.h-14)+"px";
			$this.midnodes.style.marginTop="9px";
			$this.midnodes.style.backgroundColor="rgb(255,255,255)";
			$this.midnodes.style.borderRadius="3px";
			$this.midnodes.style.cursor="pointer";
			$this.midnodes.style.position="absolute";
			$this.topnodes=document.createElement("div");
			$this.topnodes.style.width="40px";
			$this.topnodes.style.top="9px";
			$this.topnodes.style.borderRadius="100px";
			$this.topnodes.style.marginLeft=(12+$this.initalval-38)+"px";
			$this.topnodes.style.height=($this.h-14)+"px";
			$this.topnodes.style.marginTop="0px";
			$this.topnodes.style.boxShadow="0 0 5px 1px rgba(255,255,255,0.3)";
			$this.topnodes.style.setProperty("background","-webkit-linear-gradient(left, rgba(0, 0, 0,0), rgba(0, 0, 0,0.7))");
			$this.topnodes.style.setProperty("background","-moz-linear-gradient(left, rgba(0, 0, 0,0), rgba(0, 0, 0,0.7))");
			$this.topnodes.style.setProperty("background","-ms-linear-gradient(left, rgba(0, 0, 0,0), rgba(0, 0, 0,0.7))");
			$this.topnodes.style.setProperty("background","-o-linear-gradient(left, rgba(0, 0, 0,0), rgba(0, 0, 0,0.7))");
			$this.topnodes.style.setProperty("background","linear-gradient(left, rgba(0, 0, 0,0), rgba(0, 0, 0,0.7))");
			$this.topnodes.style.cursor="pointer";
			$this.topnodes.style.position="absolute";
		}
	}
	this.go=function(val){
		$this.val=val;
		if($this.val<$this.min||$this.val>$this.max){
			return;
		}
		$x=(($this.w-24)/($this.max-$this.min))*(val-$this.min);
		$this.midnodes.style.width=$x+"px";
		$this.topnodes.style.marginLeft=(12+$x-38)+"px";
		$this.outputval($this.val);
	}
	this.uilist[uis]();
	father.appendChild(this.node);
	this.node.appendChild($this.backnodes);
	this.node.appendChild($this.midnodes);
	this.node.appendChild($this.topnodes);
	this.val=0;
	this.midnodes.style.width="0px";
	this.topnodes.style.marginLeft="9px";
	this.node.addEventListener("select",function(){return false;},false);
	return this;
}
SYS_SCROLL_FUNC=0;
SYS_SCROLL_LOCK=0;
SYSLIB_ui.parse_scroll_nodes=function(){
	
	SYSLIB_dom.freshdomcache();
	var snodes=_f("[s_scroll=true]");
	if(!snodes){
		return;
	}
	for(var i=0;i<snodes.length;i++){
		var nownode=snodes[i];
		var n_w=nownode.clientWidth;
		var n_h=nownode.clientHeight;
		var t_w=nownode.scrollWidth;
		var t_h=nownode.scrollHeight;
		var needsw=nownode.getAttribute("s_scroll_x");
		needsw=(needsw=="true")?1:0;
		var needsh=nownode.getAttribute("s_scroll_y");
		needsh=(needsh=="true")?1:0;
		var needdy=nownode.getAttribute("s_scroll_dy");
		needdy=(needdy=="true")?1:0;
		var nhtml=nownode.innerHTML;
		nownode.innerHTML="";
		nownode.style.overflow="hidden";
		var n_data=document.createElement('div');
		n_data.innerHTML=nhtml;
		n_data.setAttribute("style","position:relative;top:0px;left:0px;width:100%;padding-right:8px;float:left;");
		nownode.appendChild(n_data);
		var n_bar_mom=document.createElement('div');
		n_bar_mom.setAttribute("style","position:relative;width:6px;background-color:rgba(0,0,0,0.5);height:"+(n_h-6)+"px;border-radius:5px;opacity:0;left:"+(n_w-6)+"px;margin-bottom:6px;");
		n_bar_mom.ondragstart=function(){return false;};
		nownode.appendChild(n_bar_mom);
		var n_bar_bar=document.createElement('div');
		n_bar_bar.setAttribute("style","position:relative;width:4px;background-color:rgba(0,0,0,0.5);border-radius:5px;padding-left:1px;height:0px;top:0px;");
		n_bar_mom.appendChild(n_bar_bar);
		var n_bar_mom_w=document.createElement('div');
		n_bar_mom_w.setAttribute("style","position:relative;width:"+(n_w-6)+"px;background-color:rgba(0,0,0,0.5);height:6px;border-radius:5px;opacity:0;top:-7px;");
		n_bar_mom_w.ondragstart=function(){return false;};
		nownode.appendChild(n_bar_mom_w);
		var n_bar_bar_w=document.createElement('div');
		n_bar_bar_w.setAttribute("style","position:relative;height:6px;background-color:rgba(0,0,0,0.5);border-radius:5px;padding-top:1px;width:0px;left:0px;");
		n_bar_mom_w.appendChild(n_bar_bar_w);
		nownode.sys_datasnode=n_data;
		nownode.sys_n_barnode_mom=n_bar_mom;
		nownode.sys_n_bar_wnode_mom=n_bar_mom_w;
		nownode.sys_n_barnode=n_bar_bar;
		nownode.sys_n_bar_wnode=n_bar_bar_w;
		nownode.sys_scroll_needh=needsh;
		nownode.sys_scroll_needw=needsw;
		nownode.setAttribute("s_scroll","parsed");
		if(needsh){
			nownode.sys_cal_barh=function(){
				var tmp_h=this.sys_datasnode.scrollHeight;
				var tmp_mh=this.clientHeight;
				this.sys_n_barnode.style.height=((tmp_mh/tmp_h)*tmp_mh-10-8)+"px";
			}
			nownode.sys_cal_barh();
			nownode.sys_scroll_h=function(e){
				if(SYS_SCROLL_LOCK){return;}
				var tmp_h=this.sys_datasnode.scrollHeight;
				var tmp_mh=this.clientHeight;
				var mdelta=tmp_h-tmp_mh;
				var bdelta=tmp_mh-((tmp_mh/tmp_h)*tmp_mh-10);
				var delk=(-1)*(mdelta/bdelta);
				var direct = 0;
				if (e.wheelDelta) {
					direct = e.wheelDelta*(-0.125)*(tmp_mh/tmp_h);
				} else if (e.detail) {
					direct = e.detail*12.5*(tmp_mh/tmp_h);
				}
				var typ=((tmp_mh/tmp_h)*tmp_mh-10);
		
				
				if(this.sys_n_barnode.style.top){
					if((parseInt(this.sys_n_barnode.style.top)+direct)<=0){
						_c(this.sys_n_barnode).add("scroll_over_ani");
						_c(this.sys_datasnode).add("scroll_over_ani");
						var tmpa=this;
						SYS_SCROLL_LOCK=1;
						setTimeout(function(){
							tmpa.sys_n_barnode.style.top="20px";
							tmpa.sys_datasnode.style.marginTop="20px";
							setTimeout(function(){
								tmpa.sys_n_barnode.style.top="0px";
								tmpa.sys_datasnode.style.marginTop="0px";
								setTimeout(function(){
									SYS_SCROLL_LOCK=0;
									_c(tmpa.sys_n_barnode).remove("scroll_over_ani");
									_c(tmpa.sys_datasnode).remove("scroll_over_ani");
								},300);
							},300);
						},50);
					}else if((parseInt(this.sys_n_barnode.style.top)+direct)>=(tmp_mh-typ)){
						if((tmp_mh-typ)<=0){return;}
						_c(this.sys_n_barnode).add("scroll_over_ani");
						_c(this.sys_datasnode).add("scroll_over_ani");
						var tmpa=this;
						SYS_SCROLL_LOCK=1;
						setTimeout(function(){
							tmpa.sys_n_barnode.style.top=(tmp_mh-typ+20)+"px";
							tmpa.sys_datasnode.style.marginTop=(tmp_mh-typ+20)*delk+"px";
							setTimeout(function(){
								tmpa.sys_n_barnode.style.top=(tmp_mh-typ)+"px";
								tmpa.sys_datasnode.style.marginTop=(tmp_mh-typ)*delk+"px";
								setTimeout(function(){
									SYS_SCROLL_LOCK=0;
									_c(tmpa.sys_n_barnode).remove("scroll_over_ani");
									_c(tmpa.sys_datasnode).remove("scroll_over_ani");
								},300);
							},300);
						},50);
					}else{
						var ii=parseInt(this.sys_n_barnode.style.top)+direct;
						if(ii<=0){return;}
						this.sys_n_barnode.style.top=ii+"px";
						this.sys_datasnode.style.marginTop=(ii)*delk+"px";
						
					}
				}else{
					if(direct<0){
						_c(this.sys_n_barnode).add("scroll_over_ani");
						_c(this.sys_datasnode).add("scroll_over_ani");
						var tmpa=this;
						SYS_SCROLL_LOCK=1;
						setTimeout(function(){
							tmpa.sys_n_barnode.style.top="20px";
							tmpa.sys_datasnode.style.marginTop="20px";
							setTimeout(function(){
								tmpa.sys_n_barnode.style.top="0px";
								tmpa.sys_datasnode.style.marginTop="0px";
								setTimeout(function(){
									SYS_SCROLL_LOCK=0;
									_c(tmpa.sys_n_barnode).remove("scroll_over_ani");
									_c(tmpa.sys_datasnode).remove("scroll_over_ani");
								},300);
							},300);
						},50);
					}else if(direct>=(tmp_mh-typ)){
						if((tmp_mh-typ)<=0){return;}
						_c(this.sys_n_barnode).add("scroll_over_ani");
						_c(this.sys_datasnode).add("scroll_over_ani");
						var tmpa=this;
						SYS_SCROLL_LOCK=1;
						setTimeout(function(){
							tmpa.sys_n_barnode.style.top=(tmp_mh-typ+20)+"px";
							tmpa.sys_datasnode.style.marginTop=(tmp_mh-typ+20)*delk+"px";
							setTimeout(function(){
								tmpa.sys_n_barnode.style.top=(tmp_mh-typ)+"px";
								tmpa.sys_datasnode.style.marginTop=(tmp_mh-typ)*delk+"px";
								setTimeout(function(){
									SYS_SCROLL_LOCK=0;
									_c(tmpa.sys_n_barnode).remove("scroll_over_ani");
									_c(tmpa.sys_datasnode).remove("scroll_over_ani");
								},300);
							},300);
						},50);
					}else{
						var ii=direct;
						if(ii<=0){return;}
						this.sys_n_barnode.style.top=ii+"px";
						this.sys_datasnode.style.marginTop=ii*delk+"px";
					}
				}
				SYSLIB_utils.preventDefault(e);
				if(SYS_SCROLL_FUNC){
					SYS_SCROLL_FUNC(this.sys_datasnode.style.marginTop);
				}
				this.sys_datasnode.style.marginTop
			}
			nownode.sys_clickscroll_h=function(e){
				if(SYS_SCROLL_LOCK){return;}
				var $this=this.parentNode;
				var tmp_h=$this.sys_datasnode.scrollHeight;
				var tmp_mh=$this.clientHeight;
				var mdelta=tmp_h-tmp_mh;
				var bdelta=tmp_mh-((tmp_mh/tmp_h)*tmp_mh-10);
				var delk=(-1)*(mdelta/bdelta);
				var direct = 0;
				var alltop=(SYSLIB_style.globalposition($this.sys_n_barnode_mom)).y;
				direct =(e.clientY-alltop);
				var tyui=((tmp_mh/tmp_h)*tmp_mh-10-8)/2;
				if(direct<=tyui){
					direct=tyui;
				}
				if(direct>=(tmp_mh-tyui-8)){
					direct=tmp_mh-tyui-8;
				}
				$this.sys_n_barnode.style.top=(direct-tyui)+"px";
				$this.sys_datasnode.style.marginTop=(direct-tyui)*delk+"px";
				SYSLIB_utils.preventDefault(e);
				if(SYS_SCROLL_FUNC){
					SYS_SCROLL_FUNC($this.sys_datasnode.style.marginTop);
				}
			}
			nownode.sys_n_barnode_mom.addEventListener("click",nownode.sys_clickscroll_h,false);
			nownode.sys_n_barnode_mom.addEventListener("mousedown",function(){
				this.addEventListener("mousemove",this.parentNode.sys_clickscroll_h,false);
			},false);
			nownode.sys_n_barnode_mom.addEventListener("mouseup",function(){
				this.removeEventListener("mousemove",this.parentNode.sys_clickscroll_h,false);
			},false);
			nownode.sys_n_barnode_mom.addEventListener("mouseout",function(){
				this.removeEventListener("mousemove",this.parentNode.sys_clickscroll_h,false);
			},false);
			nownode.addEventListener("mouseover",function(e){
				this.sys_n_barnode_mom.style.opacity="1";
				
				this.addEventListener("mousewheel",this.sys_scroll_h,false);
				this.addEventListener("DOMMouseScroll",this.sys_scroll_h,false);
			},false);
			
			nownode.addEventListener("mouseout",function(e){
				if(SYSLIB_dom.checkFather(this,e)){
					this.sys_n_barnode_mom.style.opacity="0";
					
					this.removeEventListener("mousewheel",this.sys_scroll_h,false);
					this.removeEventListener("DOMMouseScroll",this.sys_scroll_h,false);
					
				}
			},false);
		}
		if(needsw){
			nownode.sys_cal_barw=function(){
				var tmp_w=this.sys_datasnode.scrollWidth;
				var tmp_mw=this.clientWidth;
				this.sys_n_bar_wnode.style.width=((tmp_mw/tmp_w)*tmp_mw-10-8)+"px";
			}
			nownode.sys_cal_barw();
			nownode.sys_scroll_w=function(e){
				if(SYS_SCROLL_LOCK){return;}
				var tmp_w=this.sys_datasnode.scrollWidth;
				var tmp_mw=this.clientWidth;
				var mdelta=tmp_w-tmp_mw;
				var bdelta=tmp_mw-((tmp_mw/tmp_w)*tmp_mw-10);
				var delk=(-1)*(mdelta/bdelta);
				var direct = 0;
				if (e.wheelDelta) {
					direct = e.wheelDelta*(-0.125)*(tmp_mw/tmp_w);
				} else if (e.detail) {
					direct = e.detail*12.5*(tmp_mw/tmp_w);
				}
				var typ=((tmp_mw/tmp_w)*tmp_mw-10);
		
				
				if(this.sys_n_bar_wnode.style.left){
					if((parseInt(this.sys_n_bar_wnode.style.left)+direct)<=0){
						this.sys_n_bar_wnode.style.left="0px";
						this.sys_datasnode.style.marginLeft="0px";
					}else if((parseInt(this.sys_n_bar_wnode.style.left)+direct)>=(tmp_mw-typ)){
						this.sys_n_bar_wnode.style.left=(tmp_mw-typ)+"px";
						this.sys_datasnode.style.marginLeft=(tmp_mw-typ)*delk+"px";
					}else{
						this.sys_n_bar_wnode.style.left=parseInt(this.sys_n_bar_wnode.style.left)+direct+"px";
						this.sys_datasnode.style.marginLeft=(parseInt(this.sys_n_bar_wnode.style.left)+direct)*delk+"px";
					}
				}else{
					if(direct<=0){
						this.sys_n_bar_wnode.style.left="0px";
						this.sys_datasnode.style.marginLeft="0px";
					}else if(direct>=(tmp_mw-typ)){
						this.sys_n_bar_wnode.style.left=(tmp_mw-typ)+"px";
						this.sys_datasnode.style.marginLeft=(tmp_mw-typ)*delk+"px";
					}else{
						this.sys_n_bar_wnode.style.left=direct+"px";
						this.sys_datasnode.style.marginLeft=direct*delk+"px";
					}
				}
				if(SYS_SCROLL_FUNC){
					SYS_SCROLL_FUNC(0,this.sys_datasnode.style.marginLeft);
				}
				SYSLIB_utils.preventDefault(e);
			}
			nownode.sys_clickscroll_w=function(e){
				if(SYS_SCROLL_LOCK){return;}
				var $this=this.parentNode;
				var tmp_w=$this.sys_datasnode.scrollWidth;
				var tmp_mw=$this.clientWidth;
				var mdelta=tmp_w-tmp_mw;
				var bdelta=tmp_mw-((tmp_mw/tmp_w)*tmp_mw-10);
				var delk=(-1)*(mdelta/bdelta);
				var direct = 0;
				var allleft=(SYSLIB_style.globalposition($this.sys_n_bar_wnode_mom)).x;
				direct =(e.clientX-allleft);
				var tyui=((tmp_mw/tmp_w)*tmp_mw-10-8)/2;
				if(direct<=tyui){
					direct=tyui;
				}
				if(direct>=(tmp_mw-tyui-8)){
					direct=tmp_mw-tyui-8;
				}
				$this.sys_n_bar_wnode.style.left=(direct-tyui)+"px";
				$this.sys_datasnode.style.marginLeft=(direct-tyui)*delk+"px";
				SYSLIB_utils.preventDefault(e);
				if(SYS_SCROLL_FUNC){
					SYS_SCROLL_FUNC(0,$this.sys_datasnode.style.marginLeft);
				}
			}
			nownode.sys_n_bar_wnode_mom.addEventListener("click",nownode.sys_clickscroll_w,false);
			
			nownode.sys_n_bar_wnode_mom.addEventListener("mousedown",function(){
				this.addEventListener("mousemove",this.parentNode.sys_clickscroll_w,false);
			},false);
			nownode.sys_n_bar_wnode_mom.addEventListener("mouseup",function(){
				this.removeEventListener("mousemove",this.parentNode.sys_clickscroll_w,false);
			},false);
			nownode.sys_n_bar_wnode_mom.addEventListener("mouseout",function(){
				this.removeEventListener("mousemove",this.parentNode.sys_clickscroll_w,false);
			},false);
			nownode.addEventListener("mouseover",function(e){
				this.sys_n_bar_wnode_mom.style.opacity="1";
				if(!this.sys_scroll_needh){
					this.addEventListener("mousewheel",this.sys_scroll_w,false);
					this.addEventListener("DOMMouseScroll",this.sys_scroll_w,false);
					
				}
			},false);
			nownode.addEventListener("mouseout",function(e){
				if(SYSLIB_dom.checkFather(this,e)){
					this.sys_n_bar_wnode_mom.style.opacity="0";
					if(!this.sys_scroll_needh){
						this.removeEventListener("mousewheel",this.sys_scroll_w,false);
						this.removeEventListener("DOMMouseScroll",this.sys_scroll_w,false);
						
					}
				}
			},false);
		}
		if(needdy){
			nownode.addEventListener("change",nownode.sys_cal_barh,false)
		}
	}
}
SYSLIB_ui.slider=function(father,id,attrs,uis,max,min,w,h,initalval,outputval){
	this.node=document.createElement("div");
	if(attrs){
		for(var $attr in attrs){
			this,node.setAttritube($attr,attrs[$attr]);
		}
	}
	var $this=this;
	this.id=id;
	this.node.id=id;
	this.min=min||0;
	this.max=max||100;
	this.w=w||300;
	this.h=h||20;
	this.initalval=initalval;
	this.val=initalval;
	this.node.style.width=this.w+"px";
	this.node.style.height=this.h+"px";
	this.node.style.position="absolute";
	this.node.style.overflow="hidden";
	this.outputval=outputval;
	if(!uis){
		uis="blue";
	}
	this.uilist={
		"sketch":function(){
			$this.backnodes=document.createElement("div");
			$this.backnodes.style.width=($this.w-20)+"px";
			$this.backnodes.style.marginLeft="10px";
			$this.backnodes.style.height=($this.h-10)+"px";
			$this.backnodes.style.marginTop="5px";
			$this.backnodes.style.border="solid 2px #000";
			$this.backnodes.style.cursor="pointer";
			$this.backnodes.style.position="absolute";
			$this.midnodes=document.createElement("div");
			$this.midnodes.style.width=$this.initalval+"px";
			$this.midnodes.style.marginLeft="14px";
			$this.midnodes.style.height=($this.h-14)+"px";
			$this.midnodes.style.marginTop="9px";
			$this.midnodes.style.backgroundColor="#000";
			$this.midnodes.style.cursor="pointer";
			$this.midnodes.style.position="absolute";
			$this.topnodes=document.createElement("div");
			$this.topnodes.style.width="5px";
			$this.topnodes.style.marginLeft=(12+$this.initalval-3)+"px";
			$this.topnodes.style.height=($this.h)+"px";
			$this.topnodes.style.marginTop="0px";
			$this.topnodes.style.backgroundColor="#333";
			$this.topnodes.style.border="solid 2px #000";
			$this.topnodes.style.cursor="pointer";
			$this.topnodes.style.position="absolute";
		},
		"blue":function(){
			$this.backnodes=document.createElement("div");
			$this.backnodes.style.width=($this.w-20)+"px";
			$this.backnodes.style.marginLeft="10px";
			$this.backnodes.style.height=($this.h-10)+"px";
			$this.backnodes.style.marginTop="5px";
			$this.backnodes.style.border="solid 2px rgb(43, 141, 233)";
			$this.backnodes.style.borderRadius="3px";
			$this.backnodes.style.cursor="pointer";
			$this.backnodes.style.position="absolute";
			$this.midnodes=document.createElement("div");
			$this.midnodes.style.width=$this.initalval+"px";
			$this.midnodes.style.marginLeft="14px";
			$this.midnodes.style.height=($this.h-14)+"px";
			$this.midnodes.style.marginTop="9px";
			$this.midnodes.style.backgroundColor="rgb(68, 159, 245)";
			$this.midnodes.style.borderRadius="3px";
			$this.midnodes.style.cursor="pointer";
			$this.midnodes.style.position="absolute";
			$this.topnodes=document.createElement("div");
			$this.topnodes.style.width="4px";
			$this.topnodes.style.top="7px";
			$this.topnodes.style.borderRadius="100px";
			$this.topnodes.style.marginLeft=(12+$this.initalval-3)+"px";
			$this.topnodes.style.height=($this.h-14)+"px";
			$this.topnodes.style.marginTop="0px";
			$this.topnodes.style.backgroundColor="rgb(68, 159, 245)";
			$this.topnodes.style.border="solid 2px rgb(68, 159, 245)";
			$this.topnodes.style.cursor="pointer";
			$this.topnodes.style.position="absolute";
		}
	}
	this.startslide=function(e){
		$this.node.addEventListener("mousemove",$this.slide,false);
		$this.node.addEventListener("mouseup",$this.stopslide,false);
		$this.node.addEventListener("mouseout",$this.stopslide,false);
	}
	this.slide=function(e){
		var $x=e.clientX-SYSLIB_style.globalposition($this.node).x-10;
		$this.val=$this.min+($x/($this.w-24))*($this.max-$this.min);
		if($this.val<$this.min||$this.val>$this.max){
			return;
		}
		$x=$x;
		$this.midnodes.style.width=$x+"px";
		$this.topnodes.style.marginLeft=(12+$x-3)+"px";
		if($this.outputval){
			$this.outputval.innerHTML=$this.val;
			$this.outputval.value=$this.val;
		}
	}
	this.stopslide=function(e){
		if(SYSLIB_dom.checkFather(this,e)){
			$this.slide(e);
			$this.node.removeEventListener("mousemove",$this.slide,false);
			$this.node.removeEventListener("mouseup",$this.stopslide,false);
			$this.node.removeEventListener("mouseout",$this.stopslide,false);
		}
	}
	this.uilist[uis]();
	father.appendChild(this.node);
	this.node.appendChild($this.backnodes);
	this.node.appendChild($this.midnodes);
	this.node.appendChild($this.topnodes);
	this.val=0;
	this.midnodes.style.width="0px";
	this.topnodes.style.marginLeft="9px";
	this.node.addEventListener("mousedown",this.startslide,false);
	this.node.addEventListener("select",function(){return false;},false);
	return this;
}
//sound
var SYSLIB_sound=SYSLIB.namespace("syslib.sound");
SYSLIB_sound.soundlist=[];
SYSLIB_sound.add=function(name,url){
	if(!SYSLIB_sound.soundlist[name]){
		SYSLIB_sound.soundlist[name]=url;
	}
}
SYSLIB_sound.device=document.createElement("audio");
SYSLIB_sound.play=function(name){
	SYSLIB_sound.device.src=SYSLIB_sound.soundlist[name];
	SYSLIB_sound.device.play();
}
//Event
var SYSLIB_event=SYSLIB.namespace("syslib.event");

SYSLIB_event.add=function(node,type,listener,capture){
	if(!capture){
		var capture=false;
	}
	if(window.addEventListener){
		node.addEventListener(type,listener,capture);
	}else{
		node.attachEvent("on"+type,listener);
	}
}
//Ajax
var SYSLIB_ajax=SYSLIB.namespace("syslib.ajax");
SYSLIB_ajax.post=function(api,datas,rf_success,rf_error,notasync,timeout){
	var async=(notasync)?false:true;
	$.ajax({
		 type:"POST",
		 dataType:"json",
		 url:api,
		 data:datas,
		 async:async,
		 timeout:(timeout)?timeout:36000,
		 success:function(data,textStatus){
			 if(rf_success){
				 rf_success(data);
			 }
		 },
		 error:function(XMLHttpRequest,textStatus,errorThrown){
			if(rf_error){
				 rf_error(errorThrown);
			 }
		 }
		 
	});

}
SYSLIB_ajax.getfile=function(url,rf_success,rf_error,async){
	var $tt="";
	$.ajax({
		 type:"GET",
		 dataType:"html",
		 url:url,
		 async:(async)?async:false,
		 timeout:36000,
		 success:function(data,textStatus){
			 if(rf_success){
				 rf_success(data);
			 }else{
				 $tt= data;
			 }
		 },
		 error:function(XMLHttpRequest,textStatus,errorThrown){
			if(rf_error){
				 rf_error(errorThrown);
			 }
		 }
	});
	return $tt;
}
SYSLIB_ajax.load=function(file,cb,err){
	$.ajax({
                 type:"GET",
                 dataType:"html",
                 url:file,
                 timeout:100000,	 
                 success:function(data,textStatus){
					 if(cb){
						 cb(data);
					 }
					 return data;
                     //从服务器得到数据，显示数据并继续查询
	             },
				 //Ajax请求超时，继续查询
	             error:function(XMLHttpRequest,textStatus,errorThrown){
						//senddata(iput,start,stop,filesize,file);
						if(err){
						 err();
					 }
						return -1;
	             }
                 
		});
}
//token
var SYSLIB_token=SYSLIB.namespace("syslib.token");
SYSLIB_token.get=function(length){
	var $i=0;
	var $length=length||32;
	var $yu=Array(0,1,2,3,4,5,6,7,8,9,"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z");
	var $utk="";
	for($i=0;$i<$length;$i++){
		var $j=SYSLIB_math.rand(0,61);
		$utk+=$yu[$j];
	}
	return $utk;
}
//cookies
var SYSLIB_cookies=SYSLIB.namespace("syslib.cookies");
SYSLIB_cookies.get=function(c_name,defaultvar){
	var $defaultvar=defaultvar||"";
	if (document.cookie.length>0)
  	{
  		c_start=document.cookie.indexOf(c_name + "=");
		//console.log(c_start);
  		if (c_start!=-1)
    	{ 
    		c_start=c_start + c_name.length+1;
    		c_end=document.cookie.indexOf(";",c_start);
    		if (c_end==-1) {
				c_end=document.cookie.length;
    		} 
			//console.log(unescape(document.cookie.substring(c_start,c_end)));
			var $rvar=unescape(document.cookie.substring(c_start,c_end));
			return ($rvar!="")?$rvar:$defaultvar;
  		}else{return $defaultvar;}
	}else{return $defaultvar;}
}
SYSLIB_cookies.set=function(c_name,value,expiredays){
	var exdate=new Date();
	exdate.setDate(exdate.getDate()+(expiredays||14));
	document.cookie=c_name+ "=" +escape(value)+((expiredays==null) ? "" : ";expires="+exdate.toGMTString()+"; path=/");
}
SYSLIB_cookies.clean=function(c_name){
	SYSLIB_cookies.set(c_name,"");
}
//tittle
var SYSLIB_tittle=SYSLIB.namespace("syslib.tittle");
SYSLIB_tittle.set=function(ipt){
	document.title=ipt;
}
//brhistory
var SYSLIB_brhistory=SYSLIB.namespace("syslib.brhistory");
SYSLIB_brhistory.push=function(action){
	var $state={
		title:document.title,
		url:window.location.href,
		action:(action)?action:0
	}
	history.pushState($state,$state['title'],$state['url']);
}
//brurl
var SYSLIB_brurl=SYSLIB.namespace("syslib.brurl");
SYSLIB_brurl.set=function(ipt){
	window.location.href=SYSLIB.baseurl+"#"+ipt;
}
//syssend
var SYSLIB_send=SYSLIB.namespace("syslib.syssend");
SYSLIB_send.io=io;
SYSLIB_send.connect=function(name,host,port,run){
	if(!run){
		var run=0;
	}
	if(!SYSLIB_send.sockets[name]){
		var soc=(io.connect(host+':'+port));
		var $name=name,$host=host,$port=port,$soc=soc,$run=run;
		soc.on('connectok', function (data) {
			var tttuuu=new SYSLIB_send.socket($name,$host,$port,this);
    		SYSLIB_send.sockets[name]=tttuuu;
			if($run){
				$run();
			}
			return tttuuu;
		});
	}
};
SYSLIB_send.sockets={};
SYSLIB_send.getsocket=function(name){
	return SYSLIB_send.sockets[name];
}
SYSLIB_send.socket=function(name,host,port,socket){
	this.name=name;
	var $this=this;
	this.host=host;
	this.port=port;
	this.socket=socket;
	this.socketlist={};
	this.send=function(api,data,success,fail,token,nodelete,pass){
		if(!token){
			var token=SYSLIB_token.get();
		}
		if(!nodelete){
			var nodelete=0;
		}
		if(!success){
			var success=function(){};
		}
		if(!fail){
			var fail=function(){};
		}
		var $outdata=JSON.stringify(data);
		if(!pass){
			var pass=0;
		}else{
			$outdata=sjcl.encrypt(pass,$outdata);
		}
		
		$this.socketlist[token]={api:api,success:success,fail:fail,nodelete:nodelete,pass:pass};
		
		$this.socket.emit('senddata', { id:token,datas: $outdata });
	}
	$this.socket.on('recivedata', function (data) {
    	var token=data.id;
		if($this.socketlist[token]){
			var $outdata=data.data;
			if($this.socketlist[token].pass){
				$outdata=sjcl.decrypt($this.socketlist[token].pass,$outdata);
			}
			$outdata=JSON.parse($outdata);
			if(data.flag=="ok"){
				$this.socketlist[token].success($outdata);
			}else{
				$this.socketlist[token].fail($outdata,data.flag);
			}
			if(!$this.socketlist[token].nodelete){
				$this.socketlist[token]=0;
			}
		}
	});
	return this;
	
}



//fromr anim.js
//SYSLIB_anim(box, {marginLeft: "2%", fontSize: "20px"}, 2, "ease-out");
SYSLIB_utils.anim=anim;

//fromr js-signal.js
//var mySignal = new SYSLIB_signal();
//var myObject = {
  //started : new SYSLIB_signal(), //past tense is the recommended signal naming convention
  //stopped : new SYSLIB_signal()
//};
//https://github.com/millermedeiros/js-signals/wiki/Examples
var SYSLIB_signal=SYSLIB.namespace("syslib.signal");
SYSLIB_utils.signal=signals.Signal;

//fromr us.js
//SYSLIB_ua.isOpera()

SYSLIB_utils.ua=UA;
//fromr placeholder.js
//SYSLIB_placeholder(_f("#rrr"),color)

SYSLIB_utils.placeholder=inputPlaceholder;

SYSLIB_utils.preventDefault=function(e) {
  e = e || window.event;
  if (e.preventDefault)
      e.preventDefault();
  e.returnValue = false;  
}
SYSLIB_utils.clone=function(obj) {
    // Handle the 3 simple types, and null or undefined
    if (null == obj || "object" != typeof obj) return obj;

    // Handle Date
    if (obj instanceof Date) {
        var copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        var copy = [];
        for (var i = 0, len = obj.length; i < len; i++) {
            copy[i] = SYSLIB_utils.clone(obj[i]);
        }
        return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
        var copy = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = SYSLIB_utils.clone(obj[attr]);
        }
        return copy;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
}
SYSLIB_utils.file=new Filer();
SYSLIB_utils.save_to_ls=function(data,totalsizeinmb,filepath,encodetype){
	if(!data||!filepath){
		return;
	}
	if(!totalsizeinmb){
		var totalsizeinmb=10;
	}
	if(!encodetype){
		var encodetype=0;
	}
	switch(encodetype){
		case 1:
			data=JSON.stringify(data);
			break;
	}
	SYSLIB_utils.file.init({persistent: true, size: totalsizeinmb*1024 * 1024}, function(fs) {
		var eee=function(){
			SYSLIB_utils.file.write(filepath, {data: data, type: 'application/octet-stream'},function(fileEntry) {
			},
					function(){
						console.log('Faild To save files')
					}
			);
		}
		eee();	
		//try{
		//	SYSLIB_utils.file.rm(filepath,function(){
		//		eee();		
		//	},function(){
		//		console.log('Faild To save files')
		//	})
		//}catch(e){
		//	eee();
		//}
	
	
}, function(){
	console.log('Faild To save files')
});
};
SYSLIB_utils.load_from_ls=function(filepath,decodetype,scb){
	if(!filepath){
		scb(0);
		return;
	}
	var decodeandreturn=function(data){
		switch(decodetype){
			case 1:
				data=JSON.parse(data);
				break;
		}
		scb(data);
	}
	try{
			SYSLIB_utils.file.init({persistent: true, size: 200*1024 * 1024}, function(fs) {
				 SYSLIB_utils.file.open(filepath,function(file) {
						var reader = new FileReader();
						reader.onload = (function (theFile) {
							return function (e) {
								
								decodeandreturn(e.target.result);
							};
						})(file);
						reader.readAsText(file);
				 },
						function(){
							console.log('Faild To find saves')
							scb(0);
						}
				 );
			}, function(){
				console.log('Faild To find saves')
				scb(0);
			});
		}catch(e){
			scb(0);
		}
	
}
SYSLIB_utils.geo=function(scb,err){
	var getgeo=function(scb,scb2,err){
		if (navigator.geolocation){
    			navigator.geolocation.getCurrentPosition(scb,function(error){
				switch(error.code) {
    					case error.PERMISSION_DENIED:
      						console.log("GEO: User denied the request for Geolocation.");
      						break;
    					case error.POSITION_UNAVAILABLE:
     						console.log("GEO: Location information is unavailable.");
      						break;
    					case error.TIMEOUT:
      						console.log("GEO: The request to get user location timed out.");
      						break;
    					case error.UNKNOWN_ERROR:
      						console.log("GEO: An unknown error occurred.");
      						break;
    				}
				if(scb2){scb2();}else{ if(err){err();}}
			});
   		}else{
			if(scb2){scb2();}
		}
	}
	getgeo(function(e){
		$.ajax({
		 	 dataType:"jsonp",
			 url:'http://api.map.baidu.com/geocoder/v2/',
			 data:{ak:'6f7bcd8ebbe8209777f27f32fed49746',location:(e.coords.latitude+","+e.coords.longitude),output:'json',pois:1},
			 timeout:36000,
			 success:function(data,textStatus){
				if(!data||!data.result){
					return err();
				}
				var pos={
					accuracy:e.coords.accuracy,
					altitude:e.coords.altitude,
					altitudeAccuracy:e.coords.altitudeAccuracy,
					heading:e.coords.heading,
					latitude:e.coords.latitude,
					longitude:e.coords.longitude,
					speed:e.coords.speed,
					timestamp:e.timestamp,
					address:data.result.formatted_address,
					city:data.result.addressComponent.city,
					district:data.result.addressComponent.district,
					province:data.result.addressComponent.province,
					street:data.result.addressComponent.street,
					street_number:data.result.addressComponent.street_number
				}
				scb(pos);
		 	},
		 	error:function(XMLHttpRequest,textStatus,errorThrown){
				if(err){err();}
		 	}
		 
		});
	},function(e){
		$.ajax({
		 	 dataType:"jsonp",
			 url:'http://api.map.baidu.com/location/ip',
			 data:{ak:'6f7bcd8ebbe8209777f27f32fed49746'},
			 timeout:36000,
			 success:function(data,textStatus){
				if(!data||!data.content){
					return err();
				}
				var pos={
					accuracy:0,
					altitude:0,
					altitudeAccuracy:0,
					heading:0,
					latitude:data.content.point.x,
					longitude:data.content.point.y,
					speed:0,
					timestamp:(new Date()).getTime(),
					address:data.content.address,
					city:data.content.address_detail.city,
					district:data.content.address_detail.district,
					province:data.content.address_detail.province,
					street:data.content.address_detail.street,
					street_number:data.content.address_detail.street_number
				}
				scb(pos);
		 	},
		 	error:function(XMLHttpRequest,textStatus,errorThrown){
				if(err){err();}
		 	}
		 
		});
	},err)
	
}
var _m=SYSLIB.namespace("syslib.model").t;
var _is=SYSLIB.namespace("syslib.vilade").vilade;
var _f=SYSLIB.namespace("syslib.dom").find;
var _c=SYSLIB.namespace("syslib.dom").class;
var _search=SYSLIB.namespace("syslib.dom").search;
var _post=SYSLIB.namespace("syslib.ajax").post;
var _title=SYSLIB.namespace("syslib.tittle").set;
var _pushhistory=SYSLIB.namespace("syslib.brhistory").push;
var _seturl=SYSLIB.namespace("syslib.brurl").set;
var _connect=SYSLIB.namespace("syslib.syssend").connect;
var _socket=SYSLIB.namespace("syslib.syssend").getsocket;


var _anim=SYSLIB.namespace("syslib.utils").anim;

var _singal=SYSLIB.namespace("syslib.utils").signal;
var _us=SYSLIB.namespace("syslib.utils").useragent;
var _clone=SYSLIB.namespace("syslib.utils").clone;
var JUMP_TO=SYSLIB.namespace("syslib.model").jump_to;
var _error=function(data,where){
	SYSLIB_utils.error(data,window.location.href,where);
}

