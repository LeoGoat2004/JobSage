---
name: jobsage
description: JobSage 技能集合 — 就业指导相关的多个子模块。触发关键词：找工作、求职、招聘、岗位、实习、校招、社招、内推、春招、秋招。
---

# JobSage — 就业指导技能集合

JobSage 是一个就业咨询技能集合，包含多个子模块，按需调用。

## 子模块

| 子模块 | 说明 |
|--------|------|
| [job-seek](job-seek/SKILL.md) | 就业咨询 — 从多个数据源检索岗位信息，支持 9 个招聘网站 |

## 使用方式

当用户提出求职相关需求时，读取对应子模块的 SKILL.md，按其说明执行。

## 目录结构

```
JobSage/
├── SKILL.md       ← 总入口（本文档）
└── job-seek/      ← 子模块
    ├── SKILL.md   ← 子模块入口
    ├── sources/   ← 数据源脚本
    │   ├── company/   （8家公司）
    │   └── platform/  （1个平台）
    └── dashboard/ ← 可视化工作台
        ├── server.py
        └── index.html
```