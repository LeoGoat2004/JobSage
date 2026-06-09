#!/usr/bin/env python3
"""
华为招聘 — 职位查询脚本

华为招聘网站为 JS 动态渲染 SPA，需使用 Crawl4AI 渲染页面后提取。
URL: https://career.huawei.com/reccampportal/portal5/campus-recruitment.html

用法:
  python query.py --keyword "AI" --type campus
  python query.py --keyword "芯片" --type social
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
    """从 Markdown 中提取华为职位"""
    jobs = []
    lines = markdown.split('\n')
    current_job = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 检测类别行（如 "研发类"）
        cat_match = re.match(r'^(研发类|销售类|服务类|设计类|供应链类|职能类|市场类|人力资源类|财经类|法务类)$', line)
        if cat_match and current_job:
            current_job["jobType"] = cat_match.group(1)
            jobs.append(current_job)
            current_job = None
            continue

        # 检测地点行（如 "中国/深圳"）
        if current_job and not current_job["location"] and re.match(r'^(中国/|全球)', line):
            current_job["location"] = re.sub(r'中国/', '', line).split(',')[0]
            continue

        # 跳过非标题行
        if len(line) < 3 or len(line) > 60:
            continue
        if re.match(r'^(共\d+条|应届生|实习生|留学生|职位搜索|类型|职类|不限|国家|城市|关键字|搜索|下一页|社会招聘)', line):
            continue

        # 检测职位标题
        job_keywords = ['工程师', '经理', '专员', '分析师', '架构师', '顾问',
                        'AI', '算法', '开发', '数据', '产品', '运营', '设计', '测试',
                        '安全', '客户', '销售', '人力', '财务', '法务', '供应链']
        is_job = any(kw in line for kw in job_keywords)

        if is_job and re.match(r'^[\u4e00-\u9fa5A-Z]', line) and '版权' not in line:
            if current_job and current_job["title"]:
                jobs.append(current_job)
            current_job = {
                "id": "", "title": line, "company": "华为",
                "location": "", "description": "", "requirements": "",
                "salary": "", "url": "", "source": "huawei",
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


async def fetch_jobs(keyword, job_type="campus"):
    type_path = "social-recruitment" if job_type == "social" else "campus-recruitment"
    url = f"https://career.huawei.com/reccampportal/portal5/{type_path}.html"
    if keyword:
        url += f"?searchText={keyword}"

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
    parser = argparse.ArgumentParser(description="华为招聘职位查询")
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--type", default="campus", choices=["campus", "social"])
    args = parser.parse_args()

    try:
        jobs = asyncio.run(fetch_jobs(args.keyword, args.type))
        print(json.dumps(jobs, ensure_ascii=False, indent=2))
        print(f"[huawei] 共 {len(jobs)} 条结果", file=sys.stderr)
    except Exception as e:
        print(f"[huawei] 错误: {e}", file=sys.stderr)
        print("[]")
        sys.exit(1)


if __name__ == "__main__":
    main()
