$(document).ready(function(){
	$("#index-modal-user-login-button").click(function(){
		$("#index-modal-login").modal("show") ;
	});
	modalButtonClick();
});
/**
 * 改变登录，注册的模态框
 */
function modalButtonClick(){
	$("#index-modal-login-login").click(function(){
		$("#index-modal-regist").modal("hide");
		$("#index-modal-login").modal("show") ;
		$("#index-modal-login-login").attr("class","active");
		$("#index-modal-login-regist").removeAttr("class");
	});
	$("#index-modal-login-regist").click(function(){
		$("#index-modal-login").modal("hide");
		$("#index-modal-regist").modal("show");
		$("#index-modal-regist-regist").attr("class","active");
		$("#index-modal-regist-login").removeAttr("class");
	});
	$("#index-modal-regist-login").click(function(){
		$("#index-modal-regist").modal("hide");
		$("#index-modal-login").modal("show") ;
		$("#index-modal-login-login").attr("class","active");
		$("#index-modal-login-regist").removeAttr("class") ;
	});
	$("#index-modal-regist-regist").click(function(){
		$("#index-modal-login").modal("hide");
		$("#index-modal-regist").modal("show");
		$("#index-modal-regist-regist").attr("class","active");
		$("#index-modal-regist-login").removeAttr("class");
	});
}