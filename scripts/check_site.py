#!/usr/bin/env python3
"""Structural gate for a built site directory.

Checks forbidden artifacts, robots.txt, internal links, fragments and image
attributes. Stdlib only; exits non-zero on any failure.
"""
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

FORBIDDEN_FILES = {"README.md", "FAVICON-README.md", "mermaid.min.js"}
FORBIDDEN_SUFFIXES = {".excalidraw"}
FORBIDDEN_DIRS = {"katex", "asciinema"}
# Decorative theme chrome: the book-icon menu/toc glyphs sit beside link text
# that already names them, so width/height/alt are not required there.
IMG_EXCEPTIONS = {"book-icon": "theme chrome icon, named by adjacent link text"}

LINK_TAGS = {"a", "area", "link", "script"}
TAG_RE = re.compile(r"<([a-zA-Z][a-zA-Z0-9-]*)\b([^>]*)>", re.S)
ATTR_RE = re.compile(r"""([a-zA-Z_:.-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+)))?""")
HREF_RE = re.compile(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//)")

LISTINGS = {}


def listing(directory):
    if directory not in LISTINGS:
        try:
            LISTINGS[directory] = set(os.listdir(directory))
        except OSError:
            LISTINGS[directory] = set()
    return LISTINGS[directory]


def exists_exact(root, path):
    """Case-exact file existence: GitHub Pages serves paths case-sensitively."""
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    current = root
    for part in parts:
        if part not in listing(current):
            return False
        current = current / part
    return current.is_file()


def attrs_of(text):
    found = {}
    for name, dq, sq, bare in ATTR_RE.findall(text):
        found.setdefault(name.lower(), dq or sq or bare)
    return found


def ids_of(text):
    ids = set()
    for name, dq, sq, bare in ATTR_RE.findall(text):
        if name.lower() in {"id", "name"} and (dq or sq or bare):
            ids.add(dq or sq or bare)
    return ids


def resolve(root, page, ref):
    """Resolve an HTML reference. Returns (file or None, fragment)."""
    ref = unquote(ref)
    path, _, fragment = ref.partition("#")
    path = path.split("?", 1)[0]
    if not path:
        return page, fragment
    base = root if path.startswith("/") else page.parent
    target = Path(os.path.normpath(base / path.lstrip("/")))
    candidates = [target / "index.html"] if path.endswith("/") else [target, target / "index.html"]
    for candidate in candidates:
        if exists_exact(root, candidate):
            return candidate, fragment
    return None, fragment


def main():
    if len(sys.argv) != 2:
        print("usage: check_site.py <built-site-dir>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    pages = sorted(root.rglob("*.html"))
    texts = {page: page.read_text(errors="replace") for page in pages}
    failures = []

    artifacts = 0
    for entry in sorted(root.rglob("*")):
        relative = entry.relative_to(root)
        if entry.is_dir() and entry.name in FORBIDDEN_DIRS:
            artifacts += 1
            failures.append(f"artifact: forbidden directory {relative}/")
        elif entry.is_file() and (entry.name in FORBIDDEN_FILES or entry.suffix in FORBIDDEN_SUFFIXES):
            artifacts += 1
            failures.append(f"artifact: forbidden file {relative}")

    robots = 1
    robots_path = root / "robots.txt"
    robots_text = robots_path.read_text(errors="replace") if robots_path.is_file() else ""
    if not robots_text:
        failures.append("robots: robots.txt missing")
    else:
        for required in ("User-agent:", "Sitemap:"):
            if required not in robots_text:
                failures.append(f"robots: missing {required!r}")

    links = fragments = images = exceptions = 0
    for page in pages:
        text = texts[page]
        id_cache = {}

        def page_ids(target):
            if target not in id_cache:
                id_cache[target] = ids_of(texts.get(target) or target.read_text(errors="replace"))
            return id_cache[target]

        for tag, attr_text in TAG_RE.findall(text):
            attrs = attrs_of(attr_text)
            if tag.lower() in LINK_TAGS:
                ref = attrs.get("href") or attrs.get("src")
                if ref is None or HREF_RE.match(ref) or ref == "#":
                    continue
                links += 1
                target, fragment = resolve(root, page, ref)
                if target is None:
                    failures.append(f"link: {page.relative_to(root)} -> {ref}")
                    continue
                if fragment and target.suffix == ".html":
                    fragments += 1
                    if unquote(fragment) not in page_ids(target):
                        failures.append(
                            f"fragment: {page.relative_to(root)} -> {ref} (no id/name)")
            elif tag.lower() == "img":
                images += 1
                classes = (attrs.get("class") or "").split()
                exempt = next((c for c in classes if c in IMG_EXCEPTIONS), None)
                if exempt:
                    exceptions += 1
                    continue
                missing = [name for name in ("alt", "width", "height") if name not in attrs]
                if missing:
                    failures.append(
                        f"image: {page.relative_to(root)} -> {attrs.get('src')} missing {'/'.join(missing)}")

    print(f"artifacts: {artifacts} forbidden, {len(list(root.rglob('*')))} entries scanned")
    print(f"robots: {'ok' if robots_text and not any(f.startswith('robots:') for f in failures) else 'FAIL'}")
    print(f"links: {links} internal checked")
    print(f"fragments: {fragments} checked")
    print(f"images: {images} checked, {exceptions} theme exceptions")
    if failures:
        print(f"FAIL: {len(failures)} problem(s)", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
