# Memory Research Log

生成时间：2026-06-15

## 搜索方式

使用 `gh` / GitHub Search API 搜索公开仓库，重点关键词包括：

- `topic:llm-memory`
- `topic:ai-memory`
- `topic:agent-memory`
- `topic:long-term-memory`
- `"AI memory" agent`
- `"agent memory"`
- `"llm memory"`
- `"long-term memory" "LLM"`
- `"memory layer" "AI agents"`
- `"persistent memory" "AI agent"`
- `"RAG memory" "LLM"`
- `"conversation memory" "LLM"`
- `"episodic memory" "LLM"`
- `"semantic memory" "LLM"`
- `"graph memory" "AI"`
- `"personal AI memory"`

## 数据来源

- GitHub Search API 生成 164 个唯一候选，保留 80 个候选用于人工筛选。
- 重点 README 缓存在 `cache/readmes/`，实际深读 20 个项目。
- 最终 CSV 保留 65 个候选项目，按 `Must Study / Worth Skimming / Low Priority` 分层。

## 排除规则

排除或降级：

- 操作系统内存、硬件 RAM、游戏内存修改、普通缓存库。
- 只有资料聚合但不是 memory 系统的项目，通常标为 Low Priority 或资料入口。
- 与 AI/Agent/RAG 无关的高 star 噪声。
- 用户明确不希望出现的个人/公司敏感词。

## 分层规则

- `Must Study`：memory 设计明确、近期活跃、README/metadata 显示有直接参考价值。
- `Worth Skimming`：生态关键项目或框架内置 memory 相关能力，值得扫但不是专门 memory 系统。
- `Low Priority`：候选参考、资料入口、宽泛框架或需要进一步验证。

## 采集过程记录

- 第一版脚本尝试“搜索 + README 全量深读”，但部分 README/API 请求不稳定，容易拖慢。
- 最终采用“GitHub Search 建候选池 + 已缓存核心 README 深读”的中等深度方式。
- 这样更符合个人参考资料定位：覆盖够宽，但不做大型爬虫或公开数据库。

## 后续刷新方式

- 可复用 `scripts/collect_memory_repos.py`，但建议只在需要更新索引时运行。
- 更稳的方式是先跑轻量 Search，再只对新增的 Must Study 候选读取 README。
