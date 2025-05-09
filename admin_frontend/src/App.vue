<template>
  <div id="app">
    <el-container>
      <el-aside width="200px">
        <el-menu
          router
          :default-active="$route.path"
          class="el-menu-vertical">
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-menu-item index="/medical-records">
            <el-icon><Document /></el-icon>
            <span>病历管理</span>
          </el-menu-item>
          <el-menu-item index="/knowledge">
            <el-icon><Collection /></el-icon>
            <span>知识库管理</span>
          </el-menu-item>
          <el-menu-item index="/forum">
            <el-icon><ChatDotRound /></el-icon>
            <span>论坛管理</span>
          </el-menu-item>
          <el-menu-item index="/messages">
            <el-icon><Message /></el-icon>
            <span>留言管理</span>
          </el-menu-item>
          <el-menu-item index="/chat">
            <el-icon><ChatLineRound /></el-icon>
            <span>大模型对话</span>
          </el-menu-item>
          <el-menu-item index="/todo-list">
            <el-icon><List /></el-icon>
            <span>重要事项清单</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { HomeFilled, User, Document, Collection, ChatDotRound, Message, ChatLineRound, List } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    HomeFilled,
    User,
    Document,
    Collection,
    ChatDotRound,
    Message,
    ChatLineRound,
    List
  }
}
</script>

<style>
#app {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 94vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #304156;
  color: #fff;
}

.el-menu {
  border-right: none;
}

.el-menu-vertical {
  height: 100%;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style> 