<template>
  <div class="user-stats-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>用户统计数据</h1>
      <p class="page-description">查看新增用户和活跃用户趋势及统计数据</p>
    </div>

    <!-- 统计卡片 -->
    <!-- 第一行：基础统计数据 -->
    <div class="stats-grid-container">
      <div class="stats-row">
        <el-card class="stats-card primary-card">
          <div class="card-content">
            <div class="card-icon">
              <el-icon>
                <User />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">总用户数</div>
              <div class="card-value">{{ summary.total_users }}</div>
            </div>
          </div>
        </el-card>
        <el-card class="stats-card today-card">
          <div class="card-content">
            <div class="card-icon">
              <el-icon>
                <UserFilled />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">今日新增</div>
              <div class="card-value">{{ summary.today_new_users }}</div>
            </div>
          </div>
        </el-card>
        <el-card class="stats-card yesterday-card">
          <div class="card-content">
            <div class="card-icon">
              <el-icon>
                <Avatar />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">昨日新增</div>
              <div class="card-value">{{ summary.yesterday_new_users }}</div>
            </div>
          </div>
        </el-card>
        <el-card class="stats-card week-card">
          <div class="card-content">
            <div class="card-icon">
              <el-icon>
                <Histogram />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">周新增</div>
              <div class="card-value">{{ summary.week_new_users }}</div>
            </div>
          </div>
        </el-card>
        <el-card class="stats-card month-card">
          <div class="card-content">
            <div class="card-icon">
              <el-icon>
                <Calendar />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">月新增</div>
              <div class="card-value">{{ summary.month_new_users }}</div>
            </div>
          </div>
        </el-card>
        <el-card class="stats-card today-active-card">
          <div class="card-content">
            <div class="card-icon">
              <el-icon>
                <CircleCheck />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">今日活跃</div>
              <div class="card-value">{{ summary.today_active_users }}</div>
            </div>
          </div>
        </el-card>
        <el-card class="stats-card yesterday-active-card">
          <div class="card-content">
            <div class="card-icon">
              <el-icon>
                <CircleCheckFilled />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">昨日活跃</div>
              <div class="card-value">{{ summary.yesterday_active_users }}</div>
            </div>
          </div>
        </el-card>
        <el-card class="stats-card week-active-card">
          <div class="card-content">
            <div class="card-icon">
              <el-icon>
                <Odometer />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">周活跃用户</div>
              <div class="card-value">{{ summary.week_active_users }}</div>
            </div>
          </div>
        </el-card>
        <el-card class="stats-card month-active-card">
          <div class="card-content">
            <div class="card-icon">
              <el-icon>
                <DataBoard />
              </el-icon>
            </div>
            <div class="card-info">
              <div class="card-title">月活跃用户</div>
              <div class="card-value">{{ summary.month_active_users }}</div>
            </div>
          </div>
        </el-card>
      </div>
    </div>

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
            <el-icon>
              <Refresh />
            </el-icon>
            刷新
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- 图表区域 -->
    <el-card class="chart-container">
      <div class="chart-header">
        <h3>每日用户趋势图</h3>
        <span class="chart-info">{{ chartData.total_days }}天数据，累计新增{{ chartData.total_new_users }}人，活跃用户{{
          chartData.total_active_users }}人次</span>
      </div>

      <div v-if="loading" class="loading-container">
        <el-icon class="is-loading" size="50">
          <Loading />
        </el-icon>
        <p>数据加载中...</p>
      </div>

      <div v-else-if="error" class="error-container">
        <el-alert :title="error" type="error" show-icon :closable="false" />
      </div>

      <div v-else class="chart-wrapper">
        <Line :data="chartDataConfig" :options="chartOptions" :key="chartKey" />
      </div>
    </el-card>

    <!-- 数据表格 -->
    <el-card class="table-container">
      <div class="table-header">
        <h3>详细数据</h3>
        <el-input v-model="searchDate" placeholder="搜索日期 (YYYY-MM-DD)" style="width: 220px" clearable>
          <template #prefix>
            <el-icon>
              <Search />
            </el-icon>
          </template>
        </el-input>
      </div>

      <el-table :data="filteredTableData" style="width: 100%" height="400" stripe>
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
                <el-icon class="growth-icon">
                  <ArrowUp />
                </el-icon>
                <span class="growth-value">+{{ scope.row.new_growth }}</span>
              </span>
            </el-tag>
            <el-tag v-else-if="scope.row.new_growth < 0" type="danger" class="growth-tag">
              <span class="growth-content">
                <el-icon class="growth-icon">
                  <ArrowDown />
                </el-icon>
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
                <el-icon class="growth-icon">
                  <ArrowUp />
                </el-icon>
                <span class="growth-value">+{{ scope.row.active_growth }}</span>
              </span>
            </el-tag>
            <el-tag v-else-if="scope.row.active_growth < 0" type="danger" class="growth-tag">
              <span class="growth-content">
                <el-icon class="growth-icon">
                  <ArrowDown />
                </el-icon>
                <span class="growth-value">{{ scope.row.active_growth }}</span>
              </span>
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="备注" min-width="200">
          <template #default="scope">
            <span v-if="scope.row.new_users === 0 && scope.row.active_users === 0" class="text-gray">无新增和活跃用户</span>
            <span v-else-if="scope.row.new_users >= 50 || scope.row.active_users >= 100"
              class="text-success">用户活跃度高</span>
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
  week_new_users: number
  month_new_users: number
  today_active_users: number
  yesterday_active_users: number
  week_active_users: number
  month_active_users: number
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
  week_new_users: 0,
  month_new_users: 0,
  today_active_users: 0,
  yesterday_active_users: 0,
  week_active_users: 0,
  month_active_users: 0
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

.stats-grid-container {
  margin-bottom: 30px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 16px;
}

.stats-row:first-child {
  grid-template-columns: repeat(5, 1fr);
}

.stats-row:last-child {
  grid-template-columns: repeat(4, 1fr);
  margin-bottom: 0;
}

/* 优化后的统计卡片样式 */
.stats-card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  height: 140px;
  background: #fff;
}

.stats-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 特殊卡片样式 */
.primary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.today-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.yesterday-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.week-card {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  color: white;
}

.month-card {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  color: white;
}

.today-active-card {
  background: linear-gradient(135deg, #96fbc4 0%, #67d07a 100%);
  color: white;
}

.yesterday-active-card {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: white;
}

.week-active-card {
  background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%);
  color: white;
}

.month-active-card {
  background: linear-gradient(135deg, #fad0c4 0%, #ffd1ff 100%);
  color: white;
}

.card-content {
  display: flex;
  align-items: center;
  padding: 24px;
  height: 100%;
  position: relative;
}

.card-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  font-size: 32px;
  color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  flex-shrink: 0;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.card-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card-title {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: rgba(255, 255, 255, 0.9);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-value {
  font-size: 28px;
  font-weight: 700;
  color: white;
  line-height: 1.2;
  margin-bottom: 4px;
}

.card-desc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 400;
  line-height: 1.4;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .stats-row {
    margin-bottom: 16px;
  }

  .stats-card {
    margin-bottom: 16px;
    height: 120px;
  }

  .card-content {
    padding: 16px;
  }

  .card-icon {
    width: 48px;
    height: 48px;
    font-size: 24px;
    margin-right: 16px;
  }

  .card-value {
    font-size: 24px;
  }

  .card-title {
    font-size: 13px;
  }

  .card-desc {
    font-size: 11px;
  }
}

@media (max-width: 480px) {
  .stats-card {
    height: 100px;
  }

  .card-content {
    padding: 12px;
  }

  .card-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
    margin-right: 12px;
  }

  .card-value {
    font-size: 20px;
  }

  .card-title {
    font-size: 12px;
  }

  .card-desc {
    font-size: 10px;
  }
}

/* 移除旧样式 */

/* 移除增长率卡片样式 */

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