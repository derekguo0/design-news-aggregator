# 🚀 Vercel 部署快速设置指南

## 📋 部署前准备

您的项目现在已经准备好部署到Vercel了！已经包含以下文件：
- ✅ `vercel.json` - Vercel配置文件
- ✅ `api/` 目录 - Serverless API函数
- ✅ `.vercelignore` - 忽略不必要的文件
- ✅ `output/` 目录 - 生成的静态网站
- ✅ `.github/workflows/deploy.yml` - 自动部署工作流

## 🔧 部署步骤

### 方法一：直接部署（推荐新手）

1. **安装 Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **登录 Vercel**
   ```bash
   vercel login
   ```

3. **部署项目**
   ```bash
   vercel --prod
   ```

### 方法二：GitHub 集成 + 自动化（推荐）

1. **推送代码到 GitHub**
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push origin main
   ```

2. **在 Vercel 控制台导入项目**
   - 访问 https://vercel.com
   - 点击 "New Project"
   - 选择你的 GitHub 仓库
   - Vercel 会自动检测配置

3. **设置自动部署密钥（可选）**
   
   在 GitHub 仓库的 Settings > Secrets 中添加：
   ```
   VERCEL_TOKEN=your_vercel_token
   ORG_ID=your_org_id  
   PROJECT_ID=your_project_id
   ```

## 🌟 部署后功能

### ✅ 正常工作的功能
- 📱 **响应式网站** - 完美适配手机和桌面
- 🗂️ **分类浏览** - 按设计类别筛选资讯
- 📅 **归档查看** - 历史资讯浏览
- 🔙 **回到顶部** - 平滑滚动
- 🎨 **美观界面** - Tailwind UI 设计

### ⚠️ 功能限制说明
- **刷新功能**：在静态部署中，"刷新资讯"按钮会显示提示信息，说明这是静态版本
- **内容更新**：需要重新生成和部署来更新内容

## 🔄 内容更新方式

### 手动更新
1. 本地运行：`python3 simple_run.py`
2. 推送到 GitHub
3. Vercel 自动重新部署

### 自动更新（如果配置了 GitHub Actions）
- 每天 UTC 00:00 和 12:00 自动更新
- 推送代码时自动部署
- 可以手动触发

## 🌐 访问地址示例

部署完成后的访问地址：
- **主页**：`https://your-project-name.vercel.app`
- **归档**：`https://your-project-name.vercel.app/archive.html`
- **API**：`https://your-project-name.vercel.app/api/health`

## 📱 测试部署

部署完成后，请测试以下功能：
1. ✅ 首页加载正常
2. ✅ 资讯卡片显示完整
3. ✅ 分类筛选功能
4. ✅ 归档页面访问
5. ✅ 移动端适配
6. ✅ "刷新资讯"按钮显示适当提示

## 🆘 常见问题

### Q: 部署失败怎么办？
A: 检查 Vercel 控制台的部署日志，通常是配置文件问题

### Q: API 不工作？
A: 确认 `api/` 目录中的文件格式正确，检查 CORS 设置

### Q: 如何更新内容？
A: 运行 `python3 simple_run.py` 生成新内容，然后重新部署

### Q: 能否恢复实时刷新功能？
A: 静态部署不支持，如需此功能请使用本地部署 + refresh_server.py

## 🎉 完成！

恭喜！您的设计资讯聚合网站现在已经部署在 Vercel 上了！

💡 **提示**：保存好您的 Vercel 项目 URL，这就是您的公开网站地址。 