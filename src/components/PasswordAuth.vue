<template>
  <div class="password-auth">
    <div class="auth-container">
      <div class="auth-card">
        <div class="auth-header">
          <el-icon class="lock-icon"><Lock /></el-icon>
          <h2>密码验证</h2>
          <p>请输入密码以继续访问应用</p>
        </div>
        
        <el-form @submit.prevent="handleSubmit" class="auth-form">
          <el-form-item>
            <el-input
              v-model="password"
              type="password"
              placeholder="请输入密码"
              show-password
              size="large"
              @keyup.enter="handleSubmit"
              :class="{ 'error-input': hasError }"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              @click="handleSubmit"
              :loading="loading"
              size="large"
              class="submit-btn"
            >
              {{ loading ? '验证中...' : '进入应用' }}
            </el-button>
          </el-form-item>
        </el-form>
        
        <div v-if="errorMessage" class="error-message">
          <el-icon><Warning /></el-icon>
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Lock, Warning } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const emit = defineEmits<{
  authenticated: []
}>()

const password = ref('')
const loading = ref(false)
const hasError = ref(false)
const errorMessage = ref('')

// 设置正确的密码（在实际项目中，这应该通过更安全的方式处理）
const CORRECT_PASSWORD = 'mindnotes2025'

const handleSubmit = async () => {
  if (!password.value.trim()) {
    showError('请输入密码')
    return
  }

  loading.value = true
  hasError.value = false
  errorMessage.value = ''

  // 模拟验证过程
  setTimeout(() => {
    if (password.value === CORRECT_PASSWORD) {
      ElMessage.success('密码验证成功！')
      // 将认证状态保存到 localStorage
      localStorage.setItem('mindnotes_authenticated', 'true')
      emit('authenticated')
    } else {
      showError('密码错误，请重试')
    }
    loading.value = false
  }, 800)
}

const showError = (message: string) => {
  errorMessage.value = message
  hasError.value = true
  setTimeout(() => {
    hasError.value = false
    errorMessage.value = ''
  }, 3000)
}
</script>

<style scoped>
.password-auth {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.auth-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 16px;
  padding: 40px 32px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  text-align: center;
  backdrop-filter: blur(10px);
}

.auth-header {
  margin-bottom: 32px;
}

.lock-icon {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 16px;
}

.auth-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.auth-header p {
  color: #666;
  font-size: 14px;
}

.auth-form {
  margin-bottom: 20px;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

.error-input {
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #f56565;
  font-size: 14px;
  background: #fed7d7;
  padding: 12px;
  border-radius: 8px;
  margin-top: 16px;
}

.error-message .el-icon {
  font-size: 16px;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .auth-container {
    padding: 16px;
  }
  
  .auth-card {
    padding: 32px 24px;
  }
  
  .lock-icon {
    font-size: 40px;
  }
  
  .auth-header h2 {
    font-size: 20px;
  }
}
</style>