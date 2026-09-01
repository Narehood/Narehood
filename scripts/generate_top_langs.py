#!/usr/bin/env python3
"""Generate top-languages SVG including forks and private repos."""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

PATH = Path("profile/top-langs.svg")
TOKEN = os.environ["GH_TOKEN"]
USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER") or os.environ.get(
    "USERNAME", "Narehood"
)
LANGS_COUNT = 20


def graphql(query: str, variables: dict | None = None) -> dict:
    payload: dict = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "narehood-readme-stats",
        },
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]


def fetch_languages() -> list[tuple[str, str, int]]:
    """Return [(name, color, bytes), ...] sorted by bytes desc."""
    data = graphql(
        """
        query($login: String!) {
          user(login: $login) {
            repositories(ownerAffiliations: OWNER, first: 100) {
              nodes {
                name
                isFork
                isPrivate
                languages(first: 20, orderBy: { field: SIZE, direction: DESC }) {
                  edges {
                    size
                    node { name color }
                  }
                }
              }
            }
          }
        }
        """,
        {"login": USERNAME},
    )

    totals: dict[str, list] = {}
    fork_hits = []
    for repo in data["user"]["repositories"]["nodes"]:
        if not repo:
            continue
        edges = (repo.get("languages") or {}).get("edges") or []
        for edge in edges:
            if not edge or not edge.get("node"):
                continue
            name = edge["node"]["name"]
            color = edge["node"].get("color") or "#8b949e"
            size = edge["size"]
            if name not in totals:
                totals[name] = [color, 0]
            totals[name][1] += size
        if repo.get("isFork") and any(
            (e or {}).get("node", {}).get("name") == "C#" for e in edges
        ):
            fork_hits.append(repo["name"])

    ranked = sorted(
        ((name, color, size) for name, (color, size) in totals.items()),
        key=lambda item: item[2],
        reverse=True,
    )
    print(f"repos_with_csharp_forks={fork_hits}")
    print("top:", [(n, s) for n, _, s in ranked[:LANGS_COUNT]])
    return ranked[:LANGS_COUNT]


def render(langs: list[tuple[str, str, int]]) -> str:
    total = sum(size for _, _, size in langs) or 1
    width = 300
    # header + progress bar + rows (2 columns)
    rows = (len(langs) + 1) // 2
    height = 95 + rows * 24
    segments = []
    x = 25
    bar_width = 250
    for name, color, size in langs:
        w = bar_width * (size / total)
        segments.append(
            f'<rect height="8" x="{x:.2f}" width="{w:.2f}" fill="{color}"/>'
        )
        x += w

    items = []
    for i, (name, color, size) in enumerate(langs):
        col = i // ((len(langs) + 1) // 2)
        row = i % ((len(langs) + 1) // 2)
        tx = 25 + col * 140
        ty = 45 + row * 24
        pct = 100.0 * size / total
        items.append(
            f"""
      <g transform="translate({tx}, {ty})">
        <circle cx="5" cy="6" r="5" fill="{color}"/>
        <text data-testid="lang-name" x="15" y="10" class="lang-name">{name} {pct:.2f}%</text>
      </g>"""
        )

    return f"""
<svg
  width="{width}"
  height="{height}"
  viewBox="0 0 {width} {height}"
  fill="none"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-labelledby="descId"
>
  <title id="titleId">Most Used Languages</title>
  <desc id="descId">Most used languages including forks and private repositories</desc>
  <style>
    .header {{
      font: 600 18px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #58a6ff;
    }}
    .lang-name {{
      font: 400 14px 'Segoe UI', Ubuntu, Sans-Serif;
      fill: #c9d1d9;
    }}
  </style>
  <rect
    data-testid="card-bg"
    x="0.5"
    y="0.5"
    rx="4.5"
    height="99%"
    stroke="#e4e2e2"
    width="{width - 1}"
    fill="#0d1117"
    stroke-opacity="0"
  />
  <text x="25" y="35" class="header" data-testid="header">Most Used Languages</text>
  <svg data-testid="lang-items" x="0" y="45">
    <mask id="rect-mask">
      <rect x="25" y="0" width="{bar_width}" height="8" fill="white" rx="5"/>
    </mask>
    <g mask="url(#rect-mask)">
      {''.join(segments)}
    </g>
    {''.join(items)}
  </svg>
</svg>
"""


if __name__ == "__main__":
    langs = fetch_languages()
    PATH.parent.mkdir(parents=True, exist_ok=True)
    PATH.write_text(render(langs).strip() + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {PATH}")
