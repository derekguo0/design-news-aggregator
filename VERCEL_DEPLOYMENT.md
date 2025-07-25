# 设计资讯聚合 - Vercel 部署指南

## 🚀 快速部署

### 1. 准备部署

确保你有以下文件：
- `vercel.json` - Vercel 配置文件
- `api/` 目录 - 包含 serverless 函数
- `output/` 目录 - 包含静态网站文件

### 2. 部署到 Vercel

#### 方法一：通过 Vercel CLI
```bash
# 安装 Vercel CLI
npm i -g vercel

# 登录 Vercel
vercel login

# 部署项目
vercel --prod
```

#### 方法二：通过 GitHub 集成
1. 将代码推送到 GitHub 仓库
2. 在 Vercel 控制台中导入 GitHub 仓库
3. Vercel 会自动检测配置并部署

### 3. 环境变量（如需要）

在 Vercel 控制台设置以下环境变量：
- 暂无特殊环境变量需求

## 📁 部署结构

```
project/
├── vercel.json          # Vercel 配置
├── api/                 # Serverless 函数
│   ├── health.py       # 健康检查
│   ├── refresh.py      # 刷新 API（静态版本）
│   └── status.py       # 状态查询
├── output/             # 静态网站文件
│   ├── index.html      # 首页
│   ├── archive.html    # 归档页
│   └── daily-*.html    # 每日页面
└── .vercelignore       # 忽略文件
```

## ⚠️ 部署限制

### 静态部署说明
- **刷新功能**：静态部署版本不支持实时刷新功能
- **内容更新**：网站内容需要通过重新生成和部署来更新
- **API 限制**：Serverless 函数有执行时间限制，不适合长时间的爬取任务

### 建议的更新流程
1. 本地运行 `python3 simple_run.py` 生成最新内容
2. 提交更改到 GitHub
3. Vercel 自动重新部署

## 🔧 自动化部署

### GitHub Actions 集成（推荐）

创建 `.github/workflows/deploy.yml`：

```yaml
name: Auto Deploy

on:
  schedule:
    - cron: '0 0,12 * * *'  # 每天 0 点和 12 点
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Generate content
      run: |
        python3 simple_run.py
    
    - name: Deploy to Vercel
      run: |
        npx vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

## 🌐 访问地址

部署完成后，您可以通过以下地址访问：
- **主域名**：`https://your-project.vercel.app`
- **API 端点**：
  - `https://your-project.vercel.app/api/health`
  - `https://your-project.vercel.app/api/status`
  - `https://your-project.vercel.app/api/refresh`

## 📊 监控和维护

### 查看部署状态
- Vercel 控制台提供详细的部署日志
- 可以监控 API 函数的调用情况

### 内容更新
- 手动：重新运行生成脚本并推送代码
- 自动：配置 GitHub Actions 定时任务

## 🆘 故障排除

### 常见问题

1. **部署失败**
   - 检查 `vercel.json` 配置
   - 确认 API 函数语法正确

2. **API 不工作**
   - 检查 CORS 设置
   - 确认函数路径正确

3. **静态文件未更新**
   - 确认 `output/` 目录包含最新文件
   - 检查 `.vercelignore` 配置

### 本地测试

在部署前可以本地测试：
```bash
# 安装 Vercel CLI
npm i -g vercel

# 本地开发服务器
vercel dev
```

## 📞 支持

如有问题，请参考：
- Vercel 官方文档：https://vercel.com/docs
- 项目 GitHub Issues

---

**注意**：这是静态部署版本，如需完整的实时刷新功能，请使用本地部署方案。 