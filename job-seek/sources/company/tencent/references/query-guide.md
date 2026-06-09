# 腾讯招聘 — 查询指南

## 数据源信息

- **类型**：公司直招
- **获取方式**：REST API (公开)
- **脚本**：`python scripts/query.py --keyword "关键词"`

## API 详情

- **Endpoint**：`GET https://careers.tencent.com/tencentcareer/api/post/Query`
- **参数**：

| 参数 | 说明 |
|------|------|
| keyword | 搜索关键词 |
| pageIndex | 页码 |
| pageSize | 每页条数 |
| language | 固定 `zh-cn` |
| area | 固定 `cn` |

## 返回数据

响应 JSON 中 `Posts` 数组，每项字段：

| 字段 | 说明 |
|------|------|
| PostId | 职位 ID |
| RecruitPostName | 职位名称 |
| LocationName | 工作地点 |
| Responsibility | 岗位职责 |
| Requirement | 任职要求 |
| PostTime | 发布时间 |
| CategoryName | 职位类别 |

## 使用示例

```bash
# 基本查询
python scripts/query.py --keyword "AI"

# 翻页查询
python scripts/query.py --keyword "AI" --page 2
```

## 注意事项

- API 为公开接口，无需认证
- language 和 area 参数建议保持默认值
