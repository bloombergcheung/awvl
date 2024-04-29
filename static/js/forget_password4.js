var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        password:'',
        password_error:false,
        password_error_message:'The password does not comply with the rules',
        password2:'',
        password2_error:false,
        password2_error_message:'Two passwords do not match',

    },
    mounted(){
    },
    methods: {

        //检查密码
        check_password:function () {
            var re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.password_error = false;
            } else {
                this.password_error = true;
            }
        },
        //检查确认密码
        check_password2:function () {
            if (this.password != this.password2) {
                this.password2_error = true;
            } else {
                this.password2_error = false;
            }
        },


        //提交
        on_submit:function () {
            this.check_password();
            this.check_password2();

            if (this.password_error == true || this.password2_error == true) {
                // 不满足注册条件：禁用表单
                window.event.returnValue = false;
            }
        }
    }
});
