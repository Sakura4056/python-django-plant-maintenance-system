#!/bin/bash
# restore.sh

if [ $# -ne 1 ]; then
    echo "用法: $0 <backup_file>"
    echo "例如: $0 backups/plant_care_backup_20240101_120000.sql.gz"
    exit 1
fi

BACKUP_FILE=$1

# 检查备份文件是否存在
if [ ! -f "$BACKUP_FILE" ]; then
    echo "错误: 备份文件 $BACKUP_FILE 不存在。"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装。"
    exit 1
fi

# 检查容器是否运行
if ! docker-compose ps | grep -q "Up"; then
    echo "错误: 容器未运行。"
    exit 1
fi

# 确认恢复操作
read -p "警告: 此操作将覆盖现有数据库。是否继续? (y/n): " choice
if [[ ! $choice =~ ^[Yy]$ ]]; then
    exit 0
fi

# 恢复数据库
echo "正在恢复数据库..."

# 检查文件是否为压缩文件
if [[ $BACKUP_FILE == *.gz ]]; then
    gunzip -c $BACKUP_FILE | docker-compose exec -T db mysql -u plantuser -pplantpassword plant_care
else
    docker-compose exec -T db mysql -u plantuser -pplantpassword plant_care < $BACKUP_FILE
fi

if [ $? -eq 0 ]; then
    echo "数据库恢复成功！"
else
    echo "数据库恢复失败！"
    exit 1
fi