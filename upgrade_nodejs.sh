#!/bin/bash

# Node.js 升级脚本

set -e

echo "============================================================"
echo "Node.js 升级脚本"
echo "============================================================"
echo ""

CURRENT_VERSION=$(node --version 2>/dev/null || echo "未安装")
echo "当前 Node.js 版本: $CURRENT_VERSION"
echo ""

# 方法1: 使用 nvm (推荐)
echo "方法1: 使用 nvm 安装 Node.js 16"
echo "----------------------------------------"
echo ""
echo "执行以下命令："
echo ""
echo "1. 安装 nvm:"
echo "   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"
echo ""
echo "2. 加载 nvm:"
echo "   export NVM_DIR=\"\$HOME/.nvm\""
echo "   [ -s \"\$NVM_DIR/nvm.sh\" ] && \. \"\$NVM_DIR/nvm.sh\""
echo ""
echo "3. 安装 Node.js 16:"
echo "   nvm install 16"
echo ""
echo "4. 使用 Node.js 16:"
echo "   nvm use 16"
echo ""
echo "5. 验证版本:"
echo "   node --version"
echo ""

# 方法2: 使用 NodeSource 仓库 (Ubuntu/Debian)
if command -v apt-get &> /dev/null; then
    echo "方法2: 使用 NodeSource 仓库安装 (Ubuntu/Debian)"
    echo "----------------------------------------"
    echo ""
    echo "执行以下命令："
    echo ""
    echo "1. 添加 NodeSource 仓库:"
    echo "   curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -"
    echo ""
    echo "2. 安装 Node.js:"
    echo "   sudo apt-get install -y nodejs"
    echo ""
    echo "3. 验证版本:"
    echo "   node --version"
    echo ""
fi

# 方法3: 使用包管理器
if command -v apt-get &> /dev/null; then
    echo "方法3: 使用 apt 安装 (可能版本较旧)"
    echo "----------------------------------------"
    echo ""
    echo "执行以下命令："
    echo "   sudo apt-get update"
    echo "   sudo apt-get install -y nodejs npm"
    echo ""
elif command -v yum &> /dev/null; then
    echo "方法3: 使用 yum 安装 (CentOS/RHEL)"
    echo "----------------------------------------"
    echo ""
    echo "执行以下命令："
    echo "   sudo yum install -y nodejs npm"
    echo ""
fi

echo "============================================================"
echo "推荐使用方法1 (nvm)，因为它可以轻松管理多个 Node.js 版本"
echo "============================================================"

