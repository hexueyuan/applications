<template>
    <div id="login-box" style="width: 500px;height: 80%;margin: 0 auto;">
        <el-card style="height: 50%;width: 100%;">
        <div id="userinfo-box" style="height: auto;margin-bottom: 20px;">
            <el-input id="username-input" v-model="username" placeholder="请输入用户名"></el-input>
            <el-input id="password-input" v-model="password" placeholder="请输入密码" show-password></el-input>
        </div>
        <div id="login-box" style="width: 500px;">
            <el-button style="float: right;margin-right: 40px;margin-bottom: 20px;" type="primary" @click.native="login">登录</el-button>
        </div>
        </el-card>
        <div id="message-box" style="margin-top: 40px;">
              <el-alert
                v-show="isError"
                :title="errMsg"
                type="error"
                center
                show-icon>
                </el-alert>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: '',
            isError: false,
            errMsg: '错误'
        }
    },
    methods: {
        login: function() {
            if (this.username.replace(/ /g,'') == '') {
                this.isError = true
                this.errMsg = "请输入有效用户名"
                return
            }
            if (this.password.replace(/ /g,'') == '') {
                this.isError = true
                this.errMsg = "请输入有效密码"
                return
            }
            this.isError = false

            //请求
            //this.$http.post("")
            //登录成功
            if (this.username.replace(/ /g,'') == "admin" && this.password == "admin") {
                this.$router.push('/admin')
            } else if (this.username.replace(/ /g,'') == "bookOrder" && this.password == "123456") {
                this.$router.push('/booking')
            } else {
                this.isError = true
                this.errMsg = "用户名或者密码错误"
            }
        }
    }
}
</script>

<style>
#username-input {
    margin-bottom: 5px;
}
</style>
