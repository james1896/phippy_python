/**
 * start_ip_log
 * 每个方法后面必须加分号，以免加密出错
 */
var domain = "https://gateway.fastgoapi.com/";   //正式地址
//var domain = "http://local.gateway_api.com/";      //本地地址
var app_id = '7f82r9re9x5pi79i196j3uy5pv0jsj9l';
var bundle_id = 'ivi.hyxapp.com';
var platform = 'ios';
var timestamp = new Date().getTime();
var app_key = '6w3mgqan5gwqdoxqvk7hpij5ed8gs2a8';
var signature_val = "app_id="+app_id+"&bundle_id="+bundle_id+"&platform="+platform+"&timestamp="+timestamp+"&app_key="+app_key;
var signature = $.md5(signature_val);
var palcode = getPar('palcode');
$("#install-apk-btn").click(function(){
	$.ajax({
	   type: "POST",
	   url: domain + "auths/appToken",
	   dataType:'json',
	   data:{
		   timestamp:timestamp,
		   app_id:app_id,
		   platform:platform,
		   bundle_id:bundle_id,
		   signature:signature,
		   isCross:1,
	   }, 
	   success: function(msg){
	     if(msg.data.appToken){
	    	 var token = msg.data.appToken;
	    	 var ip = msg.data.ip;
	    	 palcodes(token,ip);
	     }
	   }
	});
});
//写数据
function palcodes(token,ip){	
	var palcode = getPar('palcode');
	if(token == '' || ip == '' || palcode == ''){
		return false;
	}
	$.ajax({
		   type: "POST",
		   url: domain + "ip/record",
		   dataType:'json',
		   data:{
			   app_token:token,
			   ip:ip,
			   palcode:palcode,
			   signature:bundle_id,
			   isCross:1,
		   }, 
		   success: function(msg){
		     console.log(msg);
		   }
	});
};

function getPar(par){
    //获取当前URL
    var local_url = document.location.href; 
    //获取要取得的get参数位置
    var get = local_url.indexOf(par +"=");
    if(get == -1){
        return false;   
    }   
    //截取字符串
    var get_par = local_url.slice(par.length + get + 1);    
    //判断截取后的字符串是否还有其他get参数
    var nextPar = get_par.indexOf("&");
    if(nextPar != -1){
        get_par = get_par.slice(0, nextPar);
    }
    return get_par;
};
//end_ip_log