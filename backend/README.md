# Mirror Notes Backend

Mirror Notes 后端API服务，使用FastAPI和MySQL构建。

## 功能特性

- 🎯 解决方案笔记管理
- 👍 点赞系统
- 🔒 匿名和签名模式支持
- 🌐 CORS支持
- 📊 用户行为追踪

## 技术栈

- **FastAPI**: 现代、快速的Web框架
- **MySQL**: 关系型数据库
- **PyMySQL**: MySQL数据库驱动
- **Uvicorn**: ASGI服务器

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 数据库配置

确保MySQL服务正在运行，并创建数据库：

```sql
CREATE DATABASE `mirror-notes-db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 导入数据库结构

```bash
mysql -u root -p123456 < schema.sql
```

### 4. 启动服务

```bash
python run.py
```

服务将在 `http://localhost:8000` 启动。

## API文档

启动服务后，访问以下地址查看API文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API端点

### 笔记管理

- `GET /api/notes` - 获取所有笔记
- `GET /api/notes/{id}` - 获取特定笔记
- `POST /api/notes` - 创建新笔记

### 点赞系统

- `POST /api/notes/{id}/like` - 点赞笔记
- `DELETE /api/notes/{id}/like` - 取消点赞
- `GET /api/notes/{id}/liked` - 检查点赞状态
- `GET /api/user/likes` - 获取用户点赞列表

## 数据库结构

### solution_notes 表
- `id`: 主键
- `content`: 笔记内容
- `author_name`: 作者名称
- `author_type`: 作者类型 (anonymous/signature)
- `like_count`: 点赞数
- `helped_count`: 帮助人数
- `created_at`: 创建时间
- `updated_at`: 更新时间

### user_likes 表
- `id`: 主键
- `user_ip`: 用户IP
- `note_id`: 笔记ID
- `created_at`: 点赞时间

## 环境变量

创建 `.env` 文件：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=mirror-notes-db
```

## 开发说明

- 使用IP地址追踪用户点赞状态
- 支持匿名和签名两种分享模式
- 自动处理点赞数和帮助人数统计
- 包含完整的错误处理和CORS支持
