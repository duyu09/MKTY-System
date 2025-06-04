<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统病历概览组件Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年06月01日 -->
<!-- 修改日期：2025年06月04日 -->
<!-- 该文件为使用Copilot人机协作完成 -->
<template>
<div style="display: flex; justify-content: center; width: 100%; background-image: url('/images/medrec_bg.jpg'); background-size: cover;">
  <div class="medical-record-overview">
    <div class="header">
      <div class="header-content">
        <div class="title-section">
          <h2 class="title">
            <span class="icon-medical"></span>
            病历管理
          </h2>
          <p class="subtitle">
            {{ userType === 1 ? '您负责的患者病历' : '您的病历记录' }}
          </p>
        </div>
        <div class="action-section" v-if="userType === 1" style="margin-left:2rem;">
          <button class="create-btn" @click="createRecord">
            <span class="icon-create"></span>
            新建病历
          </button>
        </div>
      </div>
    </div>

    <div class="loading" v-if="loading">
      <div class="loading-spinner"></div>
      <span>正在加载病历...</span>
    </div>

    <div class="records-container" v-else style="height: calc(90vh - 3.5rem - 100px);">
    <el-scrollbar height="100%">
      <div class="empty-state" v-if="medicalRecords.length === 0">
        <div class="empty-icon">📋</div>
        <h3>暂无病历记录</h3>
        <p>{{ userType === 1 ? '您还没有负责任何患者的病历' : '您还没有任何病历记录' }}</p>
      </div>

      <div class="records-grid" v-else>
        <div
          class="record-card"
          v-for="record in medicalRecords"
          :key="record.medrecId"
          @click="viewRecord(record.medrecId)"
        >
          <div class="card-header">
            <span class="record-id">病历 #{{ record.medrecId }}</span>
            <span class="record-state" :class="getStateClass(record.medrecState)">
              {{ getStateText(record.medrecState) }}
            </span>
          </div>
          
          <div class="card-content">
            <h3 class="record-abstract">{{ record.medrecAbstract || '无概要' }}</h3>
            
            <div class="record-info">
              <div class="info-item">
                <span class="icon-patient"></span>
                <span>患者：{{ record.patientName }}</span>
              </div>
              <div class="info-item">
                <span class="icon-doctor"></span>
                <span>医师：{{ record.doctorName }}</span>
              </div>
            </div>
            
            <div class="record-time">
              <div class="time-item">
                <span class="time-label">创建时间：</span>
                <span class="time-value">{{ formatTime(record.medrecCreateTime) }}</span>
              </div>
              <div class="time-item" v-if="record.medrecModifyTime !== record.medrecCreateTime">
                <span class="time-label">更新时间：</span>
                <span class="time-value">{{ formatTime(record.medrecModifyTime) }}</span>
              </div>
            </div>
          </div>
          
          <div class="card-footer">
            <button class="view-btn">
              <i class="icon-view"></i>
              查看详情
            </button>
          </div>
        </div>
      </div>
      </el-scrollbar>
    </div>

    <!-- 创建病历弹窗 -->
    <div class="modal-overlay" v-if="showCreateModal" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>创建病历</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="form-group">
            <label>所属病患ID：</label>
            <input 
              v-model="createForm.medrecPatientId" 
              type="number" 
              placeholder="请输入患者用户ID"
            >
          </div>
          
          <div class="form-group">
            <label>病历概要：</label>
            <input 
              v-model="createForm.medrecAbstract" 
              type="text" 
              placeholder="请输入病历概要"
            >
          </div>
          
          <div class="form-group">
            <label>病历状态：</label>
            <select v-model="createForm.medrecState">
              <option value="0">正常生效</option>
              <option value="1">痊愈无效</option>
              <option value="2">慢性病优先级降低</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>病历内容：</label>
            <MarkdownEditorComponents v-model="createForm.medrecContent" />
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeModal">取消</button>
          <button class="save-btn" @click="saveRecord" :disabled="saving">
            {{ saving ? '创建中...' : '创建' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import { getMedicalRecords, getUserInfo, getCookie, createMedicalRecord } from '@/api/api.js'
import { errHandle, successHandle, msgHandle } from '@/utils/tools.js'
import MarkdownEditorComponents from '@/components/modules/MarkdownEditorComponents.vue'

export default {
  name: 'MedicalRecordOverview',
  components: {
    MarkdownEditorComponents
  },
  data() {
    return {
      loading: true,
      medicalRecords: [],
      userType: 0, // 0=患者，1=医师，2=其他
      userId: null,
      showCreateModal: false,
      saving: false,
      createForm: {
        medrecPatientId: '',
        medrecAbstract: '',
        medrecState: '0',
        medrecContent: {
          html: '',
          md: ''
        }
      }
    }
  },
  
  mounted() {
    this.loadUserInfo()
  },

  methods: {
    async loadUserInfo() {
      try {
        this.userId = parseInt(getCookie('userId'))
        const userRes = await getUserInfo(this.userId)
        if (userRes.data.code === 0) {
          this.userType = parseInt(userRes.data.userInfo.userType)
          await this.loadMedicalRecords()
        } else {
          errHandle('获取用户信息失败：' + userRes.data.msg)
        }
      } catch (error) {
        errHandle('加载用户信息时出错：' + error.message)
        this.loading = false
      }
    },

    async loadMedicalRecords() {
      try {
        const res = await getMedicalRecords()
        if (res.data.code === 0) {
          this.medicalRecords = res.data.medicalRecords
        } else {
          errHandle('获取病历列表失败：' + res.data.msg)
        }
      } catch (error) {
        errHandle('加载病历列表时出错：' + error.message)
      } finally {
        this.loading = false
      }
    },

    viewRecord(medrecId) {
      // 跳转到病历详情页面
      this.$router.push(`/main/MedicalRecordInner?medrecId=${medrecId}`)
    },

    getStateClass(state) {
      const stateMap = {
        '0': 'state-active',
        '1': 'state-recovered',
        '2': 'state-chronic'
      }
      return stateMap[state] || 'state-unknown'
    },

    getStateText(state) {
      const stateMap = {
        '0': '正常生效',
        '1': '痊愈无效',
        '2': '慢性病优先级降低'
      }
      return stateMap[state] || '未知状态'
    },    formatTime(timestamp) {
      const date = new Date(parseInt(timestamp) * 1000)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    createRecord() {
      this.createForm = {
        medrecPatientId: '',
        medrecAbstract: '',
        medrecState: '0',
        medrecContent: {
          html: '',
          md: ''
        }
      }
      this.showCreateModal = true
    },

    async saveRecord() {
      if (!this.validateForm()) return

      this.saving = true
      try {
        const res = await createMedicalRecord(
          parseInt(this.createForm.medrecPatientId),
          this.createForm.medrecAbstract,
          this.createForm.medrecState,
          this.createForm.medrecContent.md
        )
        if (res.data.code === 0) {
          successHandle('病历创建成功')
          this.closeModal()
          await this.loadMedicalRecords() // 刷新列表
          // 可选：跳转到新创建的病历详情页
          this.$router.push(`/main/MedicalRecordInner?medrecId=${res.data.medrecId}`)
        } else {
          errHandle('创建病历失败：' + res.data.msg)
        }
      } catch (error) {
        errHandle('创建病历时出错：' + error.message)
      } finally {
        this.saving = false
      }
    },

    validateForm() {
      if (!this.createForm.medrecPatientId) {
        msgHandle('请输入患者ID')
        return false
      }
      if (!this.createForm.medrecAbstract.trim()) {
        msgHandle('请输入病历概要')
        return false
      }
      if (!this.createForm.medrecContent.md.trim()) {
        msgHandle('请输入病历内容')
        return false
      }
      return true
    },

    closeModal() {
      this.showCreateModal = false
      this.createForm = {
        medrecPatientId: '',
        medrecAbstract: '',
        medrecState: '0',
        medrecContent: { html: '', md: '' }
      }
    }
  }
}
</script>

<style scoped>
.medical-record-overview {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 90vh;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
}

.title-section {
  flex: 1;
}

.action-section {
  flex-shrink: 0;
}

.create-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(39, 174, 96, 0.4);
}

.icon-create::before {
  content: '➕';
}

.title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin: 0 0 10px 0;
  font-weight: 600;
}

.icon-medical::before {
  content: '🏥';
  margin-right: 10px;
}

.subtitle {
  font-size: 1.1rem;
  color: #7f8c8d;
  margin: 0;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.empty-state p {
  color: #7f8c8d;
  font-size: 1rem;
}

.records-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 25px;
}

.record-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.record-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px 15px;
  border-bottom: 1px solid #ecf0f1;
}

.record-id {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.1rem;
}

.record-state {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.state-active {
  background: #d4edda;
  color: #155724;
}

.state-recovered {
  background: #cce5ff;
  color: #004085;
}

.state-chronic {
  background: #fff3cd;
  color: #856404;
}

.state-unknown {
  background: #f8d7da;
  color: #721c24;
}

.card-content {
  padding: 0 25px 20px;
}

.record-abstract {
  font-size: 1.2rem;
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-weight: 500;
  line-height: 1.4;
}

.record-info {
  margin-bottom: 15px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  color: #7f8c8d;
  font-size: 0.95rem;
}

.icon-patient::before {
  content: '👤';
  margin-right: 8px;
}

.icon-doctor::before {
  content: '👨‍⚕️';
  margin-right: 8px;
}

.record-time {
  font-size: 0.9rem;
  color: #95a5a6;
}

.time-item {
  margin-bottom: 5px;
}

.time-label {
  font-weight: 500;
}

.time-value {
  margin-left: 5px;
}

.card-footer {
  padding: 15px 25px;
  background: #f8f9fa;
  border-top: 1px solid #ecf0f1;
}

.view-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.view-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.icon-view::before {
  /* content: '👁️'; */
  margin-right: 8px;
}

@media (max-width: 768px) {
  .medical-record-overview {
    padding: 15px;
  }
  
  .records-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .header {
    padding: 20px;
  }

  .header-content {
    flex-direction: column;
    gap: 20px;
  }
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 15px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 30px;
  border-bottom: 1px solid #ecf0f1;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #95a5a6;
  padding: 5px;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #ecf0f1;
  color: #2c3e50;
}

.modal-body {
  padding: 30px;
}

.form-group {
  margin-bottom: 25px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #ecf0f1;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
}

.modal-footer {
  display: flex;
  gap: 15px;
  padding: 25px 30px;
  border-top: 1px solid #ecf0f1;
  justify-content: flex-end;
}

.cancel-btn,
.save-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: #95a5a6;
  color: white;
}

.cancel-btn:hover {
  background: #7f8c8d;
}

.save-btn {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
}

.save-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(52, 152, 219, 0.4);
}

.save-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
</style>