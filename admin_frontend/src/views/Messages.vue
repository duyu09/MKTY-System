<template>
  <div class="messages">
    <div class="header">
      <h2>留言管理</h2>
      <el-button type="primary" @click="showAddDialog">添加留言</el-button>
    </div>

    <el-table :data="messages" style="width: 100%" v-loading="loading">
      <el-table-column prop="messageId" label="ID" width="80"></el-table-column>
      <el-table-column prop="senderName" label="发送者" width="120"></el-table-column>
      <el-table-column prop="receiverName" label="接收者" width="120"></el-table-column>
      <el-table-column prop="messageContent" label="内容">
        <template #default="scope">
          {{ formatContent(scope.row.messageContent) }}
        </template>
      </el-table-column>
      <el-table-column prop="messageStatus" label="状态" width="100">
        <template #default="scope">
          {{ getStatusText(scope.row.messageStatus) }}
        </template>
      </el-table-column>
      <el-table-column prop="messageCreateTime" label="发送时间" width="180">
        <template #default="scope">
          {{ formatTime(scope.row.messageCreateTime) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑留言对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="接收者">
          <el-select v-model="form.messageReceiverId" filterable placeholder="请选择接收者">
            <el-option
              v-for="user in users"
              :key="user.userId"
              :label="user.userName"
              :value="user.userId">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="留言内容">
          <el-input type="textarea" v-model="form.messageContent" rows="4"></el-input>
        </el-form-item>
        <el-form-item label="留言状态">
          <el-select v-model="form.messageStatus">
            <el-option label="正常" :value="0"></el-option>
            <el-option label="已删除" :value="1"></el-option>
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
  name: 'Messages',
  data() {
    return {
      messages: [],
      users: [],
      loading: false,
      dialogVisible: false,
      dialogTitle: '添加留言',
      form: {
        messageReceiverId: '',
        messageContent: '',
        messageStatus: 0
      },
      isEdit: false,
      currentMessageId: null
    }
  },
  created() {
    this.fetchMessages()
    this.fetchUsers()
  },
  methods: {
    async fetchMessages() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:5000/api/messages')
        this.messages = response.data
      } catch (error) {
        this.$message.error('获取留言列表失败')
        console.error(error)
      }
      this.loading = false
    },
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/api/users')
        this.users = response.data
      } catch (error) {
        this.$message.error('获取用户列表失败')
        console.error(error)
      }
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
    getStatusText(status) {
      const statusMap = {
        0: '正常',
        1: '已删除'
      }
      return statusMap[status] || '未知'
    },
    showAddDialog() {
      this.dialogTitle = '添加留言'
      this.isEdit = false
      this.form = {
        messageReceiverId: '',
        messageContent: '',
        messageStatus: 0
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑留言'
      this.isEdit = true
      this.currentMessageId = row.messageId
      this.form = {
        messageReceiverId: row.messageReceiverId,
        messageContent: this.formatContent(row.messageContent),
        messageStatus: row.messageStatus
      }
      this.dialogVisible = true
    },
    async handleDelete(row) {
      try {
        await this.$confirm('确认删除该留言?', '提示', {
          type: 'warning'
        })
        await axios.delete(`http://localhost:5000/api/messages/${row.messageId}`)
        this.$message.success('删除成功')
        this.fetchMessages()
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
          messageContent: JSON.stringify({ content: this.form.messageContent }),
          messageSenderId: 1 // 这里应该使用当前登录用户的ID
        }

        if (this.isEdit) {
          await axios.put(`http://localhost:5000/api/messages/${this.currentMessageId}`, submitData)
          this.$message.success('更新成功')
        } else {
          await axios.post('http://localhost:5000/api/messages', submitData)
          this.$message.success('添加成功')
        }
        this.dialogVisible = false
        this.fetchMessages()
      } catch (error) {
        this.$message.error(this.isEdit ? '更新失败' : '添加失败')
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.messages {
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