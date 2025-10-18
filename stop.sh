#!/bin/bash
# stop.sh

echo "=== 植物养护管理系统停止脚本 ==="

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装。"
    exit 1
fi

# 停止容器
echo "正在停止容器..."
docker-compose down

# 显示状态
echo "显示容器状态..."
docker-compose ps

echo "=== 停止完成 ==="