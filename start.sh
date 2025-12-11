#!/bin/bash

# DeepInsight Platform - 一键启动脚本
# 同时启动前后端服务

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo "============================================================"
    echo "$1"
    echo "============================================================"
}

# 清理函数
cleanup() {
    echo ""
    print_header "正在关闭服务..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
        print_info "后端服务已停止"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
        print_info "前端服务已停止"
    fi
    
    print_info "所有服务已关闭"
    exit 0
}

# 注册清理函数
trap cleanup SIGINT SIGTERM

# 检查依赖
print_header "检查依赖..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    print_error "未找到Python3，请先安装Python3"
    exit 1
fi
print_info "Python3 已安装"

# 检查Node.js
if ! command -v node &> /dev/null; then
    print_error "未找到Node.js，请先安装Node.js 14+"
    exit 1
fi
NODE_VERSION=$(node --version | sed 's/v//')
NODE_MAJOR_VERSION=$(echo $NODE_VERSION | cut -d. -f1)
NODE_MINOR_VERSION=$(echo $NODE_VERSION | cut -d. -f2)
NODE_VERSION_OK=0

# 检查 Node.js 版本
if [ "$NODE_MAJOR_VERSION" -lt 14 ] 2>/dev/null; then
    NODE_VERSION_OK=0
elif [ "$NODE_MAJOR_VERSION" -eq 14 ] 2>/dev/null; then
    if [ "$NODE_MINOR_VERSION" -ge 18 ] 2>/dev/null; then
        NODE_VERSION_OK=1
    fi
elif [ "$NODE_MAJOR_VERSION" -ge 16 ] 2>/dev/null; then
    NODE_VERSION_OK=1
fi

if [ "$NODE_VERSION_OK" -eq 0 ]; then
    print_warn "Node.js 版本过低 ($(node --version))"
    print_warn "前端需要 Node.js 14.18+ 或 16+ 才能运行"
    print_warn "将只启动后端服务"
    print_warn ""
    print_warn "要启动前端，请升级 Node.js："
    print_warn "  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"
    print_warn "  source ~/.bashrc"
    print_warn "  nvm install 16"
    print_warn "  nvm use 16"
    SKIP_FRONTEND=1
else
    print_info "Node.js 已安装 ($(node --version))"
    SKIP_FRONTEND=0
fi

# 检查npm
if ! command -v npm &> /dev/null; then
    print_error "未找到npm，请先安装npm"
    exit 1
fi
print_info "npm 已安装 ($(npm --version))"

# 检查后端依赖
if [ -f "requirements.txt" ]; then
    print_info "后端依赖文件存在"
    # 检查是否已安装关键包
    if python3 -c "import fastapi, multipart" 2>/dev/null; then
        print_info "后端Python依赖已安装"
    else
        print_warn "后端Python依赖未安装，正在安装..."
        pip install -q -r requirements.txt
        print_info "后端Python依赖安装完成"
    fi
else
    print_warn "未找到 requirements.txt"
fi

# 检查前端依赖（仅在 Node.js 版本足够时）
if [ "$SKIP_FRONTEND" -eq 0 ]; then
    if [ -d "frontend/node_modules" ]; then
        print_info "前端依赖已安装"
    else
        print_warn "前端依赖未安装，正在安装..."
        cd frontend
        npm install --legacy-peer-deps
        cd ..
        print_info "前端依赖安装完成"
    fi
fi

echo ""

# 启动后端服务
print_header "启动后端服务..."

# 检查端口是否被占用
if lsof -i :8000 > /dev/null 2>&1; then
    print_warn "端口 8000 已被占用，正在清理旧进程..."
    # 查找并杀死占用端口的进程
    OLD_PID=$(lsof -ti :8000)
    if [ ! -z "$OLD_PID" ]; then
        kill $OLD_PID 2>/dev/null || true
        sleep 2
        # 如果还没死，强制杀死
        if kill -0 $OLD_PID 2>/dev/null; then
            kill -9 $OLD_PID 2>/dev/null || true
            sleep 1
        fi
        print_info "已清理旧进程"
    fi
fi

cd backend

# 清空日志文件
> ../backend.log

# 启动后端（后台运行）
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
BACKEND_PID=$!

cd ..

# 等待后端启动（增加等待时间）
print_info "等待后端服务启动..."
for i in {1..10}; do
    sleep 1
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        print_info "后端服务启动成功!"
        echo "   API地址: http://localhost:8000"
        echo "   API文档: http://localhost:8000/docs"
        break
    fi
    if [ $i -eq 10 ]; then
        print_warn "后端服务启动超时，请检查日志 (backend.log)"
        print_warn "最后几行日志："
        tail -5 backend.log 2>/dev/null || echo "无法读取日志文件"
    fi
done

echo ""

# 启动前端服务（如果 Node.js 版本足够）
if [ "$SKIP_FRONTEND" -eq 0 ]; then
    print_header "启动前端服务..."
    
    # 清理可能占用 3000 端口的旧进程
    if lsof -i :3000 > /dev/null 2>&1; then
        print_warn "端口 3000 被占用，正在清理..."
        OLD_PIDS=$(lsof -ti :3000)
        if [ ! -z "$OLD_PIDS" ]; then
            for pid in $OLD_PIDS; do
                kill $pid 2>/dev/null || true
            done
            sleep 2
            # 强制杀死仍在运行的进程
            OLD_PIDS=$(lsof -ti :3000)
            if [ ! -z "$OLD_PIDS" ]; then
                for pid in $OLD_PIDS; do
                    kill -9 $pid 2>/dev/null || true
                done
            fi
            print_info "已清理旧进程"
        fi
    fi
    
    cd frontend
    
    # 清空日志文件
    > ../frontend.log
    
    # 启动前端（后台运行）
    npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    
    cd ..
    
    # 等待前端启动并检测实际端口
    print_info "等待前端服务启动..."
    FRONTEND_PORT=3000
    for i in {1..10}; do
        sleep 1
        # 从日志中提取端口号
        if [ -f frontend.log ]; then
            # 查找 "Local:" 行中的端口号
            PORT_LINE=$(grep -E "Local:.*http://localhost:[0-9]+" frontend.log | head -1)
            if [ ! -z "$PORT_LINE" ]; then
                FRONTEND_PORT=$(echo "$PORT_LINE" | grep -oE "localhost:[0-9]+" | cut -d: -f2)
                if [ ! -z "$FRONTEND_PORT" ]; then
                    break
                fi
            fi
        fi
        # 或者检查端口是否在监听
        if lsof -i :3000 > /dev/null 2>&1; then
            FRONTEND_PORT=3000
            break
        elif lsof -i :3001 > /dev/null 2>&1; then
            FRONTEND_PORT=3001
            break
        fi
    done
    
    print_info "前端服务启动成功!"
    echo "   本地地址: http://localhost:$FRONTEND_PORT"
    # 获取服务器IP地址
    SERVER_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || ip addr show 2>/dev/null | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}' | cut -d/ -f1)
    if [ ! -z "$SERVER_IP" ]; then
        echo "   网络地址: http://$SERVER_IP:$FRONTEND_PORT"
    fi
    echo ""
else
    print_warn "跳过前端启动（Node.js 版本过低）"
    FRONTEND_PID=""
    echo ""
fi

# 打印启动信息
print_header "服务启动完成!"
echo ""
echo "访问地址:"
if [ "$SKIP_FRONTEND" -eq 0 ]; then
    echo "  前端: http://localhost:3000"
fi
echo "  后端API: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "日志文件:"
echo "  后端日志: backend.log"
if [ "$SKIP_FRONTEND" -eq 0 ]; then
    echo "  前端日志: frontend.log"
fi
echo ""
if [ "$SKIP_FRONTEND" -eq 1 ]; then
    echo "注意: 前端服务未启动（Node.js 版本过低）"
    echo "      仅后端服务正在运行"
    echo ""
fi
echo "按 Ctrl+C 停止所有服务"
echo "============================================================"
echo ""

# 尝试自动打开浏览器（如果支持）
if [ "$SKIP_FRONTEND" -eq 0 ]; then
    sleep 3  # 等待前端完全启动
    # 使用检测到的端口
    FRONTEND_PORT=${FRONTEND_PORT:-3000}
    FRONTEND_URL="http://localhost:$FRONTEND_PORT"
    
    # 自动加载示例数据（通过URL参数）
    # 取消下面的注释以启用启动时自动加载示例数据
    # FRONTEND_URL="${FRONTEND_URL}?autoLoadDemo=true"
    
    if command -v xdg-open &> /dev/null; then
        xdg-open "$FRONTEND_URL" 2>/dev/null &
        echo "✅ 已尝试在浏览器中打开前端页面: $FRONTEND_URL"
    elif command -v open &> /dev/null; then
        open "$FRONTEND_URL" 2>/dev/null &
        echo "✅ 已尝试在浏览器中打开前端页面: $FRONTEND_URL"
    elif command -v start &> /dev/null; then
        start "$FRONTEND_URL" 2>/dev/null &
        echo "✅ 已尝试在浏览器中打开前端页面: $FRONTEND_URL"
    else
        echo "💡 提示: 请在浏览器中访问 $FRONTEND_URL"
    fi
    echo ""
    echo "💡 提示: 页面打开后，点击'快速体验'按钮可立即查看示例数据分析结果"
    echo ""
fi

# 等待用户中断
wait

