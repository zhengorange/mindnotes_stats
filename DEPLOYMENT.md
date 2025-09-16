# MindNotes 统计系统部署指南

## 概述
本系统已经配置为单一部署模式，前端已打包为静态文件并由后端代理。你只需要部署后端即可。

## 项目结构
```
├── backend/           # 后端API服务
│   ├── main.py       # FastAPI应用
│   ├── database.py   # 数据库连接
│   └── ...
├── dist/             # 前端构建产物（静态文件）
│   ├── index.html
│   ├── assets/
│   └── ...
├── start_server.py   # 统一启动脚本
└── ...
```

## 本地开发/测试

### 1. 构建前端（如需更新前端）
```bash
npm run build
```

### 2. 启动统一服务
```bash
python start_server.py
```

服务启动后：
- 前端访问地址: http://localhost:8000
- API文档地址: http://localhost:8000/docs

## 生产部署

### 方式一：直接运行Python（推荐用于测试）
```bash
# 安装依赖
cd backend
pip install -r requirements.txt

# 启动服务
python ../start_server.py
```

### 方式二：使用Gunicorn（推荐用于生产）
```bash
# 安装Gunicorn
pip install gunicorn

# 启动服务
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 方式三：使用Docker
```bash
# 创建Dockerfile（如需要）
# 构建镜像
docker build -t mindnotes-stats .

# 运行容器
docker run -p 8000:8000 mindnotes-stats
```

## 环境配置

### 数据库配置
确保 `backend/database.py` 中的数据库连接配置正确：
- 数据库主机地址
- 用户名和密码
- 数据库名称

### 端口配置
默认端口为8000，如需修改：
1. 编辑 `start_server.py` 中的 `port` 参数
2. 或在生产环境中通过环境变量 `PORT` 设置

## 注意事项

1. **静态文件**: 前端已打包到 `dist/` 目录，后端会自动代理这些文件
2. **API路径**: 所有API请求以 `/api/` 开头
3. **路由处理**: 非API路径会返回前端应用，支持前端路由
4. **CORS**: 已配置允许所有源访问，适合同端口部署

## 文件说明

- `dist/`: 前端构建产物，包含所有静态资源
- `backend/main.py`: 集成了静态文件服务和API的FastAPI应用
- `start_server.py`: 统一启动脚本，方便本地开发和测试

## 部署检查清单

- [ ] 数据库连接配置正确
- [ ] 前端已构建（存在dist目录）
- [ ] 后端依赖已安装
- [ ] 端口8000可用（或配置其他端口）
- [ ] 数据库表结构已创建