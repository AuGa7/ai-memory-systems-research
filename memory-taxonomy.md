# AI Memory Taxonomy

> A practical taxonomy for reading AI memory projects. The goal is not to name every possible memory type, but to separate concerns clearly enough to design a real system.

## 1. Memory Content Types

| Type | What it stores | Useful for | Typical risks | Example projects |
| --- | --- | --- | --- | --- |
| Conversation memory | Turns and summaries from prior conversations | Continuity, recent context, session recovery | Treating transcripts as facts | OpenAI Agents sessions, LangChain, CrewAI |
| User profile memory | Stable user preferences, traits, goals, constraints | Personalization, assistant adaptation | Stale or overconfident profiles | mem0, Supermemory, Memobase |
| Episodic memory | Time-bound events, runs, actions, task traces | Agent reflection, debugging, learning from experience | Event overload, weak summarization | Memary, ReMe, Hindsight-style projects |
| Semantic memory | Durable facts and concepts extracted from text/events | Recall, knowledge grounding, cross-session context | Losing source/provenance | mem0, LangMem, Supermemory |
| Graph memory | Entities, relations, facts, timestamps, provenance | Changing facts, relationships, temporal reasoning | Graph complexity and fragile schemas | Graphiti, Cognee, Zep |
| Procedural memory | Reusable workflows, skills, corrections, policies | AI coding, repeated tasks, tool-use learning | Bad habits becoming persistent | MemOS, Hivemind-style skill memory |
| Project memory | Repo facts, decisions, architecture, constraints | AI coding agents and project continuity | Leaking local/private assumptions | Local-first memory tools, Codex-style workflows |

## 2. Memory Architecture Types

| Architecture | Shape | Strength | When to use | When to avoid |
| --- | --- | --- | --- | --- |
| Buffer + summary | Rolling transcript plus summaries | Simple, cheap, easy to debug | Short/medium conversations | Long-lived personalization |
| Vector memory | Embeddings over notes/events/facts | Fast semantic recall | Broad fuzzy retrieval | Contradictions, temporal facts |
| Hybrid retrieval | Semantic + keyword + entity + recency | Higher recall precision | General assistant memory | Very small projects |
| Temporal graph | Facts with entities, relations, valid time, invalid time | Changing relationships and provenance | Multi-user or enterprise context | First prototype |
| Profile store | Structured profile fields and preferences | Predictable personalization | Product assistants | Open-ended agent reasoning |
| Event-sourced memory | Append-only events with derived views | Auditability, rollback, replay | Agent traces and memory review | Simple chatbots |
| Memory OS / platform | Unified memory service across apps and agents | Cross-agent portability | Long-term platform vision | Early MVP |

## 3. Multi-Agent Memory Topologies

Multi-agent memory is not just "more memory". The hard question is: who owns each memory, who can write it, who can read it, and how conflicts are resolved.

| Topology | Description | Best for | Failure mode | Suggested default |
| --- | --- | --- | --- | --- |
| Shared blackboard | All agents read/write one shared workspace | Small teams, transparent collaboration | Context pollution, unclear ownership | Use only for temporary team state |
| Private memory + shared facts | Each agent has private scratch memory, promoted facts go to shared memory | Planner/executor/critic teams | Promotion rules can be vague | Best default for AI coding agents |
| Role-scoped memory | Planner, researcher, coder, reviewer each keep role memory | Repeated specialized workflows | Role silos and duplicated facts | Good when roles are stable |
| Hierarchical memory | Manager agent owns task memory; subagents keep local traces | Large task decomposition | Manager bottleneck, lost detail | Good for orchestrated agents |
| Federated personal memory | Multiple agents query a user-owned local memory service | Personal assistants and IDE agents | Permission leaks between apps | Good for user-controlled memory |
| Graph-backed team memory | Agents share a temporal entity/relation graph | Relationship-heavy domains | Schema and query complexity | Use after simple event memory works |
| Procedural skill memory | Agents store reusable corrections, tool sequences, and policies | AI coding and operations | Persistent bad procedures | Require human approval before promotion |

## 4. Multi-Agent Design Checklist

| Question | Why it matters | Good first answer |
| --- | --- | --- |
| Who can write memory? | Prevents accidental or malicious memory pollution | Agents write candidates; user or policy promotes |
| Who can read memory? | Avoids leaking private role/user context | Namespace by user, project, role, and run |
| What is private vs shared? | Keeps scratch reasoning separate from durable facts | Private scratchpad, shared verified facts |
| How are conflicts handled? | Preferences and facts change over time | Keep source, timestamp, status, and superseded links |
| How is memory deleted? | Trust requires reversibility | Delete from primary store and derived indexes |
| How is memory evaluated? | Memory can silently degrade agent quality | Track recall, precision, stale recall, and contradiction rate |

## 5. Recommended First System

For an AI coding / agent workflow, start with four layers:

1. **User memory**: durable preferences and personal working style.
2. **Project memory**: repo facts, decisions, constraints, architecture notes.
3. **Agent run memory**: temporary task trace, tool outputs, errors, fixes.
4. **Shared team memory**: promoted facts that planner/coder/reviewer agents can all use.

Avoid fully automatic long-term writes. Use a **Memory Inbox**:

- agents propose candidate memories;
- each candidate has source, timestamp, type, confidence, and suggested scope;
- user or policy approves promotion;
- derived embeddings/graphs can be rebuilt from approved memories.

This is less flashy than a full memory OS, but it is safer, more debuggable, and easier to open source.
