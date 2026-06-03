# ── 基础镜像 ──────────────────────────────────────────────────────                                                                                            
# apache/spark:3.5.0 已经预装了 Java 11 + Apache Spark 3.5
# 省去自己装 JDK 和 Spark 的麻烦
FROM apache/spark:3.5.0

# ── 切换 root 安装依赖 ────────────────────────────────────────────
# apache/spark 镜像默认用非 root 用户运行，pip install 需要 root 权限                                                                                                
USER root

# ── 安装 Python 依赖 ──────────────────────────────────────────────                                                                                            
# 先只 COPY requirements.txt，利用 Docker 层缓存                                                                                                                
# 只要 requirements.txt 没变，这一层就不会重新构建                                                                                                              
COPY requirements.txt .                                                                                                                                         
RUN pip install --no-cache-dir -r requirements.txt   

# ── 设置工作目录 ──────────────────────────────────────────────────                                                                                            
WORKDIR /app  

# ── 复制 batch 层代码 ─────────────────────────────────────────────                                                                                            
COPY . /app/  

# ── 默认命令 ──────────────────────────────────────────────────────
# docker-compose run 时执行的默认命令
# --master local[*] 表示用本机所有 CPU 核心跑（单容器模式）
CMD ["spark-submit", "--master", "local[*]", "spark_batch.py"]
