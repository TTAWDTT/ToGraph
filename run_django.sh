#!/bin/bash
# ToGraph Django Server Launcher

echo "╔══════════════════════════════════════════════════════════╗"
echo "║              ToGraph Django 知识图谱平台                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django 未安装。正在安装依赖..."
    pip install -r requirements.txt
    echo ""
fi

# Run migrations if needed
echo "🔄 检查数据库迁移..."
python manage.py migrate --noinput

echo ""
echo "✅ 启动 Django 开发服务器..."
echo ""
echo "🌐 服务器地址: http://127.0.0.1:8000"
echo "📊 上传 PDF 或 Markdown 文件生成知识图谱"
echo "🎨 享受深蓝色主题的美观界面"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# Start the server
python manage.py runserver
