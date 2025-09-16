# MindNotes Stats - 用户统计系统

一个用于统计PostgreSQL数据库中用户增长数据的全栈应用，包含Python后端API和Vue.js前端界面。

## 功能特性

- 📊 **每日新增用户统计** - 可视化展示用户增长趋势
- 📈 **交互式图表** - 基于Chart.js的响应式图表
- 📋 **详细数据表格** - 支持搜索和排序的数据表格
- 🎯 **统计摘要** - 总用户数、今日新增、昨日新增、增长率
- 🎨 **现代化UI** - 基于Element Plus的美观界面
- ⚡ **实时数据** - 支持数据刷新和时间范围选择

## 技术栈

### 后端
- **FastAPI** - 现代Python Web框架
- **PostgreSQL** - 数据库
- **psycopg2** - PostgreSQL适配器
- **Uvicorn** - ASGI服务器

### 前端
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全
- **Element Plus** - Vue 3组件库
- **Chart.js** - 图表库
- **Axios** - HTTP客户端

## 快速开始

### 1. 数据库准备

确保你的PostgreSQL数据库中有`users`表，包含`create_time`字段：

```sql
-- 示例表结构
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 安装Python依赖
pip install -r requirements.txt

# 复制环境变量文件
cp .env.example .env

# 编辑环境变量文件，配置你的数据库连接
vim .env
```

配置`.env`文件：
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_database_name
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password
```

### 3. 启动后端服务

```bash
# 使用启动脚本（推荐）
python start.py

# 或者直接运行
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将在 http://localhost:8000 启动

### 4. 前端设置

```bash
# 在项目根目录安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将在 http://localhost:5173 启动

## API接口

### 获取每日新增用户统计
```
GET /api/stats/daily-new-users?days=120
```

### 获取统计摘要
```
GET /api/stats/summary
```

## SQL查询说明

核心SQL查询使用了PostgreSQL的`generate_series`函数生成日期序列，然后左连接用户数据：

```sql
WITH date_series AS (
    SELECT generate_series(
        CURRENT_DATE - INTERVAL '120 days',  -- 开始日期
        CURRENT_DATE - INTERVAL '1 day',   -- 结束日期
        INTERVAL '1 day'
    )::date AS date
)
SELECT
    ds.date,
    COALESCE(u.new_users, 0) AS new_users
FROM
    date_series ds
LEFT JOIN (
    SELECT
        DATE(create_time) AS date,
        COUNT(*) AS new_users
    FROM users
    WHERE create_time < CURRENT_DATE
    GROUP BY DATE(create_time)
) u ON ds.date = u.date
ORDER BY ds.date;
```

## 项目结构

```
mindnotes_stats/
├── backend/                 # Python后端
│   ├── main.py             # FastAPI应用主文件
│   ├── database.py         # 数据库连接配置
│   ├── start.py           # 启动脚本
│   ├── requirements.txt    # Python依赖
│   ├── .env.example       # 环境变量示例
│   └── .env               # 环境变量配置（需要创建）
├── src/                    # Vue前端
│   ├── components/
│   │   └── UserStats.vue  # 用户统计页面组件
│   ├── api/
│   │   └── index.ts       # API客户端
│   ├── App.vue            # 根组件
│   └── main.ts            # 入口文件
├── package.json           # 前端依赖配置
└── README.md              # 项目文档
```

## 开发说明

### 添加新的统计功能

1. 在`backend/main.py`中添加新的API端点
2. 在`src/api/index.ts`中添加对应的API调用方法
3. 创建新的Vue组件或扩展现有组件

### 自定义样式

项目使用Element Plus作为UI组件库，你可以通过修改CSS变量来自定义主题。

### 数据库优化

对于大量数据，建议在`users.create_time`字段上创建索引：

```sql
CREATE INDEX idx_users_create_time ON users(create_time);
```

## 故障排除

### 1. 数据库连接失败
- 检查`.env`文件中的数据库配置
- 确保PostgreSQL服务正在运行
- 验证数据库用户权限

### 2. 前端无法获取数据
- 确保后端服务已启动
- 检查浏览器控制台的CORS错误
- 验证API端点URL

### 3. 图表不显示
- 检查数据是否正确返回
- 确保Chart.js依赖已正确安装
- 查看浏览器控制台的JavaScript错误

## 许可证

MIT License