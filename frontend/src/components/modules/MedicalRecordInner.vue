<!-- Copyright (c) 2023~2025 DuYu (202103180009@stu.qlu.edu.cn, https://github.com/duyu09/MKTY-System), Faculty of Computer Science and Technology, Qilu University of Technology (Shandong Academy of Sciences) -->
<!-- 该文件为“明康慧医MKTY”智慧医疗系统病历详细内容显示组件Vue文件。该文件为MKTY系统的重要组成部分。 -->
<!-- 创建日期：2025年06月01日 -->
<!-- 修改日期：2025年06月04日 -->
<!-- 该文件为使用Copilot人机协作完成 -->
<template>
<div style="display: flex; justify-content: center; width: 100%; background-image: url('/images/medrec_bg.jpg'); background-size: cover;">
  <div class="medical-record-inner">
    <div class="loading" v-if="loading">
      <div class="loading-spinner"></div>
      <span>正在加载病历...</span>
    </div>

    <div v-else-if="medicalRecord" style="height: 95vh;">
    <el-scrollbar height="100%">
      <!-- 页面头部 -->
      <div class="header">
        <div style="padding-right: 1.5rem;">
          <button class="back-btn" @click="goBack">
            <i class="icon-back"></i>
            返回列表
          </button>
        </div>
        <div class="header-center">
          <h1 class="record-title">病历详情 #{{ medicalRecord.medrecId }}</h1>
          <span class="record-state" :class="getStateClass(medicalRecord.medrecState)">
            {{ getStateText(medicalRecord.medrecState) }}
          </span>
        </div>
        <div class="header-right" style="padding-left: 1.5rem;">
          <div v-if="canEdit">
            <button class="edit-btn" @click="editRecord">
              <i class="icon-edit"></i>
              修改病历
            </button>
          </div>
        </div>
      </div>

      <!-- 病历信息卡片 -->
      <div class="info-cards">
        <div class="info-card">
          <h3>基本信息</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">患者姓名：</span>
              <span class="value">{{ medicalRecord.patientName }}</span>
            </div>
            <div class="info-item">
              <span class="label">负责医师：</span>
              <span class="value">{{ medicalRecord.doctorName }}</span>
            </div>
            <div class="info-item">
              <span class="label">病历概要：</span>
              <span class="value">{{ medicalRecord.medrecAbstract || '无概要' }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间：</span>
              <span class="value">{{ formatTime(medicalRecord.medrecCreateTime) }}</span>
            </div>
            <div class="info-item">
              <span class="label">修改时间：</span>
              <span class="value">{{ formatTime(medicalRecord.medrecModifyTime) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 病历内容 -->
      <div class="content-card">
        <h3>病历内容</h3>
        <div class="markdown-content" v-html="renderedContent"></div>
      </div>

      <!-- 功能按钮 -->
      <div class="action-buttons" style="margin-bottom: 3rem;">
        <button class="ai-btn diagnosis-btn" @click="mri_aiAncillaryAnalysisDiagnosis()">
          <span class="icon-ai"></span>
          智能诊断
        </button>
        <button class="ai-btn medication-btn" @click="mri_aiAncillaryAnalysisRecommendations()">
          <span class="icon-medicine"></span>
          药物推荐
        </button>
      </div>
      </el-scrollbar>
    </div>

    <!-- 权限不足提示 -->
    <div class="no-permission" v-else-if="!hasPermission">
      <div class="no-permission-icon">🚫</div>
      <h2>无权查看</h2>
      <p>您没有权限查看此病历，只有患者本人和负责医师可以查看。</p>
      <button class="back-btn" @click="goBack">返回列表</button>
    </div>

    <!-- 编辑/创建病历弹窗 -->
    <div class="modal-overlay" v-if="showEditModal" @click="closeModal">
      <div class="modal-content" @click.stop>        <div class="modal-header">
          <h2>修改病历</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
          <div class="modal-body">
          <div class="form-group">
            <label>病历概要：</label>
            <input 
              v-model="editForm.medrecAbstract" 
              type="text" 
              placeholder="请输入病历概要"
            >
          </div>
          
          <div class="form-group">
            <label>病历状态：</label>
            <select v-model="editForm.medrecState">
              <option value="0">正常生效</option>
              <option value="1">痊愈无效</option>
              <option value="2">慢性病优先级降低</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>病历内容：</label>
            <MarkdownEditorComponents v-model="editForm.medrecContent" />
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeModal">取消</button>
          <button class="save-btn" @click="saveRecord" :disabled="saving">
            {{ saving ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</div>

  <el-dialog title="明康慧医大模型智能分析诊断与药物推荐（结论仅供参考）" v-model="mri_aiAncillaryAnalysisDialogVisible" width="60%" style="height: 66vh;">
    <el-scrollbar max-height="50vh">
    <el-card style="background-color: rgb(230, 230, 230);">
    <div style="color: black; font-size: 1.05rem; font-weight: bold;">
      基于<span class="rainbow_text" style="font-weight: 900;">MKTY-3B-Chat</span>大模型，
      系统针对该病历作分析，提供初步诊断和药物推荐，供您参考。
    </div>
    </el-card>
    <div v-loading="mri_aiAncillaryAnalysisLoading" element-loading-text="AI正在思考中..." element-loading-background="rgba(40, 40, 40, 0.75)">
    <el-card style="margin-top: 0.75rem; height: 100%;">
    <template #header>
      <div class="card-header" style="color: black; font-size: medium; font-weight: bold;">
        <span>{{ mri_aiAncillaryAnalysisTitle }}&nbsp;分析结果</span>
      </div>
    </template>
    <div>
      <div v-html="mri_aiAncillaryAnalysisResultRendered"></div>
    </div>
    </el-card>
    <div style="margin-top: 0.75rem; display: flex; justify-content: flex-end;">
      <el-button type="primary" @click="mri_aiAncillaryAnalysisDiagnosis()">
        💡&nbsp;大模型分析
      </el-button>
    </div>
    </div>
    </el-scrollbar>
  </el-dialog>

</template>

<script>
import { getMedicalRecord, updateMedicalRecord, getUserInfo, getCookie, llmInferenceGetStatus, llmInferenceSubmitTask } from '@/api/api.js';
import { errHandle, successHandle, msgHandle } from '@/utils/tools.js';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import MarkdownEditorComponents from '@/components/modules/MarkdownEditorComponents.vue';
import "@/assets/css/colorful_div.css";
import "@/assets/css/rainbow_text.css";

export default {
  name: 'MedicalRecordInner',
  components: {
    MarkdownEditorComponents
  },
  data() {
    return {
      loading: true,
      medicalRecord: null,
      hasPermission: true,
      userType: 0,
      userId: null,      
      canEdit: false,
      showEditModal: false,
      saving: false,      
      editForm: {
        medrecAbstract: '',
        medrecState: '0',
        medrecContent: {
          html: '',
          md: ''
        }
      },
      mri_aiAncillaryAnalysisDialogVisible: false,
      mri_aiAncillaryAnalysisLoading: false,
      mri_aiAncillaryAnalysisResultRendered: '',
      mri_aiAncillaryAnalysisTitle: '',  // 智能诊断或药物推荐
    }
  },

  computed: {
    renderedContent() {
      if (!this.medicalRecord?.medrecContent) return ''
      const html = marked.parse(this.medicalRecord.medrecContent)
      return DOMPurify.sanitize(html)
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
          this.canEdit = this.userType === 1 // 只有医师可以编辑
          await this.loadMedicalRecord()
        } else {
          errHandle('获取用户信息失败：' + userRes.data.msg)
        }
      } catch (error) {
        errHandle('加载用户信息时出错：' + error.message)
        this.loading = false
      }
    },

    async loadMedicalRecord() {
      try {
        const medrecId = this.$route.query.medrecId
        if (!medrecId) {
          errHandle('病历ID无效')
          this.goBack()
          return
        }

        const res = await getMedicalRecord(parseInt(medrecId))
        if (res.data.code === 0) {
          this.medicalRecord = res.data.medicalRecord
          this.hasPermission = true
        } else if (res.data.code === 2) {
          this.hasPermission = false
        } else {
          errHandle('获取病历详情失败：' + res.data.msg)
        }
      } catch (error) {
        errHandle('加载病历详情时出错：' + error.message)
      } finally {
        this.loading = false
      }
    },
    editRecord() {
      this.editForm = {
        medrecAbstract: this.medicalRecord.medrecAbstract || '',
        medrecState: this.medicalRecord.medrecState,
        medrecContent: {
          html: '',
          md: this.medicalRecord.medrecContent || ''
        }
      }
      this.showEditModal = true
    },

    async saveRecord() {
      if (!this.validateForm()) return      this.saving = true
      try {
        const res = await updateMedicalRecord(
          this.medicalRecord.medrecId,
          this.editForm.medrecAbstract,
          this.editForm.medrecState,
          this.editForm.medrecContent.md
        )
        if (res.data.code === 0) {
          successHandle('病历修改成功')
          this.closeModal()
          await this.loadMedicalRecord()
        } else {
          errHandle('修改病历失败：' + res.data.msg)
        }
      } catch (error) {
        errHandle('保存病历时出错：' + error.message)
      } finally {
        this.saving = false
      }
    },    validateForm() {
      if (!this.editForm.medrecAbstract.trim()) {
        msgHandle('请输入病历概要')
        return false
      }
      if (!this.editForm.medrecContent.md.trim()) {
        msgHandle('请输入病历内容')
        return false
      }
      return true
    },    closeModal() {
      this.showEditModal = false
      this.editForm = {
        medrecAbstract: '',
        medrecState: '0',
        medrecContent: { html: '', md: '' }
      }
    },

    goBack() {
      this.$router.push('/main/MedicalRecordOverview')
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
    },

    formatTime(timestamp) {
      const date = new Date(parseInt(timestamp) * 1000)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    mri_aiAncillaryAnalysisDiagnosis(){
      this.mri_aiAncillaryAnalysisTitle = '🤖智能诊断';
      this.mri_aiAncillaryAnalysisDialogVisible = true;
      this.mri_aiAncillaryAnalysisLoading = true;
      this.mri_aiAncillaryAnalysisResultRendered = '';
      const history_context = [];
        var prompt = "辅助诊断任务。以下内容是患者的病历，请你深度挖掘病历信息，从医学专业角度和逻辑方面展开论述辅助分析病情，充分阐述理由并给出详细的治疗建议。\n病历内容：";
        prompt = prompt + this.renderedContent;
        llmInferenceSubmitTask(history_context, prompt).then((res) => {
          if(res.data.code != 0) {
            errHandle("未成功发送数据：" + res.data.msg);
            this.mri_aiAncillaryAnalysisLoading = false;
            // this.mri_aiAncillaryAnalysisDialogVisible = false;
            return;
          }
          const task_id = res.data.taskId;
          const mri_aiIntervalId = setInterval(() => {
            llmInferenceGetStatus(task_id).then((res2) => {
              if(res2.data.code != 0) {
                clearInterval(mri_aiIntervalId);
                errHandle("未成功获取响应：" + res2.data.msg);
                this.mri_aiAncillaryAnalysisLoading = false;
                // this.mri_aiAncillaryAnalysisDialogVisible = false;
                return;
              }
              if (res2.data.taskStatus == 0){
                clearInterval(mri_aiIntervalId);
                const task_result = res2.data.taskResult;
                this.mri_aiAncillaryAnalysisResultRendered = task_result;
                this.mri_aiAncillaryAnalysisLoading = false;
              }
            });
          }, 3500);
        }).catch((error) => {
          errHandle("AI分析执行失败：" + error);
          this.mri_aiAncillaryAnalysisLoading = false;
          // this.mri_aiAncillaryAnalysisDialogVisible = false;
        });
    },

    mri_aiAncillaryAnalysisRecommendations(){
      this.mri_aiAncillaryAnalysisTitle = '💊药物推荐';
      this.mri_aiAncillaryAnalysisDialogVisible = true;
      this.mri_aiAncillaryAnalysisLoading = true;
      this.mri_aiAncillaryAnalysisResultRendered = '';
      const history_context = [];
        var prompt = "医药推荐任务。以下内容是患者的病历，请你深度挖掘病历信息，从医学专业角度和逻辑方面，辅助医师给出详细的推荐药物清单和治疗建议。病历内容：";
        prompt = prompt + this.renderedContent;
        llmInferenceSubmitTask(history_context, prompt).then((res) => {
          if(res.data.code != 0) {
            errHandle("未成功发送数据：" + res.data.msg);
            this.mri_aiAncillaryAnalysisLoading = false;
            // this.mri_aiAncillaryAnalysisDialogVisible = false;
            return;
          }
          const task_id = res.data.taskId;
          const mri_aiIntervalId = setInterval(() => {
            llmInferenceGetStatus(task_id).then((res2) => {
              if(res2.data.code != 0) {
                clearInterval(mri_aiIntervalId);
                errHandle("未成功获取响应：" + res2.data.msg);
                this.mri_aiAncillaryAnalysisLoading = false;
                // this.mri_aiAncillaryAnalysisDialogVisible = false;
                return;
              }
              if (res2.data.taskStatus == 0){
                clearInterval(mri_aiIntervalId);
                const task_result = res2.data.taskResult;
                this.mri_aiAncillaryAnalysisResultRendered = task_result;
                this.mri_aiAncillaryAnalysisLoading = false;
              }
            });
          }, 3500);
        }).catch((error) => {
          errHandle("AI分析执行失败：" + error);
          this.mri_aiAncillaryAnalysisLoading = false;
          // this.mri_aiAncillaryAnalysisDialogVisible = false;
        });
    }

  }
}
</script>

<style scoped>
.medical-record-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 90vh;
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.header-center {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.record-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin: 0 0 10px 0;
  font-weight: 600;
}

.record-state {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
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

.back-btn {
  padding: 10px 20px;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background: #5a6268;
  transform: translateY(-2px);
}

.icon-back::before {
  content: '←';
  margin-right: 8px;
}

.edit-btn, .create-btn {
  padding: 10px 20px;
  margin-left: 10px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.edit-btn {
  background: #007bff;
  color: white;
}

.edit-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

.create-btn {
  background: #28a745;
  color: white;
}

.create-btn:hover {
  background: #1e7e34;
  transform: translateY(-2px);
}

.icon-edit::before {
  content: '✏️';
  margin-right: 8px;
}

.icon-create::before {
  content: '➕';
  margin-right: 8px;
}

.info-cards {
  margin-bottom: 25px;
}

.info-card, .content-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  padding: 25px;
  margin-bottom: 25px;
}

.info-card h3, .content-card h3 {
  font-size: 1.4rem;
  color: #2c3e50;
  margin: 0 0 20px 0;
  font-weight: 600;
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 15px;
}

.info-item {
  display: flex;
  flex-direction: column;
}

.label {
  font-weight: 600;
  color: #495057;
  margin-bottom: 5px;
}

.value {
  color: #6c757d;
  font-size: 0.95rem;
}

.markdown-content {
  line-height: 1.6;
  color: #495057;
}

.markdown-content h1, .markdown-content h2, .markdown-content h3 {
  color: #2c3e50;
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.markdown-content p {
  margin-bottom: 1em;
}

.markdown-content ul, .markdown-content ol {
  padding-left: 1.5em;
  margin-bottom: 1em;
}

.markdown-content code {
  background: #f8f9fa;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.markdown-content pre {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 1em;
}

.action-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 30px;
}

.ai-btn {
  padding: 15px 30px;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 160px;
}

.diagnosis-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.diagnosis-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.medication-btn {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.medication-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(240, 147, 251, 0.4);
}

.icon-ai::before {
  content: '🤖';
  margin-right: 8px;
}

.icon-medicine::before {
  content: '💊';
  margin-right: 8px;
}

.no-permission {
  text-align: center;
  padding: 60px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.no-permission-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.no-permission h2 {
  font-size: 1.8rem;
  color: #e74c3c;
  margin-bottom: 15px;
}

.no-permission p {
  color: #7f8c8d;
  font-size: 1.1rem;
  margin-bottom: 30px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 15px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #adb5bd;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #6c757d;
}

.modal-body {
  padding: 25px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #495057;
}

.form-group input, .form-group select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus, .form-group select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  padding: 20px 25px;
  border-top: 1px solid #e9ecef;
}

.cancel-btn, .save-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}

.cancel-btn:hover {
  background: #5a6268;
}

.save-btn {
  background: #007bff;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background: #0056b3;
  transform: translateY(-2px);
}

.save-btn:disabled {
  background: #adb5bd;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .medical-record-inner {
    padding: 15px;
  }
  
  .header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  
  .header-right {
    display: flex;
    gap: 10px;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .modal-content {
    width: 95%;
    margin: 20px;
  }
}
</style>