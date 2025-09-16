import axios from 'axios'


// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.MODE == "development" ? 'http://localhost:23789/' : "//",
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log('发送请求:', config.url)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API请求失败:', error)
    return Promise.reject(error)
  }
)

// 用户统计相关接口
export const userStatsApi = {
  // 获取每日新增用户数据（兼容接口）
  getDailyNewUsers: (days: number = 120) => {
    return api.get(`/api/stats/daily-new-users?days=${days}`)
  },
  
  // 获取每日用户统计数据（新增用户+活跃用户）
  getDailyUsers: (days: number = 120) => {
    return api.get(`/api/stats/daily-users?days=${days}`)
  },
  
  // 获取统计摘要
  getStatsSummary: () => {
    return api.get('/api/stats/summary')
  }
}

export default api