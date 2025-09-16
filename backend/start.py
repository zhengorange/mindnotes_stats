#!/usr/bin/env python3
"""
启动脚本
运行此脚本来启动API服务器
"""

import os
import sys

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import fastapi
        import uvicorn
        import psycopg2
        import dotenv
        print("✓ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def check_env_file():
    """检查环境变量文件"""
    if not os.path.exists('.env'):
        print("✗ 未找到 .env 文件")
        print("请复制 .env.example 为 .env 并配置数据库连接信息")
        return False
    print("✓ 环境变量文件存在")
    return True

def main():
    print("=== MindNotes Stats API 启动检查 ===")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 检查环境变量
    if not check_env_file():
        sys.exit(1)
    
    print("\n=== 启动API服务器 ===")
    print("服务器将在 http://localhost:8000 启动")
    print("API文档: http://localhost:8000/docs")
    print("按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    # 启动服务器
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()