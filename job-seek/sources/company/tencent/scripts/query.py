#!/usr/bin/env python3
"""
腾讯招聘 — 职位查询脚本

腾讯招聘提供公开 REST API，可直接 HTTP GET 获取职位数据，无需浏览器。
API: https://careers.tencent.com/tencentcareer/api/post/Query

用法:
  python query.py --keyword "AI"
  python query.py --keyword "Java" --page-size 20
"""

import argparse
import json
import sys

import requests


def fetch_jobs(keyword, page_index=1, page_size=50):
    """调用腾讯招聘公开 API"""
    url = "https://careers.tencent.com/tencentcareer/api/post/Query"
    params = {
        "keyword": keyword,
        "pageIndex": page_index,
        "pageSize": page_size,
        "language": "zh-cn",
        "area": "cn",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://careers.tencent.com/",
    }

    resp = requests.get(url, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    posts = (data.get("Data") or {}).get("Posts") or []
    jobs = []
    for post in posts:
        jobs.append({
            "id": post.get("PostId", ""),
            "title": post.get("RecruitPostName", ""),
            "company": "腾讯",
            "location": post.get("LocationName", ""),
            "description": post.get("Responsibility", ""),
            "requirements": post.get("Requirement", ""),
            "salary": "",
            "url": f"https://careers.tencent.com/jobdesc.html?postId={post.get('PostId', '')}",
            "source": "tencent",
            "publishDate": post.get("PostTime", ""),
            "jobType": post.get("CategoryName", ""),
        })
    return jobs


def main():
    parser = argparse.ArgumentParser(description="腾讯招聘职位查询")
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--page-index", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=50)
    args = parser.parse_args()

    try:
        jobs = fetch_jobs(args.keyword, args.page_index, args.page_size)
        print(json.dumps(jobs, ensure_ascii=False, indent=2))
        print(f"[tencent] 共 {len(jobs)} 条结果", file=sys.stderr)
    except Exception as e:
        print(f"[tencent] 错误: {e}", file=sys.stderr)
        print("[]")
        sys.exit(1)


if __name__ == "__main__":
    main()
