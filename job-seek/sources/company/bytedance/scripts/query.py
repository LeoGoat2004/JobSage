#!/usr/bin/env python3
"""
字节跳动招聘 — 职位查询脚本

字节跳动招聘网站为 JS 动态渲染 SPA，需使用 Crawl4AI 渲染页面后提取。
URL: https://jobs.bytedance.com/{type}/position?keyword=xxx

用法:
  python query.py --keyword "Agent" --type campus
  python query.py --keyword "算法" --type experienced
"""

import argparse
import asyncio
import json
import os
import re
import sys

# Crawl4AI 缓存目录设为项目内，避免用户主目录 SQLite 兼容问题
os.environ["CRAWL4_AI_BASE_DIRECTORY"] = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig


def parse_jobs_from_markdown(markdown, keyword):
    """从 Crawl4AI 输出的 Markdown 中提取职位

    字节招聘页面的 Markdown 格式为紧凑单行：
    [ 标题 地点+类型...职位 ID：xxx 描述...]
    """
    jobs = []

    # 匹配以 [ 开头的职位行，提取完整内容
    for match in re.finditer(r'\[\s*([\u4e00-\u9fa5A-Z].*?)\]', markdown):
        content = match.group(1).strip()
        if not content:
            continue

        # 提取职位 ID
        job_id = ""
        id_match = re.search(r'职位\s*ID[：:]\s*([A-Z0-9]+)', content)
        if id_match:
            job_id = id_match.group(1)

        # 提取标题：取第一个中文/A-Z开头到地点关键词之前的部分
        # 格式如: "Agent开发实习生-中国交易与广告 杭州实习研发 - 前端ByteIntern..."
        title_match = re.match(r'^([\u4e00-\u9fa5A-Z][\u4e00-\u9fa5A-Za-z0-9\s\-/]+?)(?:\s+[\u4e00-\u9fa5]{2,4}(?:实习|正式|社招|校招))', content)
        if not title_match:
            # 备选：取到第一个"职位 ID"之前
            title_match = re.match(r'^(.+?)(?:职位\s*ID|ByteIntern)', content)
        if not title_match:
            continue

        title = title_match.group(1).strip().rstrip('-').strip()
        if len(title) < 4:
            continue

        # 提取地点+类型（地点为城市名，2-3个中文字符，在"实习/校招/社招"之前）
        location = ""
        job_type = ""
        loc_match = re.search(r'([\u4e00-\u9fa5]{2,3}?)(实习|正式|社招|校招)', content)
        if loc_match:
            candidate = loc_match.group(1)
            # 验证是否为城市名（排除"开发"、"前端"等非城市词）
            non_city_words = ['开发', '前端', '后端', '算法', '产品', '运营', '设计', '测试',
                              '数据', '架构', '安全', '研究', '工程', '技术', '平台', '系统']
            if not any(candidate.endswith(w) for w in non_city_words):
                location = candidate
            job_type = loc_match.group(2)

        # 关键词过滤
        if keyword:
            kw = keyword.lower()
            if kw not in title.lower() and kw not in location.lower() and kw not in job_type.lower():
                continue

        jobs.append({
            "id": job_id, "title": title, "company": "字节跳动",
            "location": location, "description": "", "requirements": "",
            "salary": "", "url": "", "source": "bytedance",
            "publishDate": "", "jobType": job_type,
        })

    return jobs


async def fetch_jobs(keyword, job_type="campus"):
    """使用 Crawl4AI 获取字节跳动招聘页面"""
    type_path = "campus" if job_type == "campus" else "experienced"
    url = f"https://jobs.bytedance.com/{type_path}/position?keyword={keyword}"

    config = CrawlerRunConfig(
        wait_until="networkidle",
        page_timeout=30000,
        delay_before_return_html=3.0,
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        if not result.success:
            raise RuntimeError(f"页面加载失败")
        return parse_jobs_from_markdown(result.markdown, keyword)


def main():
    parser = argparse.ArgumentParser(description="字节跳动招聘职位查询")
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--type", default="campus", choices=["campus", "experienced"])
    args = parser.parse_args()

    try:
        jobs = asyncio.run(fetch_jobs(args.keyword, args.type))
        print(json.dumps(jobs, ensure_ascii=False, indent=2))
        print(f"[bytedance] 共 {len(jobs)} 条结果", file=sys.stderr)
    except Exception as e:
        print(f"[bytedance] 错误: {e}", file=sys.stderr)
        print("[]")
        sys.exit(1)


if __name__ == "__main__":
    main()
