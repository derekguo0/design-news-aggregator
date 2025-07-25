# 🚀 部署指南

本文档介绍如何将设计资讯聚合工具部署到各种平台。

## 📝 部署方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| GitHub Pages | 免费、自动部署、支持自定义域名 | 静态页面、有流量限制 | 个人项目、团队内部使用 |
| Vercel | 简单易用、全球CDN、免费额度高 | 函数执行时间限制 | 快速原型、轻量应用 |
| Netlify | 强大的构建功能、分支预览 | 免费版有带宽限制 | 前端项目、内容网站 |
| 自建服务器 | 完全控制、无限制 | 需要维护、成本较高 | 企业级应用 |

## 🌟 推荐方案：GitHub Pages

### 1. 准备工作

1. **Fork 或上传项目到 GitHub**
2. **启用 GitHub Pages**
   - 进入仓库设置 (Settings)
   - 滚动到 Pages 部分
   - Source 选择 "GitHub Actions"

### 2. 配置自动部署

项目已包含 `.github/workflows/deploy.yml` 配置文件，支持：
- ✅ 每天自动执行（北京时间上午9点）
- ✅ 手动触发
- ✅ 自动部署到 GitHub Pages

### 3. 自定义域名（可选）

1. **购买域名并配置DNS**
   ```
   CNAME记录: your-domain.com -> your-username.github.io
   ```

2. **在GitHub设置中添加自定义域名**
   - Settings > Pages > Custom domain
   - 输入你的域名
   - 启用 "Enforce HTTPS"

### 4. 配置资讯源

编辑 `config/sources.json` 添加你需要的资讯源：

```json
{
  "sources": [
    {
      "name": "你的资讯源名称",
      "url": "https://example.com/rss",
      "type": "rss",
      "category": "设计资讯",
      "enabled": true,
      "limit": 10
    }
  ]
}
```

## 🔧 其他部署方案

### Vercel 部署

1. **连接 GitHub 仓库**
   - 登录 [Vercel](https://vercel.com)
   - Import Git Repository
   - 选择你的仓库

2. **配置构建命令**
   ```bash
   # Build Command
   python -m pip install -r requirements.txt && python main.py once
   
   # Output Directory
   output
   ```

3. **添加环境变量**
   ```
   LOG_LEVEL=INFO
   ```

### Netlify 部署

1. **连接仓库**
   - 登录 [Netlify](https://netlify.com)
   - New site from Git
   - 选择你的仓库

2. **配置构建设置**
   ```yaml
   # netlify.toml
   [build]
     command = "python -m pip install -r requirements.txt && python main.py once"
     publish = "output"
   
   [build.environment]
     PYTHON_VERSION = "3.9"
   ```

### 自建服务器部署

1. **环境准备**
   ```bash
   # 安装 Python 3.9+
   sudo apt update
   sudo apt install python3 python3-pip nginx
   
   # 克隆项目
   git clone <your-repo-url>
   cd design-news-aggregator
   
   # 安装依赖
   pip3 install -r requirements.txt
   ```

2. **设置定时任务**
   ```bash
   # 编辑 crontab
   crontab -e
   
   # 添加定时任务（每天上午9点执行）
   0 9 * * * cd /path/to/project && python3 main.py once
   ```

3. **配置 Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       root /path/to/project/output;
       index index.html;
       
       location / {
           try_files $uri $uri/ =404;
       }
   }
   ```

## 📊 监控和维护

### 1. 监控执行状态

- **GitHub Actions**: 查看 Actions 标签页的执行日志
- **本地测试**: `python main.py test-all`

### 2. 日志管理

项目会在 `logs/` 目录生成日志文件：
- `app.log`: 应用运行日志
- 自动轮转和压缩

### 3. 性能优化

```bash
# 检查生成的文件大小
du -sh output/

# 压缩图片（如果有）
find output -name "*.jpg" -o -name "*.png" | xargs optipng

# 启用 gzip 压缩（Nginx）
gzip on;
gzip_types text/css application/javascript text/xml application/xml+rss text/javascript;
```

## 🛠️ 故障排除

### 常见问题

1. **构建失败**
   ```bash
   # 本地测试
   python main.py test-sources
   python main.py test-web
   ```

2. **资讯源无法访问**
   - 检查网站是否正常
   - 更新 CSS 选择器
   - 添加请求延迟

3. **部署后页面空白**
   - 检查静态文件路径
   - 确认模板文件正确

### 调试技巧

```bash
# 启用详细日志
python main.py test-all -v

# 检查生成的 HTML
ls -la output/
head -20 output/index.html

# 验证 RSS 源
curl -s "your-rss-url" | head -20
```

## 📈 进阶配置

### 1. 自定义样式

编辑 `templates/static/css/custom.css` 添加自定义样式。

### 2. 添加分析工具

在 `templates/base.html` 中添加 Google Analytics 或其他分析代码。

### 3. 集成通知

在 `src/scheduler/task_scheduler.py` 中添加邮件、Slack 或微信通知。

### 4. 数据持久化

```python
# 保存历史数据
import sqlite3
import json

def save_to_database(digest):
    conn = sqlite3.connect('data/news.db')
    # ... 数据库操作
```

## 🎯 最佳实践

1. **定期备份数据**
2. **监控网站可用性**
3. **优化爬取频率**
4. **遵守网站爬取规则**
5. **保持依赖更新**

---

如果在部署过程中遇到问题，欢迎提交 Issue！ 