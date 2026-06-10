# JobSage — 就业指导技能集合

就业指导相关的多个子模块，按需调用。

## 子模块

| 子模块 | 说明 |
|--------|------|
| [job-sage/SKILL.md](job-sage/SKILL.md) | 总入口 |
| [job-seek](job-seek/SKILL.md) | 就业咨询 — 从多个数据源检索岗位信息 |

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

## 工作台

```bash
cd job-seek/dashboard
python server.py
# 浏览器打开 http://localhost:5000
```