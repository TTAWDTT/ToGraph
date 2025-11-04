# ToGraph Django 版本使用指南

## 概述

ToGraph 现在支持 Django 框架，提供更强大的 Web 应用框架和更美观的深蓝色主题界面。

## 主要特性

### 🎨 全新界面设计
- **深蓝色主题**：采用 #0a1931 深蓝色作为主色调，提供优雅的视觉体验
- **动画效果**：粒子动画背景、渐变效果、平滑过渡动画
- **玻璃态设计**：现代化的卡片式布局，配合毛玻璃效果
- **响应式设计**：完美适配各种屏幕尺寸

### 🚀 增强功能
- **Django 框架**：基于 Django 4.2.7，提供更强大的后端支持
- **改进的 PDF 解析**：
  - 支持多种章节编号格式（1., 1.1, 1.1.1）
  - 支持罗马数字章节（I., II., III.）
  - 改进的标题识别算法
  - 更深层的内容嵌套支持
- **优化的图谱布局**：
  - 改进的物理引擎参数
  - 更好的节点分布
  - 立体阴影效果
  - 贝塞尔曲线边缘

### 🌐 3D 可视化
- 支持 2D 和 3D 立体视图切换（UI 已就绪）
- 交互式图谱导航
- 实时物理模拟

## 安装

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖包括：
- Django 4.2.7
- pdfplumber 0.10.3
- networkx 3.2.1
- pyvis 0.3.2
- 其他依赖见 requirements.txt

### 2. 初始化数据库

```bash
python manage.py migrate
```

### 3. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

## 启动服务

### 开发服务器

```bash
# 默认在 localhost:8000
python manage.py runserver

# 指定端口
python manage.py runserver 8080

# 允许外部访问
python manage.py runserver 0.0.0.0:8000
```

服务启动后，在浏览器中访问：`http://localhost:8000`

## 使用说明

### 1. 上传文档

- 点击上传区域或拖拽文件
- 支持的格式：PDF、Markdown (.md, .markdown)
- 最大文件大小：16MB

### 2. 配置选项

- **主题风格**：选择浅色或深色主题（推荐深色）
- **图谱标题**：为您的知识图谱命名
- **可视化类型**：选择 2D 或 3D 视图

### 3. 生成图谱

- 点击"生成知识图谱"按钮
- 等待处理完成
- 查看生成的交互式图谱

### 4. 交互操作

生成的图谱支持以下操作：
- **平移**：点击并拖动图谱
- **缩放**：使用鼠标滚轮
- **悬停**：将鼠标移到节点上查看内容预览
- **点击**：点击节点查看完整详情
- **适应屏幕**：点击按钮自动调整视图
- **切换物理引擎**：开启/关闭节点动画

### 5. 下载结果

- 点击"下载 HTML"按钮保存独立的 HTML 文件
- 生成的文件可以离线使用，无需服务器

## 架构说明

### 项目结构

```
ToGraph/
├── tograph/              # 原始包（CLI 和核心功能）
│   ├── parser.py         # 文档解析（已增强）
│   ├── graph_builder.py  # 图谱构建
│   ├── visualizer.py     # 可视化（已增强）
│   ├── main.py          # CLI 接口
│   └── web_app.py       # Flask 版本（保留）
├── tograph_project/     # Django 项目配置
│   ├── settings.py      # Django 设置
│   ├── urls.py          # URL 路由
│   └── wsgi.py          # WSGI 配置
├── graph_app/           # Django 应用
│   ├── views.py         # 视图函数
│   ├── urls.py          # 应用 URL
│   ├── templates/       # 模板文件
│   │   └── index.html   # 主页面（深蓝色主题）
│   └── static/          # 静态文件
├── manage.py            # Django 管理脚本
└── requirements.txt     # Python 依赖
```

### URL 路由

- `/` - 主页面（上传和配置界面）
- `/convert/` - 文件转换 API
- `/view/<file_id>/` - 查看生成的图谱
- `/download/<file_id>/` - 下载 HTML 文件
- `/admin/` - Django 管理后台

## API 使用

### 转换 API

```bash
# 使用 curl 上传文件
curl -X POST \
  -F "file=@document.pdf" \
  -F "theme=dark" \
  -F "title=My Knowledge Graph" \
  http://localhost:8000/convert/

# 返回结果
{
    "success": true,
    "file_id": "uuid-here",
    "stats": {
        "nodes": 15,
        "edges": 28,
        "sections": 5
    }
}
```

### 查看图谱

```bash
# 在浏览器中打开
http://localhost:8000/view/<file_id>/
```

### 下载文件

```bash
# 使用 wget 或浏览器下载
wget http://localhost:8000/download/<file_id>/
```

## 与 Flask 版本比较

### 保留的功能

- ✅ 命令行工具（`tograph` 命令）
- ✅ Flask Web 服务器（`tograph-web` 命令）
- ✅ 所有原有的文档解析功能
- ✅ 多种输出格式（HTML、PNG、PDF）

### 新增功能

- ✨ Django 框架支持
- ✨ 深蓝色主题界面
- ✨ 动画和视觉效果
- ✨ 改进的 PDF 解析
- ✨ 优化的图谱布局
- ✨ 中文界面
- ✨ 更好的错误处理

### 选择建议

- **Django 版本**：适合需要完整 Web 应用、更好的界面、将来可能扩展功能的场景
- **Flask 版本**：适合快速启动、简单使用、轻量级部署的场景
- **命令行版本**：适合批处理、自动化脚本、无 GUI 环境

## 配置说明

### settings.py 主要配置

```python
# 文件上传大小限制
FILE_UPLOAD_MAX_MEMORY_SIZE = 16777216  # 16MB

# 静态文件目录
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'graph_app' / 'static']

# 媒体文件目录
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 自定义配置

您可以修改 `tograph_project/settings.py` 来自定义：
- 数据库配置
- 静态文件路径
- 文件上传限制
- 时区和语言设置

## 部署

### 开发环境

```bash
python manage.py runserver
```

### 生产环境

1. **收集静态文件**
```bash
python manage.py collectstatic
```

2. **使用 Gunicorn**
```bash
pip install gunicorn
gunicorn tograph_project.wsgi:application --bind 0.0.0.0:8000
```

3. **使用 Nginx 反向代理**

配置示例：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/ToGraph/staticfiles/;
    }
}
```

## 性能优化

### 文件清理

生成的文件会自动在 1 小时后过期并清理，防止磁盘空间占用。

### 缓存配置

可以在 `settings.py` 中配置 Django 缓存以提高性能：

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

## 故障排除

### 问题：无法启动服务器

**错误**：`Address already in use`
**解决**：更改端口或停止占用端口的进程
```bash
python manage.py runserver 8080
```

### 问题：文件上传失败

**错误**：`File too large`
**解决**：修改 `settings.py` 中的 `FILE_UPLOAD_MAX_MEMORY_SIZE`

### 问题：图谱不显示

**原因**：可能是 CDN 资源加载失败
**解决**：
1. 检查网络连接
2. 使用其他浏览器
3. 下载 HTML 文件本地打开

### 问题：PDF 解析不完整

**原因**：PDF 格式复杂
**解决**：
1. 尝试转换为 Markdown 格式
2. 使用更标准化的 PDF 文档
3. 查看日志了解具体错误

## 开发指南

### 添加新功能

1. 修改 `graph_app/views.py` 添加新的视图
2. 在 `graph_app/urls.py` 添加 URL 路由
3. 更新模板文件 `graph_app/templates/`

### 自定义主题

编辑 `graph_app/templates/index.html` 中的 CSS 变量：

```css
:root {
    --deep-blue: #0a1931;
    --medium-blue: #185adb;
    --light-blue: #4a90e2;
    --accent-blue: #00d9ff;
    /* ... 其他颜色 */
}
```

### 扩展解析器

修改 `tograph/parser.py` 中的 `_extract_structure` 方法以支持新的文档格式或章节模式。

## 许可证

MIT License - 详见 LICENSE 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 支持

- GitHub: https://github.com/TTAWDTT/ToGraph
- Issues: https://github.com/TTAWDTT/ToGraph/issues
