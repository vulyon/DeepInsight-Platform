# DeepInsight Platform 后端

基于LSTM的电商产品分析可视化Web平台后端服务

## 项目结构

```
backend/
├── app.py                 # FastAPI主应用
├── config.py              # 配置文件
├── requirements.txt       # Python依赖
├── models/
│   └── lstm_model.py      # LSTM模型加载和预测
├── services/
│   ├── data_processor.py  # 数据预处理服务
│   ├── sentiment_analyzer.py  # 情感分析服务
│   └── visualizer.py      # 可视化数据生成
├── api/
│   ├── upload.py          # 文件上传接口
│   ├── analyze.py         # 分析接口
│   └── results.py         # 结果查询接口
└── utils/
    └── file_handler.py    # 文件处理工具
```

## 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

## 配置说明

在 `config.py` 中可以配置：
- 数据文件路径
- 模型文件路径
- 词云字体路径（根据操作系统调整）
- API前缀等

## 运行服务

### 方式1：直接运行

```bash
cd backend
python app.py
```

### 方式2：使用uvicorn

```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

服务启动后，访问：
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

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

## 注意事项

1. **模型文件**: 需要训练好的LSTM模型文件 `models/sentiment_lstm.h5` 和 `models/tokenizer.pkl`
   - 如果模型文件不存在，系统会创建占位模型（仅用于测试）
   - 实际使用时需要训练或加载训练好的模型

2. **字体文件**: 词云图生成需要中文字体
   - Linux: `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf` 或安装中文字体
   - Windows: `C:/Windows/Fonts/simsun.ttc`
   - macOS: `/System/Library/Fonts/PingFang.ttc`

3. **数据文件**: 确保 `demo/数据集/` 目录下有以下文件：
   - `正面评价词语（中文）.txt`
   - `负面评价词语（中文）.txt`
   - `正面情感词语（中文）.txt` (可选)
   - `负面情感词语（中文）.txt` (可选)
   - `stoplist.txt`
   - `not.csv`

## 开发说明

- 使用FastAPI框架，支持自动API文档生成
- 支持CORS跨域请求
- 分析结果保存在 `backend/results/` 目录
- 上传文件保存在 `backend/uploads/` 目录

