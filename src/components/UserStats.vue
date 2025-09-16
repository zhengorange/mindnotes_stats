<template>
  <div class="user-stats-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>用户统计数据</h1>
      <p class="page-description">查看新增用户和活跃用户趋势及统计数据</p>
    </div>

    <!-- 统计卡片 -->
    <!-- 第一行：基础统计数据（5个等宽卡片） -->
    <el-row :gutter="20" class="stats-cards">
      <el-col :span="24/5" class="equal-width-col">
        <el-card class="stats-card">
          <div class="card-content">
            <div class="card-icon total-users">
              <el-icon><User /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">总用户数</div>
              <div class="card-value">{{ summary.total_users }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="24/5" class="equal-width-col">
        <el-card class="stats-card">
          <div class="card-content">
            <div class="card-icon today-users">
              <el-icon><UserFilled /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">今日新增</div>
              <div class="card-value">{{ summary.today_new_users }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="24/5" class="equal-width-col">
        <el-card class="stats-card">
          <div class="card-content">
            <div class="card-icon yesterday-users">
              <el-icon><Avatar /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">昨日新增</div>
              <div class="card-value">{{ summary.yesterday_new_users }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="24/5" class="equal-width-col">
        <el-card class="stats-card">
          <div class="card-content">
            <div class="card-icon today-active">
              <el-icon><CircleCheck /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">今日活跃</div>
              <div class="card-value">{{ summary.today_active_users }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="24/5" class="equal-width-col">
        <el-card class="stats-card">
          <div class="card-content">
            <div class="card-icon yesterday-active">
              <el-icon><CircleCheckFilled /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">昨日活跃</div>
              <div class="card-value">{{ summary.yesterday_active_users }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 第二行：增长率数据（自适应宽度） -->
    <el-row :gutter="20" class="stats-cards growth-cards">
      <el-col>
        <el-card class="stats-card growth-card">
          <div class="card-content">
            <div class="card-icon growth-rate">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">昨日新增增长率</div>
              <div class="card-value" :class="{ 'positive': summary.new_user_growth_rate > 0, 'negative': summary.new_user_growth_rate < 0 }">
                {{ summary.new_user_growth_rate > 0 ? '+' : '' }}{{ summary.new_user_growth_rate }}%
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col>
        <el-card class="stats-card growth-card">
          <div class="card-content">
            <div class="card-icon active-growth-rate">
              <el-icon><DataAnalysis /></el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">昨日活跃增长率</div>
              <div class="card-value" :class="{ 'positive': summary.active_user_growth_rate > 0, 'negative': summary.active_user_growth_rate < 0 }">
                {{ summary.active_user_growth_rate > 0 ? '+' : '' }}{{ summary.active_user_growth_rate }}%
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 控制面板 -->
    <el-card class="control-panel">
      <div class="control-header">
        <h3>图表设置</h3>
        <div class="controls">
          <el-select v-model="selectedDays" @change="fetchData" style="width: 120px">
            <el-option label="7天" :value="7" />
            <el-option label="30天" :value="30" />
            <el-option label="60天" :value="60" />
            <el-option label="90天" :value="90" />
            <el-option label="120天" :value="120" />
          </el-select>
          <el-button @click="fetchData" :loading="loading" type="primary">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 图表区域 -->
    <el-card class="chart-container">
      <div class="chart-header">
        <h3>每日用户趋势图</h3>
        <span class="chart-info">{{ chartData.total_days }}天数据，累计新增{{ chartData.total_new_users }}人，活跃用户{{ chartData.total_active_users }}人次</span>
      </div>
      
      <div v-if="loading" class="loading-container">
        <el-icon class="is-loading" size="50"><Loading /></el-icon>
        <p>数据加载中...</p>
      </div>
      
      <div v-else-if="error" class="error-container">
        <el-alert
          :title="error"
          type="error"
          show-icon
          :closable="false"
        />
      </div>
      
      <div v-else class="chart-wrapper">
        <Line
          :data="chartDataConfig"
          :options="chartOptions"
          :key="chartKey"
        />
      </div>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-container">
      <div class="table-header">
        <h3>详细数据</h3>
        <el-input
          v-model="searchDate"
          placeholder="搜索日期 (YYYY-MM-DD)"
          style="width: 220px"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      
      <el-table
        :data="filteredTableData"
        style="width: 100%"
        height="400"
        stripe
      >
        <el-table-column prop="date" label="日期" width="120" sortable />
        <el-table-column prop="new_users" label="新增用户数" width="120" sortable>
          <template #default="scope">
            <el-tag v-if="scope.row.new_users > 0" type="success">{{ scope.row.new_users }}</el-tag>
            <span v-else>0</span>
          </template>
        </el-table-column>
        <el-table-column prop="active_users" label="活跃用户数" width="120" sortable>
          <template #default="scope">
            <el-tag v-if="scope.row.active_users > 0" type="primary">{{ scope.row.active_users }}</el-tag>
            <span v-else>0</span>
          </template>
        </el-table-column>
        <el-table-column label="新增增长" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.new_growth > 0" type="success" class="growth-tag">
              <span class="growth-content">
                <el-icon class="growth-icon"><ArrowUp /></el-icon>
                <span class="growth-value">+{{ scope.row.new_growth }}</span>
              </span>
            </el-tag>
            <el-tag v-else-if="scope.row.new_growth < 0" type="danger" class="growth-tag">
              <span class="growth-content">
                <el-icon class="growth-icon"><ArrowDown /></el-icon>
                <span class="growth-value">{{ scope.row.new_growth }}</span>
              </span>
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="活跃增长" width="120">
          <template #default="scope">
            <el-tag v-if="scope.row.active_growth > 0" type="success" class="growth-tag">
              <span class="growth-content">
                <el-icon class="growth-icon"><ArrowUp /></el-icon>
                <span class="growth-value">+{{ scope.row.active_growth }}</span>
              </span>
            </el-tag>
            <el-tag v-else-if="scope.row.active_growth < 0" type="danger" class="growth-tag">
              <span class="growth-content">
                <el-icon class="growth-icon"><ArrowDown /></el-icon>
                <span class="growth-value">{{ scope.row.active_growth }}</span>
              </span>
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="备注" min-width="200">
          <template #default="scope">
            <span v-if="scope.row.new_users === 0 && scope.row.active_users === 0" class="text-gray">无新增和活跃用户</span>
            <span v-else-if="scope.row.new_users >= 50 || scope.row.active_users >= 100" class="text-success">用户活跃度高</span>
            <span v-else-if="scope.row.new_users >= 20 || scope.row.active_users >= 50" class="text-warning">正常水平</span>
            <span v-else class="text-info">活跃度低</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { userStatsApi } from '../api'
import { ElMessage } from 'element-plus'

// 注册Chart.js组件
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

// 定义类型接口
interface UserStatsItem {
  date: string
  new_users: number
  active_users: number
}

interface SummaryData {
  total_users: number
  today_new_users: number
  yesterday_new_users: number
  today_active_users: number
  yesterday_active_users: number
  new_user_growth_rate: number
  active_user_growth_rate: number
}

interface ChartDataResponse {
  data: UserStatsItem[]
  total_days: number
  total_new_users: number
  total_active_users: number
}

// 响应式数据
const loading = ref(false)
const error = ref('')
const selectedDays = ref(30)
const searchDate = ref('')
const chartKey = ref(0)

// 统计数据
const summary = ref<any>({
  total_users: 0,
  today_new_users: 0,
  yesterday_new_users: 0,
  today_active_users: 0,
  yesterday_active_users: 0,
  new_user_growth_rate: 0,
  active_user_growth_rate: 0
})

// 图表数据
const chartData = ref<any>({
  data: [],
  total_days: 0,
  total_new_users: 0,
  total_active_users: 0
})

// 图表配置
const chartDataConfig = computed(() => {
  const data = Array.isArray(chartData.value.data) ? chartData.value.data : []
  return {
    labels: data.map(item => item.date),
    datasets: [
      {
        label: '每日新增用户',
        data: data.map(item => item.new_users),
        borderColor: '#409EFF',
        backgroundColor: 'rgba(64, 158, 255, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#409EFF',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6
      },
      {
        label: '每日活跃用户',
        data: data.map(item => item.active_users),
        borderColor: '#67C23A',
        backgroundColor: 'rgba(103, 194, 58, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#67C23A',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: false
    },
    legend: {
      display: true,
      position: 'top' as const
    },
    tooltip: {
      mode: 'index' as const,
      intersect: false,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: '#409EFF',
      borderWidth: 1
    }
  },
  scales: {
    x: {
      display: true,
      title: {
        display: true,
        text: '日期'
      }
    },
    y: {
      display: true,
      title: {
        display: true,
        text: '用户数'
      },
      beginAtZero: true
    }
  },
  interaction: {
    mode: 'nearest' as const,
    axis: 'x' as const,
    intersect: false
  }
}

// 表格数据（带增长计算）
const tableData = computed(() => {
  const data = Array.isArray(chartData.value.data) ? [...chartData.value.data] : []
  return data.map((item, index) => {
    const newGrowth = index > 0 ? item.new_users - data[index - 1].new_users : 0
    const activeGrowth = index > 0 ? item.active_users - data[index - 1].active_users : 0
    return {
      ...item,
      new_growth: newGrowth,
      active_growth: activeGrowth
    }
  })
})

// 过滤后的表格数据
const filteredTableData = computed(() => {
  if (!searchDate.value) {
    return tableData.value
  }
  return tableData.value.filter(item => 
    item.date.includes(searchDate.value)
  )
})

// 获取统计摘要
const fetchSummary = async () => {
  try {
    const data = await userStatsApi.getStatsSummary()
    summary.value = data
  } catch (err) {
    console.error('获取统计摘要失败:', err)
    ElMessage.error('获取统计摘要失败')
  }
}

// 获取图表数据
const fetchData = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const data = await userStatsApi.getDailyUsers(selectedDays.value)
    
    // 确保数据格式正确
    if (data && Array.isArray(data.data)) {
      chartData.value = data
    } else {
      console.error('API返回数据格式:', data)
      throw new Error('返回的数据格式不正确')
    }
    
    // 强制重新渲染图表
    await nextTick()
    chartKey.value++
    
    ElMessage.success('数据更新成功')
  } catch (err) {
    console.error('获取数据失败:', err)
    error.value = '获取数据失败，请检查网络连接或后端服务'
    ElMessage.error('获取数据失败')
    
    // 设置默认值以防止错误
    chartData.value = {
      data: [],
      total_days: 0,
      total_new_users: 0,
      total_active_users: 0
    }
  } finally {
    loading.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchSummary()
  fetchData()
})
</script>

<style scoped>
.user-stats-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.page-description {
  margin: 8px 0 0 0;
  color: #909399;
  font-size: 14px;
}

.stats-cards {
  margin-bottom: 20px;
}

/* 等宽卡片列 */
.equal-width-col {
  width: 20%; /* 5个卡片，每个占20% */
  flex: 0 0 20%;
}

/* 增长率卡片行 */
.growth-cards {
  display: flex;
  justify-content: flex-start;
  gap: 20px;
}

.growth-cards .el-col {
  flex: 0 0 auto;
  width: auto;
}

.growth-card {
  min-width: 200px;
}

.stats-card {
  transition: transform 0.2s;
}

.stats-card:hover {
  transform: translateY(-2px);
}

.card-content {
  display: flex;
  align-items: center;
  padding: 16px;
  min-height: 80px;
}

.card-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  font-size: 28px;
  color: white;
  flex-shrink: 0;
}

.card-icon.total-users {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon.today-users {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.card-icon.yesterday-users {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.card-icon.today-active {
  background: linear-gradient(135deg, #96fbc4 0%, #67d07a 100%);
}

.card-icon.yesterday-active {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

.card-icon.growth-rate {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.card-icon.active-growth-rate {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.card-info {
  flex: 1;
  min-width: 0;
}

.card-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  line-height: 1.2;
}

.card-value.positive {
  color: #67c23a;
}

.card-value.negative {
  color: #f56c6c;
}

.control-panel {
  margin-bottom: 20px;
}

.control-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.control-header h3 {
  margin: 0;
  color: #303133;
}

.controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.chart-container {
  margin-bottom: 20px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
  color: #303133;
}

.chart-info {
  color: #909399;
  font-size: 14px;
}

.chart-wrapper {
  height: 400px;
  position: relative;
}

.loading-container,
.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #909399;
}

.loading-container p {
  margin-top: 16px;
}

.table-container {
  margin-bottom: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-header h3 {
  margin: 0;
  color: #303133;
}

.text-gray {
  color: #909399;
}

.text-success {
  color: #67c23a;
}

.text-warning {
  color: #e6a23c;
}

.text-info {
  color: #909399;
}

/* 增长标签样式 */
.growth-tag {
  padding: 4px 8px;
}

.growth-content {
  display: flex;
  align-items: center;
  gap: 4px;
}

.growth-icon {
  font-size: 12px;
  flex-shrink: 0;
}

.growth-value {
  font-size: 12px;
  font-weight: 500;
}
</style>