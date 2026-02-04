#!/usr/bin/env python3
import os
import sys
import re
from urllib.parse import urlparse

HTML_EXTS = {".html", ".htm"}

LINK_RE = re.compile(r"\b(?:href|src)\s*=\s*\"([^\"]+)\"|\b(?:href|src)\s*=\s*'([^']+)'", re.IGNORECASE)

SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:")


def is_external(url: str) -> bool:
    if url.startswith(SKIP_SCHEMES):
        return True
    # Protocol-relative
    if url.startswith("//"):
        return True
    return False


def normalize_target(base_dir: str, html_dir: str, url: str) -> str:
    # Strip fragment
    path = url.split("#", 1)[0]
    if not path:
        return ""
    # Queryless
    path = path.split("?", 1)[0]

    # Absolute path under site root
    if path.startswith("/"):
        candidate = os.path.join(base_dir, path.lstrip("/"))
    else:
        # Relative to the HTML file directory
        candidate = os.path.normpath(os.path.join(html_dir, path))

    # If points to a directory, assume index.html
    if os.path.isdir(candidate):
        idx = os.path.join(candidate, "index.html")
        return idx

    # If no extension and not a file, try adding index.html
    _, ext = os.path.splitext(candidate)
    if not ext:
        # Most Hugo links end with trailing slash mapping to index.html; if missing slash we still try
        idx = os.path.join(candidate, "index.html")
        if os.path.exists(idx):
            return idx

    return candidate


def collect_html_files(root: str):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if os.path.splitext(f)[1].lower() in HTML_EXTS:
                yield os.path.join(dirpath, f)


def extract_links(content: str):
    for m in LINK_RE.finditer(content):
        url = m.group(1) or m.group(2)
        if url:
            yield url.strip()


def main():
    if len(sys.argv) < 2:
        print("Usage: check_links.py <public_dir>")
        sys.exit(2)
    base_dir = sys.argv[1]
    if not os.path.isdir(base_dir):
        print(f"ERROR: Directory not found: {base_dir}")
        sys.exit(2)

    total_files = 0
    total_links = 0
    broken = []  # list of tuples (html_file, url, resolved_path)

    for html_file in collect_html_files(base_dir):
        total_files += 1
        html_dir = os.path.dirname(html_file)
        try:
            with open(html_file, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
        except Exception as e:
            print(f"WARN: Could not read {html_file}: {e}")
            continue

        for url in extract_links(content):
            # Skip trivial or external
            if not url or url.startswith("#"):
                continue
            if is_external(url):
                continue

            total_links += 1
            target = normalize_target(base_dir, html_dir, url)
            if not target:
                # empty target (e.g., just fragment) already skipped
                continue
            if not os.path.exists(target):
                broken.append((html_file, url, target))

    print("\nLink Check Summary")
    print(f" HTML files scanned: {total_files}")
    print(f" Local links validated: {total_links}")
    print(f" Broken local links: {len(broken)}")

    if broken:
        print("\nBroken Links:")
        for html_file, url, target in broken:
            rel_html = os.path.relpath(html_file, base_dir)
            rel_target = os.path.relpath(target, base_dir)
            print(f" - Page: {rel_html}\n   URL: {url}\n   Resolved: {rel_target}")
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
