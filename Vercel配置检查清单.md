# ✅ Vercel 环境变量配置检查清单

## 📋 配置前检查

- [ ] 已获得GitHub Personal Access Token
- [ ] Token包含必要权限：repo, workflow, actions
- [ ] 已登录Vercel控制台
- [ ] 找到正确的项目：design-news-aggregator

## 🔧 配置步骤检查

### GitHub Token 权限确认
- [ ] ✅ repo (完整仓库权限)
- [ ] ✅ workflow (工作流权限)  
- [ ] ✅ actions (GitHub Actions权限)

### Vercel 环境变量设置
- [ ] 环境变量名称：`GITHUB_TOKEN`
- [ ] Token值：`ghp_` 开头的长字符串
- [ ] 环境范围：Production ✅ Preview ✅ Development ✅
- [ ] 已点击保存按钮

### 部署确认
- [ ] 配置保存后触发了重新部署
- [ ] 部署状态显示为 "Ready" 或 "Success"
- [ ] 没有部署错误信息

## 🧪 测试验证

### 基本功能测试
- [ ] 网站可以正常访问
- [ ] 刷新按钮可以点击
- [ ] 点击后有进度显示

### 成功配置的表现
**期望看到：**
```
🚀 正在触发自动更新
通过GitHub Actions更新内容...
⏳ 更新进行中
预计需要2-3分钟完成...
✅ 更新已触发！
GitHub Actions已成功触发！
```

### 配置问题的表现
**如果看到以下内容，说明需要检查配置：**
```
⚠️ 需要手动触发更新
未配置GITHUB_TOKEN环境变量
API调用失败: HTTP 401/403
```

## 🔍 调试工具

### 使用调试API
访问：`https://您的域名/api/debug`

**成功配置应显示：**
```json
{
  "environment": {
    "GITHUB_TOKEN": "Configured",
    "VERCEL": "1",
    "VERCEL_ENV": "production"
  },
  "deployment_detection": {
    "is_vercel": true,
    "has_github_token": true
  }
}
```

### 常见问题排查

**问题1：Token权限不足**
- 症状：HTTP 403错误
- 解决：重新创建Token，确保勾选所有必要权限

**问题2：Token无效**  
- 症状：HTTP 401错误
- 解决：检查Token是否正确复制，没有多余空格

**问题3：环境变量未生效**
- 症状：调试API显示"Not configured"
- 解决：确认变量名拼写，重新部署项目

**问题4：仓库名不匹配**
- 症状：GitHub API找不到仓库
- 解决：额外配置 `GITHUB_REPOSITORY` 变量

## 📞 获取帮助

如果按照清单操作后仍有问题，请提供：
1. `/api/debug` 的完整返回内容
2. 浏览器控制台的错误信息
3. Vercel部署日志中的错误信息
4. 具体的错误提示截图

这样可以快速定位问题并提供针对性的解决方案！
