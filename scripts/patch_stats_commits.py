#!/usr/bin/env python3
"""Patch stats.svg with private-aware commit and PR totals."""

from __future__ import annotations

import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

PATH = Path("profile/stats.svg")
TOKEN = os.environ["GH_TOKEN"]
USERNAME = os.environ.get("GITHUB_REPOSITORY_OWNER") or os.environ.get(
    "USERNAME", "Narehood"
)


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


def yearly_commits() -> int:
    data = graphql(
        """
        query {
          viewer {
            contributionsCollection {
              totalCommitContributions
              restrictedContributionsCount
            }
          }
        }
        """
    )
    cc = data["viewer"]["contributionsCollection"]
    return cc["totalCommitContributions"] + cc["restrictedContributionsCount"]


def lifetime_commits() -> int:
    created = graphql("{ viewer { createdAt } }")["viewer"]["createdAt"]
    start = datetime.fromisoformat(created.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    total = 0
    for year in range(start.year, now.year + 1):
        data = graphql(
            """
            query($from: DateTime!, $to: DateTime!) {
              viewer {
                contributionsCollection(from: $from, to: $to) {
                  totalCommitContributions
                  restrictedContributionsCount
                }
              }
            }
            """,
            {
                "from": f"{year}-01-01T00:00:00Z",
                "to": f"{year + 1}-01-01T00:00:00Z",
            },
        )
        cc = data["viewer"]["contributionsCollection"]
        total += (
            cc["totalCommitContributions"] + cc["restrictedContributionsCount"]
        )
    return total


def total_prs() -> int:
    """PRs across owned repos, including private repos and forks."""
    data = graphql(
        """
        query($q: String!) {
          search(query: $q, type: ISSUE) { issueCount }
        }
        """,
        {"q": f"user:{USERNAME} type:pr"},
    )
    return data["search"]["issueCount"]


def bump_height(svg: str, delta: int = 25) -> str:
    svg = re.sub(
        r'(\sheight=")(\d+)(")',
        lambda m: f"{m.group(1)}{int(m.group(2)) + delta}{m.group(3)}",
        svg,
        count=1,
    )
    svg = re.sub(
        r'viewBox="0 0 (\d+) (\d+)"',
        lambda m: f'viewBox="0 0 {m.group(1)} {int(m.group(2)) + delta}"',
        svg,
        count=1,
    )
    return svg


def ensure_lifetime_row(svg: str, lifetime: int) -> str:
    if 'data-testid="lifetime-commits"' in svg:
        return re.sub(
            r'(data-testid="lifetime-commits"\s*>)\s*\d+',
            rf"\g<1>{lifetime}",
            svg,
            count=1,
        )

    svg = bump_height(svg, 25)

    for old, new in ((100, 125), (75, 100), (50, 75)):
        svg = svg.replace(
            f'<g transform="translate(0, {old})">',
            f'<g transform="translate(0, {new})">',
            1,
        )

    row = f"""<g transform="translate(0, 50)">
    <g class="stagger" style="animation-delay: 675ms" transform="translate(25, 0)">
    <svg data-testid="icon" class="icon" viewBox="0 0 16 16" version="1.1" width="16" height="16">
      <path fill-rule="evenodd" d="M1.643 3.143L.427 1.927A.25.25 0 000 2.104V5.75c0 .138.112.25.25.25h3.646a.25.25 0 00.177-.427L2.715 4.215a6.5 6.5 0 11-1.18 4.458.75.75 0 10-1.493.154 8.001 8.001 0 101.6-5.684zM7.75 4a.75.75 0 01.75.75v2.992l2.028.812a.75.75 0 01-.557 1.392l-2.5-1A.75.75 0 017 8.25v-3.5A.75.75 0 017.75 4z"/>
    </svg>
      <text class="stat  bold" x="25" y="12.5">Lifetime Commits:</text>
      <text class="stat  bold" x="224.01" y="12.5" data-testid="lifetime-commits">{lifetime}</text>
    </g>
  </g>"""

    anchor = '<g transform="translate(0, 75)">'
    idx = svg.find(anchor)
    if idx < 0:
        raise SystemExit("could not find PRs row anchor for lifetime insert")
    return svg[:idx] + row + svg[idx:]


def patch_number(svg: str, test_id: str, value: int) -> str:
    svg, n = re.subn(
        rf'(data-testid="{test_id}"\s*>)\s*[\d,]+',
        rf"\g<1>{value}",
        svg,
        count=1,
    )
    if n == 0:
        raise SystemExit(f"Failed to patch {test_id}")
    return svg


def patch(yearly: int, lifetime: int, prs: int) -> None:
    svg = PATH.read_text(encoding="utf-8")

    svg = patch_number(svg, "commits", yearly)
    svg = re.sub(
        r"(Total Commits(?:\s*\([^)]+\))?\s*:)\s*[\d,]+",
        rf"\1 {yearly}",
        svg,
        count=1,
    )

    svg = ensure_lifetime_row(svg, lifetime)
    svg = patch_number(svg, "prs", prs)

    desc = svg.split("<desc", 1)[1].split("</desc>", 1)[0]
    if "Lifetime Commits:" in desc:
        svg = re.sub(
            r"Lifetime Commits:\s*\d+",
            f"Lifetime Commits: {lifetime}",
            svg,
            count=1,
        )
    else:
        svg = svg.replace(
            "</desc>",
            f", Lifetime Commits: {lifetime}</desc>",
            1,
        )
    svg = re.sub(r"Total PRs:\s*[\d,]+", f"Total PRs: {prs}", svg, count=1)

    PATH.write_text(svg, encoding="utf-8", newline="\n")
    ET.parse(PATH)
    print(f"Patched yearly={yearly} lifetime={lifetime} prs={prs}")


if __name__ == "__main__":
    y = yearly_commits()
    life = lifetime_commits()
    prs = total_prs()
    print(f"yearly={y} lifetime={life} prs={prs}")
    patch(y, life, prs)
