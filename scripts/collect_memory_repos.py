#!/usr/bin/env python3
"""Refresh lightweight GitHub search candidates for AI memory systems."""

import csv
import json
import os
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

SEARCH_QUERIES = [
    "topic:llm-memory",
    "topic:ai-memory",
    "topic:agent-memory",
    "topic:long-term-memory",
    '"AI memory" agent in:description,readme',
    '"agent memory" in:name,description,readme',
    '"llm memory" in:name,description,readme',
    '"long-term memory" "LLM" in:readme',
    '"memory layer" "AI agents" in:readme',
    '"persistent memory" "AI agent" in:readme',
    '"RAG memory" "LLM" in:readme',
    '"conversation memory" "LLM" in:readme',
    '"episodic memory" "LLM" in:readme',
    '"semantic memory" "LLM" in:readme',
    '"graph memory" "AI" in:readme',
    '"personal AI memory" in:readme',
]

EXCLUDE_TERMS = {
    term.strip().lower()
    for term in os.environ.get("AI_MEMORY_RESEARCH_EXCLUDE", "").split(",")
    if term.strip()
}


def gh_api(args):
    try:
        result = subprocess.run(
            ["gh", "api", *args],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return None
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)


def search(query, per_page=15):
    return gh_api(
        [
            "-X",
            "GET",
            "search/repositories",
            "-f",
            f"q={query}",
            "-f",
            "sort=stars",
            "-f",
            "order=desc",
            "-f",
            f"per_page={per_page}",
        ]
    )


def relevance_score(item):
    blob = " ".join(
        [
            item.get("full_name", ""),
            item.get("description") or "",
            " ".join(item.get("topics") or []),
        ]
    ).lower()
    score = 0
    for term, points in [
        ("memory", 5),
        ("agent", 4),
        ("llm", 4),
        ("rag", 3),
        ("long-term", 3),
        ("personal", 2),
        ("episodic", 2),
        ("semantic", 2),
        ("graph", 2),
        ("chatbot", 2),
    ]:
        if term in blob:
            score += points
    if item.get("stargazers_count", 0) > 1000:
        score += 2
    if (item.get("pushed_at") or "") >= "2025-01-01":
        score += 2
    for bad in ["kernel", "ram", "game hacking", "allocator", "cache replacement"]:
        if bad in blob:
            score -= 12
    return score


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    by_name = {}
    search_log = []

    for query in SEARCH_QUERIES:
        payload = search(query)
        if not payload:
            search_log.append({"query": query, "count": 0, "repos": [], "status": "failed"})
            continue
        repos = []
        for item in payload.get("items", []):
            full_name = item["full_name"]
            if any(term in full_name.lower() for term in EXCLUDE_TERMS):
                continue
            by_name[full_name] = item
            repos.append(full_name)
        search_log.append({"query": query, "count": len(repos), "repos": repos, "status": "ok"})
        time.sleep(2.1)

    items = sorted(by_name.values(), key=lambda item: (-relevance_score(item), -item.get("stargazers_count", 0)))
    candidates = []
    for item in items[:80]:
        candidates.append(
            {
                "full_name": item["full_name"],
                "url": item["html_url"],
                "description": item.get("description") or "",
                "stars": item.get("stargazers_count", 0),
                "forks": item.get("forks_count", 0),
                "language": item.get("language") or "",
                "license": (item.get("license") or {}).get("spdx_id") or "",
                "updated_at": item.get("pushed_at") or item.get("updated_at") or "",
                "topics": item.get("topics") or [],
                "relevance_score": relevance_score(item),
            }
        )

    (DATA / "search-candidates.json").write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA / "search-log-expanded.json").write_text(json.dumps(search_log, ensure_ascii=False, indent=2), encoding="utf-8")

    csv_path = ROOT / "memory-project-index.raw.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "full_name",
                "url",
                "description",
                "stars",
                "forks",
                "language",
                "license",
                "updated_at",
                "relevance_score",
            ],
        )
        writer.writeheader()
        writer.writerows(candidates)

    print(json.dumps({"unique": len(by_name), "kept": len(candidates), "raw_csv": str(csv_path)}, indent=2))


if __name__ == "__main__":
    main()
