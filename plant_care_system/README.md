# 基于Python的Django框架植物养护管理系统

## 项目介绍

这是一个基于Python Django框架开发的植物养护管理系统，旨在帮助植物爱好者更好地管理和养护植物。系统采用前后端分离的架构设计，提供植物信息查询、养护计划制定、养护记录、成长相册等功能。

## 技术栈

### 后端技术
- **框架**: Python Django 4.2+
- **API**: Django REST Framework
- **认证**: JWT Token认证
- **数据库**: MySQL 8.0
- **缓存**: Redis (可选)
- **部署**: Gunicorn + Nginx

### 前端技术
- **框架**: Vue.js 3.x
- **UI组件**: Bootstrap 5
- **状态管理**: Vuex
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **图表**: Chart.js

## 功能模块

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

## 项目结构

```
plant_care_system/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── plant_care/                  # 项目主配置
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── users/                       # 用户管理模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── plants/                      # 植物信息模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── care/                        # 养护管理模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── growth/                      # 成长追踪模块
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
├── static/                      # 静态文件
├── media/                       # 媒体文件
└── logs/                        # 日志文件
```

## 环境配置

### 1. 数据库配置
创建MySQL数据库：
```sql
CREATE DATABASE plant_care CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 环境变量
创建`.env`文件：
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=mysql://root:password@localhost:3306/plant_care
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 安装与运行

### 后端安装
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

### 前端安装（单独的Vue项目）
```bash
# 克隆前端项目（假设前端项目在单独的仓库）
git clone https://github.com/yourusername/plant-care-frontend.git
cd plant-care-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run serve
```

## API接口文档

### 用户认证
- `POST /api/token/` - 获取JWT Token
- `POST /api/token/refresh/` - 刷新Token
- `POST /api/users/register/` - 用户注册
- `GET /api/users/profile/` - 获取用户资料

### 植物信息
- `GET /api/plants/` - 获取植物列表
- `GET /api/plants/{id}/` - 获取植物详情
- `GET /api/plants/categories/` - 获取植物分类

### 我的植物
- `GET /api/care/my-plants/` - 获取我的植物列表
- `POST /api/care/my-plants/` - 添加植物
- `GET /api/care/my-plants/{id}/` - 获取植物详情
- `PUT /api/care/my-plants/{id}/` - 更新植物信息
- `DELETE /api/care/my-plants/{id}/` - 删除植物

### 养护计划
- `GET /api/care/care-plans/` - 获取养护计划列表
- `POST /api/care/care-plans/` - 创建养护计划
- `POST /api/care/my-plants/{id}/generate_care_plan/` - 自动生成养护计划

### 养护记录
- `GET /api/care/care-records/` - 获取养护记录列表
- `POST /api/care/care-records/` - 添加养护记录

### 成长追踪
- `GET /api/growth/photos/` - 获取成长照片列表
- `POST /api/growth/photos/` - 上传成长照片
- `GET /api/growth/measurements/` - 获取生长测量数据
- `POST /api/growth/measurements/` - 添加生长测量数据

## 部署

### 生产环境部署
```bash
# 收集静态文件
python manage.py collectstatic

# 使用Gunicorn启动
gunicorn plant_care.wsgi:application --bind 0.0.0.0:8000
```

### Docker部署
```bash
# 构建镜像
docker build -t plant-care-system .

# 运行容器
docker run -d -p 8000:8000 plant-care-system
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