# 使用官方轻量级 Python 镜像
FROM python:3

COPY backend/requirements.txt ./

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /app

# 容器启动时执行的命令
CMD ["python", "start_server.py"]