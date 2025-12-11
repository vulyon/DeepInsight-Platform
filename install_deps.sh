#!/bin/bash

# 安装依赖脚本

set -e

echo "============================================================"
echo "安装项目依赖"
echo "============================================================"
echo ""

# 检查Python版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $PYTHON_VERSION"

# 安装后端依赖
echo ""
echo "安装后端依赖..."
pip install -q python-multipart jieba fastapi uvicorn pandas numpy

# 根据Python版本安装TensorFlow
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 12 ]; then
    echo "检测到 Python 3.12+，安装 TensorFlow 2.16+..."
    pip install -q "tensorflow>=2.16.0" keras wordcloud matplotlib seaborn Pillow scikit-learn pydantic
else
    echo "安装 TensorFlow 2.15.0..."
    pip install -q tensorflow==2.15.0 keras==2.15.0 wordcloud matplotlib seaborn Pillow scikit-learn pydantic
fi

echo ""
echo "✅ 后端依赖安装完成"
echo ""

# 安装前端依赖
echo "安装前端依赖..."
cd frontend

if [ ! -d "node_modules" ]; then
    npm install --legacy-peer-deps
else
    echo "前端依赖已存在，跳过安装"
fi

cd ..

echo ""
echo "✅ 所有依赖安装完成！"
echo "============================================================"

