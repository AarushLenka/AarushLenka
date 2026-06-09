#!/usr/bin/env python3
"""Generate the terminal-style profile dashboard SVG used by README.md."""

from __future__ import annotations

import base64
import calendar
import datetime as dt
import html
import io
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile-dashboard.svg"
USERNAME = os.environ.get("GITHUB_USERNAME", "AarushLenka")
BIRTHDAY = dt.date(2005, 8, 14)

WIDTH = 1472
HEIGHT = 655
TERMINAL_COLS = 78

FONT = "'JetBrains Mono', 'Fira Code', 'Cascadia Mono', Consolas, monospace"
BG = "#242927"
BG_2 = "#1f2322"
TEXT = "#c6c5c4"
MUTED = "#9f9f9e"
RED = "#a75b63"
DARK_RED = "#843f42"
AMBER = "#8b6740"
BROWN = "#724b35"
OLIVE = "#687057"
ASH = "#6d7470"
ASCII_IMAGE = ROOT / "assets" / "github.png"
STATIC_STATS = {
    "repos": 0,
    "contributed": 0,
    "stars": 0,
    "commits": 0,
    "followers": 0,
    "code_size": 0,
    "code_added": 0,
    "code_removed": 0,
}
SKIP_EXTENSIONS = {
    ".7z",
    ".avi",
    ".bmp",
    ".class",
    ".dll",
    ".exe",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".lock",
    ".m4a",
    ".mkv",
    ".mov",
    ".mp3",
    ".mp4",
    ".o",
    ".pdf",
    ".png",
    ".pyc",
    ".so",
    ".ttf",
    ".webm",
    ".webp",
    ".woff",
    ".woff2",
    ".zip",
}


def plural(value: int, unit: str) -> str:
    return f"{value} {unit}{'' if value == 1 else 's'}"


def add_months(day: dt.date, months: int) -> dt.date:
    year = day.year + (day.month - 1 + months) // 12
    month = (day.month - 1 + months) % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    return dt.date(year, month, min(day.day, last_day))


def uptime(today: dt.date | None = None) -> str:
    today = today or dt.datetime.now(dt.timezone.utc).date()
    months = (today.year - BIRTHDAY.year) * 12 + today.month - BIRTHDAY.month
    if today.day < BIRTHDAY.day:
        months -= 1

    years, remaining_months = divmod(max(0, months), 12)
    anniversary = add_months(BIRTHDAY, years * 12 + remaining_months)
    days = max(0, (today - anniversary).days)
    return ", ".join(
        [
            plural(years, "year"),
            plural(remaining_months, "month"),
            plural(days, "day"),
        ]
    )


def github_headers(token: str | None, *, graphql: bool = False) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-dashboard-generator",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if graphql:
        headers["Accept"] = "application/vnd.github+json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def request_json(
    url: str,
    *,
    token: str | None,
    data: dict[str, object] | None = None,
    retries: int = 2,
) -> object:
    body = None
    graphql = data is not None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=github_headers(token, graphql=graphql))
    if data is not None:
        request.add_header("Content-Type", "application/json")

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            if attempt >= retries:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}")


def request_bytes(url: str, *, token: str | None, retries: int = 2) -> bytes:
    request = urllib.request.Request(url, headers=github_headers(token))
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            if attempt >= retries:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}")


def paginated_rest(path: str, *, token: str | None, params: dict[str, str] | None = None) -> list[dict]:
    params = dict(params or {})
    params["per_page"] = "100"
    page = 1
    items: list[dict] = []
    while True:
        params["page"] = str(page)
        query = urllib.parse.urlencode(params)
        data = request_json(f"https://api.github.com{path}?{query}", token=token)
        if not isinstance(data, list):
            break
        items.extend(data)
        if len(data) < 100:
            break
        page += 1
    return items


def contribution_stats(username: str, token: str | None) -> tuple[int, int] | None:
    if not token:
        print("warning: no GitHub token available; contribution and commit stats will be 0")
        return None

    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(from: $from, to: $to) {
          totalCommitContributions
          repositoryContributions(first: 100) {
            totalCount
          }
        }
      }
    }
    """
    current_year = dt.datetime.now(dt.timezone.utc).year
    commits = 0
    contributed = 0
    for year in range(2005, current_year + 1):
        variables = {
            "login": username,
            "from": f"{year}-01-01T00:00:00Z",
            "to": f"{year}-12-31T23:59:59Z",
        }
        data = request_json(
            "https://api.github.com/graphql",
            token=token,
            data={"query": query, "variables": variables},
        )
        user = data.get("data", {}).get("user") if isinstance(data, dict) else None
        collection = user.get("contributionsCollection") if isinstance(user, dict) else None
        if not isinstance(collection, dict):
            continue
        commits += int(collection.get("totalCommitContributions") or 0)
        repos = collection.get("repositoryContributions") or {}
        contributed += int(repos.get("totalCount") or 0)
    return commits, contributed


def is_probably_text(data: bytes) -> bool:
    if b"\0" in data[:4096]:
        return False
    try:
        data[:4096].decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def count_repo_lines(repo: dict, token: str | None) -> int:
    full_name = repo.get("full_name")
    if not full_name:
        return 0
    default_branch = repo.get("default_branch") or "main"
    zipball_url = f"https://api.github.com/repos/{full_name}/zipball/{default_branch}"

    total = 0
    archive = request_bytes(zipball_url, token=token, retries=1)
    with zipfile.ZipFile(io.BytesIO(archive)) as zip_file:
        for item in zip_file.infolist():
            if item.is_dir() or item.file_size == 0:
                continue
            suffix = Path(item.filename).suffix.lower()
            if suffix in SKIP_EXTENSIONS:
                continue
            if item.file_size > 5_000_000:
                continue
            data = zip_file.read(item)
            if not is_probably_text(data):
                continue
            total += data.count(b"\n")
            if data and not data.endswith(b"\n"):
                total += 1
    return total


def count_all_repo_lines(repos: list[dict], token: str | None) -> int:
    total = 0
    for repo in repos:
        if repo.get("fork"):
            continue
        try:
            total += count_repo_lines(repo, token)
        except Exception as exc:
            name = repo.get("full_name") or repo.get("name") or "unknown repo"
            print(f"warning: skipped line count for {name}: {exc}")
    return total


def fetch_github_stats(username: str = USERNAME) -> dict[str, int]:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    stats = dict(STATIC_STATS)
    fetched_any = False

    try:
        user = request_json(f"https://api.github.com/users/{username}", token=token)
        if isinstance(user, dict):
            stats["repos"] = int(user.get("public_repos") or stats["repos"])
            stats["followers"] = int(user.get("followers") or stats["followers"])
            fetched_any = True

        repos = paginated_rest(
            f"/users/{username}/repos",
            token=token,
            params={"type": "owner", "sort": "updated", "direction": "desc"},
        )
        if repos:
            stats["stars"] = sum(int(repo.get("stargazers_count") or 0) for repo in repos)
            stats["repos"] = len(repos)

            if os.environ.get("COUNT_CODE_LINES") == "1":
                code_lines = count_all_repo_lines(repos, token)
                if code_lines:
                    stats["code_size"] = code_lines
                    stats["code_added"] = code_lines
                    stats["code_removed"] = 0
            else:
                language_bytes = 0
                for repo in repos:
                    languages_url = repo.get("languages_url")
                    if not languages_url:
                        continue
                    languages = request_json(str(languages_url), token=token, retries=1)
                    if isinstance(languages, dict):
                        language_bytes += sum(int(value) for value in languages.values())
                if language_bytes:
                    stats["code_size"] = language_bytes
                    stats["code_added"] = language_bytes
                    stats["code_removed"] = 0

        contributions = contribution_stats(username, token)
        if contributions:
            stats["commits"], stats["contributed"] = contributions
    except Exception as exc:
        if fetched_any:
            print(f"warning: partial GitHub stats fetch failed: {exc}")
        else:
            print(f"warning: GitHub stats fetch failed; unavailable stats will be 0: {exc}")

    return stats


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(
    x: float,
    y: float,
    body: str,
    *,
    size: int = 18,
    fill: str = TEXT,
    weight: int = 700,
    anchor: str = "start",
    opacity: float = 1.0,
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
        f'font-family="{FONT}" font-weight="{weight}" text-anchor="{anchor}" '
        f'opacity="{opacity:.3f}" xml:space="preserve">{esc(body)}</text>'
    )


def tspans(x: float, y: float, parts: list[tuple[str, str, int]], *, size: int = 18) -> str:
    out = [
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-family="{FONT}" font-weight="700" xml:space="preserve">'
    ]
    for fill, body, weight in parts:
        out.append(f'<tspan fill="{fill}" font-weight="{weight}">{esc(body)}</tspan>')
    out.append("</text>")
    return "".join(out)


def leader_line(
    label: str,
    value: str,
    y: float,
    *,
    x: float = 583,
    total_cols: int = TERMINAL_COLS,
    size: int = 18,
    value_color: str = TEXT,
    label_color: str = RED,
) -> str:
    label_text = f"· {label}:"
    dots = "." * max(2, total_cols - len(label_text) - len(value) - 2)
    return tspans(
        x,
        y,
        [
            (label_color, label_text, 700),
            (MUTED, f" {dots} ", 700),
            (value_color, value, 700),
        ],
        size=size,
    )


def dash_line(prefix: str, *, total_cols: int = TERMINAL_COLS, dash: str = "-") -> str:
    return prefix + dash * max(0, total_cols - len(prefix))


def section(y: float, title: str, *, x: float = 583, total_cols: int = TERMINAL_COLS) -> str:
    line = f"- {title} "
    return text(x, y, dash_line(line, total_cols=total_cols), fill=TEXT, size=18)


def stat_line(
    label: str,
    value_parts: list[tuple[str, str, int]],
    y: float,
    *,
    x: float = 583,
    total_cols: int = TERMINAL_COLS,
) -> str:
    value_len = sum(len(part) for _, part, _ in value_parts)
    dots = "." * max(2, total_cols - len(label) - value_len - 2)
    return tspans(x, y, [(RED, label, 700), (MUTED, f" {dots} ", 700), *value_parts])


def fmt(value: int) -> str:
    return f"{value:,}"


def github_stats(y: float, stats: dict[str, int]) -> list[str]:
    code_size = stats["code_size"]
    code_added = stats["code_added"]
    code_removed = stats["code_removed"]
    return [
        stat_line(
            "Repos:",
            value_parts=[
                (TEXT, f"{fmt(stats['repos'])} ", 700),
                (RED, f"(Contributed: {fmt(stats['contributed'])})", 700),
                (TEXT, " | ", 700),
                (RED, "Stars:", 700),
                (TEXT, f" {fmt(stats['stars'])}", 700),
            ],
            y=y,
        ),
        stat_line(
            "Commits:",
            value_parts=[
                (TEXT, f"{fmt(stats['commits'])} | ", 700),
                (RED, "Followers:", 700),
                (TEXT, f" {fmt(stats['followers'])}", 700),
            ],
            y=y + 26,
        ),
        stat_line(
            "Lines of Code on GitHub:",
            value_parts=[
                (TEXT, f"{fmt(code_size)} ", 700),
                ("#c13d43", f"( {fmt(code_added)}++", 700),
                (TEXT, f", {fmt(code_removed)}-- )", 700),
            ],
            y=y + 52,
        ),
    ]


def image_data_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def render(stats: dict[str, int] | None = None) -> str:
    stats = stats or fetch_github_stats()
    pieces: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Aarush Lenka terminal dashboard">',
        "<defs>",
        '<linearGradient id="panel-bg" x1="0" x2="1" y1="0" y2="1">',
        f'<stop offset="0" stop-color="{BG}"/>',
        f'<stop offset="0.55" stop-color="{BG_2}"/>',
        '<stop offset="1" stop-color="#191b1b"/>',
        "</linearGradient>",
        '<radialGradient id="warm-glow" cx="63%" cy="44%" r="55%">',
        '<stop offset="0" stop-color="#5c2729" stop-opacity="0.28"/>',
        '<stop offset="0.45" stop-color="#3a2727" stop-opacity="0.12"/>',
        '<stop offset="1" stop-color="#000000" stop-opacity="0"/>',
        "</radialGradient>",
        '<filter id="soft-shadow" x="-5%" y="-5%" width="110%" height="110%">',
        '<feDropShadow dx="0" dy="0" stdDeviation="2" flood-color="#0b0c0c" flood-opacity="0.75"/>',
        "</filter>",
        "</defs>",
        '<rect width="1472" height="655" fill="url(#panel-bg)"/>',
        '<rect width="1472" height="655" fill="url(#warm-glow)"/>',
        '<rect x="1" y="1" width="1470" height="653" fill="none" stroke="#101313" stroke-width="2"/>',
        '<rect x="3" y="3" width="1466" height="649" fill="none" stroke="#303735" stroke-width="1" opacity="0.5"/>',
        f'<image x="0" y="0" width="559" height="655" '
        f'href="{image_data_uri(ASCII_IMAGE)}" preserveAspectRatio="none"/>',
        text(583, 19, dash_line("aarush@lenka "), size=18),
        leader_line("OS", "Windows 11, Android 14, Linux", 45),
        leader_line("Uptime", uptime(), 71),
        leader_line("Host", "VIT, Vellore", 97),
        leader_line("Kernel", "Electronics Engineer", 123),
        leader_line("Languages.Programming", "Java, Python, Embedded C/C++, Verilog", 169),
        leader_line("Languages.Computer", "Bash, JSON, LaTeX, YAML", 195),
        leader_line("Languages.Real", "English, Hindi, Bengali", 221),
        leader_line("Tools.Software", "Docker, Git, n8n", 269),
        leader_line("Tools.Hardware", "Arduino Uno, ESP32, RaspberryPi", 295),
        leader_line("Tools.VLSI", "iVerilog, GTKWave, Yosys, OpenRoad", 321),
        leader_line("Hobbies.Creative", "Motion Graphics & 3D Artist", 369),
        leader_line("Tools.Creative", "After Effects, Blender, Figma", 395),
        section(443, "Contact"),
        leader_line("Email.Personal", "lenkaaarush@gmail.com", 469),
        leader_line("LinkedIn", "Aarush Lenka", 495),
        section(543, "GitHub Stats"),
        *github_stats(569, stats),
        "</svg>",
    ]
    return "\n".join(pieces) + "\n"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    stats = fetch_github_stats()
    print("stats: " + ", ".join(f"{key}={value}" for key, value in sorted(stats.items())))
    OUT.write_text(render(stats), encoding="utf-8")
    print(f"generated {OUT.relative_to(ROOT)} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
