# 基于LSTM的电商产品分析可视化Web平台设计文档

## 1. 项目概述

### 1.1 项目背景
基于demo目录下的LSTM情感分析代码，开发一个Web可视化展示平台。将现有的Python脚本功能转换为Web应用，提供友好的可视化界面展示分析结果。

### 1.2 核心功能
- **数据上传**：支持上传CSV格式的评论数据
- **情感分析**：基于LSTM模型对评论进行情感分类（正面/负面）
- **数据可视化**：词云图、饼图、热力图、混淆矩阵等图表展示
- **结果展示**：分析结果统计和评论列表展示

## 2. 系统架构

### 2.1 简化架构
```
┌─────────────────────────────────┐
│      前端 (React/Vue)           │
│  - 数据上传页面                  │
│  - 可视化展示页面                │
│  - 图表组件 (ECharts)            │
└─────────────────────────────────┘
              ↕ HTTP API
┌─────────────────────────────────┐
│    后端 (Flask/FastAPI)         │
│  - 文件上传接口                  │
│  - 数据分析接口                  │
│  - 图表数据接口                  │
└─────────────────────────────────┘
              ↕
┌─────────────────────────────────┐
│    分析服务 (基于demo代码)        │
│  - 文本预处理                    │
│  - LSTM情感分析                  │
│  - 可视化数据生成                │
└─────────────────────────────────┘
```

### 2.2 技术栈

#### 前端
- **框架**：React 18+ 或 Vue 3+
- **UI组件**：Ant Design 或 Element Plus
- **可视化库**：ECharts（词云、饼图、热力图）
- **HTTP客户端**：Axios

#### 后端
- **Web框架**：Flask 或 FastAPI
- **数据处理**：pandas, numpy
- **深度学习**：TensorFlow/Keras (LSTM模型)
- **文本处理**：jieba (中文分词)
- **可视化生成**：matplotlib, seaborn (服务端生成图片)

## 3. 功能模块设计

### 3.1 数据上传模块

#### 3.1.1 数据格式
基于demo代码，支持CSV格式，包含以下字段：
```csv
content,content_type
"这个产品很好用",pos
"质量太差了",neg
```

#### 3.1.2 上传流程
1. 用户上传CSV文件
2. 后端验证文件格式
3. 保存到临时目录
4. 返回文件ID用于后续分析

### 3.2 情感分析模块

#### 3.2.1 分析流程（基于demo/情感分析.py）
1. **数据预处理**
   - 数据去重
   - 去除英文、数字、特定品牌词
   - jieba分词和词性标注
   - 去除停用词和标点符号

2. **情感词典分析**
   - 加载正面/负面情感词典
   - 匹配情感词并计算情感值
   - 处理否定词修正

3. **LSTM模型分析**
   - 文本序列化
   - LSTM模型预测
   - 输出正面/负面概率

#### 3.2.2 LSTM模型结构（基于demo代码）
```python
模型架构：
- Embedding层 (10000词汇, 128维)
- LSTM层 (128单元, dropout=0.2)
- Dense层 (2输出, softmax激活)
```

### 3.3 可视化模块

#### 3.3.1 词云图
- **正面评论词云**：展示正面评论中的高频词
- **负面评论词云**：展示负面评论中的高频词
- **实现方式**：
  - 后端使用WordCloud生成图片，返回base64或URL
  - 前端使用ECharts-wordcloud组件展示

#### 3.3.2 情感分布饼图
- 展示正面/负面评论的比例
- 使用ECharts饼图组件

#### 3.3.3 混淆矩阵热力图
- 展示模型预测准确率
- 使用ECharts热力图组件

#### 3.3.4 统计卡片
- 总评论数
- 正面评论数/比例
- 负面评论数/比例
- 模型准确率

## 4. API设计

### 4.1 文件上传
```
POST /api/upload
Content-Type: multipart/form-data

Request:
  file: CSV文件

Response:
{
  "file_id": "uuid",
  "message": "上传成功"
}
```

### 4.2 开始分析
```
POST /api/analyze
Content-Type: application/json

Request:
{
  "file_id": "uuid"
}

Response:
{
  "task_id": "uuid",
  "status": "processing"
}
```

### 4.3 获取分析结果
```
GET /api/results/{task_id}

Response:
{
  "status": "completed",
  "statistics": {
    "total": 2000,
    "positive": 1500,
    "negative": 500,
    "positive_rate": 0.75,
    "accuracy": 0.85
  },
  "wordcloud": {
    "positive": "base64_image_url",
    "negative": "base64_image_url"
  },
  "charts": {
    "pie_data": [
      {"name": "正面", "value": 1500},
      {"name": "负面", "value": 500}
    ],
    "confusion_matrix": [
      [400, 50],
      [100, 1450]
    ]
  }
}
```

### 4.4 获取评论列表
```
GET /api/reviews/{task_id}
Query Parameters:
  sentiment: positive/negative (可选)
  page: 1
  page_size: 20

Response:
{
  "total": 2000,
  "page": 1,
  "data": [
    {
      "id": 1,
      "content": "这个产品很好用",
      "sentiment": "positive",
      "confidence": 0.95
    }
  ]
}
```

## 5. 前端页面设计

### 5.1 页面结构
```
/
├── /upload          # 数据上传页面
├── /analysis        # 分析结果展示页面
│   ├── 统计卡片
│   ├── 词云图
│   ├── 饼图
│   ├── 热力图
│   └── 评论列表
```

### 5.2 主要组件

#### 5.2.1 UploadPage (上传页面)
- 文件上传组件
- 上传进度显示
- 文件预览

#### 5.2.2 AnalysisPage (分析页面)
- **StatisticsCards**: 统计卡片组件
- **WordCloudChart**: 词云图组件
- **PieChart**: 饼图组件
- **HeatmapChart**: 热力图组件
- **ReviewList**: 评论列表组件

## 6. 代码结构

### 6.1 后端结构
```
backend/
├── app.py                 # Flask/FastAPI主应用
├── models/
│   └── lstm_model.py      # LSTM模型加载和预测
├── services/
│   ├── data_processor.py  # 数据预处理（基于demo代码）
│   ├── sentiment_analyzer.py  # 情感分析服务
│   └── visualizer.py      # 可视化数据生成
├── api/
│   ├── upload.py          # 文件上传接口
│   ├── analyze.py         # 分析接口
│   └── results.py         # 结果查询接口
└── utils/
    └── file_handler.py    # 文件处理工具
```

### 6.2 前端结构
```
frontend/
├── src/
│   ├── pages/
│   │   ├── UploadPage.jsx
│   │   └── AnalysisPage.jsx
│   ├── components/
│   │   ├── StatisticsCards.jsx
│   │   ├── WordCloudChart.jsx
│   │   ├── PieChart.jsx
│   │   ├── HeatmapChart.jsx
│   │   └── ReviewList.jsx
│   ├── services/
│   │   └── api.js          # API调用封装
│   └── App.jsx
```

## 7. 实现要点

### 7.1 基于demo代码的改造
- **数据预处理**：复用demo中的文本清洗、分词逻辑
- **情感分析**：使用demo中的LSTM模型结构
- **可视化**：将matplotlib图表转换为Web可用的数据格式

### 7.2 可视化优化
- **词云图**：
  - 后端生成图片，转换为base64或保存为文件返回URL
  - 或使用前端ECharts-wordcloud直接渲染
  
- **图表数据**：
  - 后端计算统计数据，返回JSON格式
  - 前端使用ECharts渲染交互式图表

### 7.3 性能优化
- 大文件分块上传
- 分析任务异步处理（可选）
- 结果缓存（Redis，可选）

## 8. 开发步骤

### 阶段一：后端基础功能（1周）
1. 搭建Flask/FastAPI框架
2. 实现文件上传接口
3. 集成demo中的数据处理代码
4. 实现基础分析接口

### 阶段二：LSTM模型集成（1周）
1. 加载或训练LSTM模型
2. 实现文本预处理服务
3. 实现情感分析服务
4. 测试模型预测功能

### 阶段三：可视化数据生成（1周）
1. 实现词云图生成（后端）
2. 实现统计数据计算
3. 实现图表数据接口
4. 测试API返回数据

### 阶段四：前端开发（1-2周）
1. 搭建React/Vue项目
2. 实现上传页面
3. 实现分析结果页面
4. 集成ECharts图表组件
5. 实现评论列表展示

### 阶段五：联调和优化（1周）
1. 前后端联调
2. 界面优化
3. 性能优化
4. 测试和bug修复

## 9. 数据流程

```
用户上传CSV文件
    ↓
后端保存文件
    ↓
数据预处理（去重、清洗、分词）
    ↓
情感分析（情感词典 + LSTM模型）
    ↓
生成可视化数据
    ├── 统计信息
    ├── 词云图（正面/负面）
    ├── 饼图数据
    ├── 混淆矩阵
    └── 评论列表
    ↓
返回JSON数据给前端
    ↓
前端渲染图表和列表
```

## 10. 关键技术点

### 10.1 中文分词
- 使用jieba进行中文分词
- 加载自定义停用词表
- 词性标注和筛选

### 10.2 LSTM模型
- 模型文件：`models/sentiment_lstm.h5`
- 文本序列化：Tokenizer + pad_sequences
- 批量预测优化

### 10.3 词云生成
- 使用WordCloud库生成图片
- 支持中文字体
- 正面/负面分别生成

### 10.4 前端图表
- ECharts词云图插件
- ECharts饼图
- ECharts热力图
- 响应式布局

## 11. 依赖文件

### 11.1 模型文件
- `models/sentiment_lstm.h5` - LSTM模型文件
- `models/tokenizer.pkl` - 文本序列化器

### 11.2 词典文件（基于demo）
- `正面评价词语（中文）.txt`
- `负面评价词语（中文）.txt`
- `stoplist.txt` - 停用词表
- `not.csv` - 否定词表

### 11.3 字体文件
- 中文字体文件（用于词云图）

## 12. 示例数据格式

### 输入数据 (reviews.csv)
```csv
content,content_type
"这个产品质量很好，使用方便",pos
"价格有点贵，但是质量不错",pos
"质量太差了，不推荐购买",neg
"物流很快，包装完好",pos
```

### 输出数据示例
```json
{
  "statistics": {
    "total": 4,
    "positive": 3,
    "negative": 1,
    "positive_rate": 0.75
  },
  "wordcloud": {
    "positive": "data:image/png;base64,...",
    "negative": "data:image/png;base64,..."
  }
}
```

---

## 总结

本设计文档基于demo目录下的代码，专注于将现有的Python脚本功能转换为Web可视化应用。核心是优化可视化展示，提供友好的Web界面来展示LSTM情感分析的结果。

主要特点：
- 简化架构，易于实现
- 复用demo代码逻辑
- 重点优化可视化展示
- 快速开发，快速上线
