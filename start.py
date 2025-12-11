#!/usr/bin/env python3
"""
一键启动脚本 - 同时启动前后端服务
"""
import os
import sys
import subprocess
import signal
import time
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"

# 存储子进程
processes = []


def check_dependencies():
    """检查依赖是否已安装"""
    import shutil
    
    skip_frontend = False
    
    print("=" * 60)
    print("检查依赖...")
    print("=" * 60)
    
    # 检查Python
    if not shutil.which("python3"):
        print("❌ 错误: 未找到Python3，请先安装Python3")
        sys.exit(1)
    print("✅ Python3 已安装")
    
    # 检查Node.js
    if not shutil.which("node"):
        print("❌ 错误: 未找到Node.js，请先安装Node.js 14+")
        sys.exit(1)
    
    # 检查Node.js版本
    try:
        import subprocess as sp
        node_version_output = sp.check_output(["node", "--version"], text=True).strip()
        node_version = node_version_output.replace("v", "")
        version_parts = node_version.split(".")
        node_major = int(version_parts[0])
        node_minor = int(version_parts[1]) if len(version_parts) > 1 else 0
        
        if node_major < 14 or (node_major == 14 and node_minor < 18):
            print(f"⚠️  警告: Node.js 版本过低 ({node_version_output})")
            print("   前端需要 Node.js 14.18+ 或 16+ 才能运行")
            print("   将只启动后端服务")
            print("")
            print("   要启动前端，请升级 Node.js：")
            print("     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash")
            print("     source ~/.bashrc")
            print("     nvm install 16")
            print("     nvm use 16")
            skip_frontend = True
        else:
            print(f"✅ Node.js 已安装 ({node_version_output})")
    except Exception as e:
        print(f"⚠️  无法检查 Node.js 版本: {e}")
        skip_frontend = True
    
    # 检查npm
    if not shutil.which("npm"):
        print("❌ 错误: 未找到npm，请先安装npm")
        sys.exit(1)
    print("✅ npm 已安装")
    
    # 检查后端依赖
    backend_req = BASE_DIR / "requirements.txt"
    if backend_req.exists():
        print("✅ 后端依赖文件存在")
        # 检查是否已安装（检查关键包）
        try:
            import fastapi
            import multipart  # 检查 python-multipart
            print("✅ 后端Python依赖已安装")
        except ImportError:
            print("⚠️  后端Python依赖未安装，正在安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", str(backend_req)], check=True)
            print("✅ 后端Python依赖安装完成")
    else:
        print("⚠️  警告: 未找到 requirements.txt")
    
    # 检查前端依赖（仅在 Node.js 版本足够时）
    if not skip_frontend:
        frontend_node_modules = FRONTEND_DIR / "node_modules"
        if frontend_node_modules.exists():
            print("✅ 前端依赖已安装")
        else:
            print("⚠️  前端依赖未安装，正在安装...")
            subprocess.run(["npm", "install", "--legacy-peer-deps"], cwd=FRONTEND_DIR, check=True)
            print("✅ 前端依赖安装完成")
    
    print("=" * 60)
    print()


def start_backend():
    """启动后端服务"""
    print("=" * 60)
    print("启动后端服务...")
    print("=" * 60)
    
    # 检查端口是否被占用
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()
        if result == 0:
            print("⚠️  端口 8000 已被占用，正在清理旧进程...")
            # 查找并杀死占用端口的进程
            try:
                import subprocess as sp
                old_pids = sp.check_output(["lsof", "-ti", ":8000"], text=True).strip().split('\n')
                for pid in old_pids:
                    if pid:
                        try:
                            sp.run(["kill", pid], check=False, timeout=2)
                            time.sleep(1)
                            # 如果还没死，强制杀死
                            try:
                                sp.run(["kill", "-0", pid], check=True, timeout=1)
                                sp.run(["kill", "-9", pid], check=False, timeout=1)
                            except:
                                pass
                        except:
                            pass
                print("✅ 已清理旧进程")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️  清理旧进程时出错: {e}")
    except Exception as e:
        print(f"⚠️  检查端口时出错: {e}")
    
    os.chdir(BACKEND_DIR)
    
    # 清空日志文件
    log_file = BASE_DIR / "backend.log"
    if log_file.exists():
        log_file.write_text("")
    
    # 启动后端
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    processes.append(backend_process)
    
    # 等待后端启动（增加等待时间和重试次数）
    print("等待后端服务启动...")
    backend_started = False
    for i in range(10):
        time.sleep(1)
        try:
            import urllib.request
            import urllib.error
            try:
                with urllib.request.urlopen("http://localhost:8000/health", timeout=2) as response:
                    if response.status == 200:
                        print("✅ 后端服务启动成功!")
                        print("   API地址: http://localhost:8000")
                        print("   API文档: http://localhost:8000/docs")
                        backend_started = True
                        break
            except urllib.error.URLError:
                if i < 9:
                    continue
        except Exception:
            if i < 9:
                continue
    
    if not backend_started:
        print("⚠️  后端服务启动超时，请检查日志 (backend.log)")
        try:
            if log_file.exists():
                log_content = log_file.read_text()
                if log_content:
                    print("最后几行日志：")
                    print('\n'.join(log_content.split('\n')[-5:]))
        except Exception:
            pass
    
    print()
    return backend_process


def start_frontend():
    """启动前端服务"""
    print("=" * 60)
    print("启动前端服务...")
    print("=" * 60)
    
    # 清理可能占用 3000 端口的旧进程
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 3000))
        sock.close()
        if result == 0:
            print("⚠️  端口 3000 被占用，正在清理...")
            try:
                import subprocess as sp
                old_pids = sp.check_output(["lsof", "-ti", ":3000"], text=True).strip().split('\n')
                for pid in old_pids:
                    if pid:
                        try:
                            sp.run(["kill", pid], check=False, timeout=2)
                            time.sleep(1)
                            sp.run(["kill", "-9", pid], check=False, timeout=1)
                        except:
                            pass
                print("✅ 已清理旧进程")
                time.sleep(2)
            except Exception as e:
                print(f"⚠️  清理旧进程时出错: {e}")
    except Exception:
        pass
    
    os.chdir(FRONTEND_DIR)
    
    # 清空日志文件
    log_file = BASE_DIR / "frontend.log"
    if log_file.exists():
        log_file.write_text("")
    
    # 启动前端
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )
    
    processes.append(frontend_process)
    
    # 等待前端启动并检测实际端口
    print("等待前端服务启动...")
    frontend_port = 3000
    for i in range(10):
        time.sleep(1)
        # 从日志中提取端口号
        if log_file.exists():
            try:
                log_content = log_file.read_text()
                import re
                # 查找 "Local: http://localhost:PORT" 模式
                match = re.search(r'Local:\s+http://localhost:(\d+)', log_content)
                if match:
                    frontend_port = int(match.group(1))
                    break
            except:
                pass
        # 或者检查端口是否在监听
        try:
            import socket
            for port in [3000, 3001, 3002]:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('localhost', port))
                sock.close()
                if result == 0:
                    frontend_port = port
                    break
            if frontend_port:
                break
        except:
            pass
    
    print(f"✅ 前端服务启动成功!")
    print(f"   前端地址: http://localhost:{frontend_port}")
    print()
    return frontend_process, frontend_port


def signal_handler(sig, frame):
    """信号处理函数，用于优雅关闭"""
    print("\n" + "=" * 60)
    print("正在关闭服务...")
    print("=" * 60)
    
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        except Exception as e:
            print(f"关闭进程时出错: {e}")
    
    print("✅ 所有服务已关闭")
    sys.exit(0)


def main():
    """主函数"""
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("=" * 60)
    print("DeepInsight Platform - 一键启动")
    print("=" * 60)
    print()
    
    # 检查依赖
    skip_frontend = check_dependencies()
    
    # 启动后端
    backend_process = start_backend()
    
    # 启动前端（如果 Node.js 版本足够）
    frontend_process = None
    frontend_port = 3000
    if not skip_frontend:
        frontend_process, frontend_port = start_frontend()
    else:
        print("⚠️  跳过前端启动（Node.js 版本过低）")
        print()
    
    # 打印启动信息
    print("=" * 60)
    print("✅ 服务启动完成!")
    print("=" * 60)
    print()
    print("访问地址:")
    if not skip_frontend:
        print(f"  前端: http://localhost:{frontend_port}")
    print("  后端API: http://localhost:8000")
    print("  API文档: http://localhost:8000/docs")
    print()
    if skip_frontend:
        print("注意: 前端服务未启动（Node.js 版本过低）")
        print("      仅后端服务正在运行")
        print()
    print("按 Ctrl+C 停止所有服务")
    print("=" * 60)
    print()
    
    # 尝试自动打开浏览器（如果支持）
    if not skip_frontend:
        time.sleep(2)  # 等待前端完全启动
        try:
            import webbrowser
            frontend_url = f'http://localhost:{frontend_port}'
            webbrowser.open(frontend_url)
            print(f"✅ 已尝试在浏览器中打开前端页面: {frontend_url}")
        except Exception:
            print(f"💡 提示: 请在浏览器中访问 http://localhost:{frontend_port}")
        print()
    
    # 实时输出日志
    try:
        while True:
            # 检查进程是否还在运行
            if backend_process.poll() is not None:
                print("❌ 后端服务已停止")
                break
            if frontend_process and frontend_process.poll() is not None:
                print("❌ 前端服务已停止")
                break
            
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    signal_handler(None, None)


if __name__ == "__main__":
    main()

