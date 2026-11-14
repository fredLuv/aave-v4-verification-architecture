#!/usr/bin/env python3
"""Minimal zero-dependency CLI to query the Aave V4 Agentic Ontology.

Mirrors Databricks Genie Ontology retrieval: instead of feeding an AI agent
hundreds of raw Solidity/Python files (~145k tokens), query curated semantic
terms, naive-agent traps, and pre-sliced source line bundles (~1k tokens).
"""

import argparse
import json
from pathlib import Path

ONTOLOGY_PATH = Path(__file__).resolve().parent.parent / "ontology" / "aave-v4-ontology.json"


def load_ontology() -> dict:
    with open(ONTOLOGY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def search_items(items: list[dict], query: str, fields: list[str]) -> list[dict]:
    q = query.lower().strip()
    if not q:
        return items
    hits = []
    for item in items:
        haystack = " ".join(str(item.get(k, "")) for k in fields).lower()
        if q in haystack:
            hits.append(item)
    return hits


def print_context_bundle(onto: dict, query: str) -> None:
    terms = search_items(onto["terms"], query, ["id", "term", "domain", "rule", "naive_agent_trap"])
    snippets = search_items(onto["snippets"], query, ["id", "title", "task_tags", "context_markdown", "files"])

    est_tokens = sum(s["estimated_tokens"] for s in snippets) + len(terms) * 90
    print(f"# Aave V4 Ontology Retrieval (query={query!r})")
    print(f"- Curated matches: {len(snippets)} snippet(s), {len(terms)} canonical rule(s)")
    if snippets:
        baseline = snippets[0]["naive_full_repo_tokens"]
        reduction = max(0.0, (1.0 - est_tokens / baseline) * 100.0)
        print(f"- Context budget: ~{est_tokens:,} tokens vs ~{baseline:,} naive repo tokens (~{reduction:.1f}% savings)\n")

    for s in snippets:
        print(s["context_markdown"])
        print("Files:", ", ".join(s["files"]))
        print()

    if terms:
        print("## Canonical Rules & Naive-Agent Traps")
        for t in terms:
            print(f"- **{t['term']}** (authority={t['authority']}): {t['rule']}")
            print(f"  - *Avoid Trap*: {t['naive_agent_trap']}")
            print(f"  - *Source*: {t['source_url']}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Query Aave V4 Agentic Ontology")
    parser.add_argument("query", nargs="?", default="", help="Keyword, domain, symbol, or task tag (e.g. 'premium', 'liquidation', 'babylon')")
    parser.add_argument("--list-domains", action="store_true", help="List all ontology domains")
    parser.add_argument("--curation-queue", action="store_true", help="Show open ontology review / verification gaps")
    args = parser.parse_args()

    onto = load_ontology()

    if args.list_domains:
        for d in onto["domains"]:
            print(f"[{d['id']}] {d['name']} ({d['coverage']}) -> {', '.join(d['paths'])}")
        return

    if args.curation_queue:
        for item in onto["curation_queue"]:
            print(f"[{item['severity']}] {item['title']} ({item['status']}): {item['detail']}")
        return

    print_context_bundle(onto, args.query)


if __name__ == "__main__":
    main()
