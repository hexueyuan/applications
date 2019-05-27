<template>
    <div style="margin: 20px;">
        <div>
            <el-button type="success" @click="handleAddEvent">新增</el-button>
            <el-button type="danger" @click="handleDeleteEvent" :disabled="disableDeleteAndEdit">删除</el-button>
            <el-button type="primary" @click="handleEditEvent" :disabled="disableDeleteAndEdit">编辑</el-button>
        </div>
        <el-table ref="singleTable" :data="tableData" highlight-current-row @current-change="handleRowSelect" style="width: 100%">
            <el-table-column type="index" width="100"></el-table-column>
            <el-table-column v-for="attr in tableAttrs" v-bind:key="attr.prop" :prop="attr.prop" :label="attr.label" :width="attrWidth"></el-table-column>
        </el-table>
        <el-dialog :visible.sync="dialogVisible" width="400px">
            <el-form ref="form" :model="form" label-width="40px">
                <el-form-item v-for="attr in tableAttrs" v-bind:key="attr.prop" :label="attr.label">
                    <el-input v-model="form[attr.prop]" :disabled="mode == 'edit' && attr['primary-key']"></el-input>
                </el-form-item>
            </el-form>
            <el-button type="primary" @click="submitData">确定</el-button>
            <el-button type="danger" @click="cancleSumbitData" plain>取消</el-button>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data() {
        return {
            tableAttrs: [
                {
                    'label': '名称',
                    'prop': 'name',
                    'type': String,
                    'primary-key': true
                },
                {
                    'label': '体力',
                    'prop': 'life',
                    'type': Number
                },
                {
                    'label': '健康',
                    'prop': 'health',
                    'type': Number
                },
                {
                    'label': '干净',
                    'prop': 'clean',
                    'type': Number
                },
                {
                    'label': '力量',
                    'prop': 'power',
                    'type': Number
                },
                {
                    'label': '智慧',
                    'prop': 'wisdom',
                    'type': Number
                },
                {
                    'label': '魅力',
                    'prop': 'charm',
                    'type': Number
                },
                {
                    'label': '酒量',
                    'prop': 'liqueur',
                    'type': Number
                },
                {
                    'label': '宅',
                    'prop': 'home',
                    'type': Number
                },
                {
                    'label': '音乐',
                    'prop': 'music',
                    'type': Number
                },
                {
                    'label': '孤独',
                    'prop': 'lonely',
                    'type': Number
                },
                {
                    'label': '钱',
                    'prop': 'money',
                    'type': Number
                }
            ],
            //表格当前选中数据，内容是当行数据对象
            currentRow: null,
            //显示浮窗，浮窗中为form表格，被用于添加和编辑数据
            dialogVisible: false,
            //form数据绑定
            form: {},
            //form中名称输入使能，编辑模式下不能修改test所以设置该项
            nameEnable: true,
            //可选值add或者edit，用于标记是新增模式或者删除模式
            mode: null,
            //禁能删除和编辑，未选中行时不能删除和编辑数据
            disableDeleteAndEdit: true,
            //表格数据绑定
            tableData: [
                {'name': 'test', 'life': 1, 'health': 2, 'clean': 3, 'power': 4, 'wisdom': 5, 'charm': 6, 'liqueur': 7, 'home': 8, 'music': 9, 'lonely': 10, 'money': 11}
            ]
        }
    },
    methods: {
        //处理表格单选事件，current为当前选中行数据对象，old是上一次选中行数据对象
        handleRowSelect(current, old) {
            this.currentRow = current
        },
        //处理新增数据事件，设置新增模式，清空form并打开浮窗
        handleAddEvent() {
            this.mode = 'add'
            this.form = {}
            this.dialogVisible = true
        },
        //处理删除数据事件，选中行时执行deleteData方法，并将currentRow当前选中行标记为null
        handleDeleteEvent() {
            var delData = this.currentRow
            this.deleteData(delData)
            this.currentRow = null
        },
        //处理编辑数据事件，设置编辑模式，把选中数据赋值给form并打开浮窗
        handleEditEvent() {
            this.mode = 'edit'
            this.form = this.currentRow
            this.dialogVisible = true
        },
        //提交数据，检查form每一项数据都存在并且格式正确，当name存在于table表中表示应该更新数据！！BAD
        //
        submitData() {
            if (this.convertData()) {
                    var data = this.form
                    if (this.mode === 'add') {
                        this.postToDB(data)
                        this.tableData.push(data)
                        this.alertMessage("添加成功", "success")
                    } else if (this.mode === 'edit') {
                        var i = this.tableData.findIndex(item => {
                            return item.name === data.name
                        })
                        this.updateInDB(data)
                        this.tableData[i] = data
                        this.alertMessage("编辑成功", "success")
                    } else {
                        this.alertMessage('模式错误', 'error')
                    }
                    this.dialogVisible = false
                    this.form = {}
            } else {
                this.alertMessage("数据不完整或者数据格式错误", "error")
            }
        },
        //删除当前table中的数据
        deleteData(data) {
            this.deleteFromDB(data)
            var i = this.tableData.findIndex(item => {
                return item.name === data.name
            })
            if (i != -1) {
                this.tableData.splice(i, 1)
                this.alertMessage('删除成功', 'success')
            } else {
                this.alertMessage('未找到数据', 'error')
            }
        },
        //取消sumbit数据
        cancleSumbitData() {
            this.dialogVisible = false
        },
        //新增数据传到后台
        postToDB(data) {
            console.log(data)
        },
        //删除数据传到后台
        deleteFromDB(data) {
            console.log(data)
        },
        //更新数据传到后台
        updateInDB(data) {
            console.log(data)
        },
        //页面弹窗
        alertMessage(msg, type) {
            if (type == "success") {
                this.$message.success(msg)
            } else if (type == "warning") {
                this.$message.warning(msg)
            } else if (type == "error") {
                this.$message.error(msg)
            } else {
                this.$message(msg)
            }
        },
        //检查数据格式
        convertData() {
            var flag = true
            this.tableAttrs.forEach(attr => {
                this.form[attr.prop] == attr.type(this.form[attr.prop])
                if (attr.type === Number && isNaN(this.form[attr.prop])) {
                    flag = false
                }
            });

            return flag
        }
    },
    watch: {
        //监控currentRow的更新来更新按钮使能
        currentRow(current, old) {
            if (current !== null) {
                this.disableDeleteAndEdit = false
            } else {
                this.disableDeleteAndEdit = true
            }
        }
    },
    computed: {
        attrWidth: function() {
            var browserLength = document.documentElement.clientWidth * 0.9
            return Math.floor(browserLength / this.tableAttrs.length)
        }
    }
}
</script>

<style>

</style>
