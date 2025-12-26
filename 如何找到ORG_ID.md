# 🔍 如何找到 ORG_ID（组织ID）

## 🎯 方法1：从项目URL直接看（最简单！）⭐⭐⭐

### 步骤：

1. **打开浏览器**，访问 https://vercel.com
2. **登录**您的账户
3. **点击**您的项目（design-news-aggregator 或类似名称）
4. **查看浏览器地址栏**的URL

### URL格式：
```
https://vercel.com/[ORG_ID]/[项目名称]
                   ^^^^^^^^
                   这就是您的 ORG_ID！
```

### 实例说明：

**示例1：个人账户**
```
URL: https://vercel.com/john-doe/my-project
ORG_ID: john-doe
```

**示例2：团队账户**
```
URL: https://vercel.com/my-team/my-project
ORG_ID: my-team
```

**示例3：有短横线的用户名**
```
URL: https://vercel.com/zhang-san-123/design-news
ORG_ID: zhang-san-123
```

✅ **就是这么简单！直接从URL复制即可！**

---

## 🎯 方法2：从Vercel项目设置页面（推荐）⭐⭐

### 步骤：

1. 在 Vercel 控制台打开您的项目
2. 点击顶部的 **Settings** 标签
3. 左侧菜单选择 **General**
4. 向下滚动查找以下信息：

**如果是个人账户，查找：**
- Owner
- Account
- User

**如果是团队账户，查找：**
- Team
- Organization

这里显示的名称就是您的 ORG_ID

---

## 🎯 方法3：从账户设置获取

### 个人账户：

1. 点击右上角**头像**
2. 选择 **Settings**
3. 在 **General** 标签中
4. 查找 **Username** 或 **User ID**

**Username 就是您的 ORG_ID**

### 团队账户：

1. 点击右上角**头像**
2. 选择 **Settings**
3. 左侧菜单选择您的**团队名称**
4. 在 **General** 标签中
5. 查找 **Team Slug** 或 **Team ID**

---

## 🎯 方法4：使用浏览器开发者工具

### 步骤：

1. 在 Vercel 项目页面按 **F12**（Mac: Command + Option + I）
2. 切换到 **Network**（网络）标签
3. **刷新页面**（F5 或 Command + R）
4. 在请求列表中查找任何 API 请求
5. 查看请求 URL，通常包含 `teamId=xxx` 或类似参数

---

## 📋 ORG_ID 格式说明

### 个人账户
- 通常就是您的**用户名**
- 格式：`username`
- 例如：`john-doe`, `zhang123`, `design-master`

### 团队账户
- 以 `team_` 开头的ID
- 格式：`team_xxxxxxxxxxxxxxxxxxxx`
- 例如：`team_abc123xyz456`

**注意：在GitHub Secrets中，两种格式都可以使用！**

---

## ✅ 最简单的获取流程（推荐）

```
第1步：打开 Vercel → 找到您的项目 → 点击进入
第2步：看浏览器地址栏
第3步：复制URL中间那段

https://vercel.com/[复制这里]/项目名
```

**就这么简单！3秒钟搞定！**

---

## 🎬 图文详解

### 场景1：您的项目URL是这样的

```
https://vercel.com/zhang-designer/design-news-aggregator
```

**您的 ORG_ID 就是：** `zhang-designer`

---

### 场景2：您的项目URL是这样的

```
https://vercel.com/my-design-team/design-news-aggregator
```

**您的 ORG_ID 就是：** `my-design-team`

---

### 场景3：不确定？用这个方法确认

1. 打开项目页面
2. 按 F12 打开开发者工具
3. 在控制台（Console）输入：

```javascript
window.location.pathname.split('/')[1]
```

4. 按回车，显示的就是您的 ORG_ID

---

## ❓ 常见问题

### Q1: ORG_ID 和 PROJECT_ID 有什么区别？

**ORG_ID (Organization ID)：**
- 您的账户或团队标识
- 格式：用户名或 `team_xxx`
- 从 URL 中可以直接看到

**PROJECT_ID：**
- 项目的唯一标识
- 格式：`prj_xxxxxxxxxxxxxxxxxxxx`
- 需要在项目设置中查看

---

### Q2: 我有多个项目，ORG_ID 是一样的吗？

**是的！** 如果所有项目都在同一个账户下：
- 同一个账户的所有项目
- **ORG_ID 都是相同的**
- 只有 PROJECT_ID 不同

---

### Q3: 我看到的是 team_xxx 格式，可以用吗？

**可以！** 两种格式都能用：
- 用户名格式：`john-doe`
- Team格式：`team_abc123xyz`

GitHub Actions 都能识别。

---

### Q4: 如何确认我找到的 ORG_ID 是正确的？

**验证方法：**
复制您找到的 ORG_ID，构造这个URL：
```
https://vercel.com/[您的ORG_ID]
```

在浏览器打开，如果能看到您的项目列表，就是对的！

---

## 📝 信息记录表

找到后立即记录：

```
┌─────────────────────────────────────────────┐
│ 我的 Vercel 配置信息                        │
├─────────────────────────────────────────────┤
│ 项目URL:                                    │
│ https://vercel.com/________________/_______ │
│                                             │
│ ORG_ID: ________________________________    │
│                                             │
│ PROJECT_ID: prj_________________________    │
│                                             │
│ VERCEL_TOKEN: 已创建 ☐                      │
└─────────────────────────────────────────────┘
```

---

## 🚀 下一步

找到 ORG_ID 后：

1. 同时获取 PROJECT_ID（在项目 Settings → General 中）
2. 准备好 VERCEL_TOKEN
3. 将这三个值添加到 GitHub Secrets
4. 测试 GitHub Actions

---

## 💡 小贴士

- ✅ ORG_ID **不是**秘密，可以公开
- ✅ 从 URL 复制最简单，不会出错
- ✅ 如果URL中有特殊字符，照样复制（比如：my-team-123）
- ⚠️ 确保没有多余的空格或换行

---

**总结：最快方法就是看项目URL！** 🎯

