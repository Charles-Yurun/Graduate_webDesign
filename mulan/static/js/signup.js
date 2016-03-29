/**
 * Created by simi on 15/5/9.
 */
var Script = function () {

//    $.validator.setDefaults({
//        submitHandler: function() {  }
//    });

    $().ready(function() {
        // validate signup form on keyup and submit
        $("#signupForm").validate({
            rules: {
                username: {
                    required: true,
                    minlength: 4
                },
                email: {
                    required: true,
                    email: true
                },
                password: {
                    required: true,
                    minlength: 6,
                    maxlength: 16
                },
                confirm_password: {
                    required: true,
                    minlength: 6,
                    maxlength: 16,
                    equalTo: "#password"
                },
                agree: "required"
            },
            messages: {
                username: {
                    required: "请输入用户名",
                    minlength: "由4-18个字母、数字组成",
                    maxlength: "由4-18个字母、数字组成"
                },
                password: {
                    required: "请输入密码",
                    minlength: "长度为6-16个字符"
                },
                confirm_password: {
                    required: "请输入确认密码",
                    minlength: "由6-16个字母、数字组成",
                    equalTo: "密码不一致"
                },
                email: "请输入一个正确的邮箱",
                agree: "请阅读并同意相关服务条款和隐私政策"
            }
        });
    });


}();