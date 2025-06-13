<!--
- 文件描述：明康慧医MKTY智慧医疗系统后台管理系统用户管理页面
- 总负责人：齐鲁工业大学（山东省科学院）计算机科学与技术学部 软件工程（软件开发）21-1班 杜宇 (@duyu09, 202103180009@stu.qlu.edu.cn)
- 著作权声明：Copyright (c) 2025 DuYu (https://github.com/duyu09/MKTY-System)
- 该文件由Copilot辅助编写，人机合作完成。
-->

<template>
  <div class="user-management">
    <div class="header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="showAddDialog">添加用户</el-button>
    </div>

    <el-table :data="users" style="width: 100%" v-loading="loading">
      <el-table-column prop="userId" label="ID" width="80"></el-table-column>
      <el-table-column prop="userName" label="姓名" width="120"></el-table-column>
      <el-table-column prop="userType" label="用户类型" width="100">
        <template #default="scope">
          {{ getUserType(scope.row.userType) }}
        </template>
      </el-table-column>
      <el-table-column prop="userSex" label="性别" width="80">
        <template #default="scope">
          {{ scope.row.userSex ? '男' : '女' }}
        </template>
      </el-table-column>
      <el-table-column prop="userAge" label="年龄" width="80"></el-table-column>
      <el-table-column prop="userFrom" label="来源地"></el-table-column>
      <el-table-column prop="userContact" label="联系方式"></el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="姓名">
          <el-input v-model="form.userName"></el-input>
        </el-form-item>
        <el-form-item label="用户类型">
          <el-select v-model="form.userType">
            <el-option label="患者" value="0"></el-option>
            <el-option label="医师" value="1"></el-option>
            <el-option label="其他" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="form.userSex">
            <el-radio :label="true">男</el-radio>
            <el-radio :label="false">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input v-model="form.userAge"></el-input>
        </el-form-item>
        <el-form-item label="来源地">
          <el-input v-model="form.userFrom"></el-input>
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="form.userContact"></el-input>
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
  name: 'UserManagement',
  data() {
    return {
      users: [],
      loading: false,
      dialogVisible: false,
      dialogTitle: '添加用户',
      form: {
        userName: '',
        userType: '0',
        userSex: true,
        userAge: '',
        userFrom: '',
        userContact: '',
        userCiphertext: 'default_password', // 默认密码
        userSexPermission: true,
        userAgePermission: true,
        userFromPermission: true,
        userContactPermission: true,
        userImportantInfoPermission: true
      },
      isEdit: false,
      currentUserId: null
    }
  },
  created() {
    this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:5000/api/users')
        this.users = response.data
      } catch (error) {
        this.$message.error('获取用户列表失败')
        console.error(error)
      }
      this.loading = false
    },
    getUserType(type) {
      const types = {
        '0': '患者',
        '1': '医师',
        '2': '其他'
      }
      return types[type] || '未知'
    },
    showAddDialog() {
      this.dialogTitle = '添加用户'
      this.isEdit = false
      this.form = {
        userName: '',
        userType: '0',
        userSex: true,
        userAge: '',
        userFrom: '',
        userContact: '',
        userCiphertext: 'default_password',
        userSexPermission: true,
        userAgePermission: true,
        userFromPermission: true,
        userContactPermission: true,
        userImportantInfoPermission: true
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑用户'
      this.isEdit = true
      this.currentUserId = row.userId
      this.form = { ...row }
      this.dialogVisible = true
    },
    async handleDelete(row) {
      try {
        await this.$confirm('确认删除该用户?', '提示', {
          type: 'warning'
        })
        await axios.delete(`http://localhost:5000/api/users/${row.userId}`)
        this.$message.success('删除成功')
        this.fetchUsers()
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
          await axios.put(`http://localhost:5000/api/users/${this.currentUserId}`, this.form)
          this.$message.success('更新成功')
        } else {
          await axios.post('http://localhost:5000/api/users', this.form)
          this.$message.success('添加成功')
        }
        this.dialogVisible = false
        this.fetchUsers()
      } catch (error) {
        this.$message.error(this.isEdit ? '更新失败' : '添加失败')
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.user-management {
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