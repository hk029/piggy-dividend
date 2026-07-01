# 小猪股息罐 🐷

股息投资追踪小程序，让每一笔分红都稳稳落袋。

## 技术栈

- **前端**: Taro 3 + React + TypeScript + Sass
- **后端**: Python FastAPI + Uvicorn

## 项目结构

```
piggy-dividend/
├── miniprogram/           # Taro 前端
│   ├── src/
│   │   ├── layouts/       # 布局组件
│   │   ├── pages/         # 页面
│   │   └── styles/        # 样式变量
│   └── config/            # 构建配置
├── server/                # Python FastAPI 后端
│   ├── main.py
│   └── requirements.txt
└── docs/                  # 项目文档
```

## 快速开始

### 前端开发

```bash
cd miniprogram
npm install
npm run dev:weapp
```

### 后端开发

```bash
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

后端启动后访问: http://localhost:8080/docs (Swagger UI)

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/health | 健康检查 |
| GET | /api/hello | Hello World |
| POST | /api/hello | Hello World (带参数) |
