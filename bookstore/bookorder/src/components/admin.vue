<template>
    <div style="width: 80%;height: 100%;margin: 0 auto;">
        <el-tabs>
            <el-tab-pane label="书籍管理">
                <div style="width:100%;">
                    <el-button type="success" style="float:left;" @click.native="addNewBook">新增</el-button>
                    <el-button type="danger" style="float:left;" @click.native="deleteBook">删除</el-button>
                    <el-button type="primary" style="float:left;margin-right:10px;" @click.native="editBook">编辑</el-button>
                    
                    <el-dialog title="添加图书" :visible.sync="addBookDialogVisible" width="30%">
                        <el-form ref="form" :model="add_form" label-width="80px">
                            <el-form-item label="图书ID">
                                <el-input v-model="add_form.id"></el-input>
                            </el-form-item>
                            <el-form-item label="书名">
                                <el-input v-model="add_form.name"></el-input>
                            </el-form-item>
                            <el-form-item label="作者">
                                <el-input v-model="add_form.author"></el-input>
                            </el-form-item>
                            <el-form-item label="出版日期">
                                <el-input v-model="add_form.date"></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                            <el-button @click="cancleAddBook">取消</el-button>
                            <el-button type="primary" @click="postNewBook">添加</el-button>
                        </span>
                    </el-dialog>

                    <el-dialog title="编辑图书" :visible.sync="editBookDialogVisible" width="30%">
                        <el-form ref="form" :model="edit_form" label-width="80px">
                            <el-form-item label="图书ID">
                                <el-input :disabled="true" v-model="edit_form.id"></el-input>
                            </el-form-item>
                            <el-form-item label="书名">
                                <el-input v-model="edit_form.name"></el-input>
                            </el-form-item>
                            <el-form-item label="作者">
                                <el-input v-model="edit_form.author"></el-input>
                            </el-form-item>
                            <el-form-item label="出版日期">
                                <el-input v-model="edit_form.date"></el-input>
                            </el-form-item>
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                            <el-button @click="cancleEditBook">取消</el-button>
                            <el-button type="primary" @click="updateBook">修改</el-button>
                        </span>
                    </el-dialog>
                </div>
                <el-table highlight-current-row :data="bookTableData"  @current-change="handleCurrentChange" style="width: 100%">
                    <el-table-column prop="id" label="图书ID" width="180"></el-table-column>
                    <el-table-column prop="name" label="书名" width="180"></el-table-column>
                    <el-table-column prop="author" label="作者" width="180"></el-table-column>
                    <el-table-column prop="date" label="出版日期"></el-table-column>
                </el-table>
            </el-tab-pane>
            <el-tab-pane label="借阅记录">
                <el-table :data="borrowTableData" style="width: 100%">
                    <el-table-column prop="time" label="借阅时间" width="180"></el-table-column>
                    <el-table-column prop="id" label="标签ID"></el-table-column>
                </el-table>
            </el-tab-pane>
        </el-tabs>
        <el-alert v-show="alertVisible" :title="alertMsg" :type="alertType"></el-alert>
    </div>
</template>

<script>
export default {
    data() {
        return {
             bookTableData: [],
             borrowTableData: [],
             bookTableCurrentRow: null,
             add_form: {
                 'id': '',
                 'name': '',
                 'author': '',
                 'date': ''
             },
             edit_form: {
                 'id': '',
                 'name': '',
                 'author': '',
                 'date': ''
             },
             addBookDialogVisible: false,
             editBookDialogVisible: false,
             alertMsg: '',
             alertType: 'success',
             alertVisible: false
        }
    },
    created() {
        var that = this
        this.$axios.get('/api/book')
            .then(function (res) {
                that.bookTableData = []
                res.data.forEach(function (book) {
                    that.bookTableData.push(book)
                })
            })
            .catch(function (res) {
                that.$notify.error({
                    title: '数据请求失败',
                    message: JSON.stringify(res)
                })
            })
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
    },
    methods: {
        handleCurrentChange(selectRow) {
            this.bookTableCurrentRow = selectRow
        },
        addNewBook() {
            this.addBookDialogVisible = true
        },
        editBook() {
            if (!this.bookTableCurrentRow) {
                return
            }
            this.editBookDialogVisible = true
            this.edit_form = {
                'id':       this.bookTableCurrentRow.id,
                'name':     this.bookTableCurrentRow.name,
                'author':   this.bookTableCurrentRow.author,
                'date':     this.bookTableCurrentRow.date
            }
        },
        //新增图书接口
        postNewBook() {
            var newBook = JSON.parse(JSON.stringify(this.add_form))

            this.addBookDialogVisible = false
            var that = this

            this.$axios({
                method: 'post',
                url:'/api/book',
                data: this.$qs.stringify(newBook)
            }).then(function (res) {
                that.bookTableData.push(newBook)
                that.$notify.success({
                    title: '添加成功',
                    message: JSON.stringify(newBook)
                })
            }, function(response) {
                that.$notify.error({
                    title: '添加失败',
                    message: JSON.stringify(newBook)
                })
            }) 
        },
        //更新图书接口
        updateBook() {
            this.editBookDialogVisible = false
            var that = this

            this.$axios({
                method: 'put',
                url:'/api/book',
                data: this.$qs.stringify(that.edit_form)
            }).then(function (res) {
                for (var i = 0; i < that.bookTableData.length; i++) {
                    if (that.bookTableData[i].id == that.edit_form.id) {
                        that.bookTableData[i].name = that.edit_form.name
                        that.bookTableData[i].author = that.edit_form.author
                        that.bookTableData[i].date = that.edit_form.date
                        break
                    }
                }
                that.$notify.success({
                    title: '修改成功',
                    message: JSON.stringify(that.edit_form)
                })
            }, function(response) {
                that.$notify.error({
                    title: '修改失败',
                    message: JSON.stringify(that.edit_form)
                })
            })
        },
        cancleAddBook() {
            this.addBookDialogVisible = false
        },
        cancleEditBook() {
            this.editBookDialogVisible = false
        },
        //删除图书接口
        deleteBook() {
            if (this.bookTableCurrentRow == null) {
                return
            }
            var tmp = JSON.parse(JSON.stringify(this.bookTableCurrentRow))

            this.$axios({
                method: 'delete',
                url:'/api/book',
                data: JSON.stringify(tmp)
            }).then((res) => {
                var index = null
                for (var i = 0; i < this.bookTableData.length; i++) {
                    if (this.bookTableData[i].id == this.bookTableCurrentRow.id) {
                        index = i
                        break
                    }
                }
                if (index != null) {
                    this.bookTableData.splice(index, 1)
                }
                this.$notify.success({
                    title: '删除成功',
                    message: JSON.stringify(tmp)
                })
            }, (res) => {
                this.$notify.error({
                    title: '删除失败',
                    message: JSON.stringify(tmp)
                })
            }) 
        }
    }
}
</script>
