#!/bin/bash
# restart.sh

echo "=== 植物养护管理系统重启脚本 ==="

# 停止现有容器
./stop.sh

# 启动新容器
./start.sh

echo "=== 重启完成 ==="