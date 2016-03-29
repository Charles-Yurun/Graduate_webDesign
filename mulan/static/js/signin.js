/**
 * Created by simi on 15/5/9.
 */
var Script = function () {

//    $.validator.setDefaults({
//        submitHandler: function() {  }
//    });

    $().ready(function() {
        // validate signup form on keyup and submit
        $("#signinForm").validate({
            rules: {
                account: {
                    required: true,
                    minlength: 4
                },
                password: {
                    required: true,
                    minlength: 6
                }
            },
            messages: {
                account: {
                    required: "请输入用户名或者注册邮箱",
                    minlength: "至少为4个字符"
                },
                password: {
                    required: "请输入密码",
                    minlength: "密码至少为5个字符"
                }
            }
        });
    });


}();