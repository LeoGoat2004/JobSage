# 哔哩哔哩 — 查询指南

## 数据源信息

- **类型**：公司直招
- **获取方式**：隐藏 API (需 CSRF)
- **脚本**：`python scripts/query.py --keyword "关键词" --type social`

## API 详情

**Step 1 — 获取 CSRF Token**

- `GET https://jobs.bilibili.com/api/auth/v1/csrf/token`

**Step 2 — 查询职位**

- 社招：`POST https://jobs.bilibili.com/api/srs/position/positionList`
- 校招：`POST https://jobs.bilibili.com/api/campus/position/positionList`

**必需 Headers**：

| Header | 值 |
|--------|-----|
| X-AppKey | `ops.ehr-api.auth` |
| X-UserType | `2` |
| X-CSRF | Step 1 返回的 token |

## 返回数据

响应列表，每项字段：

| 字段 | 说明 |
|------|------|
| id | 职位 ID |
| positionName | 职位名称 |
| workLocation | 工作地点 |
| positionDescription | 岗位描述 |
| recruitType | 招聘类型 |

## 使用示例

```bash
# 社招查询
python scripts/query.py --keyword "算法" --type social

# 校招查询
python scripts/query.py --keyword "算法" --type campus
```

## 注意事项

- 必须先获取 CSRF token 再请求职位接口
- 社招与校招使用不同的 API endpoint
