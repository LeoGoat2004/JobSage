# 智谱AI — 查询指南

## 数据源信息

- **类型**：公司直招
- **获取方式**：Crawl4AI 无头浏览器 (飞书招聘 SPA)
- **脚本**：`python scripts/query.py --keyword "关键词"`

## API 详情

- **URL**：`https://zhipu-ai.jobs.feishu.cn/index/position/list`
- **渲染方式**：Crawl4AI 无头浏览器渲染后从 Markdown 提取职位信息

## 返回数据

从渲染后 Markdown 中提取职位列表，字段随页面结构而定。

## 使用示例

```bash
# 基本查询
python scripts/query.py --keyword "Agent"
```

## 注意事项

- 同 MiniMax，飞书招聘页面为 SPA，核心 API 被 nginx 拦截，必须使用 Crawl4AI 渲染
- Crawl4AI 缓存目录通过 `CRAWL4_AI_BASE_DIRECTORY` 环境变量设为项目内
- 首次渲染较慢，后续有缓存加速
