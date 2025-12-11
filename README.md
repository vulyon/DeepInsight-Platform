# DeepInsight Platform

基于LSTM的电商产品分析可视化Web平台

## 项目简介

DeepInsight Platform 是一个基于深度学习的电商产品评论情感分析可视化平台。系统使用LSTM模型对评论进行情感分类（正面/负面），并提供丰富的可视化展示，包括词云图、饼图、热力图等。

## 技术栈

### 后端
- **FastAPI** - 现代、快速的Web框架
- **TensorFlow/Keras** - LSTM深度学习模型
- **pandas/numpy** - 数据处理
- **jieba** - 中文分词
- **WordCloud** - 词云图生成
- **matplotlib/seaborn** - 数据可视化

### 前端
- **React 18** - UI框架
- **Ant Design 5** - UI组件库
- **ECharts 5** - 数据可视化
- **React Router 6** - 路由管理
- **Axios** - HTTP客户端
- **Vite** - 构建工具

## 项目结构

```
DeepInsight-Platform/
├── backend/              # 后端服务
│   ├── app.py           # FastAPI主应用
│   ├── config.py        # 配置文件
│   ├── requirements.txt # Python依赖
│   ├── run.sh          # 启动脚本
│   ├── api/            # API路由
│   ├── models/         # LSTM模型
│   ├── services/       # 业务逻辑服务
│   └── utils/          # 工具函数
├── frontend/            # 前端应用
│   ├── src/            # 源代码
│   ├── package.json    # 前端依赖
│   └── vite.config.js  # Vite配置
├── demo/               # 示例代码和数据
│   └── 数据集/         # 词典和停用词文件
├── docs/               # 文档
│   └── design.md       # 设计文档
└── README.md           # 本文件
```

## 环境要求

### 后端环境
- Python 3.8+
- pip

### 前端环境
- **Node.js 14.18+ 或 16+（必需，推荐 16+）**
- npm 或 yarn

**重要**：Node.js 版本必须 >= 14.18，否则前端无法启动。

**升级 Node.js（如果版本过低）：**

**方法1：使用 NodeSource 仓库（Ubuntu/Debian，推荐）**
```bash
# 添加 NodeSource 仓库
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -

# 如果有旧版本冲突，先卸载
sudo apt remove -y libnode72 libnode-dev nodejs-doc nodejs
sudo apt autoremove -y

# 安装 Node.js 16
sudo apt install -y nodejs

# 验证版本
node --version  # 应该显示 v16.x.x
```

**方法2：使用 nvm（推荐用于多版本管理）**
```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc

# 安装并使用 Node.js 16
nvm install 16
nvm use 16

# 验证版本
node --version
```

**详细升级指南：** 查看 [UPGRADE_NODEJS.md](UPGRADE_NODEJS.md)

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd DeepInsight-Platform
```

### 2. 安装后端依赖

```bash
# 在项目根目录
pip install -r requirements.txt
```

**注意**：
- 如果安装TensorFlow遇到问题，可以尝试：
  ```bash
  pip install tensorflow==2.15.0 --no-cache-dir
  ```
- 如果使用 Python 3.12，某些包可能不兼容，建议使用 Python 3.10 或 3.11
- 确保 `python-multipart` 已安装（FastAPI 文件上传需要）：
  ```bash
  pip install python-multipart
  ```

### 3. 安装前端依赖

```bash
cd ../frontend
npm install
```

### 4. 配置检查

#### 后端配置

检查 `backend/config.py` 中的配置，特别是：

- **字体路径**：词云图生成需要中文字体
  - Linux: `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` 或安装中文字体
  - Windows: `C:/Windows/Fonts/simsun.ttc`
  - macOS: `/System/Library/Fonts/PingFang.ttc`

- **数据文件**：确保 `demo/数据集/` 目录下有以下文件：
  - `正面评价词语（中文）.txt`
  - `负面评价词语（中文）.txt`
  - `stoplist.txt` - 停用词表
  - `not.csv` - 否定词表

- **模型文件**（可选）：
  - `backend/models/sentiment_lstm.h5` - LSTM模型
  - `backend/models/tokenizer.pkl` - 文本序列化器
  - 如果模型文件不存在，系统会创建占位模型（仅用于测试）

#### 前端配置

前端默认配置在 `frontend/vite.config.js`：
- 开发服务器端口：`3000`
- API代理：`http://localhost:8000`

如需修改，请编辑 `vite.config.js`。

## 启动项目

### 方式一：一键启动（推荐）

使用一键启动脚本同时启动前后端服务：

**方法1：使用Shell脚本（Linux/macOS）**
```bash
chmod +x start.sh
./start.sh
```

**方法2：使用Python脚本（跨平台）**
```bash
chmod +x start.py
python3 start.py
# 或
./start.py
```

一键启动脚本会自动：
- ✅ 检查Python、Node.js、npm环境
- ✅ 检查并安装后端依赖（如果需要）
- ✅ 检查并安装前端依赖（如果需要）
- ✅ 启动后端服务（端口8000）
- ✅ 启动前端服务（端口3000）
- ✅ 显示服务访问地址

启动成功后：
- 前端地址：`http://localhost:3000`
- 后端API：`http://localhost:8000`
- API文档：`http://localhost:8000/docs`

按 `Ctrl+C` 可同时停止所有服务。

**停止服务：**
```bash
# 使用停止脚本
./stop.sh

# 或手动停止
pkill -f "uvicorn app:app"
pkill -f "vite"
```

### 方式二：分别启动（开发环境）

#### 启动后端服务

**方法1：使用启动脚本（Linux/macOS）**
```bash
chmod +x run.sh
./run.sh
```

**方法2：直接运行**
```bash
cd backend
python3 app.py
```

**方法3：使用uvicorn**
```bash
cd backend
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

后端服务启动后：
- API服务地址：`http://localhost:8000`
- API文档（Swagger）：`http://localhost:8000/docs`
- 健康检查：`http://localhost:8000/health`

#### 启动前端服务

打开新的终端窗口：

```bash
cd frontend
npm run dev
```

前端服务启动后：
- 前端地址：`http://localhost:3000`

## 使用流程

1. **访问前端页面**
   - 打开浏览器访问 `http://localhost:3000`

2. **上传数据文件**
   - 在上传页面选择或拖拽CSV文件
   - CSV文件格式需包含以下列：
     ```csv
     content,content_type
     "这个产品很好用",pos
     "质量太差了",neg
     ```

3. **开始分析**
   - 点击"上传并开始分析"
   - 系统会自动进行数据预处理、情感分析和可视化数据生成

4. **查看结果**
   - 分析完成后自动跳转到结果页面
   - 查看统计卡片、词云图、饼图、热力图和评论列表

## API接口

### 1. 文件上传
```
POST /api/upload
Content-Type: multipart/form-data
Body: file (CSV文件)
```

### 2. 开始分析
```
POST /api/analyze
Content-Type: application/json
Body: {"file_id": "uuid"}
```

### 3. 获取分析结果
```
GET /api/results/{task_id}
```

### 4. 获取评论列表
```
GET /api/results/{task_id}/reviews?sentiment=positive&page=1&page_size=20
```

详细API文档请访问：`http://localhost:8000/docs`

## 构建生产版本

### 构建前端

```bash
cd frontend
npm run build
```

构建产物将输出到 `frontend/dist` 目录。

### 部署后端

生产环境建议使用：
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

或使用 Gunicorn + Uvicorn：
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 常见问题

### 1. 后端启动失败

- **问题**：缺少依赖包（如 `python-multipart`、`jieba`、`tensorflow`）
  - **解决**：确保已安装所有依赖 `pip install -r requirements.txt`
  - 如果遇到版本冲突，可以尝试：`pip install python-multipart jieba fastapi uvicorn pandas numpy`

- **问题**：`python-multipart` 未安装
  - **错误信息**：`Form data requires "python-multipart" to be installed`
  - **解决**：`pip install python-multipart`

- **问题**：Python 版本兼容性问题
  - **解决**：推荐使用 Python 3.10 或 3.11，Python 3.12 可能不兼容某些旧版本包

- **问题**：端口被占用
  - **解决**：修改 `app.py` 中的端口号，或使用 `--port` 参数指定其他端口

- **问题**：模型文件不存在
  - **解决**：系统会自动创建占位模型，但实际使用时需要训练或加载训练好的模型

### 2. 前端启动失败

- **问题**：Node.js版本过低
  - **错误信息**：`SyntaxError: Unexpected reserved word`
  - **解决**：升级到 Node.js 14.18+ 或 16+（推荐 16+）
  - 使用 nvm 升级：
    ```bash
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    source ~/.bashrc
    nvm install 16
    nvm use 16
    ```

- **问题**：依赖安装失败
  - **解决**：尝试清除缓存后重新安装
    ```bash
    cd frontend
    rm -rf node_modules package-lock.json
    npm install --legacy-peer-deps
    ```

### 3. 词云图无法显示

- **问题**：字体文件路径不正确
  - **解决**：检查 `backend/config.py` 中的 `FONT_PATH` 配置，确保字体文件存在

### 4. 分析结果不准确

- **问题**：使用占位模型
  - **解决**：需要训练或加载训练好的LSTM模型文件

## 开发说明

- 后端使用FastAPI框架，支持自动API文档生成
- 支持CORS跨域请求
- 分析结果保存在 `backend/results/` 目录
- 上传文件保存在 `backend/uploads/` 目录
- 开发模式下，后端支持热重载（`--reload`）

## 更多文档

- [设计文档](docs/design.md) - 详细的系统设计说明
- [后端README](backend/README.md) - 后端详细文档
- [前端README](frontend/README.md) - 前端详细文档
- [故障排除指南](TROUBLESHOOTING.md) - 常见问题及解决方案

## 许可证

[根据实际情况填写]

## 贡献

欢迎提交Issue和Pull Request！

