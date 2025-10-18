#!/bin/bash
# start.sh

echo "=== 植物养护管理系统启动脚本 ==="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装。请先安装Docker和Docker Compose。"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装。请先安装Docker Compose。"
    exit 1
fi

# 检查.env文件是否存在
if [ ! -f ".env" ]; then
    echo "警告: .env文件不存在，将使用默认配置。"
    echo "建议复制.env.example为.env并配置相关参数。"
    read -p "是否继续使用默认配置? (y/n): " choice
    if [[ ! $choice =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

# 构建和启动容器
echo "正在构建和启动容器..."
docker-compose up -d --build

# 等待数据库启动
echo "等待数据库启动..."
sleep 30

# 执行数据库迁移
echo "执行数据库迁移..."
docker-compose exec backend python manage.py migrate

# 创建超级用户
echo "创建超级用户..."
docker-compose exec backend python manage.py createsuperuser

# 收集静态文件
echo "收集静态文件..."
docker-compose exec backend python manage.py collectstatic --noinput

# 显示状态
echo "显示容器状态..."
docker-compose ps

echo "=== 启动完成 ==="
echo "访问地址:"
echo "  - 前端: http://localhost"
echo "  - 后端API: http://localhost/api"
echo "  - Django管理后台: http://localhost/admin"
echo "  - API文档: http://localhost/api/docs/"