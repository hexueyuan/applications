<template>
    <div style="margin: 20px;">
        <!--按钮-->
        <div>
            <el-button type="success" @click="handleAddEvent">新增</el-button>
            <!--删除和编辑按钮应该在选中行的模式下启用-->
            <el-button type="danger"  @click="handleDeleteEvent" :disabled="disableDeleteAndEdit">删除</el-button>
            <el-button type="primary" @click="handleEditEvent"   :disabled="disableDeleteAndEdit">编辑</el-button>
        </div>
        <!--表格主体-->
        <el-table ref="singleTable" :data="tableData" highlight-current-row @current-change="handleRowSelect" style="width: 100%">
            <el-table-column type="index" width="100"></el-table-column>
            <el-table-column v-for="attr in tableAttrs" v-bind:key="attr.prop" :prop="attr.prop" :label="attr.label" :width="attr.width"></el-table-column>
        </el-table>
        <!--弹窗-->
        <el-dialog :visible.sync="dialogVisible" :show-close="false"  :close-on-press-escape="false" :close-on-click-modal="false" width="400px">
            <!--form根据配置生成-->
            <el-form ref="form" :model="form" label-width="80px">
                <el-form-item v-for="attr in tableAttrs" v-bind:key="attr.prop" :label="attr.label">
                    <el-input v-model="form[attr.prop]" :disabled="mode == 'edit' && attr['primary_key']"></el-input>
                </el-form-item>
            </el-form>
            <!--确定和取消按钮-->
            <el-button type="primary" @click="submitData">确定</el-button>
            <el-button type="danger" @click="cancleSumbitData" plain>取消</el-button>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data() {
        return {
            tableAttrs: [],
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
            tableData: []
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
        //提交数据
        submitData() {
            if (this.convertData()) {
                    var data = this.form
                    //新增模式和编辑模式
                    //编辑模式下主键不可写
                    if (this.mode === 'add') {
                        this.postToDB(data)
                    } else if (this.mode === 'edit') {
                        this.updateInDB(data)
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
        },
        //取消sumbit数据
        cancleSumbitData() {
            //清空form
            this.form = {}
            this.dialogVisible = false
        },
        //新增数据传到后台
        postToDB(data) {
            var api = this.$conf.table_data_api
            this.$axios.post(api, data).then(res => {
                this.tableData.push(data)
                this.alertMessage('新增数据成功', 'success')
            }).catch(() => {
                this.alertMessage('新增数据失败', 'error')
            })
        },
        //删除数据传到后台
        deleteFromDB(data) {
            var api = this.$conf.table_data_api
            var primary_attr = this.tableAttrs.find(one => {
                return one['primary_key'] == true
            })
            var pd = {}
            pd[primary_attr.prop] = data[primary_attr.prop]
            this.$axios.delete(api + '?' + this.$qs.stringify(pd)).then(res => {
                this.alertMessage('删除数据成功', 'success')
                var i = this.tableData.findIndex(item => {
                    return item.name === data.name
                })
                this.tableData.splice(i, 1)
            }).catch(() => {
                this.alertMessage('删除数据失败', 'error')
            })
        },
        //更新数据传到后台
        updateInDB(data) {
            var api = this.$conf.table_data_api
            this.$axios.put(api, data).then(res => {
                this.alertMessage('修改数据成功', 'success')
                var i = this.tableData.findIndex(item => {
                    return item.name === data.name
                })
                this.tableData[i] = data
            }).catch(() => {
                this.alertMessage('修改数据失败', 'error')
            })
        },

        //请求表格配置
        requestConfig() {
            var api = this.$conf.table_config_api
            this.$axios.get(api).then(res => {
                this.tableAttrs = res.data.sort((a, b) => {
                    return a.index - b.index
                })
                //计算列宽度
                this.tableAttrs.forEach(element => {
                    element.width = this.attrWidth
                })
                if (this.attrWidth == 180) {
                    this.tableAttrs[this.tableAttrs.length - 1].width = undefined
                }
                console.log(this.tableAttrs)
            })
        },

        //请求表格数据
        requestData() {
            var api = this.$conf.table_data_api
            this.$axios.get(api).then(res => {
                this.tableData = res.data
            })
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

        //转换并检查数据格式
        convertData() {
            var flag = true
            this.tableAttrs.forEach(attr => {
                var type = null
                if (attr.type == "Integer") {
                    type = Number
                } else if (attr.type == "String") {
                    type = String
                }
                this.form[attr.prop] = type(this.form[attr.prop])
                if (attr.type === 'Integer' && isNaN(this.form[attr.prop])) {
                    flag = false
                }
            });

            return flag
        }
    },
    mounted() {
        //当页面被挂载时请求配置和数据
        this.requestConfig()
        this.requestData()
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
        //计算列宽
        //当列过多时设置滑动
        attrWidth: function() {
            var browserLength = document.documentElement.clientWidth * 0.9
            var width =  Math.floor(browserLength / this.tableAttrs.length)
            if (width > 180) {
                return 180
            }else if (width < 60) {
                return 100
            } else {
                return width
            }
        }
    }
}
</script>