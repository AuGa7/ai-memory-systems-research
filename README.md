# AI Memory Systems Research

[![Research](https://img.shields.io/badge/research-AI%20memory-22d3ee?style=for-the-badge)](memory-systems-report.md)
[![Projects](https://img.shields.io/badge/projects-65-2563eb?style=for-the-badge)](memory-project-index.csv)
[![License: MIT](https://img.shields.io/badge/license-MIT-black?style=for-the-badge)](LICENSE)

A practical GitHub research note on AI memory systems for agents, LLM apps, RAG memory, user profiles, graph memory, and long-term context.

这不是一个“大全榜单”，而是一份给构建 AI agent / AI coding / personal memory 系统时参考的中等深度调研资料。

## What is inside

| File | Purpose |
| --- | --- |
| [memory-systems-report.md](memory-systems-report.md) | 中文主报告：生态结论、项目分类、20 个重点项目拆解、架构对比、后续产品启发。 |
| [memory-project-index.csv](memory-project-index.csv) | 65 个候选项目索引，包含 tier、类型、stars、更新时间、接口形态和参考价值。 |
| [memory-research-log.md](memory-research-log.md) | 搜索关键词、排除规则、分层规则和采集过程记录。 |
| [data/search-candidates.json](data/search-candidates.json) | GitHub Search API 生成的候选池快照。 |
| [scripts/collect_memory_repos.py](scripts/collect_memory_repos.py) | 轻量刷新脚本，用于重新拉取 GitHub search candidates。 |

## Key takeaways

- AI memory is moving from simple vector recall to memory lifecycle design: write, merge, conflict, forget, inspect, edit, and delete.
- Graph memory is becoming important for temporal facts, changing preferences, provenance, and relationship-aware retrieval.
- Agent frameworks expose memory/session/context primitives, but they usually do not replace a dedicated long-term memory layer.
- The best first product slice is not a full memory OS. A small, inspectable memory inbox is more useful.

## Scope

Included:

- LLM long-term memory
- AI agent memory
- conversation memory
- user profile memory
- episodic / semantic memory
- graph memory
- RAG memory
- memory layer / memory store
- memory modules inside agent frameworks

Excluded:

- operating system memory
- game memory hacking
- hardware memory
- generic cache libraries
- unrelated storage systems

## Refresh the candidate data

Requirements:

```bash
gh auth status
python3 --version
```

Run:

```bash
python3 scripts/collect_memory_repos.py
```

The script only refreshes lightweight GitHub search metadata. It does not publish anything and does not cache full third-party README files.

## Notes

- Data snapshot date: 2026-06-15.
- Stars and update dates change over time.
- This repository summarizes public GitHub metadata and project documentation. It does not include raw third-party README caches.

## License

MIT License. See [LICENSE](LICENSE).
