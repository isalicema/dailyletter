#!/usr/bin/env python3
"""
本地测试脚本 - 无需 GitHub Actions 即可测试 RSS 抓取和摘要生成
"""

import os
import sys
import yaml


def test_rss_sources():
    """测试 RSS 源是否可以正常访问"""
    import feedparser

    print("=" * 50)
    print("测试 RSS 源")
    print("=" * 50)

    # 加载配置
    with open('config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    for source in config['rss_sources']:
        name = source['name']
        url = source['url']

        print(f"\n📡 测试: {name}")
        print(f"   URL: {url}")

        try:
            feed = feedparser.parse(url)
            entries_count = len(feed.entries)
            print(f"   ✅ 成功! 获取到 {entries_count} 条记录")

            if entries_count > 0:
                # 显示最新一条的标题
                latest = feed.entries[0]
                print(f"   📰 最新: {latest.title[:50]}...")

        except Exception as e:
            print(f"   ❌ 失败: {e}")


def test_kimi_api():
    """测试 Kimi API 是否可用"""
    import requests

    print("\n" + "=" * 50)
    print("测试 Kimi API")
    print("=" * 50)

    api_key = os.environ.get('KIMI_API_KEY')

    if not api_key:
        print("❌ 未找到 KIMI_API_KEY 环境变量")
        print("   请设置: export KIMI_API_KEY='sk-xxxxx'")
        return

    print(f"✅ API Key 已加载: {api_key[:15]}...")

    # 测试请求
    url = "https://api.moonshot.cn/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            print("✅ API 连接成功!")
            models = resp.json().get('data', [])
            print(f"   可用模型: {len(models)} 个")
            for m in models[:3]:
                print(f"   - {m.get('id', 'unknown')}")
        else:
            print(f"❌ API 错误: {resp.status_code}")
            print(f"   {resp.text[:200]}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")


def test_summary():
    """测试摘要生成功能"""
    import requests
    import re
    import html

    print("\n" + "=" * 50)
    print("测试摘要生成")
    print("=" * 50)

    api_key = os.environ.get('KIMI_API_KEY')
    if not api_key:
        print("❌ 请先设置 KIMI_API_KEY")
        return

    # 测试文章
    test_title = "OpenAI 发布 GPT-5，推理能力提升 10 倍"
    test_content = """
    OpenAI 今日正式发布 GPT-5 大语言模型。据官方介绍，GPT-5 在推理能力上比 GPT-4 提升 10 倍，
    支持多模态输入（文本、图像、音频），并且 API 价格降低 50%。
    新模型已面向所有开发者开放，预计将在未来几周内推送给 ChatGPT Plus 用户。
    """

    print(f"\n测试标题: {test_title}")

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        prompt = f"用一句话（不超过25个字）总结这篇科技新闻：\n\n标题：{test_title}\n内容：{test_content}\n\n摘要："

        payload = {
            "model": "moonshot-v1-8k",
            "messages": [
                {"role": "system", "content": "你是Kimi，擅长用一句话总结科技新闻。严格控制字数在25字以内。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 50
        }

        resp = requests.post(
            "https://api.moonshot.cn/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if resp.status_code == 200:
            result = resp.json()
            summary = result['choices'][0]['message']['content'].strip()
            summary = summary.replace('摘要：', '').replace('总结：', '')
            print(f"✅ 生成成功!")
            print(f"   📝 {summary}")
        else:
            print(f"❌ API 错误: {resp.status_code}")
            print(f"   {resp.text[:200]}")

    except Exception as e:
        print(f"❌ 生成失败: {e}")


def main():
    """主函数"""
    print("""
╔════════════════════════════════════════╗
║     Daily Letter - 本地测试工具       ║
╚════════════════════════════════════════╝
""")

    if len(sys.argv) < 2:
        print("用法:")
        print("  python test_locally.py rss      # 测试 RSS 源")
        print("  python test_locally.py api      # 测试 Kimi API")
        print("  python test_locally.py summary  # 测试摘要生成")
        print("  python test_locally.py all      # 运行全部测试")
        return

    command = sys.argv[1]

    if command == 'rss':
        test_rss_sources()
    elif command == 'api':
        test_kimi_api()
    elif command == 'summary':
        test_summary()
    elif command == 'all':
        test_rss_sources()
        test_kimi_api()
        test_summary()
    else:
        print(f"未知命令: {command}")

    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)


if __name__ == '__main__':
    main()
