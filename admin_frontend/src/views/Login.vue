<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <img src="../assets/logo.svg" alt="Logo" class="logo" />
        <h2>明康慧医MKTY智慧医疗系统</h2>
        <p>管理员登录</p>
      </div>
      <el-form
        ref="loginForm"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            :prefix-icon="User"
            size="large"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            :prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            class="login-button"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'Login',
  setup() {
    return {
      User,
      Lock
    }
  },
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      try {
        await this.$refs.loginForm.validate()
        this.loading = true
        
        const response = await axios.post('http://localhost:5000/api/login', this.loginForm)
        
        if (response.data.success) {
          localStorage.setItem('token', response.data.token)
          this.$message.success('登录成功')
          this.$router.push('/')
        } else {
          this.$message.error(response.data.message || '登录失败')
        }
      } catch (error) {
        if (error.response?.data?.message) {
          this.$message.error(error.response.data.message)
        } else {
          this.$message.error('登录失败，请检查用户名和密码')
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 85vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  /* width: 120px; */
  height: 120px;
  margin-bottom: 16px;
}

.login-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
  margin-bottom: 8px;
}

.login-header p {
  margin: 0;
  font-size: 16px;
  color: #606266;
}

.login-form {
  margin-top: 20px;
}

.login-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #c0c4cc inset;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #409eff inset !important;
}
</style> 