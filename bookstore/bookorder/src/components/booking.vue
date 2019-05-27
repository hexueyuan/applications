<template>
    <div style="width:80%;height:100%;margin: 0 auto;">
        <el-table :data="borrowTableData" style="width: 100%">
            <el-table-column prop="time" label="时间" width="180"></el-table-column>
            <el-table-column prop="name" label="书名">
                <template slot-scope="scope">
                    <el-popover placement="top-start" title="图书信息" width="200" trigger="hover">
                        <p><span style="font-size: 14px;margin-right: 10px;">作者:</span><span>{{ scope.row.author }}</span></p>
                        <p><span style="font-size: 14px;margin-right: 10px;">出版日期:</span><span>{{ scope.row.date }}</span></p>
                        <span slot="reference">{{ scope.row.name }}</span>
                    </el-popover>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    data() {
        return {
            borrowTableData: []
        }
    },
    created() {
        var that = this
        this.timer = setInterval( () => {　
                that.$axios.get('/api/borrow')
                .then(function (res) {
                    that.borrowTableData = []
                    res.data.forEach(function (borrow) {
                        that.borrowTableData.push(borrow)
                    })
                })
                .catch(function (res) {
                    that.$notify.error({
                        title: '数据请求失败',
                        message: JSON.stringify(res)
                    })
                })
    　　 }, 1000)
    },
    distroyed: function () {
　　    clearInterval(this.timer)
    }
}
</script>