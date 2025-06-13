<!--
- 文件描述：明康慧医MKTY智慧医疗系统后台管理系统论坛管理页面
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
- 该文件由Copilot辅助编写，人机合作完成。
-->

<template>
  <div class="forum">
    <div class="header">
      <h2>论坛管理</h2>
      <el-button type="primary" @click="showAddForumDialog">添加论坛</el-button>
    </div>

    <el-tabs v-model="activeTab">
      <el-tab-pane label="论坛列表" name="forums">
        <el-table :data="forums" style="width: 100%" v-loading="loading">
          <el-table-column prop="forumId" label="ID" width="80"></el-table-column>
          <el-table-column prop="forumName" label="名称" width="200"></el-table-column>
          <el-table-column prop="forumType" label="类型" width="100">
            <template #default="scope">
              {{ scope.row.forumType ? '公开' : '私密' }}
            </template>
          </el-table-column>
          <el-table-column prop="forumPermission" label="权限" width="100">
            <template #default="scope">
              {{ scope.row.forumPermission ? '公开' : '私密' }}
            </template>
          </el-table-column>
          <el-table-column prop="forumStatus" label="状态" width="100">
            <template #default="scope">
              {{ getStatusText(scope.row.forumStatus) }}
            </template>
          </el-table-column>
          <el-table-column prop="creatorName" label="创建者" width="120"></el-table-column>
          <el-table-column prop="forumCreateTime" label="创建时间" width="180">
            <template #default="scope">
              {{ formatTime(scope.row.forumCreateTime) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="250">
            <template #default="scope">
              <el-button size="small" @click="handleEditForum(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDeleteForum(scope.row)">删除</el-button>
              <el-button size="small" type="primary" @click="showPosts(scope.row)">查看帖子</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="帖子列表" name="posts" v-if="selectedForum">
        <div class="posts-header">
          <h3>{{ selectedForum.forumName }} - 帖子列表</h3>
          <el-button type="primary" @click="showAddPostDialog">添加帖子</el-button>
        </div>

        <el-table :data="posts" style="width: 100%" v-loading="postsLoading">
          <el-table-column prop="postId" label="ID" width="80"></el-table-column>
          <el-table-column prop="posterName" label="发帖人" width="120"></el-table-column>
          <el-table-column prop="postContent" label="内容">
            <template #default="scope">
              <el-button type="primary" link @click="showJsonContent(scope.row.postContent)">
                查看内容
              </el-button>
            </template>
          </el-table-column>
          <el-table-column prop="postPraiseNumber" label="点赞数" width="100"></el-table-column>
          <el-table-column prop="postStatus" label="状态" width="100">
            <template #default="scope">
              {{ getPostStatusText(scope.row.postStatus) }}
            </template>
          </el-table-column>
          <el-table-column prop="postCreateTime" label="发布时间" width="180">
            <template #default="scope">
              {{ formatTime(scope.row.postCreateTime) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="scope">
              <el-button size="small" @click="handleEditPost(scope.row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDeletePost(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <!-- 添加/编辑论坛对话框 -->
    <el-dialog :title="forumDialogTitle" v-model="forumDialogVisible" width="500px">
      <el-form :model="forumForm" label-width="100px">
        <el-form-item label="论坛名称">
          <el-input v-model="forumForm.forumName"></el-input>
        </el-form-item>
        <el-form-item label="论坛类型">
          <el-select v-model="forumForm.forumType">
            <el-option label="公开" :value="true"></el-option>
            <el-option label="私密" :value="false"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="论坛权限">
          <el-select v-model="forumForm.forumPermission">
            <el-option label="公开" :value="true"></el-option>
            <el-option label="私密" :value="false"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="论坛状态">
          <el-select v-model="forumForm.forumStatus">
            <el-option label="正常" :value="0"></el-option>
            <el-option label="已关闭" :value="1"></el-option>
            <el-option label="已删除" :value="2"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="forumDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleForumSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 添加/编辑帖子对话框 -->
    <el-dialog :title="postDialogTitle" v-model="postDialogVisible" width="600px">
      <el-form :model="postForm" label-width="100px">
        <el-form-item label="帖子内容">
          <el-input type="textarea" v-model="postForm.postContent" rows="6"></el-input>
        </el-form-item>
        <el-form-item label="帖子状态">
          <el-select v-model="postForm.postStatus">
            <el-option label="正常" :value="0"></el-option>
            <el-option label="已关闭" :value="1"></el-option>
            <el-option label="已删除" :value="2"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="postDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handlePostSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- JSON 内容查看对话框 -->
    <el-dialog
      title="帖子内容详情"
      v-model="jsonDialogVisible"
      width="800px"
      class="json-dialog"
    >
      <pre class="json-content"><code>{{ formattedJsonContent }}</code></pre>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Forum',
  data() {
    return {
      activeTab: 'forums',
      forums: [],
      posts: [],
      loading: false,
      postsLoading: false,
      selectedForum: null,
      forumDialogVisible: false,
      forumDialogTitle: '添加论坛',
      postDialogVisible: false,
      postDialogTitle: '添加帖子',
      jsonDialogVisible: false,
      jsonContent: null,
      forumForm: {
        forumName: '',
        forumType: true,
        forumPermission: true,
        forumStatus: 0
      },
      postForm: {
        postContent: '',
        postStatus: 0
      },
      isEditForum: false,
      isEditPost: false,
      currentForumId: null,
      currentPostId: null
    }
  },
  computed: {
    formattedJsonContent() {
      if (!this.jsonContent) return ''
      try {
        const content = typeof this.jsonContent === 'string' 
          ? JSON.parse(this.jsonContent) 
          : this.jsonContent
        return JSON.stringify(content, null, 2)
      } catch (e) {
        return this.jsonContent
      }
    }
  },
  created() {
    this.fetchForums()
  },
  methods: {
    async fetchForums() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:5000/api/forums')
        this.forums = response.data
      } catch (error) {
        this.$message.error('获取论坛列表失败')
        console.error(error)
      }
      this.loading = false
    },
    async fetchPosts(forumId) {
      this.postsLoading = true
      try {
        const response = await axios.get('http://localhost:5000/api/forum-posts')
        this.posts = response.data.filter(post => post.postForumId === forumId)
      } catch (error) {
        this.$message.error('获取帖子列表失败')
        console.error(error)
      }
      this.postsLoading = false
    },
    formatTime(timestamp) {
      if (!timestamp) return ''
      const date = new Date(parseInt(timestamp) * 1000)
      return date.toLocaleString()
    },
    formatContent(content) {
      if (!content) return ''
      if (typeof content === 'string') return content
      if (typeof content === 'object') {
        return JSON.stringify(content, null, 2)
      }
      return String(content)
    },
    getStatusText(status) {
      const statusMap = {
        0: '正常',
        1: '已关闭',
        2: '已删除'
      }
      return statusMap[status] || '未知'
    },
    getPostStatusText(status) {
      return this.getStatusText(status)
    },
    showAddForumDialog() {
      this.forumDialogTitle = '添加论坛'
      this.isEditForum = false
      this.forumForm = {
        forumName: '',
        forumType: true,
        forumPermission: true,
        forumStatus: 0
      }
      this.forumDialogVisible = true
    },
    handleEditForum(row) {
      this.forumDialogTitle = '编辑论坛'
      this.isEditForum = true
      this.currentForumId = row.forumId
      this.forumForm = { ...row }
      this.forumDialogVisible = true
    },
    async handleDeleteForum(row) {
      try {
        await this.$confirm('确认删除该论坛?', '提示', {
          type: 'warning'
        })
        await axios.delete(`http://localhost:5000/api/forums/${row.forumId}`)
        this.$message.success('删除成功')
        this.fetchForums()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
          console.error(error)
        }
      }
    },
    async handleForumSubmit() {
      try {
        if (this.isEditForum) {
          await axios.put(`http://localhost:5000/api/forums/${this.currentForumId}`, this.forumForm)
          this.$message.success('更新成功')
        } else {
          await axios.post('http://localhost:5000/api/forums', this.forumForm)
          this.$message.success('添加成功')
        }
        this.forumDialogVisible = false
        this.fetchForums()
      } catch (error) {
        this.$message.error(this.isEditForum ? '更新失败' : '添加失败')
        console.error(error)
      }
    },
    showPosts(forum) {
      this.selectedForum = forum
      this.activeTab = 'posts'
      this.fetchPosts(forum.forumId)
    },
    showAddPostDialog() {
      this.postDialogTitle = '添加帖子'
      this.isEditPost = false
      this.postForm = {
        postContent: '',
        postStatus: 0
      }
      this.postDialogVisible = true
    },
    handleEditPost(row) {
      this.postDialogTitle = '编辑帖子'
      this.isEditPost = true
      this.currentPostId = row.postId
      this.postForm = {
        postContent: this.formatContent(row.postContent),
        postStatus: row.postStatus
      }
      this.postDialogVisible = true
    },
    async handleDeletePost(row) {
      try {
        await this.$confirm('确认删除该帖子?', '提示', {
          type: 'warning'
        })
        await axios.delete(`http://localhost:5000/api/forum-posts/${row.postId}`)
        this.$message.success('删除成功')
        this.fetchPosts(this.selectedForum.forumId)
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
          console.error(error)
        }
      }
    },
    async handlePostSubmit() {
      try {
        const submitData = {
          ...this.postForm,
          postContent: JSON.stringify({ text: this.postForm.postContent }),
          postPosterId: 1, // 这里应该使用当前登录用户的ID
          postForumId: this.selectedForum.forumId
        }

        if (this.isEditPost) {
          await axios.put(`http://localhost:5000/api/forum-posts/${this.currentPostId}`, submitData)
          this.$message.success('更新成功')
        } else {
          await axios.post('http://localhost:5000/api/forum-posts', submitData)
          this.$message.success('添加成功')
        }
        this.postDialogVisible = false
        this.fetchPosts(this.selectedForum.forumId)
      } catch (error) {
        this.$message.error(this.isEditPost ? '更新失败' : '添加失败')
        console.error(error)
      }
    },
    showJsonContent(content) {
      this.jsonContent = content
      this.jsonDialogVisible = true
    }
  }
}
</script>

<style scoped>
.forum {
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

.posts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.posts-header h3 {
  margin: 0;
}

.content-cell {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}

.json-dialog :deep(.el-dialog__body) {
  padding: 20px;
  background-color: #1e1e1e;
  border-radius: 4px;
}

.json-content {
  margin: 0;
  padding: 15px;
  background-color: #1e1e1e;
  color: #d4d4d4;
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 14px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 500px;
  overflow-y: auto;
  border-radius: 4px;
}

.json-content code {
  color: #d4d4d4;
}
</style> 