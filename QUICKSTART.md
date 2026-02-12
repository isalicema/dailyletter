# 🚀 快速开始指南

5 分钟搭建您的个人科技日报！

---

## 第一步：Fork 仓库

1. 访问您的仓库页面
2. 点击右上角 **Fork** 按钮
3. 选择您的个人账号

---

## 第二步：配置 Secrets

进入 **Settings → Secrets and variables → Actions → New repository secret**

添加以下 3 个 Secrets：

| Secret 名称 | 值 | 获取方式 |
|-------------|-----|---------|
| `KIMI_API_KEY` | `sk-xxxxx` | [platform.moonshot.cn](https://platform.moonshot.cn) |
| `EMAIL_USERNAME` | `yourname@gmail.com` | 您的 Gmail 地址 |
| `EMAIL_PASSWORD` | `abcd efgh ijkl mnop` | [Google 应用密码](https://myaccount.google.com/apppasswords) |

> 💡 **提示**：应用密码不是您的 Gmail 密码，是 16 位专用密码！

---

## 第三步：自定义配置（可选）

编辑 `config.yml`：

```yaml
# 修改推送时间
schedule:
  cron: "0 1 * * *"  # 改为早上 9 点

# 添加 RSS 源
rss_sources:
  - name: "36氪"
    url: "https://36kr.com/feed"
    lang: "zh"
    max_items: 5
```

---

## 第四步：生成工作流

在本地运行：

```bash
# 安装依赖
pip install pyyaml

# 生成工作流
python generate_workflow.py

# 提交到 GitHub
git add .
git commit -m "Update config"
git push
```

或者直接编辑 `.github/workflows/daily.yml`（跳过生成步骤）。

---

## 第五步：测试运行

1. 进入 **Actions** 标签页
2. 选择 **Daily Tech Digest**
3. 点击 **Run workflow**
4. 等待 1-2 分钟，检查您的 Gmail

---

## 🎉 完成！

从明天开始，每天您都会收到一份 AI 生成的科技日报！

---

## 常见问题

**Q: 邮件没收到？**
A: 检查 Gmail 垃圾邮件文件夹，确认 Secrets 配置正确。

**Q: 想改时间？**
A: 修改 `config.yml` 中的 `schedule.cron`，然后重新生成工作流。

**Q: 想加更多源？**
A: 在 `config.yml` 的 `rss_sources` 中添加，参考已有格式。

**Q: API 报错 401？**
A: API Key 无效，请重新从 [platform.moonshot.cn](https://platform.moonshot.cn) 获取。

---

**Enjoy!** 📧✨
