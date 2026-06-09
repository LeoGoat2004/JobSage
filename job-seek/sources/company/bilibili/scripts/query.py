#!/usr/bin/env python3
"""
哔哩哔哩招聘 — 职位查询脚本

B站招聘提供隐藏 API，需先获取 CSRF token 再请求职位列表，无需浏览器。
API:
  Step 1: GET  https://jobs.bilibili.com/api/auth/v1/csrf/token
  Step 2: POST https://jobs.bilibili.com/api/srs/position/positionList (社招)
          POST https://jobs.bilibili.com/api/campus/position/positionList (校招)

用法:
  python query.py --keyword "算法" --type social
  python query.py --keyword "前端" --type campus
"""

import argparse
import json
import sys

import requests


BASE_URL = "https://jobs.bilibili.com"

COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "X-AppKey": "ops.ehr-api.auth",
    "X-UserType": "2",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/social",
}


def _get_csrf(session):
    """Step 1: 获取 CSRF token"""
    resp = session.get(f"{BASE_URL}/api/auth/v1/csrf/token", headers=COMMON_HEADERS, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", "")


def fetch_jobs(keyword, job_type="social", page_num=1, page_size=50):
    """调用B站招聘隐藏 API"""
    session = requests.Session()

    # Step 1: 获取 CSRF token
    csrf = _get_csrf(session)

    # Step 2: 请求职位列表
    if job_type == "campus":
        api_path = "/api/campus/position/positionList"
    else:
        api_path = "/api/srs/position/positionList"

    url = f"{BASE_URL}{api_path}"
    headers = {**COMMON_HEADERS, "X-CSRF": csrf, "Content-Type": "application/json;charset=UTF-8"}

    body = {
        "pageSize": page_size,
        "pageNum": page_num,
    }
    if keyword:
        body["keyWords"] = keyword

    resp = session.post(url, json=body, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    records = data.get("data", {}).get("list", []) or []
    jobs = []
    for record in records:
        work_location = record.get("workLocation", "")
        location = work_location.split(",")[0] if work_location else ""

        jobs.append({
            "id": str(record.get("id", "")),
            "title": record.get("positionName", ""),
            "company": "哔哩哔哩",
            "location": location,
            "description": record.get("positionDescription", ""),
            "requirements": "",
            "salary": "",
            "url": f"{BASE_URL}/social/position/{record.get('id', '')}",
            "source": "bilibili",
            "publishDate": record.get("publishTime", ""),
            "jobType": "校招" if record.get("recruitType") == 1 else "社招",
        })
    return jobs


def main():
    parser = argparse.ArgumentParser(description="哔哩哔哩招聘职位查询")
    parser.add_argument("--keyword", default="", help="搜索关键词")
    parser.add_argument("--type", default="social", choices=["social", "campus"])
    parser.add_argument("--page-num", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=50)
    args = parser.parse_args()

    try:
        jobs = fetch_jobs(args.keyword, args.type, args.page_num, args.page_size)
        print(json.dumps(jobs, ensure_ascii=False, indent=2))
        print(f"[bilibili] 共 {len(jobs)} 条结果", file=sys.stderr)
    except Exception as e:
        print(f"[bilibili] 错误: {e}", file=sys.stderr)
        print("[]")
        sys.exit(1)


if __name__ == "__main__":
    main()
