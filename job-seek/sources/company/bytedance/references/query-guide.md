# 字节跳动 — 查询指南

## 数据源信息

- **类型**：公司直招
- **获取方式**：Crawl4AI 无头浏览器 (JS 动态渲染 SPA)
- **脚本**：`python scripts/query.py --keyword "关键词" --type campus`

## API 详情

- **校招 URL**：`https://jobs.bytedance.com/campus/position?keyword=xxx`
- **社招 URL**：`https://jobs.bytedance.com/experienced/position?keyword=xxx`
- **渲染方式**：Crawl4AI 无头浏览器渲染后从 Markdown 提取职位信息

## 返回数据

从渲染后 Markdown 中提取职位列表，字段随页面结构而定。

## 使用示例

```bash
# 校招查询
python scripts/query.py --keyword "AI" --type campus

# 社招查询
python scripts/query.py --keyword "AI" --type social
```

## 注意事项

- 页面为 SPA，必须使用 Crawl4AI 渲染，无法直接请求 API
- Crawl4AI 缓存目录通过 `CRAWL4_AI_BASE_DIRECTORY` 环境变量设为项目内
- 首次渲染较慢，后续有缓存加速
