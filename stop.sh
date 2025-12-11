#!/bin/bash

# 停止所有服务脚本

echo "============================================================"
echo "停止 DeepInsight Platform 服务"
echo "============================================================"
echo ""

# 停止后端服务
echo "停止后端服务..."
BACKEND_PIDS=$(lsof -ti :8000 2>/dev/null)
if [ ! -z "$BACKEND_PIDS" ]; then
    for pid in $BACKEND_PIDS; do
        kill $pid 2>/dev/null || true
    done
    sleep 2
    # 强制杀死仍在运行的进程
    BACKEND_PIDS=$(lsof -ti :8000 2>/dev/null)
    if [ ! -z "$BACKEND_PIDS" ]; then
        for pid in $BACKEND_PIDS; do
            kill -9 $pid 2>/dev/null || true
        done
    fi
    echo "✅ 后端服务已停止"
else
    echo "ℹ️  后端服务未运行"
fi

# 停止前端服务
echo "停止前端服务..."
FRONTEND_PIDS=$(lsof -ti :3000 2>/dev/null)
if [ ! -z "$FRONTEND_PIDS" ]; then
    for pid in $FRONTEND_PIDS; do
        kill $pid 2>/dev/null || true
    done
    sleep 2
    # 强制杀死仍在运行的进程
    FRONTEND_PIDS=$(lsof -ti :3000 2>/dev/null)
    if [ ! -z "$FRONTEND_PIDS" ]; then
        for pid in $FRONTEND_PIDS; do
            kill -9 $pid 2>/dev/null || true
        done
    fi
    echo "✅ 前端服务已停止"
else
    echo "ℹ️  前端服务未运行"
fi

# 停止所有 uvicorn 进程
echo "清理 uvicorn 进程..."
pkill -f "uvicorn app:app" 2>/dev/null && echo "✅ 已清理 uvicorn 进程" || echo "ℹ️  无 uvicorn 进程"

# 停止所有 vite 进程
echo "清理 vite 进程..."
pkill -f "vite" 2>/dev/null && echo "✅ 已清理 vite 进程" || echo "ℹ️  无 vite 进程"

echo ""
echo "============================================================"
echo "✅ 所有服务已停止"
echo "============================================================"

