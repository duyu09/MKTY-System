<!--
- 文件描述：明康慧医MKTY智慧医疗系统后台管理系统病历管理页面
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
- 该文件由Copilot辅助编写，人机合作完成。
-->

<template>
  <div class="medical-records">
    <div class="header">
      <h2>病历管理</h2>
      <el-button type="primary" @click="showAddDialog">添加病历</el-button>
    </div>    <el-table :data="records" style="width: 100%" v-loading="loading">
      <el-table-column prop="medrecId" label="ID" width="80"></el-table-column>
      <el-table-column prop="patientName" label="患者" width="120"></el-table-column>
      <el-table-column prop="doctorName" label="负责医师" width="120"></el-table-column>
      <el-table-column prop="medrecAbstract" label="病历概要"></el-table-column>
      <el-table-column prop="medrecState" label="状态" width="100">
        <template #default="scope">
          {{ getStateText(scope.row.medrecState) }}
        </template>
      </el-table-column>
      <el-table-column prop="medrecContent" label="病历内容" width="200" show-overflow-tooltip></el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑病历对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="患者">
          <el-select v-model="form.medrecPatientId" filterable placeholder="请选择患者">
            <el-option
              v-for="user in patients"
              :key="user.userId"
              :label="user.userName"
              :value="user.userId">
            </el-option>
          </el-select>
        </el-form-item>        <el-form-item label="负责医师">
          <el-select v-model="form.medrecDoctorId" filterable placeholder="请选择负责医师">
            <el-option
              v-for="user in doctors"
              :key="user.userId"
              :label="user.userName"
              :value="user.userId">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="病历概要">
          <el-input type="textarea" v-model="form.medrecAbstract" rows="3"></el-input>
        </el-form-item>
        <el-form-item label="病历内容">
          <el-input type="textarea" v-model="form.medrecContent" rows="5" placeholder="请输入病历详细内容（支持Markdown格式）"></el-input>
        </el-form-item>        <el-form-item label="病历状态">
          <el-select v-model="form.medrecState">
            <el-option label="正常生效" value="0"></el-option>
            <el-option label="痊愈无效" value="1"></el-option>
            <el-option label="慢性病优先级降低" value="2"></el-option>
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
  name: 'MedicalRecords',
  data() {
    return {
      records: [],
      patients: [],
      doctors: [],
      loading: false,
      dialogVisible: false,
      dialogTitle: '添加病历',      form: {
        medrecPatientId: '',
        medrecDoctorId: '',
        medrecAbstract: '',
        medrecState: '0',
        medrecContent: ''
      },
      isEdit: false,
      currentRecordId: null
    }
  },
  created() {
    this.fetchRecords()
    this.fetchUsers()
  },
  methods: {
    async fetchRecords() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:5000/api/medical-records')
        this.records = response.data
      } catch (error) {
        this.$message.error('获取病历列表失败')
        console.error(error)
      }
      this.loading = false
    },
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/api/users')
        const users = response.data
        this.patients = users.filter(user => user.userType === '0')
        this.doctors = users.filter(user => user.userType === '1')
      } catch (error) {
        this.$message.error('获取用户列表失败')
        console.error(error)
      }
    },    getStateText(state) {
      const states = {
        '0': '正常生效',
        '1': '痊愈无效',
        '2': '慢性病优先级降低'
      }
      return states[state] || '未知'
    },showAddDialog() {
      this.dialogTitle = '添加病历'
      this.isEdit = false
      this.form = {
        medrecPatientId: '',
        medrecDoctorId: '',
        medrecAbstract: '',
        medrecState: '0',
        medrecContent: ''
      }
      this.dialogVisible = true
    },    handleEdit(row) {
      this.dialogTitle = '编辑病历'
      this.isEdit = true
      this.currentRecordId = row.medrecId
      this.form = {
        medrecPatientId: row.medrecPatientId,
        medrecDoctorId: row.medrecDoctorId,
        medrecAbstract: row.medrecAbstract,
        medrecState: row.medrecState,
        medrecContent: row.medrecContent
      }
      this.dialogVisible = true
    },
    async handleDelete(row) {
      try {
        await this.$confirm('确认删除该病历?', '提示', {
          type: 'warning'
        })
        await axios.delete(`http://localhost:5000/api/medical-records/${row.medrecId}`)
        this.$message.success('删除成功')
        this.fetchRecords()
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
          console.error(error)
        }
      }
    },
    async handleSubmit() {
      try {
        if (this.isEdit) {
          await axios.put(`http://localhost:5000/api/medical-records/${this.currentRecordId}`, this.form)
          this.$message.success('更新成功')
        } else {
          await axios.post('http://localhost:5000/api/medical-records', this.form)
          this.$message.success('添加成功')
        }
        this.dialogVisible = false
        this.fetchRecords()
      } catch (error) {
        this.$message.error(this.isEdit ? '更新失败' : '添加失败')
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.medical-records {
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