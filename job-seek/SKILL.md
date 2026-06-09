---
name: job-seek
description: 就业咨询子模块 — 从多个数据源检索岗位信息。支持腾讯、美团、哔哩哔哩、京东、字节跳动、华为、MiniMax、智谱AI等公司直招，以及智联招聘等招聘平台。触发关键词：找工作、求职、招聘、岗位、实习、校招、社招、内推、春招、秋招。
---

# JobSeek — 就业咨询

JobSeek 帮助用户从多个合法合规的招聘数据源检索岗位信息，提供结构化的职位数据。

## 任务目标

- 本技能用于：根据用户求职需求，从公司直招和招聘平台两类数据源检索匹配的岗位
- 触发条件：当用户需要找工作、查岗位、了解招聘信息时使用

## 数据源分类

### 公司直招（8家）

| 公司 | 目录路径 | 获取方式 |
|------|----------|----------|
| 腾讯招聘 | `sources/company/tencent/` | REST API |
| 美团招聘 | `sources/company/meituan/` | 隐藏 API |
| 哔哩哔哩 | `sources/company/bilibili/` | 隐藏 API（CSRF） |
| 京东招聘 | `sources/company/jd/` | 服务端 HTML 解析 |
| 字节跳动 | `sources/company/bytedance/` | Crawl4AI 无头浏览器 |
| 华为招聘 | `sources/company/huawei/` | Crawl4AI 无头浏览器 |
| MiniMax | `sources/company/minimax/` | Crawl4AI 无头浏览器 |
| 智谱AI | `sources/company/zhipu/` | Crawl4AI 无头浏览器 |

### 招聘平台（1家）

| 平台 | 目录路径 | 获取方式 |
|------|----------|----------|
| 智联招聘 | `sources/platform/zhaopin/` | 隐藏 API |

## 统一职位数据结构

所有数据源返回的数据映射为以下统一结构：

```typescript
interface Job {
  id: string;              // 唯一标识
  title: string;          // 职位名称
  company: string;        // 公司名称
  location: string;       // 工作地点
  description: string;    // 职位描述
  requirements?: string;   // 岗位要求
  salary?: string;         // 薪资范围
  url: string;             // 原始链接
  source: string;          // 数据源标识
  publishDate?: string;    // 发布日期
  jobType?: string;        // 职位类型：社招/校招/实习
}
```

## 执行流程

### 步骤1：意图识别

根据用户输入判断：
- 目标公司（如"腾讯"、"字节"）→ 指定公司直招数据源
- 目标平台（如"智联"）→ 指定招聘平台数据源
- 通用求职（如"找AI岗位"）→ 多数据源并行检索

### 步骤2：数据源选择

1. 用户指定公司 → 读取对应 `sources/company/{name}/references/query-guide.md`
2. 用户指定平台 → 读取对应 `sources/platform/{name}/references/query-guide.md`
3. 用户未指定 → 优先从腾讯招聘（数据最全）检索，按需扩展其他数据源

### 步骤3：执行检索

按照 `query-guide.md` 中的说明执行检索，或直接运行脚本：

```bash
python sources/company/{name}/scripts/query.py --keyword "关键词"
```

获取方式说明：
- **REST API / 隐藏 API**：直接 HTTP 请求获取 JSON 数据，速度快、结构化好
- **服务端 HTML**：请求页面后解析 HTML 表格，无需浏览器
- **Crawl4AI 无头浏览器**：针对 JS 动态渲染 SPA 页面，使用 Crawl4AI 渲染后提取

### 步骤4：结果整合

将各数据源返回的原始数据映射为统一 Job 结构，按相关度排序后展示给用户。

## 输出格式

向用户展示结构化的职位列表：

```markdown
## 检索结果（共 N 条）

| # | 职位名称 | 公司 | 地点 | 类型 | 薪资 |
|---|----------|------|------|------|------|
| 1 | xxx | 腾讯 | 深圳 | 社招 | 面议 |

### 职位详情
**职位名称**：xxx
**公司**：xxx
**地点**：xxx
**描述**：xxx
**链接**：xxx
```

## 工作台

可选的可视化界面，用于浏览器中直接检索：

```bash
cd dashboard
python server.py
# 浏览器打开 http://localhost:5000
```

## 错误处理

- 数据源不可达：提示用户该数据源暂时不可用，建议尝试其他数据源
- 无匹配结果：建议调整关键词或更换数据源
- 请求频率限制：适当延迟后重试

## 合规声明

所有数据源均通过合法合规方式获取公开招聘信息，不涉及登录绕过、验证码破解等违规行为。