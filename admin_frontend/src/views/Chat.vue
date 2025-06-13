<!--
- 文件描述：明康慧医MKTY智慧医疗系统后台管理系统LLM对话管理页面
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
- 该文件由Copilot辅助编写，人机合作完成。
-->

<template>
  <div class="chat-container">
    <div class="header">
      <h2>大模型对话管理</h2>
      <el-button type="primary" @click="showAddDialog">新建对话</el-button>
    </div>

    <el-table :data="chats" style="width: 100%">
      <el-table-column prop="chatId" label="ID" width="80" />
      <el-table-column prop="userName" label="用户" width="120" />
      <el-table-column label="对话内容" min-width="200">
        <template #default="scope">
          <el-button type="primary" link @click="showContentDialog(scope.row)">
            查看对话内容
          </el-button>
        </template>
      </el-table-column>
      <el-table-column prop="chatStatus" label="状态" width="100">
        <template #default="scope">
          {{ scope.row.chatStatus ? '私密' : '公开' }}
        </template>
      </el-table-column>
      <el-table-column prop="chatCreateTime" label="创建时间" width="180">
        <template #default="scope">
          {{ formatTime(scope.row.chatCreateTime) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="primary" link @click="handleEdit(scope.row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑对话' : '新建对话'"
      width="50%"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="用户">
          <el-select v-model="form.chatUserId" placeholder="请选择用户">
            <el-option
              v-for="user in users"
              :key="user.userId"
              :label="user.userName"
              :value="user.userId"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="对话内容">
          <el-input
            v-model="form.chatContent"
            type="textarea"
            :rows="4"
            placeholder="请输入对话内容（JSON格式）"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="form.chatStatus"
            :active-value="true"
            :inactive-value="false"
            active-text="私密"
            inactive-text="公开"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 查看对话内容对话框 -->
    <el-dialog
      v-model="contentDialogVisible"
      title="对话内容"
      width="70%"
    >
      <div class="json-content">
        <pre><code class="language-json">{{ formattedContent }}</code></pre>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import 'highlight.js/lib/languages/json'

export default {
  name: 'Chat',
  data() {
    return {
      chats: [],
      users: [],
      dialogVisible: false,
      contentDialogVisible: false,
      isEdit: false,
      currentContent: null,
      form: {
        chatUserId: '',
        chatContent: '',
        chatStatus: false
      }
    }
  },
  computed: {
    formattedContent() {
      if (!this.currentContent) return ''
      try {
        return JSON.stringify(this.currentContent, null, 2)
      } catch (e) {
        return this.currentContent
      }
    }
  },
  mounted() {
    this.fetchChats()
    this.fetchUsers()
  },
  methods: {
    async fetchChats() {
      try {
        const response = await axios.get('http://localhost:5000/api/chats')
        this.chats = response.data
      } catch (error) {
        console.error('获取对话列表失败:', error)
        this.$message.error('获取对话列表失败')
      }
    },
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/api/users')
        this.users = response.data
      } catch (error) {
        console.error('获取用户列表失败:', error)
        this.$message.error('获取用户列表失败')
      }
    },
    formatTime(timestamp) {
      if (!timestamp) return ''
      const date = new Date(parseInt(timestamp))
      return date.toLocaleString()
    },
    showContentDialog(row) {
      this.currentContent = row.chatContent
      this.contentDialogVisible = true
      this.$nextTick(() => {
        document.querySelectorAll('pre code').forEach((block) => {
          hljs.highlightElement(block)
        })
      })
    },
    showAddDialog() {
      this.isEdit = false
      this.form = {
        chatUserId: '',
        chatContent: '',
        chatStatus: false
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.isEdit = true
      this.form = {
        chatId: row.chatId,
        chatUserId: row.chatUserId,
        chatContent: JSON.stringify(row.chatContent, null, 2),
        chatStatus: row.chatStatus
      }
      this.dialogVisible = true
    },
    async handleDelete(row) {
      try {
        await this.$confirm('确认删除该对话吗？', '提示', {
          type: 'warning'
        })
        await axios.delete(`http://localhost:5000/api/chats/${row.chatId}`)
        this.$message.success('删除成功')
        this.fetchChats()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除对话失败:', error)
          this.$message.error('删除对话失败')
        }
      }
    },
    async handleSubmit() {
      try {
        const data = {
          chatUserId: this.form.chatUserId,
          chatContent: JSON.parse(this.form.chatContent),
          chatStatus: this.form.chatStatus
        }

        if (this.isEdit) {
          await axios.put(`http://localhost:5000/api/chats/${this.form.chatId}`, data)
          this.$message.success('更新成功')
        } else {
          await axios.post('http://localhost:5000/api/chats', data)
          this.$message.success('创建成功')
        }
        this.dialogVisible = false
        this.fetchChats()
      } catch (error) {
        console.error('提交失败:', error)
        this.$message.error('提交失败：' + (error.response?.data?.message || error.message))
      }
    }
  }
}
</script>

<style scoped>
.chat-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.json-content {
  background-color: #f8f9fa;
  border-radius: 4px;
  padding: 16px;
  max-height: 500px;
  overflow: auto;
}

.json-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

:deep(.el-dialog__body) {
  padding-top: 10px;
}
</style> 