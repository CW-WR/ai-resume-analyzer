# 部署指南

## 1. 前置准备

### 1.1 创建GitHub账户
- 访问 https://github.com
- 注册或登录你的GitHub账户

### 1.2 安装Git
- 下载安装: https://git-scm.com/downloads
- 验证安装: `git --version`

## 2. 上传项目到GitHub

### 2.1 创建新仓库
1. 登录 GitHub
2. 点击右上角 "+" → "New repository"
3. 仓库名: `ai-resume-analyzer` (或其他你喜欢的名字)
4. 选择 Public/Private (建议Public)
5. **不要**勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

### 2.2 推送本地代码
在你的项目目录下执行：

```bash
# 初始化Git仓库（已完成）
# git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: AI resume analyzer system"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/ai-resume-analyzer.git

# 推送到main分支
git branch -M main
git push -u origin main
```

如果第一次使用Git，需要先配置用户信息：
```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

## 3. GitHub Pages部署（前端）

### 3.1 方法一：使用gh-pages分支（推荐）

```bash
# 创建并切换到gh-pages分支
git checkout -b gh-pages

# 将frontend文件夹的内容复制到根目录
# 在Windows PowerShell中执行:
Copy-Item -Path frontend\* -Destination . -Recurse

# 添加并提交
git add .
git commit -m "Deploy frontend to GitHub Pages"

# 推送到gh-pages分支
git push -u origin gh-pages

# 切回main分支继续开发
git checkout main
```

### 3.2 方法二：使用main分支的frontend文件夹

1. 确保frontend文件夹已推送到main分支
2. 进入仓库 Settings → Pages
3. 在 "Build and deployment" 部分:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/frontend`
4. 点击 Save

### 3.3 启用GitHub Pages

1. 打开你的GitHub仓库页面
2. 点击 "Settings" 标签
3. 在左侧菜单找到 "Pages" (在 "Code and automation" 下)
4. 在 "Build and deployment" 部分:
   - Source: `Deploy from a branch`
   - Branch: `gh-pages` (或 `main`)
   - Folder: `/ (root)` (或 `/frontend`)
5. 点击 "Save"
6. 等待1-2分钟，页面上方会显示: "Your site is live at https://你的用户名.github.io/ai-resume-analyzer/"

## 4. 后端部署

由于GitHub Pages只能托管静态文件，后端API需要部署到其他平台：

### 4.1 阿里云函数计算（推荐）

#### 4.1.1 安装Serverless Devs
```bash
npm install -g @serverless-devs/s
```

#### 4.1.2 配置s.yaml
创建 `s.yaml` 文件:
```yaml
edition: 3.0.0
name: ai-resume-analyzer
access: default

services:
  resume-analyzer:
    component: fc3
    props:
      region: cn-hangzhou
      description: AI Resume Analyzer
      functionName: resume-analyzer
      runtime: python3.10
      handler: index.handler
      code: ./
      environmentVariables:
        AI_API_KEY: your_api_key
        AI_BASE_URL: https://api.chatanywhere.tech/v1
      instanceConcurrency: 10
      memorySize: 512
      timeout: 30
      triggers:
        - triggerName: httpTrigger
          triggerType: http
          description: HTTP trigger
          qualifier: LATEST
          triggerConfig:
            authType: anonymous
            methods:
              - GET
              - POST
```

#### 4.1.3 部署
```bash
s deploy
```

### 4.2 Vercel部署（简单快捷）

1. 访问 https://vercel.com
2. 使用GitHub账户登录
3. 点击 "Add New" → "Project"
4. 选择你的仓库
5. 配置环境变量:
   - `AI_API_KEY`: 你的API密钥
   - `AI_BASE_URL`: https://api.chatanywhere.tech/v1
6. 点击 "Deploy"

### 4.3 Railway部署

1. 访问 https://railway.app
2. 登录并连接GitHub
3. 点击 "New Project" → "Deploy from repo"
4. 选择你的仓库
5. 配置环境变量
6. 部署

## 5. 更新前端API地址

部署后端后，需要更新前端的API地址：

编辑 `frontend/index.html`，找到:
```javascript
const API_BASE = '/api';
```

修改为你的后端地址:
```javascript
// 例如部署到Vercel
const API_BASE = 'https://your-backend.vercel.app/api';

// 或者部署到阿里云函数计算
const API_BASE = 'https://xxx.cn-hangzhou.fc.aliyuncs.com/api';
```

## 6. 常见问题

### 6.1 GitHub Pages不更新
- 等待5-10分钟，GitHub Pages需要时间构建
- 检查仓库 Settings → Pages 中的部署状态
- 尝试重新推送代码

### 6.2 CORS跨域问题
- 确保后端已正确配置CORS
- 本项目已在 `app/main.py` 中配置了CORS

### 6.3 API调用失败
- 检查环境变量是否正确配置
- 查看后端日志
- 确认API密钥有效且有足够配额

## 7. 项目演示

部署完成后，你可以:

1. 访问前端页面: https://你的用户名.github.io/ai-resume-analyzer/
2. 下载示例简历: 使用 `sample_resume.html` 生成PDF
3. 测试功能: 上传简历并输入岗位需求

## 8. 持续部署

每次推送到main分支时，可以配置自动部署：

### GitHub Actions (可选)
创建 `.github/workflows/deploy.yml`:
```yaml
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend
```
