#!/usr/bin/env python3
"""
MiniMax 招聘 — 职位查询脚本

MiniMax 使用飞书招聘页面，为 JS 动态渲染 SPA，需使用 Crawl4AI 渲染后提取。
URL: https://vrfi1sk8a0.jobs.feishu.cn/index/position/list

用法:
  python query.py --keyword "AI"
  python query.py --keyword "算法"
"""

import argparse
import asyncio
import json
import os
import re
import sys

os.environ["CRAWL4_AI_BASE_DIRECTORY"] = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig


def parse_jobs_from_markdown(markdown, keyword):
    """从 Markdown 中提取飞书招聘职位"""
    jobs = []
    lines = markdown.split('\n')
    current_job = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 检测地点+类型行（如 "广州社招全职"）
        loc_match = re.match(r'^([\u4e00-\u9fa5、]+?)(社招|校招|实习|全职)', line)
        if loc_match and current_job:
            current_job["location"] = re.split(r'[、,，]', loc_match.group(1))[0]
            current_job["jobType"] = loc_match.group(2)
            continue

        # 跳过非标题行
        if len(line) < 4 or len(line) > 80:
            continue
        if re.match(r'^\d+[、.．\-]', line):
            continue
        if line.startswith('-') or line.startswith('—'):
            continue
        if re.match(r'^[a-z]', line):
            continue
        if re.match(r'^(岗位背景|你将负责|团队介绍|要求|职责|任职)', line):
            continue

        # 检测职位标题
        job_keywords = ['实习', '工程师', '开发', '算法', '产品', '运营', '设计',
                        '分析师', '研究员', '经理', 'Agent', 'LLM', 'AI', '大模型',
                        '前端', '后端', '测试', '数据', '架构', '安全', '负责人',
                        '销售', '增长', '技术', '美术']
        is_job = any(kw in line for kw in job_keywords)

        if is_job and re.match(r'^[\u4e00-\u9fa5A-Z]', line):
            if current_job and current_job["title"]:
                jobs.append(current_job)
            current_job = {
                "id": "", "title": line, "company": "MiniMax",
                "location": "", "description": "", "requirements": "",
                "salary": "", "url": "", "source": "minimax",
                "publishDate": "", "jobType": "",
            }

    if current_job and current_job["title"]:
        jobs.append(current_job)

    if keyword:
        kw = keyword.lower()
        jobs = [j for j in jobs
                if kw in j["title"].lower()
                or kw in j["location"].lower()
                or kw in j["jobType"].lower()]

    return jobs


async def fetch_jobs(keyword, job_type=""):
    url = "https://vrfi1sk8a0.jobs.feishu.cn/index/position/list"

    config = CrawlerRunConfig(
        wait_until="networkidle",
        page_timeout=30000,
        delay_before_return_html=3.0,
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=url, config=config)
        if not result.success:
            raise RuntimeError("页面加载失败")
        return parse_jobs_from_markdown(result.markdown, keyword)


def main():
    parser = argparse.ArgumentParser(description="MiniMax招聘职位查询")
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--type", default="", help="招聘类型筛选")
    args = parser.parse_args()

    try:
        jobs = asyncio.run(fetch_jobs(args.keyword, args.type))
        print(json.dumps(jobs, ensure_ascii=False, indent=2))
        print(f"[minimax] 共 {len(jobs)} 条结果", file=sys.stderr)
    except Exception as e:
        print(f"[minimax] 错误: {e}", file=sys.stderr)
        print("[]")
        sys.exit(1)


if __name__ == "__main__":
    main()
