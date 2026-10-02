# Nested diagram spacing

Use explicit role-based geometry for new or locally revised nested diagrams.
The first application is Pardosa's `#crypto-diagram`, invariant C5.40: both
Fiber Alpha and Fiber Beta use the same vertical rhythm. This is an authoring
reference, not a mandate to migrate unrelated diagrams or introduce a generator.

## SVG roles and measurements

Measure nominal rectangle edges in SVG user units, not rendered CSS pixels.
Badge means its background rectangle; card means its enclosing rectangle.

| Role | Minimum clearance |
| --- | ---: |
| Parent heading badge bottom → child heading badge top | 30 |
| Child heading badge bottom → first card top | 16 |
| Card bottom → connector badge top | 12 |
| Connector badge bottom → next card top | 12 |
| Last card bottom → fiber enclosure bottom | 24 |
| Fiber enclosure bottom → parent enclosure bottom | 24 |
| Card sides → fiber enclosure sides | 20 |
| Sibling fiber enclosure gap | 30 |
| Label glyph bounds → badge sides at computed font | 8 |

Heading badges intentionally straddle their enclosure borders. Connector badges
intentionally cover arrow shafts; arrowheads still point from update to root.
These designed overlaps are not whitespace failures. Inspect rendered glyphs,
strokes, arrowheads and shadows separately: rectangle arithmetic does not prove
painted clearance or label fit. Measure the actual full-page computed fonts,
because later embedded styles can override earlier diagram rules. Prefer a
locally widened badge over shrinking type or changing global CSS.

The C5.40 recipe keeps 240 × 48 cards: parent badge bottom 186; child badges
216–234; roots 250–298; connector badges 310–328; updates 340–388; fiber
bottom 412; parent bottom 436; canvas bottom 456. Thus both fibers have
30 / 16 / 12 / 12 / 24 / 24 clearances. Horizontal card positions, insets,
sibling gap, event labels and E2 → E0 / E3 → E1 relationships remain unchanged.

## Grounding and HTML analogue

[Pardosa's dragline diagram](../../content/projects/pardosa/index.md) has a
heading badge at y=169 with height=22 and its first lane at y=221: a 30-unit
hierarchy clearance. This is a precedent for breathing room, not a pre-existing
badge-to-badge rule. C5.40 already supplied the 20-unit insets and 30-unit
sibling gap; the remaining minima are the local editorial spacing standard.

[sf-sdlc](../../content/projects/sf-sdlc/index.md) uses `.5rem` minor title
gaps, `.75rem` sibling/card gaps, `1rem` card/container padding, and `2rem`
container margins. Reuse these roles for HTML authoring. **Do not convert these
rem values into SVG units**: rem depends on the root font and SVG scale depends
on its viewBox and rendered width. C5.40 deliberately retains its 780px minimum
width and horizontally scrollable wrapper on small screens.

## Repeatable checks

From the repository root, before committing the edit:

```sh
python3 docs/editorial/verify-crypto-spacing.py --baseline HEAD
git diff --check
hugo build --renderToMemory --noBuildLock
```

After committing, supply the pre-edit revision instead of `HEAD`. The verifier
checks both fibers' gaps, equal spacing, horizontal insets/sibling gap, backward
arrows and canvas clearance. It compares text, structure, IDs, non-layout
attributes and content outside the diagram against the selected Git baseline.
It does not prove rendered font fit, visual appearance or arbitrary geometry
changes in the permitted layout attributes. Run Python normally, **not with
`-O`**, which disables assertions.

For browser inspection, build a fresh local preview into an ignored directory:

```sh
hugo build --noBuildLock --destination .ooda/tmp/crypto-preview \
  --baseURL file:///Users/anders.jensen/code/acje.github.io/.ooda/tmp/crypto-preview/
```

Use the absolute `file://` URL for your own checkout. Load the complete rendered
`projects/pardosa/index.html` with its CSS assets (not an isolated SVG). Inspect
at 1440 × 1000 and 390 × 844 in light and dark modes, including horizontal
scrolling to Beta on mobile. Wait for `document.fonts.ready`; use `getBBox()`
on each C5.40 heading/connector text and compare x bounds with its badge x/width.
Require at least eight SVG units on both sides. Retain full-page screenshots
and diagram crops as local artifacts; shut down every preview/browser process.
