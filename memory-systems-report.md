# AI Memory GitHub 调研报告

> 生成时间：2026-06-15。数据来自 GitHub Search API、`gh repo view`、重点项目 README 缓存。
> 用途：个人长期参考，不作为公开榜单或严格排名。

## 1. 整体结论

AI memory 生态已经从早期的“把聊天记录塞进向量库”进入到更分层的阶段：

1. **Memory layer 正在产品化**：[mem0ai/mem0](https://github.com/mem0ai/mem0) · 58576 stars · 更新 2026-06-15、[supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) · 27014 stars · 更新 2026-06-15、[letta-ai/letta](https://github.com/letta-ai/letta) · 23332 stars · 更新 2026-05-14 这类项目不再只讲 RAG，而是讲用户画像、会话状态、agent state、自动抽取、遗忘和 API/SDK。
2. **Graph memory 很强势**：[getzep/graphiti](https://github.com/getzep/graphiti) · 27431 stars · 更新 2026-06-12、[topoteretes/cognee](https://github.com/topoteretes/cognee) · 17830 stars · 更新 2026-06-15 把 memory 看成会随时间变化的实体/关系/事实网络，比普通向量检索更适合处理“偏好变了”“事实过期了”“关系有来源”。
3. **Agent 框架把 memory 当基础能力，但通常不够专门**：LangChain/LangGraph、CrewAI、AutoGen、OpenAI Agents SDK 都有 session/context/memory 相关能力，但它们更像运行时或编排框架，不会替你完整解决长期用户记忆。
4. **新项目越来越强调本地、可控、MCP/IDE 场景**：搜索结果里出现很多 local-first memory、Claude/Codex/Copilot memory、MCP memory server。这说明开发者已经从“聊天机器人记忆”走向“AI coding/agent 工作环境记忆”。
5. **真正难点不是存储，而是 memory 生命周期**：写入、合并、冲突、遗忘、可见、可编辑、可删除，比选向量库还是图数据库更关键。

最值得我们学习的方向：

- **显式 memory lifecycle API**：`remember / recall / forget / improve` 这种语义比 CRUD 更适合产品。
- **user profile + event memory + semantic memory 分层**：不要把所有东西混成一个向量集合。
- **hybrid retrieval**：语义、关键词、实体、图遍历、时间过滤一起做召回，再 rerank。
- **用户控制面**：memory 必须可见、可编辑、可删除，否则很难建立信任。
- **先做可调试的小系统**：比追求“memory OS”大叙事更重要。

## 2. 项目分类地图

| 类别 | 代表项目 | 主要价值 | 风险 |
| --- | --- | --- | --- |
| 长期记忆框架 / Memory layer | mem0, Letta, Supermemory, LangMem, Honcho | API/SDK 直接接入 agent 或 app | 容易平台化过重 |
| RAG / 向量记忆 | memvid, LlamaIndex, zvec, memsearch | 简单、快、工程成熟 | 容易退化成“搜索历史记录” |
| 图谱记忆 | Graphiti, Cognee, Memary, Memgraph, GraphRAG | 适合关系、时间、事实变化 | 建模、查询和调试成本高 |
| 用户画像 / 个性化记忆 | Memobase, Supermemory, MemoryOS, MIRIX | 适合 assistant/chatbot 个性化 | 可能忽视任务/事件记忆 |
| Agent 框架内置 memory | LangChain/LangGraph, CrewAI, AutoGen, OpenAI Agents, Eliza | 和 agent runtime 结合紧 | memory 通常不是一等产品 |
| 应用型 memory 产品 | LobeHub, OpenMemory, local AI memory tools | 产品体验启发强 | 实现细节不一定可复用 |

## 3. 重点项目拆解

### 1. [mem0ai/mem0](https://github.com/mem0ai/mem0) · 58576 stars · 更新 2026-06-15

- **它解决什么**：通用 memory layer，面向 AI assistants/agents 做个性化长期记忆。
- **memory 设计思路**：把对话里的偏好、事实、用户/会话/agent 状态抽取成可检索记忆；README 强调 multi-level memory、多信号检索、SDK/API 和托管/自托管。
- **接入方式**：SDK/API + 自托管/托管服务。
- **值得学**：最值得学“记忆不是聊天记录”，而是用户、会话、agent 多层状态；也值得学 benchmark 和迁移文档做法。
- **不适合我们学**：不要一开始照搬它的完整平台化和商业化边界，第一版容易过重。

### 2. [letta-ai/letta](https://github.com/letta-ai/letta) · 23332 stars · 更新 2026-05-14

- **它解决什么**：stateful agent 平台，核心卖点是 agent 有持久 memory 并能持续学习。
- **memory 设计思路**：通过 memory blocks 初始化和维护 agent 状态，API/SDK 让应用创建带 memory 的 agent。
- **接入方式**：Letta API、Python/TypeScript SDK、本地 CLI。
- **值得学**：值得学“agent = model + tools + memory state”的产品建模，以及 memory block 这种显式可解释容器。
- **不适合我们学**：对个人项目来说平台面较大，不适合一开始做完整 agent runtime。

### 3. [getzep/graphiti](https://github.com/getzep/graphiti) · 27431 stars · 更新 2026-06-12

- **它解决什么**：实时 temporal knowledge graph，用于 agent context graph memory。
- **memory 设计思路**：把用户交互、结构化/非结构化数据增量写入图，实体/关系/事实带时间和来源，支持语义+关键词+图遍历混合检索。
- **接入方式**：Python framework + MCP server。
- **值得学**：最值得学 temporal graph：事实会变，记忆必须知道“什么时候是真的”。
- **不适合我们学**：图谱建模和查询复杂度高，第一版不要为了高级而牺牲可调试性。

### 4. [topoteretes/cognee](https://github.com/topoteretes/cognee) · 17830 stars · 更新 2026-06-15

- **它解决什么**：开源 AI memory platform，强调自托管知识图谱和长期记忆。
- **memory 设计思路**：用 remember/recall/forget/improve 这类操作组织 memory 生命周期，结合向量、图推理、ontology 和数据摄取。
- **接入方式**：Python API、自托管、graph/vector backend。
- **值得学**：值得学 API 命名：remember/recall/forget 比“insert/search/delete”更贴近 memory 语义。
- **不适合我们学**：完整 ontology/graph pipeline 对第一版偏重，可以先学接口和生命周期。

### 5. [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory) · 27014 stars · 更新 2026-06-15

- **它解决什么**：memory/context engine + app，覆盖 personal/company brain。
- **memory 设计思路**：自动从对话抽取 facts、维护 user profile、处理知识更新/矛盾和遗忘，把 RAG 与个性化 context 合并查询。
- **接入方式**：API、Web app、SDK、自托管文档。
- **值得学**：值得学 user profile + recent activity 的组合，以及“遗忘/矛盾处理”是 memory 产品核心能力。
- **不适合我们学**：产品和平台都很完整，做参考时要拆小，不要一次做全栈。

### 6. [langchain-ai/langmem](https://github.com/langchain-ai/langmem) · 1502 stars · 更新 2026-06-12

- **它解决什么**：LangChain/LangGraph 生态里的长期记忆工具包。
- **memory 设计思路**：提供 core memory API、agent 可调用的 manage/search memory tools、后台抽取/合并记忆，并接入 LangGraph Store。
- **接入方式**：Python package + LangGraph integration。
- **值得学**：值得学 hot path 工具调用与 background memory manager 的分工。
- **不适合我们学**：强绑定 LangGraph 思维，如果我们做独立系统，需要抽象出框架无关接口。

### 7. [MemTensor/MemOS](https://github.com/MemTensor/MemOS) · 9865 stars · 更新 2026-06-15

- **它解决什么**：面向 LLM/AI agents 的 memory OS，强调超持久记忆、混合检索和跨任务 skill。
- **memory 设计思路**：更像“记忆操作系统”：把 memory 管理、检索、任务迁移和 skill reuse 作为统一层。
- **接入方式**：平台/SDK 形态，TypeScript 主语言。
- **值得学**：值得观察“memory OS”叙事：把 memory 从功能点提升为 agent infrastructure。
- **不适合我们学**：需要警惕概念过大，先验证实际 API 与使用路径。

### 8. [plastic-labs/honcho](https://github.com/plastic-labs/honcho) · 5157 stars · 更新 2026-06-12

- **它解决什么**：stateful agents memory library。
- **memory 设计思路**：定位为构建有状态 agent 的 memory library，强调让 agent 保持上下文。
- **接入方式**：Python library。
- **值得学**：值得学轻量 library 的切入：不必一开始做平台，先把 stateful memory 做顺。
- **不适合我们学**：需要进一步验证长期维护和具体 API 深度。

### 9. [BAI-LAB/MemoryOS](https://github.com/BAI-LAB/MemoryOS) · 1462 stars · 更新 2026-04-28

- **它解决什么**：个性化 AI agent 的 memory operating system，偏研究系统。
- **memory 设计思路**：围绕个人 agent 的长期记忆管理，强调 memory OS 范式。
- **接入方式**：Python research/system repo。
- **值得学**：值得学研究侧分类和 personalized agent 的问题定义。
- **不适合我们学**：偏论文/研究路线，工程落地可能需要重新简化。

### 10. [memodb-io/memobase](https://github.com/memodb-io/memobase) · 2755 stars · 更新 2026-01-11

- **它解决什么**：user profile-based long-term memory for chatbot apps。
- **memory 设计思路**：以用户画像为中心组织长期记忆，适合客服/聊天类应用持续个性化。
- **接入方式**：Python package/API。
- **值得学**：值得学从 user profile 出发，而不是从 vector store 出发。
- **不适合我们学**：若我们的目标是 agent 工作流，不要只做 profile，任务/事件记忆也要考虑。

### 11. [getzep/zep](https://github.com/getzep/zep) · 4669 stars · 更新 2026-04-09

- **它解决什么**：Zep 产品/生态仓库，Graphiti 是其底层图谱 memory。
- **memory 设计思路**：强调 Graph RAG、temporal knowledge graph、SDK 生态和 context assembly。
- **接入方式**：SDK/API/server examples。
- **值得学**：值得学产品化 context assembly：memory 最终要服务 agent prompt/context。
- **不适合我们学**：仓库更多是 examples/integration，不是单一核心实现。

### 12. [kingjulio8238/Memary](https://github.com/kingjulio8238/Memary) · 2623 stars · 更新 2024-10-22

- **它解决什么**：较早的 autonomous agent memory layer，强调 human-like memory。
- **memory 设计思路**：使用 persona、memory stream、graph database 等模拟人类记忆，支持多个 agent/context。
- **接入方式**：Python/Streamlit + graph DB。
- **值得学**：值得学早期 memory system 如何把 persona、事件流、图谱结合起来。
- **不适合我们学**：安装和依赖较重，维护活跃度一般，不适合直接照抄。

### 13. [run-llama/llama_index](https://github.com/run-llama/llama_index) · 50132 stars · 更新 2026-06-12

- **它解决什么**：RAG/data framework，不是专门 memory 系统，但影响很多 memory 项目。
- **memory 设计思路**：提供数据连接、索引、retriever、query engine、rerank 等 building blocks。
- **接入方式**：Python framework。
- **值得学**：值得学 ingestion/index/retrieval 的模块化，memory 系统常要复用这套能力。
- **不适合我们学**：它解决的是 data/RAG 平台，不是用户记忆生命周期。

### 14. [langchain-ai/langchain](https://github.com/langchain-ai/langchain) · 139318 stars · 更新 2026-06-15

- **它解决什么**：agent/LLM app 基础框架，生态里有 memory、retriever、LangGraph Store 等概念。
- **memory 设计思路**：更偏 agent engineering platform；memory 往往作为 chain/agent/context 的组件出现。
- **接入方式**：Python/JS ecosystem。
- **值得学**：值得学 memory 如何作为可插拔组件进入 agent runtime。
- **不适合我们学**：历史 API 多，直接学可能混乱；优先看 LangGraph/LangMem 新路线。

### 15. [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI) · 53571 stars · 更新 2026-06-14

- **它解决什么**：多 agent orchestration 框架，README 提到 agent 配置、memory 和 guardrails。
- **memory 设计思路**：memory 是 agent 配置/执行的一部分，重点不是 memory 本身，而是多 agent 协作时的状态。
- **接入方式**：Python framework。
- **值得学**：值得学多 agent 场景中 memory 和 role/backstory/task 的关系。
- **不适合我们学**：不要把编排框架当 memory 系统本体。

### 16. [microsoft/autogen](https://github.com/microsoft/autogen) · 58956 stars · 更新 2026-04-15

- **它解决什么**：多 agent 框架，当前 README 提示新项目迁移到 Microsoft Agent Framework。
- **memory 设计思路**：以 agent chat、工具、MCP、分层框架为核心；memory 不是主卖点，但对 agent 状态管理有生态参考价值。
- **接入方式**：Python framework。
- **值得学**：值得学成熟框架如何处理迁移、文档和长期维护。
- **不适合我们学**：作为 memory 参考优先级下降，尤其 README 已提示维护/迁移方向。

### 17. [openai/openai-agents-python](https://github.com/openai/openai-agents-python) · 27153 stars · 更新 2026-06-13

- **它解决什么**：轻量 multi-agent workflow SDK，包含 sessions 管理会话历史。
- **memory 设计思路**：Sessions 自动管理跨 agent run 的 conversation history，偏短中期会话状态。
- **接入方式**：Python SDK。
- **值得学**：值得学 sessions 与 long-term memory 的边界：会话历史不是完整 memory，但可作为 memory 输入源。
- **不适合我们学**：不要把 session 当长期记忆系统；缺少 profile、遗忘、冲突处理等层。

### 18. [elizaOS/eliza](https://github.com/elizaOS/eliza) · 18582 stars · 更新 2026-06-14

- **它解决什么**：开放 agent runtime，核心里有 message/memory/state primitives。
- **memory 设计思路**：通过 runtime/plugin/model 层组织 autonomous agents，memory/state 是 agent loop 的基础结构。
- **接入方式**：TypeScript framework/app。
- **值得学**：值得学 runtime 级别如何暴露 message、memory、state 原语。
- **不适合我们学**：生态庞大，调研时只看 memory primitives，不必陷入插件宇宙。

### 19. [lobehub/lobehub](https://github.com/lobehub/lobehub) · 78669 stars · 更新 2026-06-15

- **它解决什么**：应用型 agent/operator 产品，强调 agents 协作与上下文。
- **memory 设计思路**：不是纯 memory 基建，但 README 对“agent 缺上下文、浅层全局记忆”问题说得很产品化。
- **接入方式**：Web app/product。
- **值得学**：值得学产品表达：memory 的用户价值是减少切换、形成持续协作空间。
- **不适合我们学**：实现细节不如专用 memory repo 直接。

### 20. [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) · 184945 stars · 更新 2026-06-15

- **它解决什么**：早期 autonomous agent 代表，现在更像 agent platform。
- **memory 设计思路**：memory 曾是 AutoGPT 类 agent 的核心需求之一，但当前 README 更偏构建、部署、运行 agent。
- **接入方式**：Platform/app。
- **值得学**：值得作为历史参照：早期 agent 为什么需要长期记忆。
- **不适合我们学**：不适合作为新 memory 架构样板，当前方向更偏自动化平台。

## 4. 架构对比

| 维度 | 常见路线 | 观察 | 我们的取舍 |
| --- | --- | --- | --- |
| 写入 | 自动抽取、agent 工具手动保存、事件流后台处理 | 自动抽取体验好，但容易误写；手动保存可控但打断 flow | 第一版用“事件流 + 可审查候选记忆”，先不全自动写入 |
| 存储 | 向量库、图数据库、SQL/文档库、混合 | 向量适合语义召回，图适合关系和时间，SQL 适合可见/可编辑 | 第一版用 SQLite/JSON + embedding 可选，别一上来依赖重图数据库 |
| 检索 | 语义搜索、关键词、实体匹配、graph traversal、rerank | 强项目都在走 hybrid retrieval | 第一版做关键词 + embedding + recency，保留 rerank 接口 |
| 更新 | 追加、合并、覆盖、过期、冲突处理 | memory 会过期，偏好会变化，这是核心问题 | 第一版必须有 source、created_at、updated_at、confidence/status |
| 用户控制 | 可见、可编辑、可删除、导出、关闭 | 这是 memory 产品信任的核心 | 第一版就做 memory inbox / review list，不要黑箱 |
| 多租户/隔离 | user/session/agent namespace | mem0、Cognee、Supermemory 都强调不同层级 | 第一版至少区分 user、project、agent/session |

## 5. 给我们自己的启发

如果我们自己做一个 memory 系统，第一版不要做“大而全 memory OS”，建议切成一个 **AI coding / agent 工作记忆的小系统**：

### 第一版应该做

- **Memory Inbox**：从对话、任务、项目笔记里抽取候选记忆，先进入待确认列表。
- **三类记忆**：`preference`（用户偏好）、`project_fact`（项目事实）、`workflow_rule`（工作方式/约束）。
- **可见可控**：每条记忆都有来源、时间、置信度、状态；用户能编辑、删除、禁用。
- **轻量检索**：关键词 + 简单 embedding/semantic adapter + 最近更新时间排序。
- **导出格式**：Markdown/JSON，方便迁移到 Codex skill、agent prompt 或本地知识库。

### 第一版先不要做

- 不要一开始做完整知识图谱和 ontology。
- 不要做全自动写入且不可审查。
- 不要绑定某一个 agent 框架。
- 不要追求多模态、企业权限、团队协作。
- 不要把 memory 和普通 RAG 文档库混为一谈。

### 最适合后续开源练手的方向

1. **agent-memory-auditor**：检查一个 agent 项目的 memory 是否可见、可删、可导出、可追溯。
2. **memory-inbox**：本地-first 的候选记忆审查器，支持 Markdown/JSON。
3. **codex-memory-bridge**：把本地 memory 转成 Codex/agent 可消费的上下文包。
4. **memory-eval-notebook**：用小型自建测试集评估 recall、冲突处理和遗忘。

## 6. 附：推荐阅读顺序

1. 先看 mem0、Supermemory、Letta：理解 memory layer 怎么产品化。
2. 再看 Graphiti、Cognee：理解为什么 graph/temporal 对长期记忆重要。
3. 再看 LangMem：理解 agent 在 hot path 和 background path 怎么管理记忆。
4. 最后扫 LangChain/LangGraph、CrewAI、OpenAI Agents：理解 memory 如何接入 agent runtime。

完整项目索引见 [`memory-project-index.csv`](memory-project-index.csv)。调研过程见 [`memory-research-log.md`](memory-research-log.md)。
