# 基于轻量的Python 3.9镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制脚本到容器内
COPY barkmonitor.py /app/

# 安装依赖（requests）
RUN pip install --no-cache-dir requests

# 设置容器启动命令
CMD ["python", "/app/barkmonitor.py"]