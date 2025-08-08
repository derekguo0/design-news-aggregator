# 🔑 Vercel 环境变量配置完整指南

## 🎯 为什么需要配置环境变量？

修复后的刷新功能需要 `GITHUB_TOKEN` 来自动触发GitHub Actions，从而实现线上内容更新。

## 📋 配置步骤

### 1. 创建 GitHub Personal Access Token

1. **登录 GitHub**：访问 [github.com](https://github.com)
2. **进入设置**：点击右上角头像 → Settings  
3. **开发者设置**：左侧菜单最底部 → Developer settings
4. **创建 Token**：Personal access tokens → Tokens (classic) → Generate new token (classic)

### 2. 设置 Token 权限

**必须勾选以下权限**：
- ✅ **repo** (完整仓库访问权限)
- ✅ **workflow** (GitHub Actions工作流权限)  
- ✅ **actions** (GitHub Actions权限)

**Token 有效期**：建议选择 90 天或更长

### 3. 在 Vercel 中配置环境变量

1. **登录 Vercel**：访问 [vercel.com](https://vercel.com)
2. **选择项目**：找到您的设计资讯网站项目
3. **项目设置**：点击项目名称 → Settings 标签
4. **环境变量**：左侧菜单 → Environment Variables
5. **添加变量**：

```
Name: GITHUB_TOKEN
Value: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Environment: ✅ Production ✅ Preview ✅ Development
```

6. **保存配置**：点击 Save

### 4. 可选配置（如果仓库名不同）

如果您的GitHub仓库名不是 `design-news-aggregator`，需要额外配置：

```
Name: GITHUB_REPOSITORY  
Value: 您的用户名/您的仓库名
Environment: ✅ Production ✅ Preview ✅ Development
```

## 🔄 触发重新部署

配置完成后，需要重新部署项目：

### 方法1：Vercel 控制台
1. 在项目页面点击 **"Redeploy"** 按钮
2. 选择最新的部署版本
3. 点击 **"Redeploy"**

### 方法2：GitHub 推送（已完成）
- ✅ 代码已推送，Vercel 会自动重新部署

## ✅ 验证配置是否成功

部署完成后，测试刷新功能：

1. **访问线上网站**
2. **点击 "🔄 刷新资讯" 按钮**
3. **查看响应**：

### 🎉 配置成功的表现：
```
🚀 正在触发自动更新
⏳ 更新进行中 - 预计需要2-3分钟完成...
✅ 更新已触发！请稍候2-3分钟后手动刷新页面查看新内容
```

### ⚠️ 需要检查的表现：
```
⚠️ 需要手动触发更新
将为您执行以下操作...
```

### ❌ 配置有问题的表现：
```
🚫 刷新失败
API错误 - 服务器响应错误: 401 Unauthorized
```

## 🔧 故障排除

### 问题1：显示"未配置GITHUB_TOKEN"
**解决**：按照上述步骤配置环境变量

### 问题2：显示"API调用失败: HTTP 403"
**解决**：Token权限不足，重新创建时确保勾选了 workflow 和 actions 权限

### 问题3：显示"API调用失败: HTTP 401"  
**解决**：Token无效或过期，重新生成新的Token

### 问题4：仍然提示手动触发
**检查**：
1. Token是否正确复制（没有多余空格）
2. 环境变量名是否准确：`GITHUB_TOKEN`
3. 是否选择了所有环境（Production, Preview, Development）

## 🔍 调试工具

如果仍有问题，可以使用新增的调试功能：

1. **访问调试页面**：`https://您的域名/api/debug`
2. **或在刷新失败时**：选择"查看详细调试信息"

调试信息会显示：
- 环境变量配置状态
- 部署环境检测结果
- 具体的错误原因和解决建议

## 📞 需要帮助？

如果按照指南操作后仍有问题，请提供：
- 调试API的返回内容 (`/api/debug`)
- 浏览器控制台的错误信息
- 具体的错误提示文字

这样可以帮您快速定位和解决问题！
