<template>
  <div class="todo-list">
    <div class="header">
      <h2>重要事项清单管理</h2>
      <el-button type="primary" @click="showAddDialog">添加事项</el-button>
    </div>

    <el-table :data="todos" style="width: 100%" v-loading="loading">
      <el-table-column prop="todoId" label="ID" width="80"></el-table-column>
      <el-table-column prop="userName" label="用户" width="120"></el-table-column>
      <el-table-column prop="todoContent" label="内容">
        <template #default="scope">
          {{ formatContent(scope.row.todoContent) }}
        </template>
      </el-table-column>
      <el-table-column prop="todoPriority" label="优先级" width="100">
        <template #default="scope">
          {{ getPriorityText(scope.row.todoPriority) }}
        </template>
      </el-table-column>
      <el-table-column prop="todoStatus" label="状态" width="100">
        <template #default="scope">
          {{ getStatusText(scope.row.todoStatus) }}
        </template>
      </el-table-column>
      <el-table-column prop="todoCreateTime" label="创建时间" width="180">
        <template #default="scope">
          {{ formatTime(scope.row.todoCreateTime) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑事项对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="事项内容">
          <el-input type="textarea" v-model="form.todoContent" rows="4"></el-input>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="form.todoPriority">
            <el-option label="高" :value="0"></el-option>
            <el-option label="中" :value="1"></el-option>
            <el-option label="低" :value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.todoStatus">
            <el-option label="未完成" :value="0"></el-option>
            <el-option label="已完成" :value="1"></el-option>
            <el-option label="已删除" :value="2"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TodoList',
  data() {
    return {
      todos: [],
      loading: false,
      dialogVisible: false,
      dialogTitle: '添加事项',
      form: {
        todoContent: '',
        todoPriority: 1,
        todoStatus: 0
      },
      isEdit: false,
      currentTodoId: null
    }
  },
  created() {
    this.fetchTodos()
  },
  methods: {
    async fetchTodos() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:5000/api/todos')
        this.todos = response.data
      } catch (error) {
        this.$message.error('获取事项列表失败')
        console.error(error)
      }
      this.loading = false
    },
    formatTime(timestamp) {
      const date = new Date(parseInt(timestamp) * 1000)
      return date.toLocaleString()
    },
    formatContent(content) {
      try {
        const parsedContent = JSON.parse(content)
        return parsedContent.content || ''
      } catch {
        return content
      }
    },
    getPriorityText(priority) {
      const priorityMap = {
        0: '高',
        1: '中',
        2: '低'
      }
      return priorityMap[priority] || '未知'
    },
    getStatusText(status) {
      const statusMap = {
        0: '未完成',
        1: '已完成',
        2: '已删除'
      }
      return statusMap[status] || '未知'
    },
    showAddDialog() {
      this.dialogTitle = '添加事项'
      this.isEdit = false
      this.form = {
        todoContent: '',
        todoPriority: 1,
        todoStatus: 0
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑事项'
      this.isEdit = true
      this.currentTodoId = row.todoId
      this.form = {
        todoContent: this.formatContent(row.todoContent),
        todoPriority: row.todoPriority,
        todoStatus: row.todoStatus
      }
      this.dialogVisible = true
    },
    async handleDelete(row) {
      try {
        await this.$confirm('确认删除该事项?', '提示', {
          type: 'warning'
        })
        await axios.delete(`http://localhost:5000/api/todos/${row.todoId}`)
        this.$message.success('删除成功')
        this.fetchTodos()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
          console.error(error)
        }
      }
    },
    async handleSubmit() {
      try {
        const submitData = {
          ...this.form,
          todoContent: JSON.stringify({ content: this.form.todoContent }),
          todoUserId: 1 // 这里应该使用当前登录用户的ID
        }

        if (this.isEdit) {
          await axios.put(`http://localhost:5000/api/todos/${this.currentTodoId}`, submitData)
          this.$message.success('更新成功')
        } else {
          await axios.post('http://localhost:5000/api/todos', submitData)
          this.$message.success('添加成功')
        }
        this.dialogVisible = false
        this.fetchTodos()
      } catch (error) {
        this.$message.error(this.isEdit ? '更新失败' : '添加失败')
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.todo-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
}
</style> 