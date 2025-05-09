<template>
  <div class="home">
    <div class="header">
      <h2>系统概览</h2>
      <el-button type="danger" @click="handleLogout">退出登录</el-button>
    </div>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>用户总数</span>
              <el-icon><User /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ stats.userCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>病历总数</span>
              <el-icon><Document /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ stats.medicalRecordCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>知识条目</span>
              <el-icon><Collection /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ stats.knowledgeCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>论坛帖子</span>
              <el-icon><ChatDotRound /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ stats.forumPostCount }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>留言数量</span>
              <el-icon><Message /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ stats.messageCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>对话数量</span>
              <el-icon><ChatLineRound /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ stats.chatCount }}</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>待办事项</span>
              <el-icon><List /></el-icon>
            </div>
          </template>
          <div class="card-value">{{ stats.todoCount }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios'
import { User, Document, Collection, ChatDotRound, Message, ChatLineRound, List } from '@element-plus/icons-vue'

export default {
  name: 'Home',
  components: {
    User,
    Document,
    Collection,
    ChatDotRound,
    Message,
    ChatLineRound,
    List
  },
  data() {
    return {
      stats: {
        userCount: 0,
        medicalRecordCount: 0,
        knowledgeCount: 0,
        forumPostCount: 0,
        messageCount: 0,
        chatCount: 0,
        todoCount: 0
      }
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const [users, medicalRecords, knowledge, forumPosts, messages, chats, todos] = await Promise.all([
          axios.get('http://localhost:5000/api/users'),
          axios.get('http://localhost:5000/api/medical-records'),
          axios.get('http://localhost:5000/api/knowledge'),
          axios.get('http://localhost:5000/api/forum-posts'),
          axios.get('http://localhost:5000/api/messages'),
          axios.get('http://localhost:5000/api/chats'),
          axios.get('http://localhost:5000/api/todos')
        ])

        this.stats = {
          userCount: users.data.length,
          medicalRecordCount: medicalRecords.data.length,
          knowledgeCount: knowledge.data.length,
          forumPostCount: forumPosts.data.length,
          messageCount: messages.data.length,
          chatCount: chats.data.length,
          todoCount: todos.data.length
        }
      } catch (error) {
        this.$message.error('获取数据失败')
      }
    },
    handleLogout() {
      this.$confirm('确认退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.removeItem('token')
        this.$router.push('/login')
        this.$message.success('已退出登录')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.home {
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  text-align: center;
  padding: 10px 0;
}

.mt-20 {
  margin-top: 20px;
}
</style> 