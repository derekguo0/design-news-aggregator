# 🔑 Vercel GitHub Token 配置指南

## 🎯 解决线上刷新功能问题

如果您的线上"刷新资讯"按钮无法自动触发更新，需要配置GitHub Token来启用自动触发功能。

## 📋 配置步骤

### 1. 创建GitHub Personal Access Token

1. **登录GitHub**：访问 [github.com](https://github.com)
2. **进入设置**：点击右上角头像 → Settings
3. **开发者设置**：左侧菜单最底部 → Developer settings
4. **创建Token**：Personal access tokens → Tokens (classic) → Generate new token (classic)

### 2. 配置Token权限

创建Token时，**必须勾选以下权限**：

- ✅ **repo** (完整仓库访问权限)
  - repo:status
  - repo_deployment  
  - public_repo
- ✅ **workflow** (GitHub Actions工作流权限)
- ✅ **actions** (GitHub Actions权限)
  - actions:read
  - actions:write

**Token有效期**：建议选择90天或更长

### 3. 在Vercel中配置环境变量

1. **登录Vercel**：访问 [vercel.com](https://vercel.com)
2. **选择项目**：找到您的设计资讯网站项目
3. **项目设置**：点击项目 → Settings标签
4. **环境变量**：左侧菜单 → Environment Variables
5. **添加变量**：

```
Name: GITHUB_TOKEN
Value: 您刚创建的GitHub Token
Environment: Production, Preview, Development (全选)
```

6. **保存配置**：点击Save

### 4. 重新部署项目

配置完成后需要重新部署：

1. **触发部署**：在Vercel项目页面点击"Redeploy"
2. **或推送代码**：向GitHub仓库推送任意提交

## ✅ 验证配置

配置完成后，测试刷新功能：

1. **访问线上网站**
2. **点击"刷新资讯"按钮**
3. **查看响应**：
   - ✅ **配置成功**：显示"GitHub Actions已成功触发"
   - ⚠️ **仍需手动**：显示手动触发指导

## 🔧 故障排除

### Token权限不足
```
错误：API调用失败: HTTP 403
解决：重新创建Token，确保勾选了workflow和actions权限
```

### Token无效或过期
```
错误：API调用失败: HTTP 401
解决：重新创建Token并更新Vercel环境变量
```

### 仓库名称错误
```
错误：API调用失败: HTTP 404
解决：确认Token有访问目标仓库的权限
```

## 🎉 配置完成后

配置成功后，您的刷新功能将：

- ✅ **自动触发**：点击按钮直接触发GitHub Actions
- ✅ **实时更新**：2-3分钟内自动生成最新内容
- ✅ **无需手动**：无需手动操作GitHub页面

## 🔒 安全注意事项

1. **Token保密**：请勿将Token分享给他人
2. **最小权限**：只勾选必要的权限
3. **定期更新**：建议定期更换Token
4. **监控使用**：定期检查Token的使用记录

## 💡 备用方案

如果暂时无法配置Token，您可以：

1. **手动触发**：通过GitHub Actions页面手动运行workflow
2. **定时更新**：等待每天的自动定时更新（00:00和12:00 UTC）
3. **本地刷新**：使用本地刷新服务器立即更新

---

配置完成后，您的线上刷新功能就能完美工作了！🎉