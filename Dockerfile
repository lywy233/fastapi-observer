# -------- 基础镜像 --------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# -------- 工作目录 --------
WORKDIR /app

# -------- 复制依赖文件 --------
COPY pyproject.toml ./

# -------- 创建虚拟环境并安装依赖 --------
RUN uv sync

# -------- 复制代码 --------
COPY main.py ./

# -------- 创建存储目录 --------
RUN mkdir -p /app/storage

# -------- 端口 --------
EXPOSE 9000

# -------- 启动 --------
CMD ["/app/.venv/bin/python", "main.py"]
