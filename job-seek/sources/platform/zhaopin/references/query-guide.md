# 智联招聘 — 查询指南

## 数据源信息

- **类型**：招聘平台
- **获取方式**：隐藏 API
- **脚本**：`python scripts/query.py --keyword "关键词" --city "城市"`

## API 详情

- **Endpoint**：`POST https://fe-api.zhaopin.com/c/i/search/positions?_v=0.43240637&x-zp-page-request-id={uuid}`
- **Content-Type**：`application/json`
- **Body**：

```json
{
  "S_SOU_FULL_INDEX": "AI",
  "S_SOU_WORK_CITY": "北京",
  "order": 4,
  "pageIndex": 1,
  "pageSize": 10,
  "anonymous": 1
}
```

| 参数 | 说明 |
|------|------|
| S_SOU_FULL_INDEX | 搜索关键词 |
| S_SOU_WORK_CITY | 工作城市 |
| order | 排序方式 |
| pageIndex | 页码 |
| pageSize | 每页条数 |
| anonymous | 匿名标识 |

**必需 Headers**：

| Header | 值 |
|--------|-----|
| Content-Type | `application/json;charset=UTF-8` |
| User-Agent | 标准浏览器 User-Agent |
| Origin | `https://www.zhaopin.com` |
| Referer | `https://www.zhaopin.com/` |

## 返回数据

响应 JSON 中 `data.list` 数组，每项字段：

| 字段 | 说明 |
|------|------|
| jobId | 职位 ID |
| name | 职位名称 |
| companyName | 公司名称 |
| cityDistrict | 城市区域 |
| salary60 | 薪资范围 |
| positionURL | 职位详情链接 |
| publishTime | 发布时间 |

## 使用示例

```bash
# 基本查询
python scripts/query.py --keyword "AI" --city "北京"

# 其他城市
python scripts/query.py --keyword "产品经理" --city "上海"
```

## 注意事项

- API 非公开文档，接口可能变更
- URL 中 `_v` 和 `x-zp-page-request-id` 参数需动态生成（uuid）