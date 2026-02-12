#!/usr/bin/env python3
"""
Daily Letter - Workflow Generator
根据 config.yml 生成 GitHub Actions 工作流文件
"""

import yaml
import json
from datetime import datetime


def load_config(config_file='config.yml'):
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_rss_sources_code(sources):
    """生成 RSS 源配置代码"""
    lines = []
    for src in sources:
        name = src['name']
        url = src['url']
        lines.append(f'            "{name}": "{url}"')
    return ',\n'.join(lines)


def generate_workflow(config):
    """生成 GitHub Actions 工作流文件"""

    rss_sources = generate_rss_sources_code(config['rss_sources'])
    cron = config['schedule']['cron']
    hours_back = config['content']['hours_back']
    max_entries = config['content']['max_entries']
    max_summary_length = config['content']['summary']['max_length']
    model = config['content']['summary']['model']
    api_delay = config['advanced']['api_delay']

    workflow = f'''name: Daily Tech Digest

on:
  schedule:
    - cron: '{cron}'
  workflow_dispatch:

jobs:
  digest:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - run: pip install feedparser requests python-dateutil pyyaml

      - name: Generate Digest
        env:
          KIMI_API_KEY: ${{{{ secrets.KIMI_API_KEY }}}}
        run: |
          python3 << 'SCRIPT_EOF'
          import feedparser
          import requests
          import os
          import sys
          import re
          import html
          import hashlib
          import time
          from datetime import datetime, timedelta
          from dateutil import parser as date_parser

          KIMI_KEY = os.environ.get('KIMI_API_KEY', '')
          if not KIMI_KEY:
              print("ERROR: KIMI_API_KEY not found")
              sys.exit(1)

          # Moonshot 官方 API
          API_URL = "https://api.moonshot.cn/v1/chat/completions"
          MODEL = "{model}"

          RSS_SOURCES = {{
{rss_sources}
          }}

          def clean_text(text):
              if not text:
                  return ""
              text = re.sub(r'<[^>]+>', '', text)
              text = html.unescape(text)
              text = ' '.join(text.split())
              return text.strip()

          def get_content(url):
              try:
                  if url.startswith('http://') or url.startswith('https://'):
                      jina_url = "https://r.jina.ai/" + url
                  else:
                      jina_url = "https://r.jina.ai/http://" + url
                  resp = requests.get(jina_url, timeout=15)
                  if resp.status_code == 200:
                      return clean_text(resp.text)[:2000]
              except:
                  pass
              return None

          def summarize(title, content):
              if not content:
                  return None
              try:
                  headers = {{
                      "Authorization": "Bearer " + KIMI_KEY,
                      "Content-Type": "application/json"
                  }}

                  prompt_text = "用一句话（不超过{max_summary_length}个字）总结这篇科技新闻：\\n\\n标题：" + title + "\\n内容：" + content[:1000] + "\\n\\n要求：只说核心事实，不要本文文章等词。摘要："

                  payload = {{
                      "model": MODEL,
                      "messages": [
                          {{"role": "system", "content": "你是Kimi，擅长用一句话总结科技新闻。严格控制字数在{max_summary_length}字以内。"}},
                          {{"role": "user", "content": prompt_text}}
                      ],
                      "temperature": 0.3,
                      "max_tokens": 50,
                      "stream": False
                  }}

                  resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)

                  if resp.status_code != 200:
                      print("API Error: " + str(resp.status_code))
                      return None

                  result = resp.json()
                  if 'choices' in result and len(result['choices']) > 0:
                      summary = result['choices'][0]['message']['content'].strip()
                      summary = clean_text(summary)
                      summary = summary.replace('摘要：', '').replace('总结：', '')
                      if len(summary) > 60:
                          summary = summary[:57] + '...'
                      return summary
              except Exception as e:
                  print("Summarize error: " + str(e))
              return None

          cutoff = datetime.now() - timedelta(hours={hours_back})
          entries = []
          seen = set()

          for source, url in RSS_SOURCES.items():
              try:
                  feed = feedparser.parse(url)
                  for entry in feed.entries[:5]:
                      try:
                          pub_str = entry.get('published', entry.get('updated', ''))
                          if not pub_str:
                              continue
                          pub = date_parser.parse(pub_str)
                          pub = pub.replace(tzinfo=None) if pub.tzinfo else pub
                          if pub < cutoff:
                              continue

                          title = clean_text(entry.title)
                          h = hashlib.md5(title.lower().encode()).hexdigest()[:8]
                          if h in seen:
                              continue
                          seen.add(h)

                          content = get_content(entry.link)
                          summary = summarize(title, content) if content else None
                          if not summary:
                              raw = entry.get('summary', '')
                              summary = clean_text(raw)[:100] + '...' if raw else '点击查看详情'

                          entries.append({{
                              'title': title,
                              'link': entry.link,
                              'source': source,
                              'summary': summary
                          }})
                          time.sleep({api_delay})
                      except:
                          continue
              except:
                  continue

          today = datetime.now().strftime('%Y-%m-%d %a')

          html_parts = []
          html_parts.append('<!DOCTYPE html><html><head><meta charset="utf-8"><style>')
          html_parts.append('body{{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;max-width:600px;margin:0 auto;padding:20px}}')
          html_parts.append('h1{{color:#1a73e8;border-bottom:2px solid #1a73e8;padding-bottom:10px}}')
          html_parts.append('h2{{color:#444;font-size:16px;margin-top:25px;border-left:3px solid #1a73e8;padding-left:10px}}')
          html_parts.append('.item{{margin:15px 0;padding:12px;background:#f8f9fa;border-radius:8px}}')
          html_parts.append('.title{{font-weight:600;color:#1a73e8;text-decoration:none}}')
          html_parts.append('.summary{{color:#555;font-size:14px;margin-top:8px}}')
          html_parts.append('.footer{{margin-top:30px;padding-top:15px;border-top:1px solid #ddd;color:#999;font-size:12px;text-align:center}}')
          html_parts.append('</style></head><body>')
          html_parts.append('<h1>📰 科技日报 ' + today + '</h1>')
          html_parts.append('<p>过去{hours_back}小时共 <strong>' + str(len(entries)) + '</strong> 条精选</p>')

          current = None
          for e in entries[:{max_entries}]:
              if e['source'] != current:
                  current = e['source']
                  html_parts.append('<h2>' + current + '</h2>')
              html_parts.append('<div class="item"><a href="' + e['link'] + '" class="title">' + html.escape(e['title']) + '</a>')
              html_parts.append('<div class="summary">📝 ' + html.escape(e['summary']) + '</div></div>')

          html_parts.append('<div class="footer">🤖 摘要由 Kimi AI 生成<br>📧 GitHub Actions 自动推送</div>')
          html_parts.append('</body></html>')

          with open('digest.html', 'w', encoding='utf-8') as f:
              f.write(''.join(html_parts))

          print("Generated " + str(len(entries)) + " entries")
          SCRIPT_EOF

      - name: Send Email
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 587
          username: ${{{{ secrets.EMAIL_USERNAME }}}}
          password: ${{{{ secrets.EMAIL_PASSWORD }}}}
          subject: 📰 科技日报 ${{{{ github.run_date }}}}
          html_body: file://digest.html
          to: ${{{{ secrets.EMAIL_USERNAME }}}}
          from: Daily Digest Bot

# 配置文件: config.yml
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 由 generate_workflow.py 自动生成
'''

    return workflow


def main():
    """主函数"""
    print("Loading config.yml...")
    config = load_config()

    print("Generating workflow...")
    workflow = generate_workflow(config)

    output_file = '.github/workflows/daily.yml'

    # 确保目录存在
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(workflow)

    print(f"✅ Workflow generated: {output_file}")
    print(f"   Cron: {config['schedule']['cron']}")
    print(f"   RSS Sources: {len(config['rss_sources'])}")
    print(f"   Max entries: {config['content']['max_entries']}")


if __name__ == '__main__':
    main()
