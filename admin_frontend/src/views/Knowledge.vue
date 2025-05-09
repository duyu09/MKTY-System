<template>
  <div class="knowledge">
    <div class="header">
      <h2>知识库管理</h2>
      <el-button type="primary" @click="showAddDialog">添加知识</el-button>
    </div>

    <el-table :data="entities" style="width: 100%" v-loading="loading">
      <el-table-column prop="keId" label="ID" width="80"></el-table-column>
      <el-table-column prop="keName" label="名称" width="200"></el-table-column>
      <el-table-column prop="keFileType" label="文件类型" width="120"></el-table-column>
      <el-table-column prop="keAbstract" label="概要"></el-table-column>
      <el-table-column prop="isKeMultimodal" label="多模态" width="100">
        <template #default="scope">
          {{ scope.row.isKeMultimodal ? '是' : '否' }}
        </template>
      </el-table-column>
      <el-table-column prop="keCreateTime" label="创建时间" width="180">
        <template #default="scope">
          {{ formatTime(scope.row.keCreateTime) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加/编辑知识对话框 -->
    <el-dialog :title="dialogTitle" v-model="dialogVisible" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="form.keName"></el-input>
        </el-form-item>
        <el-form-item label="文件类型">
          <el-select v-model="form.keFileType">
            <el-option label="文本" value="text"></el-option>
            <el-option label="图片" value="image"></el-option>
            <el-option label="视频" value="video"></el-option>
            <el-option label="音频" value="audio"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="概要">
          <el-input type="textarea" v-model="form.keAbstract" rows="4"></el-input>
        </el-form-item>
        <el-form-item label="多模态">
          <el-switch v-model="form.isKeMultimodal"></el-switch>
        </el-form-item>
        <el-form-item label="特征向量">
          <el-input type="textarea" v-model="form.keTextEigenVectors" rows="4" placeholder="请输入JSON格式的特征向量"></el-input>
        </el-form-item>
        <el-form-item label="资源列表">
          <el-input type="textarea" v-model="form.keResList" rows="4" placeholder="请输入JSON格式的资源列表"></el-input>
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
  name: 'Knowledge',
  data() {
    return {
      entities: [],
      loading: false,
      dialogVisible: false,
      dialogTitle: '添加知识',
      form: {
        keName: '',
        keFileType: 'text',
        keAbstract: '',
        isKeMultimodal: false,
        keTextEigenVectors: '',
        keResList: ''
      },
      isEdit: false,
      currentEntityId: null
    }
  },
  created() {
    this.fetchEntities()
  },
  methods: {
    async fetchEntities() {
      this.loading = true
      try {
        const response = await axios.get('http://localhost:5000/api/knowledge')
        this.entities = response.data
      } catch (error) {
        this.$message.error('获取知识列表失败')
        console.error(error)
      }
      this.loading = false
    },
    formatTime(timestamp) {
      const date = new Date(parseInt(timestamp) * 1000)
      return date.toLocaleString()
    },
    showAddDialog() {
      this.dialogTitle = '添加知识'
      this.isEdit = false
      this.form = {
        keName: '',
        keFileType: 'text',
        keAbstract: '',
        isKeMultimodal: false,
        keTextEigenVectors: '',
        keResList: ''
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑知识'
      this.isEdit = true
      this.currentEntityId = row.keId
      this.form = {
        ...row,
        keTextEigenVectors: JSON.stringify(row.keTextEigenVectors, null, 2),
        keResList: JSON.stringify(row.keResList, null, 2)
      }
      this.dialogVisible = true
    },
    async handleDelete(row) {
      try {
        await this.$confirm('确认删除该知识?', '提示', {
          type: 'warning'
        })
        await axios.delete(`http://localhost:5000/api/knowledge/${row.keId}`)
        this.$message.success('删除成功')
        this.fetchEntities()
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
          keTextEigenVectors: JSON.parse(this.form.keTextEigenVectors || 'null'),
          keResList: JSON.parse(this.form.keResList || 'null')
        }

        if (this.isEdit) {
          await axios.put(`http://localhost:5000/api/knowledge/${this.currentEntityId}`, submitData)
          this.$message.success('更新成功')
        } else {
          await axios.post('http://localhost:5000/api/knowledge', submitData)
          this.$message.success('添加成功')
        }
        this.dialogVisible = false
        this.fetchEntities()
      } catch (error) {
        this.$message.error(this.isEdit ? '更新失败' : '添加失败')
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.knowledge {
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