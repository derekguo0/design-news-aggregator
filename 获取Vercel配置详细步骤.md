# 🔑 获取Vercel Token和项目ID - 详细步骤

> 这是配置刷新功能的必要步骤，预计耗时：5分钟

---

## 📋 第一部分：获取Vercel Token

### 步骤1：登录Vercel控制台

1. 打开浏览器，访问：**https://vercel.com**
2. 点击右上角 **Login** 按钮登录
3. 使用您的账号登录（GitHub/GitLab/Email等）

### 步骤2：进入Token设置页面

1. 登录后，点击**右上角的头像**
2. 在下拉菜单中点击 **Settings**
3. 在左侧菜单中找到并点击 **Tokens**

```
路径：头像 → Settings → Tokens
```

### 步骤3：创建新Token

1. 在Tokens页面，点击右上角的 **Create Token** 按钮
2. 填写Token信息：

   **Token Name（必填）**
   ```
   GitHub Actions Deploy
   ```
   
   **Scope（作用域）**
   - 如果是个人账户：会自动选择您的用户名
   - 如果是团队账户：从下拉菜单选择对应的团队
   
   **Expiration（过期时间）**
   - 建议选择：**No Expiration**（永不过期）
   - 或者选择：**Custom** → 设置较长时间（如1年）

3. 点击页面底部的 **Create** 按钮

### 步骤4：复制Token

⚠️ **重要：Token只会显示一次！**

1. Token创建成功后，会立即显示一个长字符串
2. 格式类似：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`（32位字符）
3. **立即点击复制按钮** 或 **手动选中并复制**
4. 将Token保存到安全的地方（建议使用密码管理器或临时记事本）

```
示例Token格式：
kQpX9YmZnAbCdEfGhIjKlMnOpQrStUvW
```

5. 复制完成后，点击 **Done** 关闭对话框

---

## 📋 第二部分：获取项目ID和组织ID

有两种方法获取，推荐使用方法A（更简单）。

---

### 方法A：使用Vercel CLI（推荐）⭐

#### 前置要求
如果您还没有安装Vercel CLI，先安装：

```bash
# 使用npm安装（推荐）
npm install -g vercel

# 或使用yarn
yarn global add vercel

# 或使用pnpm
pnpm add -g vercel
```

#### 步骤1：导航到项目目录

```bash
cd /Users/ithppc02110/Documents/推送机器人
```

#### 步骤2：链接项目

```bash
vercel link
```

这个命令会：
1. 要求您登录（如果还没登录）
2. 询问要链接哪个项目
3. 选择对应的项目即可

**交互示例：**
```
? Set up "~/Documents/推送机器人"? [Y/n] Y
? Which scope should contain your project? [您的用户名/团队名]
? Link to existing project? [Y/n] Y
? What's the name of your existing project? design-news-aggregator
✅ Linked to [您的用户名]/design-news-aggregator
```

#### 步骤3：查看项目信息

```bash
cat .vercel/project.json
```

**输出示例：**
```json
{
  "orgId": "team_xxxxxxxxxxxxxxxxxxxx",
  "projectId": "prj_xxxxxxxxxxxxxxxxxxxx"
}
```

#### 步骤4：记录信息

从输出中复制：
- **orgId**: `team_xxxxxxxxxxxxxxxxxxxx`（或 `user_xxx` 开头）
- **projectId**: `prj_xxxxxxxxxxxxxxxxxxxx`

✅ **完成！您已获取到所需的ID**

---

### 方法B：从Vercel控制台获取

如果您不想使用命令行，可以从Vercel控制台获取。

#### 步骤1：获取Project ID

1. 登录 **https://vercel.com**
2. 在主页面找到您的项目（design-news-aggregator 或类似名称）
3. 点击项目名称进入项目详情页
4. 点击顶部的 **Settings** 标签
5. 在左侧菜单选择 **General**
6. 向下滚动找到 **Project ID** 部分
7. 复制显示的ID（格式：`prj_xxxxxxxxxxxxxxxxxxxx`）

```
路径：项目 → Settings → General → Project ID
```

#### 步骤2：获取Organization ID（orgId）

**方式2-1：从项目设置获取（推荐）**

1. 还是在项目的 Settings → General 页面
2. 找到 **Root Directory** 上方或附近的项目信息区域
3. 可能会显示 **Team** 或 **Owner** 信息
4. 记下团队名称或用户名

**方式2-2：从账户设置获取**

1. 点击右上角头像 → **Settings**
2. 如果是团队账户：
   - 左侧选择对应的团队
   - 在 **General** 标签中查找 **Team ID**
3. 如果是个人账户：
   - 在 **General** 标签中查找 **User ID**

**方式2-3：通过项目URL推断**

项目URL格式：`https://vercel.com/[orgId]/[project-name]`

例如：`https://vercel.com/your-team/design-news`
- orgId 就是：`your-team`

**方式2-4：使用Vercel API**

```bash
# 使用您的Token查询
curl -H "Authorization: Bearer [您的Vercel Token]" \
  https://api.vercel.com/v2/teams
```

返回结果中会包含 team ID。

---

## 📝 信息汇总

完成以上步骤后，您应该得到三个关键信息：

| 配置项 | 值 | 格式示例 |
|--------|-----|----------|
| **VERCEL_TOKEN** | `____________________________` | `kQpX9YmZnAbCdEfGhI...` |
| **ORG_ID** | `____________________________` | `team_xxx` 或 `user_xxx` |
| **PROJECT_ID** | `____________________________` | `prj_xxxxxxxxxxxx` |

---

## 🔐 安全提示

⚠️ **Token安全非常重要！**

✅ **应该做的：**
- 将Token保存在安全的地方
- 只添加到GitHub Secrets中
- 定期更换Token（建议90天）
- 使用密码管理器保存

❌ **不应该做的：**
- ❌ 不要提交到代码仓库
- ❌ 不要分享给他人
- ❌ 不要在公开场合发布
- ❌ 不要保存在明文文件中

---

## 🎯 下一步

获取到这三个信息后，请按照以下步骤继续：

### 方式1：按照操作清单（推荐）
打开 `✅操作检查清单.md`，跳到第三步"添加GitHub Secrets"

### 方式2：快速配置
```bash
# 1. 打开GitHub仓库的Secrets设置页面
# 访问：https://github.com/[你的用户名]/[仓库名]/settings/secrets/actions

# 2. 添加三个Secrets（点击 "New repository secret"）

Secret 1:
Name: VERCEL_TOKEN
Value: [粘贴您的Vercel Token]

Secret 2:
Name: ORG_ID
Value: [粘贴您的Organization ID]

Secret 3:
Name: PROJECT_ID
Value: [粘贴您的Project ID]
```

---

## ❓ 常见问题

### Q1: Token创建后忘记复制怎么办？
**A:** Token只显示一次，无法再次查看。需要：
1. 回到 Vercel → Settings → Tokens
2. 找到之前创建的Token，点击 **Delete**
3. 重新创建一个新Token
4. 这次记得立即复制！

### Q2: 如何验证Token是否有效？
**A:** 可以使用以下命令测试：
```bash
curl -H "Authorization: Bearer [您的Token]" \
  https://api.vercel.com/v2/user
```
如果返回用户信息，说明Token有效。

### Q3: 找不到Project ID怎么办？
**A:** 尝试以下方法：
1. 确认您登录的是正确的Vercel账户
2. 确认项目已成功部署到Vercel
3. 使用 `vercel link` 命令重新链接项目
4. 查看项目的Settings → General页面

### Q4: orgId是team还是user？
**A:** 
- 如果使用**团队账户**：格式为 `team_xxxx`
- 如果使用**个人账户**：格式可能为 `user_xxxx` 或直接是用户名

### Q5: 我有多个项目，如何确认是哪个？
**A:** 
1. 查看项目名称是否匹配
2. 检查项目的Git仓库链接
3. 查看项目的域名
4. 使用 `vercel list` 命令查看所有项目

---

## 🔍 验证信息是否正确

在添加到GitHub Secrets之前，可以验证：

### 验证1：使用Vercel CLI
```bash
# 设置环境变量（临时）
export VERCEL_TOKEN="您的Token"
export VERCEL_ORG_ID="您的orgId"
export VERCEL_PROJECT_ID="您的projectId"

# 验证Token
vercel whoami

# 列出项目
vercel list
```

### 验证2：使用API测试
```bash
# 测试Token和获取项目信息
curl -H "Authorization: Bearer [您的Token]" \
  "https://api.vercel.com/v9/projects/[您的projectId]?teamId=[您的orgId]"
```

如果返回项目信息，说明三个值都正确！

---

## 📚 相关文档

- **✅操作检查清单.md** - 完整配置流程
- **快速修复刷新功能.md** - 5分钟快速配置
- **完整配置修复指南.md** - 详细配置说明

---

## 🆘 需要帮助？

如果按照本指南操作后仍有问题：

1. **运行诊断工具**
   ```bash
   python3 diagnose_refresh.py
   ```

2. **查看Vercel文档**
   - Token文档：https://vercel.com/docs/rest-api#authentication
   - CLI文档：https://vercel.com/docs/cli

3. **检查配置**
   - 确认Token权限正确
   - 确认ID格式正确
   - 确认项目已部署到Vercel

---

✨ **获取完成！** 现在您可以继续配置GitHub Secrets了！

🚀 **下一步**: 打开 `✅操作检查清单.md` 继续配置

