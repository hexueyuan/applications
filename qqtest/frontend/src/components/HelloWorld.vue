<template>
  <div style="width:80%;height:100%;margin: 0 auto;">
    <div id="input" style="width: 100%;margin-bottom: 20px;height: 10%;">
      <el-input v-model="input" placeholder="请输入你的qq号"></el-input>
      <el-button style="margin-top: 10px;" type="primary" @click.native="get_result">科学算命</el-button>
    </div>
    <div id="result" style="width: 100%;height: 60%;margin-top: 40px;margin-bottom: 20px;">
      <img :src="path" v-show="success" style="width: 80%;height: 80%;margin: 0 auto;"/>
    </div>
    <div id="err" style="height: 10%;">
      <el-alert v-show="isErr" :title="errMsg" type="error"></el-alert>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      input: '',
      isErr: false,
      errMsg: '',
      path: '',
      success: false
    }
  },
  methods: {
    check_input() {
      var reg = /^\d{6,13}$/;
      if (!reg.test(this.input)) {
        return false;
      }
      return true
    },
    get_result() {
      if (!this.check_input()) {
        this.errMsg = "请输入合法的QQ号"
        this.isErr = true
      } else {
        this.errMsg = '',
        this.isErr = false
        var that = this

        let api = ""
        this.$axios.get(api + '/application/qqtest/result/' + this.input).then((res) => {
          that.path = api + res.data
          that.success = true
        }).catch((res) => {
          that.errMsg = "请求失败，可能是服务器抽了:-("
          that.isErr = true
          console.log(res)
        })
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
