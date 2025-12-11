# 电商产品评论情感分析系统

## 项目简介

这是一个基于Flask框架开发的电商产品评论情感分析Web应用系统。系统可以对电商平台的用户评论进行情感分析，展示评论列表、情感统计分布、词云分析等功能。

## 技术栈

- **后端框架**: Flask 1.1.2
- **数据库**: SQLite
- **前端**: Bootstrap, ECharts, jQuery
- **数据分析**: Pandas, Jieba, WordCloud, Scikit-learn
- **可视化**: Matplotlib, Seaborn

## 项目结构

```
sentiment_analysis_web/
├── app.py              # Flask主应用文件
├── init_db.py          # 数据库初始化脚本
├── requirements.txt    # 依赖包列表
├── reviews.db          # SQLite数据库（运行init_db.py后生成）
├── data/               # 数据文件目录
│   └── reviews.csv     # 评论数据CSV文件
├── templates/          # HTML模板目录
│   ├── index.html      # 首页
│   ├── reviews.html    # 评论列表页
│   ├── sentiment.html  # 情感统计页
│   ├── cloud.html      # 词云分析页
│   └── about.html      # 关于页面
└── static/             # 静态资源目录
    └── assets/         # CSS、JS、图片等资源
```

## 安装步骤

1. **克隆或下载项目**

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **复制数据文件（如果还没有）**
   ```bash
   python copy_data.py
   ```
   这将从 `demo/数据集` 复制数据文件到 `data/` 目录。

4. **初始化数据库**
   ```bash
   python init_db.py
   ```
   这将从 `data/reviews.csv` 导入评论数据到SQLite数据库。

5. **生成词云图片（可选）**
   ```bash
   python generate_wordcloud.py
   ```
   这将生成正面和负面评论的词云图片，保存到 `static/assets/img/` 目录。

6. **运行应用**
   ```bash
   python app.py
   ```

7. **访问系统**
   打开浏览器访问: http://localhost:5000

## 功能说明

### 1. 首页
- 显示系统概览和统计信息
- 提供导航链接到各个功能模块

### 2. 评论列表
- 展示所有评论数据
- 显示评论内容、情感类型、评论时间等信息
- 支持分页显示（默认显示前500条）

### 3. 情感统计
- 使用ECharts饼图展示正面/负面评论分布
- 显示详细的统计数字

### 4. 词云分析
- 展示正面评论和负面评论的词云图
- 直观显示高频关键词

### 5. 关于页面
- 系统介绍和技术说明

## 数据格式

CSV文件应包含以下列：
- `content`: 评论内容
- `creationTime`: 评论时间
- `nickname`: 用户昵称
- `referenceName`: 产品名称
- `content_type`: 情感类型（pos/neg）

## 注意事项

1. 确保 `data/reviews.csv` 文件存在且格式正确
2. 首次运行前需要执行 `init_db.py` 初始化数据库
3. 词云图片需要预先生成，或通过运行demo中的情感分析脚本生成

## 开发说明

本项目基于lstm的评论情感分析系统。

## 许可证

本项目仅供学习和研究使用。
