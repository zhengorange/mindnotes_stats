#!/usr/bin/env python3
"""
启动MindNotes统计服务器
集成了前端静态文件和后端API
"""

import os
import sys
import uvicorn

def main():
    # 确保当前目录在Python路径中
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    sys.path.insert(0, backend_dir)
    
    # 检查静态文件是否存在
    dist_dir = os.path.join(os.path.dirname(__file__), 'dist')
    if not os.path.exists(dist_dir):
        print("警告: 没有找到前端构建文件 (dist 目录)")
        print("请先运行: npm run build")
        print("继续启动后端服务...")
    
    # 启动服务器
    print("启动MindNotes统计服务器...")
    print("前端访问地址: http://localhost:8000")
    print("API文档地址: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        app_dir=backend_dir
    )

if __name__ == "__main__":
    main()