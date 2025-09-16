import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Generator

# 加载环境变量
load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv("DATABASE_HOST", "localhost")
        self.port = os.getenv("DATABASE_PORT", "5432")
        self.database = os.getenv("DATABASE_NAME")
        self.user = os.getenv("DATABASE_USER")
        self.password = os.getenv("DATABASE_PASSWORD")
        
        # 如果提供了完整的DATABASE_URL，优先使用
        self.database_url = os.getenv("DATABASE_URL")
    
    def get_connection_params(self):
        if self.database_url:
            return {"dsn": self.database_url}
        else:
            return {
                "host": self.host,
                "port": self.port,
                "database": self.database,
                "user": self.user,
                "password": self.password
            }

db_config = DatabaseConfig()

@contextmanager
def get_db_connection() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    数据库连接上下文管理器（只读模式）
    """
    conn = None
    try:
        conn = psycopg2.connect(
            **db_config.get_connection_params(),
            cursor_factory=RealDictCursor
        )
        # 设置连接为只读模式
        conn.set_session(readonly=True)
        # 设置时区为Asia/Shanghai (UTC+8)
        with conn.cursor() as cursor:
            cursor.execute("SET TIME ZONE 'Asia/Shanghai'")
            conn.commit()  # 提交时区设置
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def execute_query(query: str, params=None):
    """
    执行查询并返回结果（只读模式，仅支持查询语句）
    """
    # 检查是否为查询语句
    query_type = query.strip().split()[0].upper()
    if query_type not in ['SELECT', 'WITH', 'SHOW', 'EXPLAIN', 'DESCRIBE']:
        raise ValueError(f"只读模式下不允许执行 {query_type} 语句")
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            # 确保返回的是列表
            return result if result is not None else []