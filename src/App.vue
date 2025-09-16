<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { SwitchButton } from '@element-plus/icons-vue'
import UserStats from './components/UserStats.vue'
import PasswordAuth from './components/PasswordAuth.vue'

const isAuthenticated = ref(false)

// 检查是否已经认证过
onMounted(() => {
  const authStatus = localStorage.getItem('mindnotes_authenticated')
  if (authStatus === 'true') {
    isAuthenticated.value = true
  }
})

// 处理认证成功
const handleAuthenticated = () => {
  isAuthenticated.value = true
}

// 注销功能（可选）
const logout = () => {
  localStorage.removeItem('mindnotes_authenticated')
  isAuthenticated.value = false
}
</script>

<template>
  <div id="app">
    <!-- 显示密码验证组件或主应用 -->
    <PasswordAuth 
      v-if="!isAuthenticated" 
      @authenticated="handleAuthenticated" 
    />
    
    <!-- 主应用内容 -->
    <div v-else class="app-content">
      <!-- 顶部工具栏（包含注销按钮） -->
      <div class="app-header">
        <h1 class="app-title">MindNotes 统计面板</h1>
        <el-button 
          type="text" 
          @click="logout" 
          class="logout-btn"
          size="small"
        >
          <el-icon><SwitchButton /></el-icon>
          注销
        </el-button>
      </div>
      
      <!-- 主要内容 -->
      <UserStats />
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.app-content {
  min-height: 100vh;
}

.app-header {
  background: white;
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e8eaec;
}

.app-title {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.logout-btn {
  color: #909399;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s;
}

.logout-btn:hover {
  background-color: #f5f7fa;
  color: #409eff;
}

.logout-btn .el-icon {
  margin-right: 4px;
}
</style>
