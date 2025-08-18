# 设计资讯聚合工具

一个自动化的设计类资讯聚合工具，通过爬取多个设计网站的内容，将每日设计资讯生成美观的静态网站，便于团队同步和后续检索。支持GitHub Pages、Vercel等多种部署方案。

## ✨ 功能特性

- 🕷️ **多源爬取**: 支持网页爬取和RSS订阅，已预配置Dribbble、Behance、Design Milk等知名设计网站
- 📝 **智能处理**: 自动去重、内容清洗、分类聚合
- 📊 **结构化输出**: 生成美观的静态网站，包含分类、统计信息等
- ⏰ **定时任务**: 支持每日定时执行，自动生成资讯日报
- 🔧 **灵活配置**: 支持自定义资讯源、爬取规则、调度时间等
- 🚀 **易于扩展**: 模块化设计，便于添加新的资讯源和集成方式

## 📋 系统要求

- Python 3.8+
- 稳定的网络连接
- GitHub账号（用于免费部署）或其他静态网站托管服务

## 🚀 快速开始

### 1. 安装依赖

```bash
# 克隆项目
git clone <repository-url>
cd design-news-aggregator

# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置部署环境

选择以下方案之一：

**方案A: GitHub Pages（推荐）**
1. Fork 这个仓库到你的 GitHub 账号
2. 在仓库设置中启用 GitHub Pages
3. 选择 "GitHub Actions" 作为源

**方案B: 本地运行**
1. 无需额外配置，直接使用默认设置

### 3. 配置环境变量

```bash
# 复制配置模板
cp config/.env.example config/.env

# 编辑配置文件
nano config/.env
```

在 `.env` 文件中填写以下配置信息：

```env
# 调度配置
SCHEDULE_HOUR=9
SCHEDULE_MINUTE=0
TIMEZONE=Asia/Shanghai

# 日志配置
LOG_LEVEL=INFO
LOG_RETENTION=30 days
```

### 4. 测试配置

```bash
# 测试所有功能
python main.py test-all

# 单独测试网页生成
python main.py test-web

# 测试资讯源
python main.py test-sources
```

### 5. 运行程序

```bash
# 立即执行一次（生成网站）
python main.py once

# 启动定时调度器（每日自动生成）
python main.py start

# 查看生成的网站
open output/index.html
```

## 📖 使用指南

### 命令行界面

```bash
python main.py [command] [options]
```

**可用命令：**

- `start` / `run` - 启动定时调度器
- `once` - 立即执行一次爬取任务
- `test-all` - 测试所有功能
- `test-sources` - 测试资讯源连通性
- `test-web` - 测试网页生成功能
- `config` - 显示当前配置

**选项：**

- `--config-reload` - 重新加载配置文件
- `--verbose` / `-v` - 详细输出模式

### 配置文件说明

#### 资讯源配置 (`config/sources.json`)

```json
{
  "sources": [
    {
      "name": "网站名称",
      "url": "https://example.com",
      "type": "web",  // 或 "rss"
      "category": "分类名称",
      "selectors": {  // 仅web类型需要
        "item": ".item-class",
        "title": ".title-class", 
        "author": ".author-class",
        "link": "a",
        "image": "img"
      },
      "enabled": true,
      "limit": 10
    }
  ]
}
```

#### 环境变量配置 (`.env`)

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `SITE_TITLE` | 网站标题 | 设计资讯聚合 |
| `SITE_URL` | 网站地址 | https://your-site.com |
| `SCHEDULE_HOUR` | 执行小时(0-23) | 9 |
| `SCHEDULE_MINUTE` | 执行分钟(0-59) | 0 |
| `TIMEZONE` | 时区 | Asia/Shanghai |
| `USER_AGENT` | 爬虫User-Agent | 默认浏览器UA |
| `REQUEST_TIMEOUT` | 请求超时(秒) | 30 |
| `REQUEST_DELAY` | 请求间隔(秒) | 1 |
| `LOG_LEVEL` | 日志级别 | INFO |

## 🎨 支持的资讯源

目前预配置支持以下设计网站：

### 作品展示类
- **Dribbble Popular** - 热门设计作品
- **Behance Featured** - 精选设计项目

### 设计资讯类  
- **Design Milk** - 设计新闻和趋势
- **Core77** - 工业设计资讯
- **Dezeen** - 建筑和设计杂志

### 设计社区类
- **Designer News** - 设计师社区讨论

## 🔧 高级配置

### 添加新的资讯源

1. 编辑 `config/sources.json` 文件
2. 添加新的资讯源配置
3. 对于网页类型，需要配置CSS选择器
4. 对于RSS类型，只需要提供订阅链接
5. 重启程序或使用 `--config-reload` 选项

### 自定义爬取规则

为Web类型的资讯源配置CSS选择器：

```json
{
  "selectors": {
    "item": ".article-item",        // 文章容器
    "title": ".article-title",      // 标题选择器  
    "author": ".article-author",    // 作者选择器
    "link": ".article-link",        // 链接选择器
    "image": ".article-image",      // 图片选择器
    "stats": ".article-stats"       // 统计信息选择器
  }
}
```

### 修改调度时间

在 `.env` 文件中修改：

```env
SCHEDULE_HOUR=8     # 每天8点执行
SCHEDULE_MINUTE=30  # 30分钟
TIMEZONE=Asia/Shanghai
```

## 📁 项目结构

```
design-news-aggregator/
├── config/                    # 配置文件
│   ├── .env.example          # 环境变量模板
│   └── sources.json          # 资讯源配置
├── src/                       # 源代码
│   ├── crawlers/             # 爬虫模块
│   │   └── base.py           # 基础爬虫类
│   ├── processors/           # 内容处理模块
│   │   └── content_processor.py
│   ├── integrations/         # 第三方集成
│   │   └── feishu_client.py  # 飞书API客户端
│   ├── scheduler/            # 调度模块
│   │   └── task_scheduler.py
│   ├── config.py             # 配置管理
│   └── models.py             # 数据模型
├── data/                     # 数据存储
├── logs/                     # 日志文件
├── requirements.txt          # Python依赖
├── main.py                   # 程序入口
└── README.md                 # 项目文档
```

## 🐛 故障排除

### 常见问题

**1. 飞书API连接失败**
- 检查App ID和App Secret是否正确
- 确认应用权限配置
- 检查网络连接

**2. 爬取失败**
- 检查网站是否可访问
- 验证CSS选择器是否正确
- 查看日志文件获取详细错误信息

**3. 文档创建失败**
- 确认飞书应用有文档创建权限
- 检查文件夹Token是否有效
- 查看飞书API错误信息

### 日志文件

程序会在 `logs/` 目录下生成日志文件：
- `app.log` - 应用程序日志
- 日志文件会自动轮转和压缩

### 调试模式

使用 `-v` 参数启用详细日志：

```bash
python main.py test-all -v
```

## 🤝 贡献指南

欢迎提交Issues和Pull Requests！

1. Fork项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 支持

如果您在使用过程中遇到问题：

1. 查看本文档的故障排除部分
2. 查看项目Issues
3. 提交新的Issue描述问题

---

**🎉 感谢使用设计资讯聚合工具！** 

希望这个工具能帮助您和团队更好地跟踪设计行业的最新动态。 # 触发重新部署
