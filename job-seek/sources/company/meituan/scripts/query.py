#!/usr/bin/env python3
"""
美团招聘 — 职位查询脚本

美团招聘提供隐藏 API，可直接 HTTP POST 获取职位数据，无需浏览器。
API: https://zhaopin.meituan.com/api/official/job/getJobList

用法:
  python query.py --keyword "AI"
  python query.py --keyword "Java" --type social
"""

import argparse
import json
import sys

import requests


BASE_URL = "https://zhaopin.meituan.com"

# 招聘类型映射
JOB_TYPE_MAP = {
    "campus": 1,
    "social": 2,
    "intern": 3,
}


def fetch_jobs(keyword, job_type="campus", page_num=1, page_size=50):
    """调用美团招聘隐藏 API"""
    url = f"{BASE_URL}/api/official/job/getJobList"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/web/campus",
    }

    body = {
        "pageSize": page_size,
        "pageNum": page_num,
        "recruitType": JOB_TYPE_MAP.get(job_type, 1),
    }
    if keyword:
        body["keyWords"] = keyword

    resp = requests.post(url, json=body, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    records = data.get("data", {}).get("list", []) or []
    jobs = []
    for record in records:
        city_list = record.get("cityList", [])
        location = city_list[0].get("name", "") if city_list else ""

        jobs.append({
            "id": record.get("jobUnionId", ""),
            "title": record.get("name", ""),
            "company": "美团",
            "location": location,
            "description": record.get("jobDuty", ""),
            "requirements": record.get("jobRequirement", ""),
            "salary": "",
            "url": f"{BASE_URL}/web/campus/detail/{record.get('jobUnionId', '')}",
            "source": "meituan",
            "publishDate": record.get("publishDate", ""),
            "jobType": record.get("recruitTypeName", ""),
        })
    return jobs


def main():
    parser = argparse.ArgumentParser(description="美团招聘职位查询")
    parser.add_argument("--keyword", default="", help="搜索关键词")
    parser.add_argument("--type", default="campus", choices=["campus", "social", "intern"])
    parser.add_argument("--page-num", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=50)
    args = parser.parse_args()

    try:
        jobs = fetch_jobs(args.keyword, args.type, args.page_num, args.page_size)
        print(json.dumps(jobs, ensure_ascii=False, indent=2))
        print(f"[meituan] 共 {len(jobs)} 条结果", file=sys.stderr)
    except Exception as e:
        print(f"[meituan] 错误: {e}", file=sys.stderr)
        print("[]")
        sys.exit(1)


if __name__ == "__main__":
    main()
