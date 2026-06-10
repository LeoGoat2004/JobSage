---
name: jobsage
description: JobSage 技能集合 — 就业指导相关的多个子模块。触发关键词：找工作、求职、招聘、岗位、实习、校招、社招、内推、春招、秋招。
---

# JobSage — 就业指导技能集合

JobSage 是一个就业指导技能集合，包含多个子模块，按需调用。

## 子模块

| 子模块 | 说明 |
|--------|------|
| [job-seek](job-seek/SKILL.md) | 就业咨询 — 从多个数据源检索岗位信息 |

## 使用方式

当用户提出求职相关需求时，读取对应子模块的 SKILL.md，按其说明执行。

## 目录结构

```
JobSage/
├── job-sage/       ← 总入口
│   └── SKILL.md
└── job-seek/       ← 子模块
    ├── SKILL.md
    ├── sources/
    └── dashboard/
```