# 📰 Daily Letter - 每日科技简报

一个基于 GitHub Actions 的自动化 RSS 聚合工具，每天定时抓取科技资讯，通过 Kimi AI 生成智能摘要，并推送到您的邮箱。

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-blue?logo=github-actions)
![Python](https://img.shields.io/badge/Python-3.11-green?logo=python)
![Kimi AI](https://img.shields.io/badge/Kimi%20AI-Powered-purple)

---

## ✨ 功能特点

- 🤖 **AI 智能摘要**：使用 Kimi (Moonshot) API 为每篇文章生成一句话核心摘要
- 📡 **多源聚合**：支持 Reddit、HackerNews、Product Hunt、爱范儿等科技媒体
- ⏰ **定时推送**：每天北京时间 14:00 自动推送至邮箱
- 🔄 **自动去重**：相同标题的文章只保留一次
- 🎯 **时间过滤**：只抓取过去 24 小时内的最新文章
- 📱 **邮件格式**：精美的 HTML 邮件，支持手机/桌面端阅读
- ⚙️ **灵活配置**：通过 `config.yml` 轻松自定义 RSS 源、时间等

---

## 📁 文件结构

```
.
├── .github/
│   └── workflows/
│       └── daily.yml          # GitHub Actions 工作流（自动生成）
├── config.yml                 # ⚙️ 主配置文件（修改这里自定义）
├── generate_workflow.py       # 🛠️ 根据 config.yml 生成工作流
├── test_locally.py           # 🧪 本地测试脚本
├── README.md                  # 📖 项目说明
├── QUICKSTART.md             # 🚀 快速开始指南
├── LICENSE                   # 📄 MIT 许可证
└── .gitignore                # 🚫 Git 忽略文件
```

---

## 🚀 快速开始

### 方式一：5 分钟快速搭建（推荐）

👉 查看 [QUICKSTART.md](QUICKSTART.md) 获取详细步骤

### 方式二：一句话概括

1. **Fork** 本仓库
2. 添加 **3 个 Secrets**（Kimi API Key + Gmail 账号 + Gmail 应用密码）
3. 运行 **GitHub Actions** 测试
4. 每天 **14:00** 准时收到科技日报！

---

## ⚙️ 自定义配置

所有配置都在 `config.yml` 中，无需修改代码！

### 修改推送时间

```yaml
schedule:
  cron: "0 6 * * *"  # 北京时间 14:00
```

常用时间：
- `"0 1 * * *"` = 北京时间 09:00
- `"0 6 * * *"` = 北京时间 14:00（默认）
- `"0 12 * * *"` = 北京时间 20:00

### 添加 RSS 源

```yaml
rss_sources:
  - name: "36氪"
    url: "https://36kr.com/feed"
    lang: "zh"
    max_items: 5
```

### 修改后生成工作流

```bash
python generate_workflow.py
```

或者直接编辑 `.github/workflows/daily.yml`

---

## 📮 默认订阅源

| 来源 | 语言 | 类型 |
|------|------|------|
| 爱范儿 | 中文 | 科技媒体 |
| Reddit r/technology | 英文 | 社区讨论 |
| HackerNews | 英文 | 技术新闻 |
| Product Hunt | 英文 | 新产品 |

更多推荐：36氪、少数派、TechCrunch、The Verge...

---

## 🛠️ 技术栈

- **GitHub Actions**：定时任务调度
- **Python 3.11**：核心处理逻辑
- **PyYAML**：配置文件解析
- **Feedparser**：RSS 订阅解析
- **Kimi (Moonshot) API**：AI 文本摘要
- **Jina AI**：网页内容提取
- **Gmail SMTP**：邮件推送

---

## 🧪 本地测试

在提交到 GitHub 前，可以在本地测试：

```bash
# 1. 安装依赖
pip install feedparser requests python-dateutil pyyaml

# 2. 设置环境变量
export KIMI_API_KEY="sk-xxxxx"

# 3. 测试 RSS 源
python test_locally.py rss

# 4. 测试 Kimi API
python test_locally.py api

# 5. 测试摘要生成
python test_locally.py summary

# 或运行全部测试
python test_locally.py all
```

---

## 💰 费用说明

### 免费额度

| 服务 | 免费额度 |
|------|---------|
| GitHub Actions | 私有仓库 2000 分钟/月 |
| Moonshot API | 新用户有试用额度 |
| Gmail | 免费发送 |

### 预估成本

按每天 10-15 篇文章：
- 每篇约 1K tokens
- 每天约 ¥0.2-0.3 RMB
- 每月约 ¥6-9 RMB

---

## 🔧 故障排除

### 邮件未收到

1. 检查 Gmail **垃圾邮件/推广邮件** 文件夹
2. 确认 `EMAIL_USERNAME` 和 `EMAIL_PASSWORD` 正确
3. 查看 Actions 日志中的 **Send Email** 步骤

### Kimi API 错误

| 错误码 | 原因 | 解决 |
|--------|------|------|
| 401 | API Key 无效 | 重新获取 Key |
| 403 | 无权限 | 检查是否用 Moonshot API（不是 Kimi Code） |
| 404 | 端点错误 | 检查 API URL 配置 |
| 429 | 请求过频 | 增加 `api_delay` 间隔 |

### RSS 抓取失败

部分源（如 Reddit）可能有限流，可以：
- 减少该源的 `max_items`
- 使用代理（需额外配置）
- 更换为其他 RSS 源

---

## 📝 更新日志

### v1.0 (2026-02-12)
- ✨ 初始版本发布
- 🤖 集成 Kimi AI 摘要
- 📧 支持 Gmail 邮件推送
- 🇨🇳 添加爱范儿等中文 RSS 源
- ⚙️ 支持 `config.yml` 自定义配置

---

## 📄 License

MIT License - 可自由使用和修改

---

## 🙏 致谢

- [Moonshot AI](https://www.moonshot.cn/) 提供 Kimi 大模型 API
- [Jina AI](https://jina.ai/) 提供网页内容提取服务
- GitHub Actions 提供自动化执行环境

---

## 💬 反馈

如有问题或建议：
- 提交 GitHub Issue
- 发送邮件联系

---

**Enjoy your daily tech digest!** 📰✨
