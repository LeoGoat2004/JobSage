#!/usr/bin/env python3
"""
JobSage Dashboard — Flask 后端服务

提供 REST API 端点，调用各数据源查询脚本获取职位数据。
启动: python server.py
访问: http://localhost:5000
"""

import json
import os
import subprocess
import sys

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder="static", static_url_path="/static")

# 项目根目录
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 数据源配置: key -> (目录路径, 默认参数)
SOURCES = {
    "tencent":   {"dir": "sources/company/tencent",   "method": "api"},
    "meituan":   {"dir": "sources/company/meituan",   "method": "api"},
    "bilibili":  {"dir": "sources/company/bilibili",  "method": "api"},
    "jd":        {"dir": "sources/company/jd",        "method": "html"},
    "zhaopin":   {"dir": "sources/platform/zhaopin",  "method": "api"},
    "bytedance": {"dir": "sources/company/bytedance", "method": "crawl4ai"},
    "huawei":    {"dir": "sources/company/huawei",    "method": "crawl4ai"},
    "minimax":   {"dir": "sources/company/minimax",   "method": "crawl4ai"},
    "zhipu":     {"dir": "sources/company/zhipu",     "method": "crawl4ai"},
}

# 数据源中文名
SOURCE_NAMES = {
    "tencent": "腾讯招聘", "meituan": "美团招聘", "bilibili": "哔哩哔哩",
    "jd": "京东招聘", "zhaopin": "智联招聘",
    "bytedance": "字节跳动", "huawei": "华为招聘", "minimax": "MiniMax", "zhipu": "智谱AI",
}

# 数据源分类
SOURCE_CATEGORIES = {
    "company": ["tencent", "meituan", "bilibili", "jd", "bytedance", "huawei", "minimax", "zhipu"],
    "platform": ["zhaopin"],
}


def run_query_script(source_key, keyword, job_type=""):
    """调用指定数据源的查询脚本"""
    source = SOURCES.get(source_key)
    if not source:
        return []

    script_path = os.path.join(PROJECT_ROOT, source["dir"], "scripts", "query.py")
    if not os.path.exists(script_path):
        return []

    cmd = [sys.executable, script_path, "--keyword", keyword]
    if job_type:
        cmd.extend(["--type", job_type])

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60,
            cwd=os.path.dirname(script_path),
            env={**os.environ, "CRAWL4_AI_BASE_DIRECTORY": os.path.join(PROJECT_ROOT, ".crawl4ai")},
        )
        if result.returncode == 0 and result.stdout.strip():
            jobs = json.loads(result.stdout.strip())
            return jobs
        return []
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception):
        return []


@app.route("/")
def index():
    """返回 Dashboard 页面"""
    return send_from_directory(".", "index.html")


@app.route("/api/sources")
def get_sources():
    """获取所有数据源信息"""
    sources = []
    for key, info in SOURCES.items():
        sources.append({
            "key": key,
            "name": SOURCE_NAMES.get(key, key),
            "method": info["method"],
            "category": "platform" if key in SOURCE_CATEGORIES["platform"] else "company",
        })
    return jsonify(sources)


@app.route("/api/search")
def search():
    """搜索职位: ?keyword=AI&sources=tencent,meituan&type=campus"""
    keyword = request.args.get("keyword", "").strip()
    sources_param = request.args.get("sources", "")
    job_type = request.args.get("type", "")

    if not keyword:
        return jsonify({"error": "请提供关键词"}), 400

    # 确定要查询的数据源
    if sources_param:
        target_sources = [s.strip() for s in sources_param.split(",") if s.strip() in SOURCES]
    else:
        # 默认查询所有直接 HTTP 数据源（速度快）
        target_sources = [k for k, v in SOURCES.items() if v["method"] != "crawl4ai"]

    all_jobs = []
    errors = []

    for source_key in target_sources:
        jobs = run_query_script(source_key, keyword, job_type)
        all_jobs.extend(jobs)
        if not jobs:
            errors.append(source_key)

    return jsonify({
        "keyword": keyword,
        "total": len(all_jobs),
        "sources_queried": target_sources,
        "sources_empty": errors,
        "jobs": all_jobs,
    })


@app.route("/api/search/<source_key>")
def search_source(source_key):
    """搜索单个数据源: /api/search/tencent?keyword=AI"""
    keyword = request.args.get("keyword", "").strip()
    job_type = request.args.get("type", "")

    if not keyword:
        return jsonify({"error": "请提供关键词"}), 400
    if source_key not in SOURCES:
        return jsonify({"error": f"未知数据源: {source_key}"}), 404

    jobs = run_query_script(source_key, keyword, job_type)
    return jsonify({
        "source": source_key,
        "name": SOURCE_NAMES.get(source_key, source_key),
        "total": len(jobs),
        "jobs": jobs,
    })


if __name__ == "__main__":
    print("=" * 50)
    print("  JobSage Dashboard 启动中...")
    print(f"  项目目录: {PROJECT_ROOT}")
    print(f"  访问地址: http://localhost:5000")
    print("=" * 50)
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("FLASK_DEBUG", "").lower() == "true")
