#!/usr/bin/env python3
"""
京东招聘 — 职位查询脚本

京东招聘页面为服务端渲染，HTML 中直接包含职位表格数据，
可直接 HTTP GET 获取并解析，无需浏览器。
URL: https://zhaopin.jd.com/home

用法:
  python query.py --keyword "AI"
  python query.py --keyword "Java"
"""

import argparse
import json
import re
import sys

import requests


def fetch_jobs(keyword):
    """获取京东招聘页面并解析职位表格"""
    url = "https://zhaopin.jd.com/home"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    html = resp.text

    jobs = []

    # 提取热招职位表格区域
    table_match = re.search(r'热招职位[\s\S]*?<table[^>]*>([\s\S]*?)</table>', html, re.IGNORECASE)
    if not table_match:
        return jobs

    table_content = table_match.group(1)

    # 提取所有行
    for row_match in re.finditer(r'<tr[^>]*>([\s\S]*?)</tr>', table_content, re.IGNORECASE):
        cells = []
        for cell_match in re.finditer(r'<td[^>]*>([\s\S]*?)</td>', row_match.group(1), re.IGNORECASE):
            link = re.search(r'<a[^>]*href="([^"]*)"[^>]*>([\s\S]*?)</a>', cell_match.group(1), re.IGNORECASE)
            if link:
                text = re.sub(r'<[^>]+>', '', link.group(2)).strip()
                href = link.group(1).strip()
                cells.append((text, href))
            else:
                text = re.sub(r'<[^>]+>', '', cell_match.group(1)).strip()
                cells.append((text, ''))

        # 京东表格: [职位名称, 职位类别, 工作地点, 发布时间]
        if len(cells) >= 4:
            title, url_link = cells[0]
            category = cells[1][0]
            location = cells[2][0]
            publish_date = cells[3][0]

            if keyword:
                kw = keyword.lower()
                if kw not in title.lower() and kw not in category.lower() and kw not in location.lower():
                    continue

            jobs.append({
                "id": "",
                "title": title,
                "company": "京东",
                "location": location,
                "description": "",
                "requirements": "",
                "salary": "",
                "url": url_link,
                "source": "jd",
                "publishDate": publish_date,
                "jobType": category,
            })

    return jobs


def main():
    parser = argparse.ArgumentParser(description="京东招聘职位查询")
    parser.add_argument("--keyword", default="", help="搜索关键词")
    args = parser.parse_args()

    try:
        jobs = fetch_jobs(args.keyword)
        print(json.dumps(jobs, ensure_ascii=False, indent=2))
        print(f"[jd] 共 {len(jobs)} 条结果", file=sys.stderr)
    except Exception as e:
        print(f"[jd] 错误: {e}", file=sys.stderr)
        print("[]")
        sys.exit(1)


if __name__ == "__main__":
    main()
