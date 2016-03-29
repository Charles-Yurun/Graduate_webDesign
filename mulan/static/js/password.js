/**
 * Created by simi on 15/5/9.
 */
var Script = function () {

//    $.validator.setDefaults({
//        submitHandler: function() {  }
//    });

    $().ready(function() {
        // validate form on keyup and submit
        $("#passwordForm").validate({
            rules: {
                old_password: {
                    required: true,
                    minlength: 6,
                    maxlength: 16
                },
                new_password: {
                    required: true,
                    minlength: 6,
                    maxlength: 16
                },
                confirm_password: {
                    required: true,
                    minlength: 6,
                    maxlength: 16,
                    equalTo: "#new_password"
                },
                agree: "required"
            },
            messages: {
                old_password: {
                    required: "请输入当前密码",
                    minlength: "长度为6-16个字符"
                },
                new_password: {
                    required: "请输入新的密码",
                    minlength: "长度为6-16个字符"
                },
                confirm_password: {
                    required: "请输入确认密码",
                    minlength: "由6-16个字母、数字组成",
                    equalTo: "新的密码和确认密码不一致"
                },
                email: "请输入一个正确的邮箱",
                agree: "请阅读并同意相关服务条款和隐私政策"
            }
        });
    });
}();