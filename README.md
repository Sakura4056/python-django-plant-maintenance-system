# 植物养护管理系统

## 项目介绍

这是一个基于Python Django框架开发的植物养护管理系统，旨在帮助植物爱好者更好地管理和养护植物。系统采用前后端分离的架构设计，提供植物信息查询、养护计划制定、养护记录、成长相册等功能。

## 技术架构

### 后端技术栈
- **框架**: Python Django 4.2+
- **API**: Django REST Framework
- **认证**: JWT Token认证
- **数据库**: MySQL 8.0
- **缓存**: Redis
- **部署**: Gunicorn + Nginx

### 前端技术栈
- **框架**: Vue.js 3.x
- **UI组件**: Bootstrap 5
- **状态管理**: Vuex
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **图表**: Chart.js

## 项目结构

```
plant-care-system/
├── plant_care_system/          # Django后端项目
│   ├── plant_care/             # 项目配置
│   ├── users/                  # 用户管理模块
│   ├── plants/                 # 植物信息模块
│   ├── care/                   # 养护管理模块
│   └── growth/                 # 成长追踪模块
├── plant_care_frontend/        # Vue.js前端项目
│   ├── src/                    # 源代码
│   │   ├── components/         # 组件
│   │   ├── views/              # 页面
│   │   ├── store/              # Vuex状态管理
│   │   └── router/             # 路由配置
│   └── public/                 # 静态资源
├── nginx/                      # Nginx配置
├── backups/                    # 数据库备份
├── logs/                       # 日志文件
├── docker-compose.yml          # Docker Compose配置
├── .env.example                # 环境变量示例
├── start.sh                    # 启动脚本
├── stop.sh                     # 停止脚本
├── backup.sh                   # 备份脚本
└── README.md                   # 项目说明
```

## 主要功能模块

### 1. 用户管理模块
- 用户注册与登录
- 个人信息管理
- 权限控制

### 2. 植物信息库模块
- 植物信息查询与浏览
- 植物分类管理
- 植物详情展示

### 3. 我的植物管理模块
- 添加个人养护的植物
- 记录购买时间、放置位置等信息
- 植物状态更新与管理

### 4. 养护计划制定模块
- 自动生成养护计划
- 浇水提醒设置
- 施肥提醒设置
- 养护计划调整

### 5. 养护记录模块
- 记录浇水时间
- 记录施肥种类和用量
- 记录病虫害防治情况
- 养护历史查询

### 6. 成长相册模块
- 上传植物照片
- 记录植物成长变化
- 照片时间轴展示
- 生长数据分析

## 快速开始

### 环境要求
- Docker 和 Docker Compose
- Git
- 至少2GB内存
- 10GB可用磁盘空间

### 部署步骤

1. **克隆项目**
```bash
git clone https://github.com/yourusername/plant-care-system.git
cd plant-care-system
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑.env文件，配置数据库密码等信息
```

3. **设置权限**
```bash
chmod +x *.sh
./setup_permissions.sh
```

4. **启动系统**
```bash
./start.sh
```

5. **访问系统**
- **前端**: http://localhost
- **后端API**: http://localhost/api
- **管理后台**: http://localhost/admin

## 数据库设计

系统包含以下主要数据表：

1. **用户相关**: User, UserProfile
2. **植物信息**: Plant, PlantCategory, PlantCareGuide
3. **我的植物**: MyPlant
4. **养护计划**: CarePlan, CareTask
5. **养护记录**: CareRecord
6. **成长追踪**: GrowthPhoto, GrowthMeasurement, GrowthAnalysis

## API接口文档

系统提供RESTful API接口，主要包括：

### 认证接口
- `POST /api/token/` - 获取JWT Token
- `POST /api/users/register/` - 用户注册

### 植物接口
- `GET /api/plants/` - 获取植物列表
- `GET /api/plants/{id}/` - 获取植物详情

### 养护接口
- `GET /api/care/my-plants/` - 获取我的植物
- `POST /api/care/care-records/` - 添加养护记录

## 部署说明

### Docker部署
系统使用Docker Compose进行容器化部署，包含以下服务：
- MySQL数据库
- Redis缓存
- Django后端
- Vue.js前端
- Nginx服务器

### 生产环境配置
1. 修改`.env`文件中的配置
2. 配置Nginx SSL证书
3. 设置定期备份任务
4. 配置监控告警

## 维护与更新

### 数据库备份
```bash
./backup.sh
```

### 系统更新
```bash
git pull
./restart.sh
```

### 日志查看
```bash
docker-compose logs -f
```

## 贡献指南

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

## 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## 联系方式

- 项目维护者: [Your Name]
- 邮箱: your.email@example.com
- 项目地址: https://github.com/yourusername/plant-care-system