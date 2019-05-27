<template>
    <div class="page">
        <div style="height:40%;width:100%">
            <h2 id="title" style="margin-top:5px;margin-bottom:10px">说说词云</h2>
            <p id="description">基于输入QQ号过去一年的说说内容，使用结巴分词并统计词频，使用wordcloud制作专属的词图云，见证过去中二的自己。</p>
            <p>由于资源有限，每个ip只能提供一次服务，谨慎尝试!</p>
        </div>
        <div style="height: 20%;">
            <el-input v-model="input" placeholder="输入QQ号"></el-input>
            <el-button type="primary" @click="get_nick_name" style="margin-top: 10px;">点击生成</el-button>
        </div>
        <div v-show="isErr" style="height: 5%;margin-top:10px;">
            <el-alert :title="errMsg" type="error" :closable="false"></el-alert>
        </div>
        <div style="height: 40%">
            <h4 style="text-align:left;margin-top: 10px;margin-bottom:0;">示例图云：</h4>
            <img src="http://p1.pstatp.com/large/pgc-image/15390832645185cd251c668" style="width:100%;height: 80%;"/>
        </div>
        <el-dialog title="提示" :visible.sync="dialogVisible" width="90%">
            <span>{{ dialogMsg }}</span>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="gotoLast">查看耻辱榜</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data() {
        return {
            input: '',
            isErr: false,
            errMsg: '',
            dialogTitle: 'FBI Warning！',
            dialogMsg: '',
            dialogVisible: false
        }
    },
    methods: {
        get_nick_name: function() {
            if (!this.check_input()) {
                this.isErr = true
                return
            } else {
                this.isErr = false
            }
            this.axios.get('/api/get_nick_name/' + this.input)
            .then((response) => {
                if (response.data.status == "success") {
                    var data = response.data.data
                    console.log(data)
                    this.$store.commit('setNickName', data.nickName)
                    this.$store.commit('setQQNumber', this.input)
                    this.$store.commit('setCount', data.count)
                    this.$router.push('/second')
                } else {
                    this.dialogMsg = response.data.errMsg
                    this.dialogVisible = true
                }
            })
            .catch((res) => {
                this.errMsg = "服务器请求失败"
                this.isErr = true
            })
        },
        check_input: function() {
            if (this.input.length == 0) {
                this.errMsg = "请输入QQ号码"
                return false
            }
            var reg = /^\d{6,11}$/;
            if (!reg.test(this.input)) {
                this.errMsg = "QQ号码格式错误，请检查后重新输入"
                return false;
            }
            return true
        },
        gotoLast() {
            this.$router.push('/third')
        }
    }
}
</script>

