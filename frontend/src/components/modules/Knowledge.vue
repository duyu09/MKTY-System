<!--
- 文件描述：明康慧医MKTY智慧医疗系统知识库管理组件
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 文件名：Knowledge.vue
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
- 该文件由Copilot协作人机合作完成。
-->

<template>
  <div class="knowledge-overview">
    <el-scrollbar height="100%">
    <div class="header">
      <div class="nav-buttons">
        <button 
          :class="['nav-btn', { active: currentTab === 'browse' }]"
          @click="currentTab = 'browse'"
        >
          <b>浏览知识</b>
        </button>
        <button 
          :class="['nav-btn', { active: currentTab === 'create' }]"
          @click="currentTab = 'create'"
        >
          <b>创建知识</b>
        </button>
        <button 
          :class="['nav-btn', { active: currentTab === 'favorites' }]"
          @click="currentTab = 'favorites'; loadUserFavorites()"
        >
          <b>我的收藏</b>
        </button>
      </div>
      <div></div>
    </div>

    <!-- 浏览知识板块 -->
    <div v-if="currentTab === 'browse'" style="display: flex; flex-direction: column;">
      <div class="search-bar">
        <el-input 
          v-model="searchKeyword" 
          @keyup.enter="searchEntities"
          placeholder="输入关键词搜索知识实体，留空显示全部"
          class="search-input"
        />
        <button @click="searchEntities" class="search-btn">搜索</button>
      </div>
    <div style="flex:1; overflow: hidden;">
      <div class="entities-grid" v-if="entities.length > 0">
        <div 
          v-for="entity in entities" 
          :key="entity.keId"
          class="entity-card"
        >
          <div class="entity-header">
            <h3 @click="showEntityDetail(entity)" class="entity-title">{{ entity.keName }}</h3>
            <div class="entity-meta">
              <span class="create-time">
                <el-icon><Clock /></el-icon>创建时间：{{ formatTime(entity.keCreateTime) }}
              </span>
            </div>
          </div>
          <div class="entity-abstract">
            <el-icon><EditPen /></el-icon>
            {{ entity.keAbstract || '暂无描述' }}
          </div>
          <div class="entity-actions">
            <button @click="showEntityDetail(entity)" class="action-btn detail-btn">查看详情</button>
            <button @click="downloadEntity(entity.keId)" class="action-btn download-btn">下载</button>
            <button @click="favoriteEntity(entity.keId)" class="action-btn favorite-btn">收藏</button>
          </div>
        </div>
      </div>
      <div v-else class="no-data">
        <p>暂无知识实体</p>
      </div>
    </div>
    </div>

    <!-- 创建知识板块 -->
    <div v-if="currentTab === 'create'" style="display: flex; justify-content: center; align-items: center;">
      <div class="create-form" style="width: 60%;">
        <h3>新建知识资源实体</h3>
        
        <div class="form-group">
          <label>知识实体名称 *</label>
          <el-input 
            v-model="createForm.keName" 
            placeholder="请输入知识实体名称"
          />
        </div>

        <div class="form-group">
          <label>概要描述</label>
          <el-input 
            type="textarea"
            v-model="createForm.keAbstract" 
            placeholder="请输入知识实体的概要描述"
            rows="4"
          ></el-input>
        </div>

        <div class="form-group">
          <label>上传文件 *</label>
          <div class="file-upload">
            <input 
              type="file" 
              @change="handleFileSelect"
              accept=".txt,.docx,.pptx,.pdf"
              class="file-input"
              ref="fileInput"
              style="margin-bottom: 10px;"
            />
            <div class="file-info" v-if="selectedFile">
              <span>{{ selectedFile.name }}</span>
              <span class="file-size">({{ formatFileSize(selectedFile.size) }})</span>
            </div>
            <div class="file-hint">
              支持格式：txt、docx、pptx、pdf
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button @click="resetCreateForm" class="action-btn cancel-btn">重置</button>
          <button 
            @click="createEntity" 
            :disabled="!canSubmit"
            class="action-btn submit-btn"
          >
            新建知识实体
          </button>
        </div>
      </div>
    </div>

    <!-- 我的收藏板块 -->
    <div v-if="currentTab === 'favorites'">
      <div class="collection-header">
        <h3><el-icon><Collection /></el-icon> {{ this.userName }} 的个人资源收藏夹</h3>
      </div>
      
      <div class="entities-grid" v-if="favorites.length > 0">
        <div 
          v-for="entity in favorites" 
          :key="entity.keId"
          class="entity-card"
        >
          <div class="entity-header">
            <h3 @click="showEntityDetail(entity)" class="entity-title">{{ entity.keName }}</h3>
            <div class="entity-meta">
              <span><el-icon><Clock /></el-icon>创建时间：{{ formatTime(entity.keCreateTime) }}</span>
            </div>
          </div>
          <div class="entity-abstract"><el-icon><EditPen /></el-icon>{{ entity.keAbstract || '暂无描述' }}</div>
          <div class="entity-actions">
            <button @click="showEntityDetail(entity)" class="action-btn detail-btn">查看详情</button>
            <button @click="downloadEntity(entity.keId)" class="action-btn download-btn">下载</button>
          </div>
        </div>
      </div>

      <div v-else class="no-data">
        <p>暂无收藏的知识实体</p>
      </div>
    </div>

    <!-- 实体详情弹窗 -->
    <div v-if="showDetailModal" class="modal-overlay" @click="closeDetailModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ selectedEntity.keName }}</h3>
          <button @click="closeDetailModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="detail-item">
            <label><b>创建时间：</b></label>
            <span>{{ formatTime(selectedEntity.keCreateTime) }}</span>
          </div>
          <div class="detail-item">
            <label><b>文件类型：</b></label>
            <span>{{ getFileTypeName(selectedEntity.keFileType) }}</span>
          </div>
          <div class="detail-item">
            <label><b>概要描述：</b></label>
            <p>{{ selectedEntity.keAbstract || '暂无描述' }}</p>
          </div>
          
          <!-- 知识检索功能 -->
          <div class="search-pieces-section">
            <h4><el-icon><Search /></el-icon>片段检索</h4>
            <div class="search-pieces-form">
              <el-input 
                v-model="searchQuery" 
                placeholder="输入查询内容，检索相关知识片段"
                class="search-input"
                @keyup.enter="searchPieces"
              />
              <button @click="searchPieces" class="search-btn">检索</button>
            </div>
            
            <div v-if="searchResults.length > 0" class="search-results">
              <h5>相关知识片段：</h5>
              <div 
                v-for="(result, index) in searchResults" 
                :key="index"
                class="result-item"
              >
                <div class="similarity-score">相似度得分: {{ result.similarity.toFixed(4) }}</div>
                <div class="content">{{ result.content }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="downloadEntity(selectedEntity.keId)" class="action-btn download-btn">下载文件</button>
          <button @click="closeDetailModal" class="action-btn cancel-btn">关闭</button>
        </div>
      </div>
    </div>

    <!-- 加载提示 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>{{ loadingText }}</p>
    </div>
    </el-scrollbar>
  </div>
</template>

<script>
import { 
  createKnowledgeEntity, 
  searchKnowledgeEntities, 
  downloadKnowledgeEntity, 
  favoriteKnowledgeEntity, 
  getUserFavorites, 
  searchKnowledgePieces,
  convertBlobToBase64,
  getUserInfo,
  getCookie
} from '@/api/api.js';
import { msgHandle, errHandle, convertTime } from '@/utils/tools.js';
import { Clock, EditPen, Search, Collection } from "@element-plus/icons-vue";
import "@/assets/css/file_input.css";

export default {
  name: 'KnowledgeOverview',
  data() {
    return {
      currentTab: 'browse', // 当前激活的标签页
      
      // 浏览相关
      searchKeyword: '',
      entities: [],
      
      // 创建相关
      createForm: {
        keName: '',
        keAbstract: ''
      },
      selectedFile: null,
      
      // 收藏相关
      favorites: [],
      
      // 详情弹窗相关
      showDetailModal: false,
      selectedEntity: {},
      searchQuery: '',
      searchResults: [],
      
      // 状态相关
      loading: false,
      loadingText: '处理中...',

      // 用户相关
      userName: '加载中...'
    }
  },
  components:{
    Clock, EditPen, Search, Collection
  },
  computed: {
    canSubmit() {
      return this.createForm.keName.trim() && this.selectedFile
    }
  },
  mounted() {
    this.searchEntities()
    this.getUserName()
  },
  methods: {
    // 读取用户名称
    async getUserName(){
      try {
        const userId = parseInt(getCookie('userId'));
        const response = await getUserInfo(userId);
        if (response.data.code == 0) {
          this.userName = response.data.userInfo.userName
        } else {
          errHandle(response.data.msg)
        }
      } catch (error) {
        errHandle('加载用户名称失败：' + error.message)
      }
    },
    // 搜索知识实体
    async searchEntities() {
      try {
        this.loading = true
        this.loadingText = '搜索中...'
        console.log(this.searchKeyword)
        const response = await searchKnowledgeEntities(this.searchKeyword)
        if (response.data.code === 0) {
          this.entities = response.data.entities
        } else {
          errHandle(response.data.msg)
        }
      } catch (error) {
        errHandle('搜索失败：' + error.message)
      } finally {
        this.loading = false
      }
    },

    // 处理文件选择
    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        // 检查文件类型
        const allowedTypes = [
          'text/plain',
          'application/pdf',
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
          'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        ]
        
        if (!allowedTypes.includes(file.type)) {
          errHandle('不支持的文件格式，请选择txt、docx、pptx或pdf文件')
          return
        }
        
        this.selectedFile = file
      }
    },

    // 创建知识实体
    async createEntity() {
      if (!this.canSubmit) {
        errHandle('请填写完整信息')
        return
      }

      try {
        this.loading = true
        this.loadingText = '创建中，请稍候...'

        // 将文件转换为base64
        const fileContent = await convertBlobToBase64(this.selectedFile)
        
        const response = await createKnowledgeEntity(
          this.createForm.keName,
          this.createForm.keAbstract,
          fileContent.split(',')[1], // 移除data:mime/type;base64,前缀
          this.selectedFile.type
        )

        if (response.data.code === 0) {
          msgHandle('知识实体创建成功')
          this.resetCreateForm()
          // 切换到浏览页面并刷新
          this.currentTab = 'browse'
          this.searchEntities()
        } else {
          errHandle(response.data.msg)
        }
      } catch (error) {
        errHandle('创建失败：' + error.message)
      } finally {
        this.loading = false
      }
    },

    // 重置创建表单
    resetCreateForm() {
      this.createForm = {
        keName: '',
        keAbstract: ''
      }
      this.selectedFile = null
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
    },

    // 下载知识实体
    downloadEntity(keId) {
      try {
        downloadKnowledgeEntity(keId)
      } catch (error) {
        errHandle('下载失败：' + error.message)
      }
    },

    // 收藏知识实体
    async favoriteEntity(keId) {
      try {
        const response = await favoriteKnowledgeEntity(keId)
        if (response.data.code === 0) {
          msgHandle('收藏成功')
        } else {
          errHandle(response.data.msg)
        }
      } catch (error) {
        errHandle('收藏失败：' + error.message)
      }
    },

    // 加载用户收藏
    async loadUserFavorites() {
      try {
        this.loading = true
        this.loadingText = '加载中...'
        
        const response = await getUserFavorites()
        if (response.data.code === 0) {
          this.favorites = response.data.favorites
        } else {
          errHandle(response.data.msg)
        }
      } catch (error) {
        errHandle('加载失败：' + error.message)
      } finally {
        this.loading = false
      }
    },

    // 显示实体详情
    showEntityDetail(entity) {
      this.selectedEntity = entity
      this.searchQuery = ''
      this.searchResults = []
      this.showDetailModal = true
    },

    // 关闭详情弹窗
    closeDetailModal() {
      this.showDetailModal = false
      this.selectedEntity = {}
      this.searchQuery = ''
      this.searchResults = []
    },

    // 搜索知识片段
    async searchPieces() {
      if (!this.searchQuery.trim()) {
        errHandle('请输入搜索内容')
        return
      }

      try {
        this.loading = true
        this.loadingText = '检索中...'
        
        const response = await searchKnowledgePieces(
          this.selectedEntity.keId,
          this.searchQuery,
          3
        )
        
        if (response.data.code === 0) {
          this.searchResults = response.data.results
          if (this.searchResults.length === 0) {
            msgHandle('未找到相关知识片段')
          }
        } else {
          errHandle(response.data.msg)
        }
      } catch (error) {
        errHandle('检索失败：' + error.message)
      } finally {
        this.loading = false
      }
    },

    // 格式化时间
    formatTime(timestamp) {
      if (!timestamp) return '未知'
      // const date = new Date(parseInt(timestamp) * 1000)
      // return date.toLocaleString('zh-CN')
      return convertTime(parseInt(timestamp) * 1000)
    },

    // 格式化文件大小
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },

    // 获取文件类型名称
    getFileTypeName(mimeType) {
      const typeMap = {
        'text/plain': 'TXT文档',
        'application/pdf': 'PDF文档',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Word文档',
        'application/msword': 'Word文档',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'PowerPoint演示文稿',
        'application/vnd.ms-powerpoint': 'PowerPoint演示文稿'
      }
      return typeMap[mimeType] || '未知格式'
    }
  }
}
</script>

<style scoped>
.knowledge-overview {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  height: 84vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0;
  padding-bottom: 20px;
}

.header h2 {
  margin: 0;
  color: #333;
  font-size: 28px;
}

.nav-buttons {
  display: flex;
  gap: 10px;
}

.nav-btn {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: #f8f9fa;
  color: #666;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: #e9ecef;
  border-color: #adb5bd;
}

.nav-btn.active {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  width: 61.8%;
}

.search-input {
  flex: 1;
  padding: 2px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.search-btn {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.search-btn:hover {
  background: #0056b3;
}

.entities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.entity-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: box-shadow 0.3s ease;
}

.entity-card:hover {
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
  background-color: rgb(245, 245, 245);
}

.entity-header {
  margin-bottom: 15px;
}

.entity-title {
  margin: 0 0 8px 0;
  color: #007bff;
  cursor: pointer;
  font-size: 18px;
  transition: color 0.3s ease;
}

.entity-title:hover {
  color: #0056b3;
  text-decoration: underline;
}

.entity-meta {
  font-size: 12px;
  color: #666;
}

.entity-abstract {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.5;
  max-height: 3.6em;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.entity-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.action-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s ease;
}

.detail-btn {
  background: #28a745;
  color: white;
  border-color: #28a745;
}

.detail-btn:hover {
  background: #218838;
}

.download-btn {
  background: #17a2b8;
  color: white;
  border-color: #17a2b8;
}

.download-btn:hover {
  background: #138496;
}

.favorite-btn {
  background: #ffc107;
  color: white;
  border-color: #ffc107;
}

.favorite-btn:hover {
  background: #e0a800;
}

.submit-btn {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.submit-btn:hover:not(:disabled) {
  background: #0056b3;
}

.submit-btn:disabled {
  background: #6c757d;
  border-color: #6c757d;
  cursor: not-allowed;
}

.cancel-btn {
  background: #6c757d;
  color: white;
  border-color: #6c757d;
}

.cancel-btn:hover {
  background: #545b62;
}

.create-form {
  max-width: 600px;
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.create-form h3 {
  margin: 0 0 25px 0;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.file-upload {
  border: 2px dashed #ddd;
  border-radius: 6px;
  padding: 20px;
  text-align: center;
  transition: border-color 0.3s ease;
}

.file-upload:hover {
  border-color: #007bff;
}

.file-info {
  margin: 10px 0;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
}

.file-size {
  color: #666;
  font-size: 12px;
}

.file-hint {
  font-size: 12px;
  color: #666;
  margin-top: 8px;
}

.form-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 30px;
}

.no-data {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

.detail-item {
  margin-bottom: 15px;
}

.detail-item label {
  font-weight: 500;
  color: #333;
  margin-right: 10px;
}

.search-pieces-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
}

.search-pieces-section h4 {
  margin: 0 0 15px 0;
  color: #333;
}

.search-pieces-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-results h5 {
  margin: 0 0 15px 0;
  color: #333;
}

.result-item {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 10px;
  background: #f8f9fa;
}

.similarity-score {
  font-size: 12px;
  color: #007bff;
  font-weight: 500;
  margin-bottom: 8px;
}

.result-item .content {
  line-height: 1.6;
  color: #333;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255,255,255,0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading p {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.collection-header {
  margin-bottom: 1rem; 
  background-color: rgb(210,210,210); 
  text-align: center; 
  padding-top: 0.75rem; 
  padding-bottom: 0.75rem; 
  border-radius: 10px;
}

.collection-header:hover{
  background-color: rgb(180,180,180);
  transition: background-color 0.3s ease;
}

</style>