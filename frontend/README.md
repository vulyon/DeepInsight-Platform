# DeepInsight Frontend

基于React + Ant Design + ECharts的电商产品分析可视化前端应用。

## 技术栈

- **React 18** - UI框架
- **Ant Design 5** - UI组件库
- **ECharts 5** - 数据可视化
- **React Router 6** - 路由管理
- **Axios** - HTTP客户端
- **Vite** - 构建工具

## 功能特性

- 📤 **文件上传** - 支持CSV格式评论数据上传
- 📊 **数据可视化** - 词云图、饼图、热力图等多种图表展示
- 📈 **统计分析** - 情感分布统计、模型准确率等
- 📝 **评论列表** - 支持分页、筛选、排序的评论列表展示
- 🎨 **美观界面** - 现代化的UI设计，响应式布局

## 安装依赖

```bash
cd frontend
npm install
```

## 开发运行

```bash
npm run dev
```

前端将在 `http://localhost:3000` 启动。

**注意**：确保后端服务运行在 `http://localhost:8000`，或者修改 `vite.config.js` 中的代理配置。

## 构建生产版本

```bash
npm run build
```

构建产物将输出到 `dist` 目录。

## 项目结构

```
frontend/
├── src/
│   ├── pages/           # 页面组件
│   │   ├── UploadPage.jsx      # 上传页面
│   │   └── AnalysisPage.jsx    # 分析结果页面
│   ├── components/       # 通用组件
│   │   ├── StatisticsCards.jsx # 统计卡片
│   │   ├── WordCloudChart.jsx  # 词云图
│   │   ├── PieChart.jsx        # 饼图
│   │   ├── HeatmapChart.jsx    # 热力图
│   │   └── ReviewList.jsx      # 评论列表
│   ├── services/        # API服务
│   │   └── api.js       # API封装
│   ├── App.jsx          # 主应用组件
│   └── main.jsx         # 入口文件
├── package.json
└── vite.config.js       # Vite配置
```

## API接口

前端通过以下API与后端交互：

- `POST /api/upload` - 上传CSV文件
- `POST /api/analyze` - 开始分析
- `GET /api/results/{task_id}` - 获取分析结果
- `GET /api/results/{task_id}/reviews` - 获取评论列表

## 页面说明

### 上传页面 (`/upload`)

- 支持拖拽上传CSV文件
- 文件格式验证
- 上传后自动开始分析

### 分析结果页面 (`/analysis/:taskId`)

- **统计卡片**：总评论数、正面/负面评论数、模型准确率
- **词云图**：正面和负面评论的词云可视化
- **饼图**：情感分布比例
- **热力图**：混淆矩阵可视化
- **评论列表**：支持分页、筛选、排序

## 注意事项

1. 确保后端API服务正常运行
2. 后端需要配置CORS允许前端域名访问
3. 词云图需要后端返回base64格式的图片数据

