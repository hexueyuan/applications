<template>
    <div style="width: 100%">
        <h1>耻辱榜👏</h1>
        <el-table :data="tableData" style="width: 100%">
            <el-table-column prop="nickName" label="昵称" width="100"></el-table-column>
            <el-table-column prop="qq" label="QQ" width="100"></el-table-column>
            <el-table-column prop="time" label="时间"></el-table-column>
        </el-table>
    </div>
</template>

<script>
export default {
    data() {
        return {
            tableData: []
        }
    },
    created() {
        this.axios.get('/api/get_all_list')
        .then((response) => {
            if (response.data.status == "success") {
                this.tableData = response.data.data
            }
        })
        .catch((res) => {
            this.tableData = []
        })
    }
}
</script>