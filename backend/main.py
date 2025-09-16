from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from database import execute_query
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MindNotes Stats API", 
    version="1.0.0",
    docs_url=None,  # 禁用API文档
    redoc_url=None  # 禁用ReDoc文档
)

# 获取静态文件目录路径
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dist")

# 挂载静态文件
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")
    logger.info(f"Static files mounted from: {static_dir}")
else:
    logger.warning(f"Static directory not found: {static_dir}")

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，因为现在前后端在同一端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserStatsItem(BaseModel):
    date: str
    new_users: int
    active_users: int

class UserStatsResponse(BaseModel):
    data: List[UserStatsItem]
    total_days: int
    total_new_users: int
    total_active_users: int

@app.get("/")
async def root():
    """
    服务前端应用
    """
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dist")
    index_file = os.path.join(static_dir, "index.html")
    
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        return {"message": "MindNotes Stats API - Frontend not built"}

@app.get("/api/stats/daily-new-users", response_model=UserStatsResponse)
async def get_daily_new_users_legacy(days: Optional[int] = 120):
    """
    获取每日新增用户统计数据（兼容接口）
    
    参数:
    - days: 统计天数，默认120天
    """
    # 调用新的统一接口
    return await get_daily_users(days)

@app.get("/api/stats/daily-users", response_model=UserStatsResponse)
async def get_daily_users(days: Optional[int] = 120):
    """
    获取每日新增用户和活跃用户统计数据
    
    参数:
    - days: 统计天数，默认120天
    """
    try:
        # 验证参数
        if days <= 0 or days > 365:
            raise HTTPException(status_code=400, detail="days参数必须在1-365之间")
        
        # 构建SQL查询，同时获取新增用户和活跃用户数据
        query = """
        WITH date_series AS (
            SELECT generate_series(
                CURRENT_DATE - INTERVAL %s,  -- 开始日期
                CURRENT_DATE - INTERVAL '1 day',   -- 结束日期
                INTERVAL '1 day'
            )::date AS date
        )
        SELECT
            ds.date,
            COALESCE(nu.new_users, 0) AS new_users,
            COALESCE(au.active_users, 0) AS active_users
        FROM
            date_series ds
        LEFT JOIN (
            SELECT
                DATE(create_time) AS date,
                COUNT(*) AS new_users
            FROM users
            WHERE create_time < CURRENT_DATE
            GROUP BY DATE(create_time)
        ) nu ON ds.date = nu.date
        LEFT JOIN (
            SELECT
                DATE(created_at) AS date,
                COUNT(DISTINCT user_id) AS active_users
            FROM user_logs
            WHERE created_at < CURRENT_DATE
            GROUP BY DATE(created_at)
        ) au ON ds.date = au.date
        ORDER BY ds.date;
        """
        
        logger.info(f"执行每日新增用户和活跃用户查询，天数: {days}")
        
        # 执行查询，使用参数化查询
        results = execute_query(query, (f'{days} days',))
        
        # 调试：检查返回结果类型
        logger.info(f"查询结果类型: {type(results)}, 内容: {results}")
        
        # 确保返回的是列表
        if not isinstance(results, list):
            logger.error(f"查询返回类型错误: {type(results)}, 期望 list")
            raise HTTPException(status_code=500, detail="查询返回数据格式错误")
        
        # 处理结果
        data = []
        total_new_users = 0
        total_active_users = 0
        
        for row in results:
            item = UserStatsItem(
                date=row['date'].strftime('%Y-%m-%d'),
                new_users=row['new_users'],
                active_users=row['active_users']
            )
            data.append(item)
            total_new_users += row['new_users']
            total_active_users += row['active_users']
        
        response = UserStatsResponse(
            data=data,
            total_days=len(data),
            total_new_users=total_new_users,
            total_active_users=total_active_users
        )
        
        logger.info(f"返回数据: {len(data)}条记录，总新增用户: {total_new_users}，总活跃用户: {total_active_users}")
        return response
        
    except Exception as e:
        logger.error(f"获取每日用户统计数据时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@app.get("/api/stats/daily-new-users", response_model=UserStatsResponse)
async def get_daily_new_users_legacy(days: Optional[int] = 120):
    """
    获取每日新增用户统计数据（兼容接口）
    
    参数:
    - days: 统计天数，默认120天
    """
    # 调用新的统一接口
    return await get_daily_users(days)

@app.get("/api/stats/summary")
async def get_stats_summary():
    """
    获取统计数据摘要
    """
    try:
        # 总用户数
        total_users_query = "SELECT COUNT(*) as total FROM users"
        total_users_result = execute_query(total_users_query)
        total_users = total_users_result[0]['total'] if total_users_result else 0
        
        # 今日新增用户
        today_users_query = """
        SELECT COUNT(*) as today_new 
        FROM users 
        WHERE DATE(create_time) = CURRENT_DATE
        """
        today_users_result = execute_query(today_users_query)
        today_new_users = today_users_result[0]['today_new'] if today_users_result else 0
        
        # 昨日新增用户
        yesterday_users_query = """
        SELECT COUNT(*) as yesterday_new 
        FROM users 
        WHERE DATE(create_time) = CURRENT_DATE - INTERVAL '1 day'
        """
        yesterday_users_result = execute_query(yesterday_users_query)
        yesterday_new_users = yesterday_users_result[0]['yesterday_new'] if yesterday_users_result else 0
        
        # 周新增用户 (最近7天)
        week_new_users_query = """
        SELECT COUNT(*) as week_new 
        FROM users 
        WHERE DATE(create_time) >= CURRENT_DATE - INTERVAL '7 days'
        """
        week_new_users_result = execute_query(week_new_users_query)
        week_new_users = week_new_users_result[0]['week_new'] if week_new_users_result else 0
        
        # 月新增用户 (最近30天)
        month_new_users_query = """
        SELECT COUNT(*) as month_new 
        FROM users 
        WHERE DATE(create_time) >= CURRENT_DATE - INTERVAL '30 days'
        """
        month_new_users_result = execute_query(month_new_users_query)
        month_new_users = month_new_users_result[0]['month_new'] if month_new_users_result else 0
        
        # 今日活跃用户
        today_active_query = """
        SELECT COUNT(DISTINCT user_id) as today_active 
        FROM user_logs 
        WHERE DATE(created_at) = CURRENT_DATE
        """
        today_active_result = execute_query(today_active_query)
        today_active_users = today_active_result[0]['today_active'] if today_active_result else 0
        
        # 昨日活跃用户
        yesterday_active_query = """
        SELECT COUNT(DISTINCT user_id) as yesterday_active 
        FROM user_logs 
        WHERE DATE(created_at) = CURRENT_DATE - INTERVAL '1 day'
        """
        yesterday_active_result = execute_query(yesterday_active_query)
        yesterday_active_users = yesterday_active_result[0]['yesterday_active'] if yesterday_active_result else 0
        
        # 周活跃用户 (最近7天)
        week_active_query = """
        SELECT COUNT(DISTINCT user_id) as week_active 
        FROM user_logs 
        WHERE DATE(created_at) >= CURRENT_DATE - INTERVAL '7 days'
        """
        week_active_result = execute_query(week_active_query)
        week_active_users = week_active_result[0]['week_active'] if week_active_result else 0
        
        # 月活跃用户 (最近30天)
        month_active_query = """
        SELECT COUNT(DISTINCT user_id) as month_active 
        FROM user_logs 
        WHERE DATE(created_at) >= CURRENT_DATE - INTERVAL '30 days'
        """
        month_active_result = execute_query(month_active_query)
        month_active_users = month_active_result[0]['month_active'] if month_active_result else 0
        
        return {
            "total_users": total_users,
            "today_new_users": today_new_users,
            "yesterday_new_users": yesterday_new_users,
            "week_new_users": week_new_users,
            "month_new_users": month_new_users,
            "today_active_users": today_active_users,
            "yesterday_active_users": yesterday_active_users,
            "week_active_users": week_active_users,
            "month_active_users": month_active_users
        }
        
    except Exception as e:
        logger.error(f"获取统计摘要时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

# Catch-all 路由，用于处理前端路由
@app.get("/{path:path}")
async def catch_all(path: str):
    """
    捕获所有未匹配的路由，返回前端应用
    """
    # 如果请求的是API路径，返回404
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # 否则返回前端应用
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dist")
    index_file = os.path.join(static_dir, "index.html")
    
    if os.path.exists(index_file):
        return FileResponse(index_file)
    else:
        raise HTTPException(status_code=404, detail="Page not found")
