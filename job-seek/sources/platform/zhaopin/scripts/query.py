#!/usr/bin/env python3
"""
智联招聘 — 职位查询脚本

智联招聘提供隐藏 API，可通过 POST 请求直接获取职位数据，无需浏览器。
API: https://fe-api.zhaopin.com/c/i/search/positions

用法:
  python query.py --keyword "AI"
  python query.py --keyword "Agent" --city "北京"
"""

import argparse
import json
import sys
import uuid

import requests


def fetch_jobs(keyword, city="", page_index=1, page_size=50):
    """调用智联招聘 API"""
    request_id = str(uuid.uuid4())
    api_url = (
        f"https://fe-api.zhaopin.com/c/i/search/positions"
        f"?_v=0.43240637&x-zp-page-request-id={request_id}"
    )

    body = {
        "S_SOU_FULL_INDEX": keyword,
        "S_SOU_WORK_CITY": city,
        "order": 4,
        "pageIndex": page_index,
        "pageSize": page_size,
        "anonymous": 1,
    }
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Origin": "https://www.zhaopin.com",
        "Referer": "https://www.zhaopin.com/",
    }

    resp = requests.post(api_url, json=body, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    positions = data.get("data", {}).get("list", []) or []
    jobs = []
    for pos in positions:
        salary = pos.get("salary60", "") or pos.get("salaryReal", "")
        if not salary:
            card_json_str = pos.get("cardCustomJson", "")
            if card_json_str:
                try:
                    card_json = json.loads(card_json_str)
                    salary = card_json.get("salary60", "")
                except (json.JSONDecodeError, TypeError):
                    pass

        jobs.append({
            "id": str(pos.get("jobId", "")),
            "title": pos.get("name", ""),
            "company": pos.get("companyName", ""),
            "location": pos.get("cityDistrict", "") or pos.get("workCity", ""),
            "description": pos.get("jobSummary", ""),
            "requirements": "",
            "salary": salary,
            "url": pos.get("positionURL", "") or pos.get("positionUrl", ""),
            "source": "zhaopin",
            "publishDate": pos.get("publishTime", "") or pos.get("firstPublishTime", ""),
            "jobType": pos.get("propertyName", "") or pos.get("workType", ""),
        })
    return jobs


def main():
    parser = argparse.ArgumentParser(description="智联招聘职位查询")
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--city", default="", help="城市筛选")
    parser.add_argument("--page-index", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=50)
    args = parser.parse_args()

    try:
        jobs = fetch_jobs(args.keyword, args.city, args.page_index, args.page_size)
        print(json.dumps(jobs, ensure_ascii=False, indent=2))
        print(f"[zhaopin] 共 {len(jobs)} 条结果", file=sys.stderr)
    except Exception as e:
        print(f"[zhaopin] 错误: {e}", file=sys.stderr)
        print("[]")
        sys.exit(1)


if __name__ == "__main__":
    main()