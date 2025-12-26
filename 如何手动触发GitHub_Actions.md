# 🚀 如何手动触发 GitHub Actions 测试

## 🎯 方法1：直接访问URL（最快！）⭐⭐⭐

### URL格式：
```
https://github.com/[您的用户名]/[仓库名]/actions
```

### 示例：
```
https://github.com/zhangsan/design-news-aggregator/actions
```

---

## 🎯 方法2：通过GitHub网页操作（详细步骤）

### 第1步：进入 Actions 页面

#### 方式A：从仓库主页
```
1. 访问 https://github.com
2. 登录并进入您的仓库
3. 点击顶部的 "Actions" 标签

┌─────────────────────────────────────────────────┐
│ < > Code  Issues  Pull requests  Actions  ...  │
│                                   ^^^^^^^       │
│                                   点击这里      │
└─────────────────────────────────────────────────┘
```

#### 方式B：直接访问
```
https://github.com/[用户名]/[仓库名]/actions
```

---

### 第2步：选择 Workflow

在 Actions 页面，您会看到左侧有 Workflow 列表：

```
All workflows
├── Auto Deploy to Vercel    ← 点击这个！
└── 其他workflows（如果有）
```

**点击 "Auto Deploy to Vercel"**

---

### 第3步：手动运行 Workflow

在 Workflow 页面：

1. **找到 "Run workflow" 按钮**
   - 位置：页面右上角，蓝色按钮
   - 如果看不到，说明workflow不支持手动触发

2. **点击 "Run workflow" 按钮**

3. **会弹出一个小窗口：**
   ```
   ┌────────────────────────────────────┐
   │ Run workflow                       │
   ├────────────────────────────────────┤
   │ Branch: main                  ▼    │
   │                                    │
   │        [Run workflow]              │
   └────────────────────────────────────┘
   ```

4. **确认分支为 "main"**（通常默认就是）

5. **点击绿色的 "Run workflow" 按钮**

---

### 第4步：查看运行状态

触发后，页面会自动刷新：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Workflow runs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟡 Auto Deploy to Vercel  #123
   main  •  workflow_dispatch  •  just now
   ↑
   黄色圆圈 = 正在运行
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**状态说明：**
- 🟡 **黄色圆圈** = 正在运行（Running）
- ✅ **绿色对勾** = 成功完成（Success）
- ❌ **红色叉号** = 失败（Failed）
- 🟠 **橙色** = 取消（Cancelled）

---

### 第5步：查看详细日志

**点击运行记录**（如 "Auto Deploy to Vercel #123"）

会进入详细页面，显示：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Jobs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ deploy  (2m 15s)
   ├── ✅ Checkout code
   ├── ✅ Set up Python
   ├── ✅ Install dependencies
   ├── ✅ Generate content
   ├── ✅ Commit and push
   └── ✅ Notify completion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**点击任意步骤**可查看详细日志。

---

## ✅ 成功的标志

### 1. Actions运行成功
```
✅ 所有步骤都显示绿色对勾
✅ 没有红色错误
✅ 最后一步"Notify completion"完成
```

### 2. 代码已提交
```
在 Actions 日志中看到：
"✅ 已推送最新内容到仓库"
```

### 3. Vercel自动部署
```
- Vercel检测到代码更新
- 自动触发重新部署
- 1-2分钟后部署完成
```

---

## ❌ 如果失败了怎么办？

### 查看错误信息：

1. **点击失败的运行记录**
2. **找到红色❌的步骤**
3. **点击展开查看错误日志**

### 常见错误和解决方案：

#### 错误1：权限错误
```
Error: Resource not accessible by integration
或
Error: Bad credentials
```

**原因：** Secrets配置错误或权限不足

**解决：**
1. 检查 VERCEL_TOKEN 是否正确
2. 检查 Token 是否有效（未过期）
3. 重新创建 Token 并更新

---

#### 错误2：项目ID错误
```
Error: Project not found
或
Error: Invalid project id
```

**原因：** PROJECT_ID 或 ORG_ID 错误

**解决：**
1. 重新获取 PROJECT_ID（在 Vercel 项目设置中）
2. 确认 ORG_ID 正确（从 URL 中获取）
3. 确保没有多余空格

---

#### 错误3：依赖安装失败
```
Error: Command failed: pip install
```

**原因：** Python依赖问题

**解决：**
1. 检查 requirements.txt 是否正确
2. 查看具体哪个包安装失败
3. 可能需要更新包版本

---

## 🔍 验证部署是否成功

### 方法1：查看Vercel部署状态

1. 访问 https://vercel.com
2. 进入您的项目
3. 查看 "Deployments" 标签
4. 最新的部署应该显示为 "Ready"

---

### 方法2：访问网站测试

1. 打开您的网站：`https://[您的域名].vercel.app`
2. 查看内容是否更新
3. 检查日期是否为当天
4. 测试刷新按钮是否工作

---

### 方法3：测试刷新按钮

1. 访问网站
2. 点击 "刷新资讯" 按钮
3. 应该看到：**"✅ GitHub Actions已成功触发！"**
4. 而不是配置错误提示

---

## 📋 完整测试流程

```
第1步：添加 Secrets
  ├── VERCEL_TOKEN ✅
  ├── ORG_ID ✅
  └── PROJECT_ID ✅
         ↓
第2步：手动触发 Actions
  └── Actions 页面 → Run workflow
         ↓
第3步：等待运行完成（2-3分钟）
  └── 查看是否全部绿色✅
         ↓
第4步：等待 Vercel 部署（1-2分钟）
  └── 查看 Vercel 部署状态
         ↓
第5步：测试网站功能
  ├── 访问网站
  ├── 查看内容是否更新
  └── 测试刷新按钮
         ↓
✅ 完成！功能正常工作！
```

---

## 🎬 图解说明

### 触发 Workflow 的位置：

```
GitHub 仓库页面
  ↓
Actions 标签
  ↓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
左侧 Workflows 列表          右侧区域
────────────────────    ──────────────────
All workflows           [Run workflow] 按钮 ← 点这里
├─ Auto Deploy                         ↑
└─ ...                      蓝色按钮，右上角
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 💡 小贴士

### ✅ 首次测试建议：

1. **先查看现有的运行记录**
   - 了解之前为什么失败
   - 对比修复后的变化

2. **保持页面打开**
   - 实时查看运行状态
   - 方便查看日志

3. **耐心等待**
   - Actions 运行需要 2-3 分钟
   - Vercel 部署需要 1-2 分钟
   - 总共约 5 分钟

4. **多次刷新**
   - Actions 页面可能不会自动更新
   - 手动刷新查看最新状态

---

### ✅ 成功后的维护：

1. **定期查看 Actions 运行状态**
2. **关注失败通知邮件**
3. **定期更新 Token（建议90天）**
4. **备份重要的 Secrets 值**

---

## 🆘 故障排除清单

运行失败时，逐项检查：

- [ ] Secrets 名称完全正确（大小写）
  - VERCEL_TOKEN
  - ORG_ID
  - PROJECT_ID

- [ ] Secrets 值正确无误
  - Token 有效未过期
  - ID 格式正确
  - 没有多余空格或换行

- [ ] Workflow 文件存在
  - `.github/workflows/deploy.yml` 文件存在
  - 文件格式正确

- [ ] 权限正确
  - 您是仓库管理员
  - Token 有足够权限

- [ ] 网络正常
  - GitHub 可访问
  - Vercel 可访问

---

## 📚 相关命令

### 本地验证（可选）

在运行 Actions 之前，可以本地测试：

```bash
# 进入项目目录
cd /Users/ithppc02110/Documents/推送机器人

# 运行诊断
python3 diagnose_refresh.py

# 本地测试内容生成
python3 actions_refresh.py
```

---

## 🎯 快速链接模板

**保存这些链接方便使用：**

```
Actions 页面：
https://github.com/[用户名]/[仓库名]/actions

特定 Workflow：
https://github.com/[用户名]/[仓库名]/actions/workflows/deploy.yml

Secrets 设置：
https://github.com/[用户名]/[仓库名]/settings/secrets/actions
```

---

## ✨ 配置成功的最终效果

完成所有配置并测试成功后：

1. **自动化工作流程**
   - 点击网站刷新按钮
   - 自动触发 GitHub Actions
   - 自动生成最新内容
   - 自动部署到 Vercel

2. **定时自动更新**
   - 每天 UTC 00:00（北京时间 08:00）
   - 每天 UTC 12:00（北京时间 20:00）

3. **完整监控**
   - GitHub Actions 运行记录
   - Vercel 部署历史
   - 错误自动通知

---

**总结：进入 Actions 页面 → 点击 Run workflow → 等待完成 → 验证结果！** 🚀

