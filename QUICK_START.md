# 植物养护管理系统 - 快速开始指南

## 系统概述

这是一个基于Python Django框架开发的植物养护管理系统，采用前后端分离架构：
- **后端**: Django + Django REST Framework + MySQL + Redis
- **前端**: Vue.js 3 + Bootstrap 5 + Chart.js
- **部署**: Docker + Docker Compose + Nginx

## 主要功能

1. **用户管理**: 注册、登录、个人资料管理
2. **植物信息库**: 植物信息查询、分类浏览
3. **我的植物**: 个人植物管理、状态跟踪
4. **养护计划**: 智能养护计划生成、提醒管理
5. **养护记录**: 详细养护操作记录
6. **成长相册**: 植物照片上传、成长时间轴
7. **数据可视化**: 养护数据统计、图表展示

## 快速部署

### 1. 环境准备
- Docker 和 Docker Compose
- Git
- 至少2GB内存
- 10GB可用磁盘空间

### 2. 克隆项目
```bash
git clone https://github.com/yourusername/plant-care-system.git
cd plant-care-system
```

### 3. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，配置数据库密码等信息
```

### 4. 设置权限
```bash
./setup_permissions.sh
```

### 5. 启动系统
```bash
./start.sh
```

### 6. 访问系统
- **前端**: http://localhost
- **后端API**: http://localhost/api
- **管理后台**: http://localhost/admin
- **API文档**: http://localhost/api/docs/

## 常用命令

### 启动系统
```bash
./start.sh
```

### 停止系统
```bash
./stop.sh
```

### 重启系统
```bash
./restart.sh
```

### 数据库备份
```bash
./backup.sh
```

### 数据库恢复
```bash
./restore.sh backups/backup_file.sql.gz
```

### 查看日志
```bash
docker-compose logs -f
```

### 进入容器
```bash
# 进入后端容器
docker-compose exec backend bash

# 进入数据库容器
docker-compose exec db bash
```

## 系统维护

### 定期备份
建议设置定时任务定期备份数据库：
```bash
# 每天凌晨2点备份
0 2 * * * /path/to/plant-care-system/backup.sh >> /path/to/plant-care-system/logs/backup.log 2>&1
```

### 清理日志
```bash
# 清理Docker日志
truncate -s 0 /var/lib/docker/containers/*/*-json.log

# 清理系统日志
rm -rf logs/*
```

### 更新系统
```bash
git pull
./restart.sh
```

## 故障排除

### 常见问题

1. **容器启动失败**
   - 检查Docker和Docker Compose是否正常运行
   - 检查端口是否被占用
   - 检查.env文件配置是否正确

2. **数据库连接失败**
   - 检查数据库容器是否正常运行
   - 检查数据库用户名和密码是否正确
   - 检查数据库是否已创建

3. **静态文件无法访问**
   - 检查collectstatic命令是否执行成功
   - 检查Nginx配置是否正确
   - 检查静态文件目录权限

4. **API访问失败**
   - 检查后端容器是否正常运行
   - 检查API URL是否正确
   - 检查认证令牌是否有效

### 联系方式

如遇到问题，请联系：
- Email: support@plantcare.com
- GitHub Issues: https://github.com/yourusername/plant-care-system/issues

## 许可证

本项目采用MIT许可证，详见LICENSE文件。