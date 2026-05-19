# AI智能简历分析系统

一个基于AI的智能简历分析系统，支持PDF简历上传、信息提取、岗位匹配和评分功能。
<video src="[movie.mp4.mp4](https://github.com/user-attachments/assets/bca09fec-3cd9-474e-aaba-83189ac39451)" controls="controls" width="500" height="300"></video>

## 功能特性

### 模块一：简历上传与解析
- 支持上传单个PDF格式的简历文件
- 解析PDF内容，提取文本信息（兼容多页简历）
- 对提取文本进行清洗和结构化处理

### 模块二：关键信息提取
- 基本信息：姓名、电话、邮箱、地址
- 求职信息：求职意向、期望薪资
- 背景信息：工作年限、学历背景、项目经历

### 模块三：简历评分与匹配
- 提供接口接收招聘岗位的需求描述
- 对岗位需求进行关键词提取和分析
- 将解析后的简历信息与岗位需求进行匹配
- 计算匹配度评分（技能匹配率、工作经验相关性等）

### 模块四：结果返回与缓存
- JSON格式结构化返回解析结果、关键信息和匹配度评分
- Redis缓存机制，避免重复计算

### 模块五：前端页面
- 简洁易用的交互界面
- 支持简历上传和岗位匹配

## 技术栈

### 后端
- Python 3.x
- FastAPI
- PyPDF2
- OpenAI API（兼容格式）
- Redis

### 前端
- HTML5
- CSS3
- JavaScript
- Tailwind CSS

## 快速开始

### 本地运行

1. 克隆仓库
```bash
git clone <your-repo-url>
cd <your-repo-name>
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

4. 启动Redis（可选）
```bash
# Windows: 使用Docker或下载Redis
# Docker: docker run -d -p 6379:6379 redis
```

5. 启动后端服务
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

6. 访问前端页面
- 浏览器打开: http://localhost:8000

## 部署指南

### GitHub Pages部署（前端）

1. 将 `frontend` 文件夹的内容复制到仓库根目录或 `gh-pages` 分支
2. 打开 GitHub 仓库页面
3. 进入 Settings → Pages
4. 选择源分支（如 `main` 或 `gh-pages`）
5. 选择文件夹（如 `/ (root)` 或 `/frontend`）
6. 点击 Save，等待部署完成

### 后端部署（推荐）

由于GitHub Pages只能托管静态文件，后端需要部署到以下平台之一：

#### 阿里云函数计算
1. 安装 Serverless Devs
2. 配置 Serverless.yml
3. 部署到阿里云函数计算

#### Vercel / Railway
1. 连接 GitHub 仓库
2. 配置环境变量
3. 一键部署

#### 传统服务器
1. 配置 Nginx 反向代理
2. 使用 Gunicorn + Uvicorn 部署
3. 配置 Redis 服务

## 项目结构

```
.
├── app/
│   ├── main.py              # FastAPI主入口
│   ├── config.py            # 配置文件
│   ├── routes/
│   │   ├── resume.py        # 简历相关接口
│   │   └── job_matching.py  # 岗位匹配接口
│   ├── schemas/
│   │   └── resume.py        # 数据模型定义
│   └── utils/
│       ├── pdf_parser.py    # PDF解析工具
│       ├── ai_client.py     # AI客户端
│       └── cache.py         # Redis缓存管理
├── frontend/
│   └── index.html           # 前端页面
├── temp/                    # 临时文件目录
├── .env                     # 环境变量配置
├── .gitignore
├── requirements.txt
└── README.md
```

## API文档

启动服务后访问：http://localhost:8000/docs

### 主要接口

#### 上传简历
```
POST /api/resume/upload
Content-Type: multipart/form-data

Response: ResumeParseResult (JSON)
```

#### 获取简历详情
```
GET /api/resume/{resume_id}
Response: ResumeParseResult (JSON)
```

#### 岗位匹配评分
```
POST /api/match/score
Content-Type: application/json

{
  "resume_id": "xxx",
  "job_description": "..."
}

Response: ResumeMatchResult (JSON)
```

## 环境变量配置

```env
# AI API配置（兼容OpenAI格式）
AI_API_KEY=your_api_key_here
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-3.5-turbo

# Redis配置（可选）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
CACHE_EXPIRE=86400
```

## 演示示例

1. 使用 `sample_resume.html` 创建PDF简历
2. 上传到系统
3. 输入岗位需求：
```
职位：Python后端开发工程师
要求：本科及以上学历，计算机相关专业，熟悉Python、SQL、Redis
```

## 注意事项

- 免费API有Token限制，长简历可能导致AI匹配失败
- 当AI失败时，系统会自动回退到简单匹配算法
- Redis为可选功能，不影响核心功能使用
-前端部署链接：https://cw-wr.github.io/ai-resume-analyzer/
github page部署的静态网站，仅供参考
<img width="2254" height="1354" alt="image" src="https://github.com/user-attachments/assets/130322b8-e844-4263-8495-d8eb1af29952" />

## 许可证

MIT License
