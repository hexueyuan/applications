<template>
    <div>
        <img src="http://5b0988e595225.cdn.sohucs.com/images/20180401/3a7dd85613104d4c80c23d1e5953d94c.jpeg"/>
        <p style="color: red">上当人数 + 1</p>
        <p>截止到目前已有: <span style="color:red">{{ count }}</span>人上钩。</p>

        <p>点击查看耻辱榜</p>
        <el-button type="primary" @click="gotoNext">查看</el-button>

        <el-dialog :title="nickname" :visible.sync="firstDialogVisible" width="90%">
            <span>{{ firstDialogMsg }}</span>
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="firstDialogVisible = false">认栽</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data() {
        return {
            count: 1,
            nickname: '',
            firstDialogVisible: false,
            firstDialogMsg: "👏👏👏当你看到这条消息的时候表示你已经上当了，你的愚蠢行为会被雪源放在本页面耻辱榜上展示😊",
            list: []
        }
    },
    created() {
        this.nickname = this.$store.getters.nickName + '(' + this.$store.getters.qqNumber + ')'
        this.count = this.$store.getters.count
        this.firstDialogVisible = true
    },
    methods: {
        gotoNext: function() {
            this.$router.push('/third')
        }
    }
}
</script>
