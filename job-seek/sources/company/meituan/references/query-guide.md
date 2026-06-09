# 美团招聘 — 查询指南

## 数据源信息

- **类型**：公司直招
- **获取方式**：隐藏 API
- **脚本**：`python scripts/query.py --keyword "关键词" --type campus`

## API 详情

- **Endpoint**：`POST https://zhaopin.meituan.com/api/official/job/getJobList`
- **Content-Type**：`application/json`
- **Body**：

```json
{
  "pageSize": 10,
  "pageNum": 1,
  "recruitType": 1,
  "keyWords": "AI"
}
```

| 参数 | 说明 |
|------|------|
| pageSize | 每页条数 |
| pageNum | 页码 |
| recruitType | 招聘类型：1=校招, 2=社招, 3=实习 |
| keyWords | 搜索关键词 |

## 返回数据

响应 JSON 列表，每项字段：

| 字段 | 说明 |
|------|------|
| name | 职位名称 |
| cityList | 工作城市列表 |
| jobDuty | 岗位职责 |
| jobRequirement | 任职要求 |
| jobUnionId | 职位 ID |
| recruitTypeName | 招聘类型名称 |

## 使用示例

```bash
# 校招查询
python scripts/query.py --keyword "AI" --type campus

# 社招查询
python scripts/query.py --keyword "AI" --type social

# 实习查询
python scripts/query.py --keyword "AI" --type intern
```

## 注意事项

- API 非公开文档，接口可能变更
- recruitType 映射：campus→1, social→2, intern→3
