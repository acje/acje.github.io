"""Check C5.40 nominal geometry and preservation against a Git baseline."""
import argparse
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTICLE = "content/projects/pardosa/index.md"


def diagram(source):
    start = source.index('<svg id="crypto-diagram"')
    end = source.index("</svg>", start) + len("</svg>")
    return source[:start], ET.fromstring(source[start:end]), source[end:]


def number(element, key):
    return float(element.get(key, "0"))


def position(group):
    match = re.fullmatch(r"translate\((\d+),\s*(\d+)\)", group.get("transform", ""))
    assert match, "Expected explicit card translation"
    return tuple(map(float, match.groups()))


def verify(source, baseline):
    before, svg, after = diagram(source)
    old_before, old, old_after = diagram(baseline)
    assert (before, after) == (old_before, old_after), "Outside-diagram content changed"
    elements, originals = list(svg.iter()), list(old.iter())
    assert len(elements) == len(originals), "Diagram structure changed"
    for element, original in zip(elements, originals):
        assert element.tag == original.tag and element.text == original.text, "Text/structure changed"
        allowed = {"y", "height"} if element.tag == "rect" and element.get("y") else set()
        if element.tag == "text":
            allowed = {"y"}
        if element.get("id", "").startswith("fiber-"):
            allowed = {"transform"}
            assert position(element)[0] == position(original)[0], "Horizontal card position changed"
        if element.tag == "path" and element.get("class") == "edge-dashed":
            allowed = {"d"}
        if element is svg:
            allowed = {"viewBox"}
        if element.tag == "rect" and original.get("width") in {"340", "110"}:
            allowed |= {"x", "width"}
        assert {k: v for k, v in element.attrib.items() if k not in allowed} == {
            k: v for k, v in original.attrib.items() if k not in allowed
        }, "Non-layout attribute changed"
    direct = list(svg)
    rects = [e for e in direct if e.tag == "rect"]
    parent = next(e for e in rects if e.get("width") == "630")
    parent_badge = next(e for e in rects if e.get("y") == "164" and number(e, "x") < 100)
    groups = {e.get("id"): e for e in svg.iter("g") if e.get("id")}
    paths = [e for e in direct if e.tag == "path" and e.get("class") == "edge-dashed"]
    fibers = [e for e in rects if e.get("width") == "280"]
    assert len(fibers) == 2 and len(paths) == 2
    measurements = []
    for index, key in enumerate(("a", "b")):
        fiber = fibers[index]
        badge = direct[direct.index(fiber) + 1]
        connector = direct[direct.index(paths[index]) + 1].find("rect")
        root, update = groups[f"fiber-{key}-root"], groups[f"fiber-{key}-update"]
        x, root_y = position(root)
        _, update_y = position(update)
        root_bottom = root_y + number(root.find("rect"), "height")
        update_bottom = update_y + number(update.find("rect"), "height")
        fiber_bottom = number(fiber, "y") + number(fiber, "height")
        gaps = [number(badge, "y") - number(parent_badge, "y") - number(parent_badge, "height"),
                root_y - number(badge, "y") - number(badge, "height"),
                number(connector, "y") - root_bottom,
                update_y - number(connector, "y") - number(connector, "height"),
                fiber_bottom - update_bottom,
                number(parent, "y") + number(parent, "height") - fiber_bottom]
        assert all(gap >= minimum for gap, minimum in zip(gaps, [30, 16, 12, 12, 24, 24])), f"Fiber {key}: insufficient gaps {gaps}"
        assert x - number(fiber, "x") == 20
        assert number(fiber, "x") + number(fiber, "width") - x - number(root.find("rect"), "width") == 20
        center = x + 120
        assert paths[index].get("d") == f"M {center:g},{update_y:g} L {center:g},{root_bottom + 7:g}", "Backward link changed"
        measurements.append(gaps)
    assert measurements[0] == measurements[1], "Fibers use different spacing"
    assert number(fibers[1], "x") - number(fibers[0], "x") - number(fibers[0], "width") == 30
    box = list(map(float, svg.get("viewBox").split()))
    assert box[:3] == [0, 0, 1020] and box[3] >= number(parent, "y") + number(parent, "height") + 20
    print("PASS both fibers:", measurements[0], "text, IDs, attributes and outside content preserved")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", default="HEAD", help="Git revision before the spacing edit")
    args = parser.parse_args()
    baseline = subprocess.run(["git", "show", f"{args.baseline}:{ARTICLE}"], cwd=ROOT,
                              check=True, capture_output=True, text=True).stdout
    verify((ROOT / ARTICLE).read_text(), baseline)
