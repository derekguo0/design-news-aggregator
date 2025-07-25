# 📰 设计资讯源维护指南

本文档详细说明了设计资讯聚合工具的资讯源配置、维护和优化策略。

## 🎯 当前资讯源配置

### ✅ 正常工作的资讯源 (12个)

| 资讯源 | URL | 分类 | 限制 | 状态 | 特色 |
|--------|-----|------|------|------|------|
| **UX Design CC** | https://uxdesign.cc/feed | 用户体验设计 | 10条 | ✅ | 全球最大UX设计师社区 |
| **Smashing Magazine** | https://www.smashingmagazine.com/feed/ | 网页设计 | 10条 | ✅ | 权威前端设计资源 |
| **UX Planet** | https://uxplanet.org/feed | 用户体验设计 | 8条 | ✅ | UX案例分析与实践 |
| **A List Apart** | https://alistapart.com/main/feed/ | 网页设计 | 6条 | ✅ | Web标准与设计哲学 |
| **Design Milk** | https://design-milk.com/feed/ | 产品设计 | 6条 | ✅ | 创新产品与工业设计 |
| **Intercom Blog** | https://blog.intercom.com/feed/ | 产品设计 | 6条 | ✅ | 产品策略与用户沟通 |
| **CSS-Tricks** | https://css-tricks.com/feed/ | 前端设计 | 5条 | ✅ | CSS技巧与前端实现 |
| **Marvel Blog** | https://blog.marvelapp.com/rss/ | 原型设计 | 4条 | ✅ | 原型工具与设计流程 |
| **UX Mastery** | https://uxmastery.com/feed/ | 用户体验设计 | 4条 | ✅ | UX技能与方法论 |
| **UX Myths** | https://uxmyths.com/rss.xml | 用户体验设计 | 3条 | ✅ | UX误区澄清 |
| **UX Collective** | https://uxdesign.cc/feed/tagged/ux-collective | 用户体验设计 | 4条 | ✅ | 精选UX深度文章 |
| **🆕 Product Hunt** | https://www.producthunt.com/ | 产品发现 | 8条 | ✅ | **每日热门新产品** |

### ⚠️ 需要关注的资讯源

| 资讯源 | 问题 | 解决方案 |
|--------|------|----------|
| **Inside Design by InVision** | RSS格式错误 | 寻找替代RSS地址或使用网页爬虫 |

## 📊 资讯获取统计

- **总资讯源**: 13个配置，12个正常工作
- **每日获取**: 约71条高质量资讯
- **成功率**: 92.3%
- **覆盖领域**: UI设计、UX设计、产品设计、前端设计、原型设计、产品发现

## 🆕 Product Hunt 特别说明

### 配置详情
```json
{
  "name": "Product Hunt",
  "url": "https://www.producthunt.com/",
  "type": "web",
  "category": "产品发现",
  "selectors": {
    "item": "section[data-test^='post-item']",
    "title": "a[data-test^='post-name'] ",
    "link": "a[data-test^='post-name']",
    "image": "img",
    "points": "button[data-test='vote-button'] span"
  },
  "enabled": true,
  "limit": 8
}
```

### 特色功能
- **每日新产品**: 自动获取当日最热门的新产品
- **社区投票**: 显示产品的社区认可度
- **产品截图**: 包含产品的视觉展示
- **分类标签**: 自动识别产品所属领域
- **稳定爬取**: 使用现代CSS选择器确保可靠性

### 维护注意事项
- Product Hunt 为网页爬虫类型，需要定期检查选择器有效性
- 如果网站结构变化，需要更新CSS选择器
- 建议每月检查一次爬取效果

## 🔧 维护操作指南

### 1. 添加新资讯源

```json
{
  "name": "新资讯源名称",
  "url": "https://example.com/feed/",
  "type": "rss",
  "category": "用户体验设计",
  "enabled": true,
  "limit": 5
}
```

**注意事项**:
- 优先选择RSS源，稳定性更好
- 分类应符合UI/UX/产品设计领域
- 设置合理的限制数量（3-10条）
- 新增源后务必测试

### 2. 测试资讯源

```bash
# 测试所有资讯源
python main.py test-sources

# 测试特定源（修改配置后）
python main.py test-sources | grep "源名称"
```

### 3. 修复异常源

#### RSS格式问题
```bash
# 直接测试RSS链接
curl -s "https://example.com/feed/" | head -20

# 检查RSS有效性
curl -s "https://example.com/feed/" | xmllint --format -
```

#### 网页爬虫问题
1. 检查页面结构变化
2. 更新CSS选择器
3. 检查反爬虫策略

### 4. 优化配置

#### 调整获取数量
根据资讯质量调整每个源的limit值：
- 高质量源：8-10条
- 一般质量源：4-6条
- 补充性源：2-4条

#### 平衡分类分布
确保各设计领域的资讯比例合理：
- 用户体验设计：40-50%
- 网页设计：20-30%
- 产品设计：15-25%
- 产品发现：10-15%
- 其他专业领域：10-15%

## 🎯 推荐资讯源候选

### RSS源候选（优先级高）

| 资讯源 | URL | 分类 | 说明 |
|--------|-----|------|------|
| **Figma Blog** | https://www.figma.com/blog/rss/ | UI设计 | 设计工具官方博客 |
| **Adobe XD Ideas** | https://xd.adobe.com/ideas/feed/ | UI设计 | Adobe设计理念 |
| **UsabilityHub Blog** | https://usabilityhub.com/blog/rss | 用户研究 | 可用性测试平台 |
| **UserTesting Blog** | https://www.usertesting.com/blog/feed/ | 用户研究 | 用户测试方法 |
| **Sketch Blog** | https://www.sketch.com/blog/feed/ | UI设计 | 设计工具博客 |

### 网页爬虫候选（需要维护）

| 网站 | 分类 | 说明 |
|------|------|------|
| **Dribbble** | UI作品 | 设计师作品展示 |
| **Behance** | 创意作品 | 创意作品集平台 |
| **Designer News** | 设计社区 | 设计师讨论社区 |

## 🚨 故障排除

### 常见问题及解决方案

#### 1. RSS解析错误
```
症状: RSS feed parsing warning
原因: RSS格式不规范或编码问题
解决: 
- 检查RSS链接有效性
- 尝试不同的RSS地址
- 考虑使用网页爬虫替代
```

#### 2. 获取数量为0
```
症状: 成功爬取但0条资讯
原因: 
- RSS源暂时无更新
- 网页结构变化
- 访问限制
解决:
- 检查源网站是否正常
- 更新爬虫选择器
- 调整请求头和延迟
```

#### 3. Product Hunt爬虫问题
```
症状: Product Hunt获取失败
原因: 网页结构变化或反爬虫
解决:
- 检查CSS选择器是否有效
- 更新data-test属性选择器
- 检查是否需要User-Agent
```

#### 4. 连接超时
```
症状: Failed to fetch URL
原因: 网络问题或服务器响应慢
解决:
- 增加请求超时时间
- 检查网络连接
- 使用代理（如需要）
```

## 📈 性能优化

### 1. 请求优化
```python
# 在 config/.env 中调整
REQUEST_TIMEOUT=30
REQUEST_DELAY=1.0
USER_AGENT="Mozilla/5.0 (compatible; DesignBot/1.0)"
```

### 2. 并发控制
- 当前支持并发爬取
- 建议同时并发数不超过12个
- 设置合理的请求延迟避免被封

### 3. 缓存策略
- RSS内容变化不频繁，可考虑缓存
- 实施ETag或Last-Modified检查
- 避免重复爬取相同内容

## 🔄 定期维护任务

### 每周检查
- [ ] 运行测试命令检查所有源状态
- [ ] 查看日志中的警告和错误
- [ ] 统计各源的获取成功率
- [ ] 检查Product Hunt爬虫是否正常

### 每月优化
- [ ] 分析资讯质量和用户反馈
- [ ] 调整各源的获取数量限制
- [ ] 评估是否需要添加新源或移除低质量源
- [ ] 检查网页爬虫选择器有效性

### 季度更新
- [ ] 重新评估所有资讯源的价值
- [ ] 寻找新的高质量资讯源
- [ ] 更新分类和标签体系
- [ ] 优化网页爬虫的稳定性

## 💡 最佳实践

1. **质量优于数量**: 宁要12条高质量资讯，不要50条低质量内容
2. **RSS优先**: RSS源比网页爬虫更稳定可靠
3. **分类明确**: 确保资讯源的分类准确，便于用户查找
4. **及时维护**: 发现问题及时修复，保持系统健康运行
5. **用户反馈**: 定期收集用户反馈，优化资讯源选择
6. **爬虫监控**: 网页爬虫需要更频繁的监控和维护

---

## 📞 技术支持

如果在维护过程中遇到问题：
1. 查看 `logs/app.log` 获取详细错误信息
2. 运行 `python main.py test-sources` 诊断具体问题
3. 参考本文档的故障排除部分
4. 对于Product Hunt等网页爬虫问题，检查CSS选择器
5. 提交Issue或联系技术团队 