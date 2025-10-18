#!/bin/bash
# backup.sh

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/plant_care_backup_$TIMESTAMP.sql"

# 创建备份目录
mkdir -p $BACKUP_DIR

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

# 执行数据库备份
echo "正在备份数据库..."
docker-compose exec -T db mysqldump -u plantuser -pplantpassword plant_care > $BACKUP_FILE

# 检查备份是否成功
if [ $? -eq 0 ]; then
    echo "备份成功: $BACKUP_FILE"
    
    # 压缩备份文件
    gzip $BACKUP_FILE
    echo "备份文件已压缩: $BACKUP_FILE.gz"
    
    # 清理旧备份（保留最近30天）
    echo "清理旧备份文件..."
    find $BACKUP_DIR -name "plant_care_backup_*.sql.gz" -mtime +30 -delete
    
    echo "备份完成！"
else
    echo "备份失败！"
    rm -f $BACKUP_FILE
    exit 1
fi