---
title: "Pardosa: Event-Driven Storage with Fiber Semantics"
description: "Append-only fiber storage, generation-local integrity, and consumer-owned event projections"
weight: 20
draft: true
homeFeatured: true
---

## Pardosa: Event-Driven Storage with Fiber Semantics

Event-sourced applications need reliable entity histories, independent consumers, and a way to remove selected histories without corrupting the rest.

`Pardosa` is an append-only event-driven storage engine implemented in Rust, built upon **Fiber Semantics**. Its storage core admits event envelopes, checks fiber-local predecessor links and lifecycle rules, and records interleaved frames. Applications supply domain facts and define their views.

The implementation described here is [Pardosa at `bed69b8`](https://github.com/acje/pardosa/tree/bed69b854e3cf84c8e36c354feca3f36db2112b4). The migration section describes the [1.0 specification at that revision](https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/docs/spec/pardosa-1.0.md); the consumer examples distinguish complete snapshots from folds and retry handling.

<div class="pardosa-architecture-diagram" style="margin: 2rem 0; padding: 1.5rem 1rem; border-radius: 0.75rem; border: 1px solid var(--gray-200, #e2e8f0); background: var(--body-background, #ffffff); overflow-x: auto;">
<svg id="architecture-diagram" role="img" aria-labelledby="architecture-title architecture-desc" viewBox="0 0 1020 370" width="100%" height="auto" style="display: block; min-width: 780px; max-width: 1020px; margin: 0 auto; overflow: visible;">
<title id="architecture-title">Storage admission and consumer-owned projections</title>
<desc id="architecture-desc">Application facts pass authority, predecessor and lifecycle checks into an interleaved storage log. Consumers own read models and audit views.</desc>
<defs>
<marker id="arch-arrow-amber" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-amber-fill" />
</marker>
<marker id="arch-arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-blue-fill" />
</marker>
<marker id="arch-arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-green-fill" />
</marker>
<marker id="arch-arrow-cyan" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-cyan-fill" />
</marker>
<filter id="arch-shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.08"/>
</filter>
</defs>
<style>
:root {
--sm-edge-halo: var(--body-background, #ffffff);
--sm-badge-bg: var(--gray-100, #f8fafc);
--sm-badge-border: var(--gray-200, #cbd5e1);
--sm-badge-text: var(--body-font-color, #1e293b);
--sm-slate-bg: #f8fafc;
--sm-slate-stroke: #475569;
--sm-slate-text: #475569;
--sm-slate-sub: #64748b;
--sm-blue-bg: #eff6ff;
--sm-blue-stroke: #2563eb;
--sm-blue-text: #1d4ed8;
--sm-blue-sub: #2563eb;
--sm-amber-bg: #fffbeb;
--sm-amber-stroke: #d97706;
--sm-amber-text: #b45309;
--sm-amber-sub: #d97706;
--sm-green-bg: #ecfdf5;
--sm-green-stroke: #059669;
--sm-green-text: #047857;
--sm-green-sub: #059669;
--sm-cyan-bg: #ecfeff;
--sm-cyan-stroke: #0891b2;
--sm-cyan-text: #0e7490;
--sm-cyan-sub: #0891b2;
}
@media (prefers-color-scheme: dark) {
:root:not([data-theme="light"]) {
--sm-edge-halo: var(--body-background, #2e3440);
--sm-badge-bg: var(--gray-100, #3b4252);
--sm-badge-border: var(--gray-200, #434c5e);
--sm-badge-text: var(--body-font-color, #f1f5f9);
--sm-slate-bg: #1e293b;
--sm-slate-stroke: #64748b;
--sm-slate-text: #cbd5e1;
--sm-slate-sub: #94a3b8;
--sm-blue-bg: #172554;
--sm-blue-stroke: #3b82f6;
--sm-blue-text: #93c5fd;
--sm-blue-sub: #60a5fa;
--sm-amber-bg: #451a03;
--sm-amber-stroke: #f59e0b;
--sm-amber-text: #fde68a;
--sm-amber-sub: #fbbf24;
--sm-green-bg: #064e3b;
--sm-green-stroke: #10b981;
--sm-green-text: #6ee7b7;
--sm-green-sub: #34d399;
--sm-cyan-bg: #164e63;
--sm-cyan-stroke: #06b6d4;
--sm-cyan-text: #67e8f9;
--sm-cyan-sub: #22d3ee;
}
}
:root[data-theme="dark"] {
--sm-edge-halo: var(--body-background, #2e3440);
--sm-badge-bg: var(--gray-100, #3b4252);
--sm-badge-border: var(--gray-200, #434c5e);
--sm-badge-text: var(--body-font-color, #f1f5f9);
--sm-slate-bg: #1e293b;
--sm-slate-stroke: #64748b;
--sm-slate-text: #cbd5e1;
--sm-slate-sub: #94a3b8;
--sm-blue-bg: #172554;
--sm-blue-stroke: #3b82f6;
--sm-blue-text: #93c5fd;
--sm-blue-sub: #60a5fa;
--sm-amber-bg: #451a03;
--sm-amber-stroke: #f59e0b;
--sm-amber-text: #fde68a;
--sm-amber-sub: #fbbf24;
--sm-green-bg: #064e3b;
--sm-green-stroke: #10b981;
--sm-green-text: #6ee7b7;
--sm-green-sub: #34d399;
--sm-cyan-bg: #164e63;
--sm-cyan-stroke: #06b6d4;
--sm-cyan-text: #67e8f9;
--sm-cyan-sub: #22d3ee;
}
.arrow-amber-fill { fill: var(--sm-amber-stroke); }
.arrow-blue-fill { fill: var(--sm-blue-stroke); }
.arrow-green-fill { fill: var(--sm-green-stroke); }
.arrow-cyan-fill { fill: var(--sm-cyan-stroke); }
.node-title { font-size: 13.5px; font-weight: 700; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.node-sub { font-size: 11px; font-weight: 500; opacity: 0.9; font-family: system-ui, -apple-system, sans-serif; }
.tier-title { font-size: 12px; font-weight: 700; letter-spacing: 0.05em; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.edge-label { font-size: 11px; font-weight: 600; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.edge-path { fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.edge-halo { fill: none; stroke: var(--sm-edge-halo); stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; }
.badge-bg { fill: var(--sm-badge-bg); stroke: var(--sm-badge-border); stroke-width: 1.2; }
.badge-txt { fill: var(--sm-badge-text); }
</style>

<!-- Tier 1: Single-Writer Ingestion -->
<rect x="25" y="25" width="290" height="320" rx="10" fill="none" stroke="var(--sm-amber-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="40" y="14" width="180" height="22" rx="11" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="130" y="25" fill="var(--sm-amber-text)" dominant-baseline="central" text-anchor="middle">Storage Admission</text>

<!-- Tier 2: Storage Core -->
<rect x="365" y="25" width="290" height="320" rx="10" fill="none" stroke="var(--sm-blue-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="380" y="14" width="170" height="22" rx="11" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="465" y="25" fill="var(--sm-blue-text)" dominant-baseline="central" text-anchor="middle">Pardosa Storage Core</text>

<!-- Tier 3: Decoupled Consumption -->
<rect x="705" y="25" width="290" height="320" rx="10" fill="none" stroke="var(--sm-green-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="720" y="14" width="180" height="22" rx="11" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="810" y="25" fill="var(--sm-green-text)" dominant-baseline="central" text-anchor="middle">Decoupled Consumption</text>

<!-- Connecting Inter-Tier Curves -->
<!-- Ingestion ADMIT (275, 275) to Storage Core SM (405, 90) -->
<path d="M 275,275 C 330,275 350,90 398,90" class="edge-halo"/>
<path d="M 275,275 C 330,275 350,90 398,90" class="edge-path" stroke="var(--sm-blue-stroke)" marker-end="url(#arch-arrow-blue)"/>
<g>
<rect class="badge-bg" x="307" y="170" width="66" height="22" rx="11"/>
<text class="edge-label badge-txt" x="340" y="181" dominant-baseline="central" text-anchor="middle">Admitted</text>
</g>

<!-- Storage Core DRAG (615, 275) to Decoupled ECST (745, 185) -->
<path d="M 615,275 C 670,275 690,185 738,185" class="edge-halo"/>
<path d="M 615,275 C 670,275 690,185 738,185" class="edge-path" stroke="var(--sm-green-stroke)" marker-end="url(#arch-arrow-green)"/>
<g>
<rect class="badge-bg" x="647" y="217" width="66" height="22" rx="11"/>
<text class="edge-label badge-txt" x="680" y="228" dominant-baseline="central" text-anchor="middle">Committed</text>
</g>

<!-- Tier 1 Nodes & Links -->
<path d="M 170,118 L 170,147" class="edge-path" stroke="var(--sm-amber-stroke)" marker-end="url(#arch-arrow-amber)"/>
<path d="M 170,208 L 170,237" class="edge-path" stroke="var(--sm-amber-stroke)" marker-end="url(#arch-arrow-amber)"/>

<g id="node-cmd" transform="translate(45, 60)">
<rect width="250" height="58" rx="8" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-amber-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-amber-text)" dominant-baseline="central">Application Event Fact</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-amber-sub)">Caller IDs &amp; Opaque Payload</text>
</g>

<g id="node-cas" transform="translate(45, 150)">
<rect width="250" height="58" rx="8" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-amber-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-amber-text)" dominant-baseline="central">Authority &amp; Link Checks</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-amber-sub)">Writer Epoch; Fiber Predecessor</text>
</g>

<g id="node-admit" transform="translate(45, 240)">
<rect width="250" height="58" rx="8" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-amber-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-amber-text)" dominant-baseline="central">State Machine Admission</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-amber-sub)">10 Legal Transitions Gate</text>
</g>

<!-- Tier 2 Nodes & Links -->
<path d="M 510,118 L 510,147" class="edge-path" stroke="var(--sm-blue-stroke)" marker-end="url(#arch-arrow-blue)"/>
<path d="M 510,208 L 510,237" class="edge-path" stroke="var(--sm-blue-stroke)" marker-end="url(#arch-arrow-blue)"/>

<g id="node-sm" transform="translate(385, 60)">
<rect width="250" height="58" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-blue-text)" dominant-baseline="central">5-State Fiber Lifecycle</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-blue-sub)">Storage State, Not Domain State</text>
</g>

<g id="node-blake" transform="translate(385, 150)">
<rect width="250" height="58" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-blue-text)" dominant-baseline="central">CRC32C &amp; BLAKE3</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-blue-sub)">Frame Checksum; Prefix Commitment</text>
</g>

<g id="node-drag" transform="translate(385, 240)">
<rect width="250" height="58" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-blue-text)" dominant-baseline="central">Interleaved Dragline Stream</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-blue-sub)">Append-Only Disk Log (.pgno)</text>
</g>

<!-- Tier 3 Nodes & Links -->
<!-- From ECST up to PROJ -->
<path d="M 850,150 L 850,123" class="edge-path" stroke="var(--sm-cyan-stroke)" marker-end="url(#arch-arrow-cyan)"/>
<!-- From ECST down to AUDIT -->
<path d="M 850,218 L 850,237" class="edge-path" stroke="var(--sm-green-stroke)" marker-end="url(#arch-arrow-green)"/>

<g id="node-proj" transform="translate(725, 60)">
<rect width="250" height="58" rx="8" fill="var(--sm-cyan-bg)" stroke="var(--sm-cyan-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-cyan-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-cyan-text)" dominant-baseline="central">Autonomous Projections</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-cyan-sub)">Consumer-Owned Read Models</text>
</g>

<g id="node-ecst" transform="translate(725, 150)">
<rect width="250" height="58" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-green-text)" dominant-baseline="central">Consumer Event Reading</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-green-sub)">Complete Facts or Delta Folds</text>
</g>

<g id="node-audit" transform="translate(725, 240)">
<rect width="250" height="58" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-green-text)" dominant-baseline="central">Application Audit Views</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-green-sub)">Separate Retention &amp; Trust Anchors</text>
</g>

</svg>
</div>

---

## Fiber Lifecycle & Target Retention

Immutable histories support replay and audit, but retention policies may require selected histories to be removed. Pardosa separates fiber lifecycle admission from the **dragline**, the unit of serialization, durability and recorded order. Its file backend realizes that unit with append-only storage. The 1.0 migration design selects what a new generation retains; applications separately manage old generations, audit copies and downstream views.

---

## Fiber Semantics: Entities as Ordered Event Chains

In Fiber Semantics, the lifecycle history of each domain entity is modeled as an independent **fiber**:

- **Definition**: A fiber is a singly linked history identified by a storage `fiber_id`. The 1.0 specification scopes fiber identity to a dragline and event identity to a generation. Applications own the mapping between domain keys and storage histories.
- **Chain Topology**: Each event references its immediate predecessor through a `precursor` identifier and hash, linking the entity's history independently of other fibers.
- **Head-Anchored Traversal**: A fiber's newest event is its head. A latest-event lookup returns that event's envelope, not an automatically reconstructed entity view. Reading only the head suffices when its payload contains all data needed for the requested view; delta events require a consumer-defined fold or projection over the relevant history. Fiber-local links support historical traversal without requiring a full-log scan.

---

## Draglines: Append-Only Interleaved Commit Streams

Independent fiber histories can share one sequentially recorded **dragline**. This illustration interleaves A₀, B₀, A₁, C₀, B₁ and A₂; its ordinals indicate positions in each example history, not a persisted sequence field or a required ordering between fibers:

<div class="pardosa-dragline-diagram" style="margin: 2rem 0; padding: 1.5rem 1rem; border-radius: 0.75rem; border: 1px solid var(--gray-200, #e2e8f0); background: var(--body-background, #ffffff); overflow-x: auto;">
<svg id="dragline-diagram" role="img" aria-labelledby="dragline-title dragline-desc" viewBox="0 0 1040 480" width="100%" height="auto" style="display: block; min-width: 780px; max-width: 1040px; margin: 0 auto; overflow: visible;">
<title id="dragline-title">Interleaved frames and fiber-local histories</title>
<desc id="dragline-desc">Six illustrative frames interleave three fibers. Backward precursor links connect each fiber's history; ordinals are illustrative, not stored sequence fields.</desc>
<defs>
<marker id="drag-arrow-slate" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-slate-fill" />
</marker>
<marker id="drag-arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-blue-fill" />
</marker>
<marker id="drag-arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-green-fill" />
</marker>
<marker id="drag-arrow-amber" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-amber-fill" />
</marker>
<filter id="drag-shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.08"/>
</filter>
</defs>
<style>
:root {
--sm-edge-halo: var(--body-background, #ffffff);
--sm-badge-bg: var(--gray-100, #f8fafc);
--sm-badge-border: var(--gray-200, #cbd5e1);
--sm-badge-text: var(--body-font-color, #1e293b);
--sm-slate-bg: #f8fafc;
--sm-slate-stroke: #475569;
--sm-slate-text: #475569;
--sm-slate-sub: #64748b;
--sm-blue-bg: #eff6ff;
--sm-blue-stroke: #2563eb;
--sm-blue-text: #1d4ed8;
--sm-blue-sub: #2563eb;
--sm-amber-bg: #fffbeb;
--sm-amber-stroke: #d97706;
--sm-amber-text: #b45309;
--sm-amber-sub: #d97706;
--sm-green-bg: #ecfdf5;
--sm-green-stroke: #059669;
--sm-green-text: #047857;
--sm-green-sub: #059669;
}
@media (prefers-color-scheme: dark) {
:root:not([data-theme="light"]) {
--sm-edge-halo: var(--body-background, #2e3440);
--sm-badge-bg: var(--gray-100, #3b4252);
--sm-badge-border: var(--gray-200, #434c5e);
--sm-badge-text: var(--body-font-color, #f1f5f9);
--sm-slate-bg: #1e293b;
--sm-slate-stroke: #64748b;
--sm-slate-text: #cbd5e1;
--sm-slate-sub: #94a3b8;
--sm-blue-bg: #172554;
--sm-blue-stroke: #3b82f6;
--sm-blue-text: #93c5fd;
--sm-blue-sub: #60a5fa;
--sm-amber-bg: #451a03;
--sm-amber-stroke: #f59e0b;
--sm-amber-text: #fde68a;
--sm-amber-sub: #fbbf24;
--sm-green-bg: #064e3b;
--sm-green-stroke: #10b981;
--sm-green-text: #6ee7b7;
--sm-green-sub: #34d399;
}
}
:root[data-theme="dark"] {
--sm-edge-halo: var(--body-background, #2e3440);
--sm-badge-bg: var(--gray-100, #3b4252);
--sm-badge-border: var(--gray-200, #434c5e);
--sm-badge-text: var(--body-font-color, #f1f5f9);
--sm-slate-bg: #1e293b;
--sm-slate-stroke: #64748b;
--sm-slate-text: #cbd5e1;
--sm-slate-sub: #94a3b8;
--sm-blue-bg: #172554;
--sm-blue-stroke: #3b82f6;
--sm-blue-text: #93c5fd;
--sm-blue-sub: #60a5fa;
--sm-amber-bg: #451a03;
--sm-amber-stroke: #f59e0b;
--sm-amber-text: #fde68a;
--sm-amber-sub: #fbbf24;
--sm-green-bg: #064e3b;
--sm-green-stroke: #10b981;
--sm-green-text: #6ee7b7;
--sm-green-sub: #34d399;
}
.arrow-slate-fill { fill: var(--sm-slate-stroke); }
.arrow-blue-fill { fill: var(--sm-blue-stroke); }
.arrow-green-fill { fill: var(--sm-green-stroke); }
.arrow-amber-fill { fill: var(--sm-amber-stroke); }
.node-title { font-size: 13.5px; font-weight: 700; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.node-sub { font-size: 11px; font-weight: 500; opacity: 0.9; font-family: system-ui, -apple-system, sans-serif; }
.tier-title { font-size: 12px; font-weight: 700; letter-spacing: 0.05em; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.edge-label { font-size: 11px; font-weight: 600; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.edge-path { fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.edge-dashed { fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 4 3; }
.edge-halo { fill: none; stroke: var(--sm-edge-halo); stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; }
.badge-bg { fill: var(--sm-badge-bg); stroke: var(--sm-badge-border); stroke-width: 1.2; }
.badge-txt { fill: var(--sm-badge-text); }
</style>

<!-- Top Section: Physical Dragline -->
<rect x="15" y="25" width="1010" height="130" rx="10" fill="none" stroke="var(--sm-slate-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="35" y="14" width="300" height="22" rx="11" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="185" y="25" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle">Physical Dragline (Append-Only Stream)</text>

<!-- Left Gutter: Physical Dragline Badge -->
<g id="badge-physical">
<rect x="25" y="79" width="95" height="32" rx="8" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="72.5" y="89" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle" font-size="10px">Physical</text>
<text class="tier-title" x="72.5" y="101" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle" font-size="10px">Dragline</text>
</g>

<!-- Physical Sequential Append Links -->
<path d="M 260,95 L 288,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>
<path d="M 410,95 L 438,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>
<path d="M 560,95 L 588,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>
<path d="M 710,95 L 738,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>
<path d="M 860,95 L 888,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>

<!-- Physical Frame Cards -->
<g id="phys-e1" transform="translate(145, 63)">
<rect width="115" height="64" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="15" y="24" fill="var(--sm-blue-text)" dominant-baseline="central">E1: Id=A</text>
<text class="node-sub" x="15" y="44" fill="var(--sm-blue-sub)">A₀ (Create)</text>
</g>

<g id="phys-e2" transform="translate(295, 63)">
<rect width="115" height="64" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="15" y="24" fill="var(--sm-green-text)" dominant-baseline="central">E2: Id=B</text>
<text class="node-sub" x="15" y="44" fill="var(--sm-green-sub)">B₀ (Create)</text>
</g>

<g id="phys-e3" transform="translate(445, 63)">
<rect width="115" height="64" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="15" y="24" fill="var(--sm-blue-text)" dominant-baseline="central">E3: Id=A</text>
<text class="node-sub" x="15" y="44" fill="var(--sm-blue-sub)">A₁ (Update)</text>
</g>

<g id="phys-e4" transform="translate(595, 63)">
<rect width="115" height="64" rx="8" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-amber-stroke)"/>
<text class="node-title" x="15" y="24" fill="var(--sm-amber-text)" dominant-baseline="central">E4: Id=C</text>
<text class="node-sub" x="15" y="44" fill="var(--sm-amber-sub)">C₀ (Create)</text>
</g>

<g id="phys-e5" transform="translate(745, 63)">
<rect width="115" height="64" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="15" y="24" fill="var(--sm-green-text)" dominant-baseline="central">E5: Id=B</text>
<text class="node-sub" x="15" y="44" fill="var(--sm-green-sub)">B₁ (Update)</text>
</g>

<g id="phys-e6" transform="translate(895, 63)">
<rect width="115" height="64" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="15" y="24" fill="var(--sm-blue-text)" dominant-baseline="central">E6: Id=A</text>
<text class="node-sub" x="15" y="44" fill="var(--sm-blue-sub)">A₂ (Detach)</text>
</g>

<!-- Bottom Section: Logical Singly-Linked Fiber Histories -->
<rect x="15" y="180" width="1010" height="275" rx="10" fill="none" stroke="var(--sm-slate-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="35" y="169" width="340" height="22" rx="11" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="205" y="180" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle">Logical Singly-Linked Fiber Histories</text>

<!-- Horizontal Swimlane Backgrounds -->
<rect x="20" y="221" width="1000" height="70" rx="6" fill="var(--sm-blue-bg)" opacity="0.35"/>
<rect x="20" y="301" width="1000" height="70" rx="6" fill="var(--sm-green-bg)" opacity="0.35"/>
<rect x="20" y="381" width="1000" height="65" rx="6" fill="var(--sm-amber-bg)" opacity="0.35"/>

<!-- Left Gutter: Swimlane Badges -->
<g id="badge-fiber-a">
<rect x="25" y="244" width="95" height="24" rx="12" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="72.5" y="256" fill="var(--sm-blue-text)" dominant-baseline="central" text-anchor="middle">Fiber A</text>
</g>

<g id="badge-fiber-b">
<rect x="25" y="324" width="95" height="24" rx="12" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="72.5" y="336" fill="var(--sm-green-text)" dominant-baseline="central" text-anchor="middle">Fiber B</text>
</g>

<g id="badge-fiber-c">
<rect x="25" y="401" width="95" height="24" rx="12" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="72.5" y="413" fill="var(--sm-amber-text)" dominant-baseline="central" text-anchor="middle">Fiber C</text>
</g>

<!-- Precursor Backward Dashed Arrows for Fiber A -->
<!-- E6 (895) to E3 (445+115=560) -->
<path d="M 895,251 C 785,224 675,224 568,251" class="edge-halo"/>
<path d="M 895,251 C 785,224 675,224 568,251" class="edge-dashed" stroke="var(--sm-blue-stroke)" marker-end="url(#drag-arrow-blue)"/>
<g>
<rect class="badge-bg" x="688" y="219" width="80" height="20" rx="10"/>
<text class="edge-label badge-txt" x="728" y="229" dominant-baseline="central" text-anchor="middle">precursor</text>
</g>

<!-- E3 (445) to E1 (145+115=260) -->
<path d="M 445,251 C 385,224 320,224 268,251" class="edge-halo"/>
<path d="M 445,251 C 385,224 320,224 268,251" class="edge-dashed" stroke="var(--sm-blue-stroke)" marker-end="url(#drag-arrow-blue)"/>
<g>
<rect class="badge-bg" x="313" y="219" width="80" height="20" rx="10"/>
<text class="edge-label badge-txt" x="353" y="229" dominant-baseline="central" text-anchor="middle">precursor</text>
</g>

<!-- Swimlane A Event Cards -->
<g id="logic-e1" transform="translate(145, 231)">
<rect width="115" height="50" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-blue-text)" dominant-baseline="central">E1: Create</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-blue-sub)">A₀ (Root)</text>
</g>

<g id="logic-e3" transform="translate(445, 231)">
<rect width="115" height="50" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-blue-text)" dominant-baseline="central">E3: Update</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-blue-sub)">A₁</text>
</g>

<g id="logic-e6" transform="translate(895, 231)">
<rect width="115" height="50" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-blue-text)" dominant-baseline="central">E6: Detach</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-blue-sub)">A₂ (Head)</text>
</g>

<!-- Precursor Backward Dashed Arrow for Fiber B: E5 (745) to E2 (295+115=410) -->
<path d="M 745,331 C 655,304 510,304 418,331" class="edge-halo"/>
<path d="M 745,331 C 655,304 510,304 418,331" class="edge-dashed" stroke="var(--sm-green-stroke)" marker-end="url(#drag-arrow-green)"/>
<g>
<rect class="badge-bg" x="538" y="299" width="80" height="20" rx="10"/>
<text class="edge-label badge-txt" x="578" y="309" dominant-baseline="central" text-anchor="middle">precursor</text>
</g>

<!-- Swimlane B Event Cards -->
<g id="logic-e2" transform="translate(295, 311)">
<rect width="115" height="50" rx="7" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-green-text)" dominant-baseline="central">E2: Create</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-green-sub)">B₀ (Root)</text>
</g>

<g id="logic-e5" transform="translate(745, 311)">
<rect width="115" height="50" rx="7" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-green-text)" dominant-baseline="central">E5: Update</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-green-sub)">B₁ (Head)</text>
</g>

<!-- Swimlane C Event Card & Root Frame Badge -->
<g id="logic-e4" transform="translate(595, 388)">
<rect width="115" height="50" rx="7" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-amber-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-amber-text)" dominant-baseline="central">E4: Create</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-amber-sub)">C₀ (Root)</text>
</g>

<g>
<rect class="badge-bg" x="715" y="394" width="205" height="22" rx="11"/>
<text class="edge-label badge-txt" x="817" y="405" dominant-baseline="central" text-anchor="middle">Root Frame (precursor=0x00)</text>
</g>

<!-- Projection Drop Lines from Physical Stream down to Logical Chains -->
<path d="M 202.5,127 L 202.5,231" class="edge-dashed" stroke="var(--sm-blue-stroke)" opacity="0.35"/>
<path d="M 352.5,127 L 352.5,311" class="edge-dashed" stroke="var(--sm-green-stroke)" opacity="0.35"/>
<path d="M 502.5,127 L 502.5,231" class="edge-dashed" stroke="var(--sm-blue-stroke)" opacity="0.35"/>
<path d="M 652.5,127 L 652.5,388" class="edge-dashed" stroke="var(--sm-amber-stroke)" opacity="0.35"/>
<path d="M 802.5,127 L 802.5,311" class="edge-dashed" stroke="var(--sm-green-stroke)" opacity="0.35"/>
<path d="M 952.5,127 L 952.5,231" class="edge-dashed" stroke="var(--sm-blue-stroke)" opacity="0.35"/>

</svg>
</div>

- **Interleaving**: A dragline records frames from multiple fibers in one physical order; predecessor links retain each fiber's own order.
- **Admission and fencing**: The [append pipeline](https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/crates/pardosa/src/store/pipeline.rs#L355-L470) checks writer authority, envelope validity and fiber admission. Matching the current predecessor is one requirement, separate from artefact ownership/epoch fencing and lifecycle checks.
- **Write outcomes**: The file append path writes to the existing file and calls `sync_data`. The pipeline distinguishes `Landed` from `Undetermined`; an uncertain landing requires reconciliation before continued use. Creation/replacement protocols are distinct from per-frame append.

---

## Physical Data Structure: On-Disk Dragline Layout

Pardosa separates line state into an artefact pair on disk:

1. **`<stem>.meta` (Descriptor File)**: Stores the line descriptor and schema commitments.
2. **`<stem>.pgno` (Dragline Container File)**: Append-only storage file containing the container header followed by framed event records.

<style>
  .dragline-container {
    --dl-bg: #ffffff;
    --dl-text: #0f172a;
    --dl-text-muted: #475569;
    --dl-code-bg: rgba(15, 23, 42, 0.06);
    --dl-code-text: #0f172a;

    --dl-slate-border: #64748b;
    --dl-slate-bg: rgba(100, 116, 139, 0.05);
    --dl-slate-tag-bg: #475569;
    --dl-slate-tag-text: #ffffff;

    --dl-blue-border: #2563eb;
    --dl-blue-bg: rgba(37, 99, 235, 0.04);
    --dl-blue-tag-bg: #1d4ed8;
    --dl-blue-tag-text: #ffffff;

    --dl-purple-border: #7c3aed;
    --dl-purple-bg: rgba(124, 58, 237, 0.04);
    --dl-purple-tag-bg: #6d28d9;
    --dl-purple-tag-text: #ffffff;

    --dl-connector-bg: rgba(241, 245, 249, 0.95);
    --dl-connector-border: #cbd5e1;

    box-sizing: border-box;
    width: 100%;
    margin: 2rem 0;
    padding: 1rem;
    background: var(--dl-bg);
    border: 1.5px solid var(--dl-slate-border);
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 0.875rem;
    line-height: 1.5;
    color: var(--dl-text);
  }

  :root[data-theme="dark"] .dragline-container {
    --dl-bg: #0f172a;
    --dl-text: #f1f5f9;
    --dl-text-muted: #94a3b8;
    --dl-code-bg: rgba(0, 0, 0, 0.4);
    --dl-code-text: #f8fafc;

    --dl-slate-border: #64748b;
    --dl-slate-bg: rgba(100, 116, 139, 0.15);
    --dl-slate-tag-bg: #334155;
    --dl-slate-tag-text: #f8fafc;

    --dl-blue-border: #3b82f6;
    --dl-blue-bg: rgba(59, 130, 246, 0.12);
    --dl-blue-tag-bg: #1d4ed8;
    --dl-blue-tag-text: #eff6ff;

    --dl-purple-border: #8b5cf6;
    --dl-purple-bg: rgba(139, 92, 246, 0.12);
    --dl-purple-tag-bg: #5b21b6;
    --dl-purple-tag-text: #f5f3ff;

    --dl-connector-bg: rgba(30, 41, 59, 0.9);
    --dl-connector-border: #475569;
  }

  @media (prefers-color-scheme: dark) {
    :root[data-theme="auto"] .dragline-container,
    :root:not([data-theme="light"]):not([data-theme="dark"]) .dragline-container {
      --dl-bg: #0f172a;
      --dl-text: #f1f5f9;
      --dl-text-muted: #94a3b8;
      --dl-code-bg: rgba(0, 0, 0, 0.4);
      --dl-code-text: #f8fafc;

      --dl-slate-border: #64748b;
      --dl-slate-bg: rgba(100, 116, 139, 0.15);
      --dl-slate-tag-bg: #334155;
      --dl-slate-tag-text: #f8fafc;

      --dl-blue-border: #3b82f6;
      --dl-blue-bg: rgba(59, 130, 246, 0.12);
      --dl-blue-tag-bg: #1d4ed8;
      --dl-blue-tag-text: #eff6ff;

      --dl-purple-border: #8b5cf6;
      --dl-purple-bg: rgba(139, 92, 246, 0.12);
      --dl-purple-tag-bg: #5b21b6;
      --dl-purple-tag-text: #f5f3ff;

      --dl-connector-bg: rgba(30, 41, 59, 0.9);
      --dl-connector-border: #475569;
    }
  }

  .dragline-container * {
    box-sizing: border-box;
  }

  .dl-card {
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.25rem;
    background: var(--dl-bg);
    transition: border-color 0.2s ease;
  }

  .dl-card-header {
    border: 1.5px solid var(--dl-slate-border);
    background: var(--dl-slate-bg);
  }

  .dl-card-frame {
    border: 2px solid var(--dl-slate-border);
    background: var(--dl-slate-bg);
  }

  .dl-card-envelope {
    border: 1.5px solid var(--dl-blue-border);
    background: var(--dl-blue-bg);
    border-radius: 6px;
    padding: 0.875rem;
    margin: 0.875rem 0;
  }

  .dl-card-title-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.875rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(100, 116, 139, 0.2);
  }

  .dl-title-group {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .dl-title {
    font-weight: 600;
    font-size: 0.9375rem;
  }

  .dl-tag {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.025em;
    text-transform: uppercase;
  }

  .dl-tag-slate { background: var(--dl-slate-tag-bg); color: var(--dl-slate-tag-text); }
  .dl-tag-blue { background: var(--dl-blue-tag-bg); color: var(--dl-blue-tag-text); }
  .dl-tag-purple { background: var(--dl-purple-tag-bg); color: var(--dl-purple-tag-text); }

  .dl-section-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--dl-text-muted);
    margin: 0.75rem 0 0.375rem 0;
  }

  .dl-grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 0.75rem;
  }

  .dl-grid-envelope {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 0.5rem;
  }

  .dl-field {
    border-radius: 6px;
    padding: 0.625rem 0.75rem;
    border: 1px solid rgba(100, 116, 139, 0.25);
    background: var(--dl-bg);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  .dl-field-slate { border-left: 3px solid var(--dl-slate-border); }
  .dl-field-blue { border-left: 3px solid var(--dl-blue-border); }
  .dl-field-purple { border-left: 3px solid var(--dl-purple-border); }

  .dl-field-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--dl-text-muted);
    margin-bottom: 0.25rem;
  }

  .dl-field-val {
    font-size: 0.8125rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.375rem;
  }

  .dl-field-val code {
    background: var(--dl-code-bg);
    color: var(--dl-code-text);
    padding: 0.15rem 0.35rem;
    border-radius: 3px;
    font-size: 0.8125rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }

  .dl-field-hex {
    font-size: 0.75rem;
    color: var(--dl-text-muted);
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }

  .dl-field-desc {
    font-size: 0.72rem;
    color: var(--dl-text-muted);
  }

  .dl-flow-arrow {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0.5rem 0;
  }

  .dl-arrow-line {
    width: 2px;
    height: 14px;
    background: var(--dl-slate-border);
  }

  .dl-arrow-badge {
    background: var(--dl-connector-bg);
    border: 1px solid var(--dl-connector-border);
    border-radius: 12px;
    padding: 0.2rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--dl-text-muted);
    margin: 2px 0;
  }

  .dl-arrow-head {
    font-size: 0.75rem;
    color: var(--dl-slate-border);
    line-height: 1;
  }

  @media (max-width: 640px) {
    .dl-grid-envelope {
      grid-template-columns: 1fr 1fr;
    }
    .dl-grid-2 {
      grid-template-columns: 1fr;
    }
  }

  .consumer-proj-container {
    --cp-bg: #ffffff;
    --cp-text: #0f172a;
    --cp-text-muted: #475569;
    --cp-slate-border: #64748b;
    --cp-blue-border: #2563eb;

    box-sizing: border-box;
    width: 100%;
    max-width: 100%;
    margin: 2rem 0;
    padding: 1rem;
    background: var(--cp-bg);
    border: 1.5px solid var(--cp-slate-border);
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 0.875rem;
    line-height: 1.5;
    color: var(--cp-text);
    overflow-wrap: anywhere;
  }

  :root[data-theme="dark"] .consumer-proj-container,
  :root[data-theme$="dark"] .consumer-proj-container {
    --cp-bg: #0f172a;
    --cp-text: #f1f5f9;
    --cp-text-muted: #94a3b8;
    --cp-slate-border: #64748b;
    --cp-blue-border: #3b82f6;
  }

  @media (prefers-color-scheme: dark) {
    :root[data-theme="auto"] .consumer-proj-container,
    :root:not([data-theme="light"]):not([data-theme="dark"]) .consumer-proj-container {
      --cp-bg: #0f172a;
      --cp-text: #f1f5f9;
      --cp-text-muted: #94a3b8;
      --cp-slate-border: #64748b;
      --cp-blue-border: #3b82f6;
    }
  }

  .consumer-proj-container * {
    box-sizing: border-box;
  }

  .consumer-proj-container h3 {
    margin: 0 0 .5rem;
    font-size: 1rem;
    color: var(--cp-text);
  }

  .consumer-proj-container p {
    margin: 0 0 .75rem;
    color: var(--cp-text-muted);
  }

  .consumer-proj-container a {
    color: var(--cp-blue-border);
    text-decoration: underline;
  }

  .consumer-proj-container code {
    padding: 0;
    background: transparent;
    color: var(--cp-text);
    font-size: .8125rem;
    white-space: normal;
    overflow-wrap: anywhere;
  }

  .consumer-proj-container .cp-layer {
    padding: 1rem;
    border: 1px solid var(--cp-slate-border);
    border-radius: 6px;
  }

  .consumer-proj-container .cp-layer + .cp-layer {
    margin-top: .75rem;
  }

  .consumer-proj-container h4 {
    margin: 0 0 .5rem;
    font-size: .875rem;
    color: var(--cp-text);
  }

  .consumer-proj-container .cp-facts,
  .consumer-proj-container .cp-paths {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: .75rem;
    margin: 0 0 .75rem;
  }

  .consumer-proj-container .cp-fact,
  .consumer-proj-container .cp-path {
    min-width: 0;
    padding: 1rem;
    border: 1px solid var(--cp-slate-border);
    border-radius: 6px;
  }

  .consumer-proj-container ol {
    padding-left: 1.25rem;
    margin: 0 0 .75rem;
  }

  .consumer-proj-container li + li {
    margin-top: .75rem;
  }

  .consumer-proj-container .cp-layer p:last-child,
  .consumer-proj-container .cp-path p:last-child {
    margin-bottom: 0;
  }

  @media (max-width: 640px) {
    .consumer-proj-container .cp-facts,
    .consumer-proj-container .cp-paths {
      grid-template-columns: 1fr;
    }
  }

  .consumer-proj-container .cp-result {
    color: var(--cp-blue-border);
    font-weight: 600;
  }

</style>

<div class="dragline-container">
  <!-- Container Header Block -->
  <div class="dl-card dl-card-header">
    <div class="dl-card-title-bar">
      <div class="dl-title-group">
        <span class="dl-tag dl-tag-slate">Format Identity</span>
        <span class="dl-title">Container Header · Storage Format Identity</span>
      </div>
      <span class="dl-tag dl-tag-slate">Immutable Prefix</span>
    </div>
    <div class="dl-grid-2">
      <div class="dl-field dl-field-slate">
        <div class="dl-field-label">Engine signature</div>
        <div class="dl-field-val"><code>PARDOSA\x01</code></div>
        <div class="dl-field-desc">8-byte magic, including terminal 0x01</div>
      </div>
      <div class="dl-field dl-field-slate">
        <div class="dl-field-label">Format version</div>
        <div class="dl-field-val"><code>1</code></div>
        <div class="dl-field-desc">u32 little-endian format version</div>
      </div>
    </div>
  </div>
  <!-- Flow Boundary: Container Header to Frame 0 -->
  <div class="dl-flow-arrow">
    <div class="dl-arrow-line"></div>
    <div class="dl-arrow-badge">Events follow the container header</div>
    <div class="dl-arrow-head">▼</div>
  </div>
  <!-- FRAME 0 -->
  <div class="dl-card dl-card-frame">
    <div class="dl-card-title-bar">
      <div class="dl-title-group">
        <span class="dl-tag dl-tag-slate">FRAME 0</span>
        <span class="dl-title">Event 0 : Genesis on Fiber A</span>
      </div>
      <span class="dl-tag dl-tag-blue">Genesis Root</span>
    </div>
    <div class="dl-section-label">Record Boundary</div>
    <div class="dl-field dl-field-slate">
      <div class="dl-field-label">Record length</div>
      <div class="dl-field-val"><code>Envelope size</code></div>
      <div class="dl-field-desc">Enclosed envelope byte length</div>
    </div>
    <!-- Inner Envelope 0 Card (Strictly Contained) -->
    <div class="dl-card dl-card-envelope">
      <div class="dl-card-title-bar">
        <div class="dl-title-group">
          <span class="dl-tag dl-tag-blue">Envelope 0</span>
          <span class="dl-title">Envelope 0 · Event and Storage Fiber</span>
        </div>
        <span class="dl-tag dl-tag-purple">Domain Fact</span>
      </div>
      <div class="dl-section-label">Identity and History Links</div>
      <div class="dl-grid-envelope">
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">Event identity</div>
          <div class="dl-field-val"><code>E0</code></div>
          <div class="dl-field-desc">16-byte event identifier</div>
        </div>
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">Storage fiber identity</div>
          <div class="dl-field-val"><code>Fiber A</code></div>
          <div class="dl-field-desc">16-byte storage fiber identifier</div>
        </div>
        <div class="dl-field dl-field-slate">
          <div class="dl-field-label">Attachment</div>
          <div class="dl-field-val"><code>Attached</code></div>
          <div class="dl-field-desc">Lifecycle marker</div>
        </div>
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">Previous event</div>
          <div class="dl-field-val"><code>No predecessor</code></div>
          <div class="dl-field-desc">Genesis begins the fiber</div>
        </div>
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">Predecessor commitment</div>
          <div class="dl-field-val"><code>Root marker</code></div>
          <div class="dl-field-desc">No earlier event to verify</div>
        </div>
      </div>
      <div class="dl-section-label">Domain Event Payload</div>
      <div class="dl-grid-2">
        <div class="dl-field dl-field-purple">
          <div class="dl-field-label">Payload length</div>
          <div class="dl-field-val"><code>Fact size</code></div>
          <div class="dl-field-desc">Domain payload byte length</div>
        </div>
        <div class="dl-field dl-field-purple">
          <div class="dl-field-label">Domain fact</div>
          <div class="dl-field-val"><code>GenesisState</code></div>
          <div class="dl-field-desc">State transition payload</div>
        </div>
      </div>
    </div>
    <div class="dl-section-label">Corruption Check</div>
    <div class="dl-field dl-field-slate">
      <div class="dl-field-label">Frame checksum</div>
      <div class="dl-field-val"><code>CRC32C</code></div>
      <div class="dl-field-desc">CRC32C over enclosed envelope bytes</div>
    </div>
  </div>
  <!-- Contiguous On-Disk Boundary -->
  <div class="dl-flow-arrow">
    <div class="dl-arrow-line"></div>
    <div class="dl-arrow-badge">Next event appends after the previous frame</div>
    <div class="dl-arrow-head">▼</div>
  </div>
  <!-- FRAME 1 -->
  <div class="dl-card dl-card-frame">
    <div class="dl-card-title-bar">
      <div class="dl-title-group">
        <span class="dl-tag dl-tag-slate">FRAME 1</span>
        <span class="dl-title">Event 1 : State Mutation on Fiber A</span>
      </div>
      <span class="dl-tag dl-tag-blue">Fiber A Mutation</span>
    </div>
    <div class="dl-section-label">Record Boundary</div>
    <div class="dl-field dl-field-slate">
      <div class="dl-field-label">Record length</div>
      <div class="dl-field-val"><code>Envelope size</code></div>
      <div class="dl-field-desc">Enclosed envelope byte length</div>
    </div>
    <!-- Inner Envelope 1 Card (Strictly Contained) -->
    <div class="dl-card dl-card-envelope">
      <div class="dl-card-title-bar">
        <div class="dl-title-group">
          <span class="dl-tag dl-tag-blue">Envelope 1</span>
          <span class="dl-title">Envelope 1 · Event and Storage Fiber</span>
        </div>
        <span class="dl-tag dl-tag-purple">Domain Fact</span>
      </div>
      <div class="dl-section-label">Identity and History Links</div>
      <div class="dl-grid-envelope">
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">Event identity</div>
          <div class="dl-field-val"><code>E1</code></div>
          <div class="dl-field-desc">16-byte event identifier</div>
        </div>
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">Storage fiber identity</div>
          <div class="dl-field-val"><code>Fiber A</code></div>
          <div class="dl-field-desc">16-byte storage fiber identifier</div>
        </div>
        <div class="dl-field dl-field-slate">
          <div class="dl-field-label">Attachment</div>
          <div class="dl-field-val"><code>Attached</code></div>
          <div class="dl-field-desc">Lifecycle marker</div>
        </div>
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">Previous event</div>
          <div class="dl-field-val"><code>E0</code></div>
          <div class="dl-field-desc">Preceding event on fiber</div>
        </div>
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">Predecessor commitment</div>
          <div class="dl-field-val"><code>BLAKE3(Env 0)</code></div>
          <div class="dl-field-desc">Digest of precursor envelope</div>
        </div>
      </div>
      <div class="dl-section-label">Domain Event Payload</div>
      <div class="dl-grid-2">
        <div class="dl-field dl-field-purple">
          <div class="dl-field-label">Payload length</div>
          <div class="dl-field-val"><code>Fact size</code></div>
          <div class="dl-field-desc">Domain payload byte length</div>
        </div>
        <div class="dl-field dl-field-purple">
          <div class="dl-field-label">Domain fact</div>
          <div class="dl-field-val"><code>AccountUpdated</code></div>
          <div class="dl-field-desc">State transition payload</div>
        </div>
      </div>
    </div>
    <div class="dl-section-label">Corruption Check</div>
    <div class="dl-field dl-field-slate">
      <div class="dl-field-label">Frame checksum</div>
      <div class="dl-field-val"><code>CRC32C</code></div>
      <div class="dl-field-desc">CRC32C over enclosed envelope bytes</div>
    </div>
  </div>
</div>

The cards group fields by role rather than showing byte offsets. The **container header** identifies the format; **framing** uses a u32 little-endian enclosed-envelope length and trailing CRC32C over those enclosed bytes ([C3.4](https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/docs/spec/pardosa-1.0.md#c34--invariant)). The envelope carries 16-byte event and fiber IDs, a one-byte attachment flag, a 16-byte predecessor ID, a 32-byte predecessor commitment, then u32 little-endian payload length and opaque payload bytes. Genesis predecessor fields are zero; domain fact names in the cards are application examples.

### Physical vs. Logical Cryptographic Commitments

Pardosa maintains two complementary, orthogonal cryptographic chains:

<div class="pardosa-crypto-diagram" style="margin: 2rem 0; padding: 1.5rem 1rem; border-radius: 0.75rem; border: 1px solid var(--gray-200, #e2e8f0); background: var(--body-background, #ffffff); overflow-x: auto;">
<svg id="crypto-diagram" role="img" aria-labelledby="crypto-title crypto-desc" viewBox="0 0 1020 456" width="100%" height="auto" style="display: block; min-width: 780px; max-width: 1020px; margin: 0 auto; overflow: visible;">
<title id="crypto-title">Physical prefix and logical predecessor commitments</title>
<desc id="crypto-desc">One continuous BLAKE3 hasher commits to physical frame order. Fiber-local hashes commit to canonical predecessor headers and payloads within one generation. Migration remints and rechains retained events.</desc>
<defs>
<marker id="crypto-arrow-slate" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-slate-fill" />
</marker>
<marker id="crypto-arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-blue-fill" />
</marker>
<marker id="crypto-arrow-green" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-green-fill" />
</marker>
<filter id="crypto-shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.08"/>
</filter>
</defs>
<style>
:root {
--sm-edge-halo: var(--body-background, #ffffff);
--sm-badge-bg: var(--gray-100, #f8fafc);
--sm-badge-border: var(--gray-200, #cbd5e1);
--sm-badge-text: var(--body-font-color, #1e293b);
--sm-slate-bg: #f8fafc;
--sm-slate-stroke: #475569;
--sm-slate-text: #475569;
--sm-slate-sub: #64748b;
--sm-blue-bg: #eff6ff;
--sm-blue-stroke: #2563eb;
--sm-blue-text: #1d4ed8;
--sm-blue-sub: #2563eb;
--sm-green-bg: #ecfdf5;
--sm-green-stroke: #059669;
--sm-green-text: #047857;
--sm-green-sub: #059669;
--sm-purple-bg: #f5f3ff;
--sm-purple-stroke: #7c3aed;
--sm-purple-text: #6d28d9;
--sm-purple-sub: #7c3aed;
}
@media (prefers-color-scheme: dark) {
:root:not([data-theme="light"]) {
--sm-edge-halo: var(--body-background, #2e3440);
--sm-badge-bg: var(--gray-100, #3b4252);
--sm-badge-border: var(--gray-200, #434c5e);
--sm-badge-text: var(--body-font-color, #f1f5f9);
--sm-slate-bg: #1e293b;
--sm-slate-stroke: #64748b;
--sm-slate-text: #cbd5e1;
--sm-slate-sub: #94a3b8;
--sm-blue-bg: #172554;
--sm-blue-stroke: #3b82f6;
--sm-blue-text: #93c5fd;
--sm-blue-sub: #60a5fa;
--sm-green-bg: #064e3b;
--sm-green-stroke: #10b981;
--sm-green-text: #6ee7b7;
--sm-green-sub: #34d399;
--sm-purple-bg: #2e1065;
--sm-purple-stroke: #a855f7;
--sm-purple-text: #d8b4fe;
--sm-purple-sub: #c084fc;
}
}
:root[data-theme="dark"] {
--sm-edge-halo: var(--body-background, #2e3440);
--sm-badge-bg: var(--gray-100, #3b4252);
--sm-badge-border: var(--gray-200, #434c5e);
--sm-badge-text: var(--body-font-color, #f1f5f9);
--sm-slate-bg: #1e293b;
--sm-slate-stroke: #64748b;
--sm-slate-text: #cbd5e1;
--sm-slate-sub: #94a3b8;
--sm-blue-bg: #172554;
--sm-blue-stroke: #3b82f6;
--sm-blue-text: #93c5fd;
--sm-blue-sub: #60a5fa;
--sm-green-bg: #064e3b;
--sm-green-stroke: #10b981;
--sm-green-text: #6ee7b7;
--sm-green-sub: #34d399;
--sm-purple-bg: #2e1065;
--sm-purple-stroke: #a855f7;
--sm-purple-text: #d8b4fe;
--sm-purple-sub: #c084fc;
}
.arrow-slate-fill { fill: var(--sm-slate-stroke); }
.arrow-blue-fill { fill: var(--sm-blue-stroke); }
.arrow-green-fill { fill: var(--sm-green-stroke); }
.node-title { font-size: 13.5px; font-weight: 700; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.node-sub { font-size: 11px; font-weight: 500; opacity: 0.9; font-family: system-ui, -apple-system, sans-serif; }
.tier-title { font-size: 12px; font-weight: 700; letter-spacing: 0.05em; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.edge-label { font-size: 10.5px; font-weight: 600; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.edge-path { fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.edge-dashed { fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 4 3; }
.edge-halo { fill: none; stroke: var(--sm-edge-halo); stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; }
.badge-bg { fill: var(--sm-badge-bg); stroke: var(--sm-badge-border); stroke-width: 1.2; }
.badge-txt { fill: var(--sm-badge-text); }
.callout-body { font-size: 11.5px; line-height: 1.5; font-family: system-ui, -apple-system, sans-serif; fill: var(--sm-badge-text); opacity: 0.95; }
</style>

<!-- Top Section: Physical Integrity Chain (Invariant C5.26) -->
<rect x="20" y="25" width="980" height="130" rx="10" fill="none" stroke="var(--sm-slate-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="35" y="14" width="330" height="22" rx="11" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="200" y="25" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle">Physical Integrity Chain (Invariant <a href="https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/docs/spec/pardosa-1.0.md#c526--invariant">C5.26</a>)</text>

<!-- Sequential Links with BLAKE3 Fold badges -->
<path d="M 175,90 L 227,90" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#crypto-arrow-slate)"/>
<g>
<rect class="badge-bg" x="180" y="58" width="42" height="18" rx="9"/>
<text class="edge-label badge-txt" x="201" y="67" dominant-baseline="central" text-anchor="middle">Fold</text>
</g>

<path d="M 365,90 L 417,90" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#crypto-arrow-slate)"/>
<g>
<rect class="badge-bg" x="370" y="58" width="42" height="18" rx="9"/>
<text class="edge-label badge-txt" x="391" y="67" dominant-baseline="central" text-anchor="middle">Fold</text>
</g>

<path d="M 555,90 L 607,90" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#crypto-arrow-slate)"/>
<g>
<rect class="badge-bg" x="560" y="58" width="42" height="18" rx="9"/>
<text class="edge-label badge-txt" x="581" y="67" dominant-baseline="central" text-anchor="middle">Fold</text>
</g>

<path d="M 745,90 L 797,90" class="edge-path" stroke="var(--sm-green-stroke)" marker-end="url(#crypto-arrow-green)"/>
<g>
<rect class="badge-bg" x="735" y="58" width="72" height="18" rx="9"/>
<text class="edge-label badge-txt" x="771" y="67" dominant-baseline="central" text-anchor="middle">Digest H_k</text>
</g>

<!-- Physical Frame Nodes -->
<g id="frame-0" transform="translate(45, 62)">
<rect width="130" height="56" rx="8" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="2" filter="url(#crypto-shadow)"/>
<rect width="5" height="56" rx="2.5" fill="var(--sm-slate-stroke)"/>
<text class="node-title" x="16" y="22" fill="var(--sm-slate-text)" dominant-baseline="central">Frame 0</text>
<text class="node-sub" x="10" y="40" fill="var(--sm-slate-sub)">BLAKE3(F₀)</text>
</g>

<g id="frame-1" transform="translate(235, 62)">
<rect width="130" height="56" rx="8" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="2" filter="url(#crypto-shadow)"/>
<rect width="5" height="56" rx="2.5" fill="var(--sm-slate-stroke)"/>
<text class="node-title" x="16" y="22" fill="var(--sm-slate-text)" dominant-baseline="central">Frame 1</text>
<text class="node-sub" x="10" y="40" fill="var(--sm-slate-sub)">BLAKE3(F₀||F₁)</text>
</g>

<g id="frame-2" transform="translate(425, 62)">
<rect width="130" height="56" rx="8" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="2" filter="url(#crypto-shadow)"/>
<rect width="5" height="56" rx="2.5" fill="var(--sm-slate-stroke)"/>
<text class="node-title" x="16" y="22" fill="var(--sm-slate-text)" dominant-baseline="central">Frame 2</text>
<text class="node-sub" x="10" y="40" fill="var(--sm-slate-sub)">BLAKE3(F₀||…||F₂)</text>
</g>

<g id="frame-3" transform="translate(615, 62)">
<rect width="130" height="56" rx="8" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="2" filter="url(#crypto-shadow)"/>
<rect width="5" height="56" rx="2.5" fill="var(--sm-slate-stroke)"/>
<text class="node-title" x="16" y="22" fill="var(--sm-slate-text)" dominant-baseline="central">Frame 3</text>
<text class="node-sub" x="10" y="40" fill="var(--sm-slate-sub)">BLAKE3(F₀||…||F₃)</text>
</g>

<g id="frame-proof" transform="translate(805, 62)">
<rect width="175" height="56" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2.2" filter="url(#crypto-shadow)"/>
<rect width="5" height="56" rx="2.5" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="16" y="22" fill="var(--sm-green-text)" dominant-baseline="central">Log Commitment</text>
<text class="node-sub" x="16" y="40" fill="var(--sm-green-sub)">Trusted Anchor Comparison</text>
</g>

<!-- Bottom Section Left: Logical Precursor Chains (Invariant C5.40) -->
<rect x="20" y="175" width="630" height="261" rx="10" fill="none" stroke="var(--sm-slate-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="30" y="164" width="350" height="22" rx="11" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="205" y="175" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle">Logical Precursor Chains (Invariant <a href="https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/docs/spec/pardosa-1.0.md#c540--invariant">C5.40</a>)</text>

<!-- Fiber Alpha Sub-box -->
<rect x="40" y="225" width="280" height="187" rx="8" fill="none" stroke="var(--sm-blue-stroke)" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.7"/>
<rect x="55" y="216" width="105" height="18" rx="9" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1"/>
<text class="tier-title" x="107" y="225" fill="var(--sm-blue-text)" dominant-baseline="central" text-anchor="middle">Fiber Alpha</text>

<!-- Link from A1 up to A0 -->
<path d="M 180,340 L 180,305" class="edge-dashed" stroke="var(--sm-blue-stroke)" marker-end="url(#crypto-arrow-blue)"/>
<g>
<rect class="badge-bg" x="123" y="310" width="114" height="18" rx="9"/>
<text class="edge-label badge-txt" x="180" y="319" dominant-baseline="central" text-anchor="middle">precursor_hash</text>
</g>

<g id="fiber-a-root" transform="translate(60, 250)">
<rect width="240" height="48" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#crypto-shadow)"/>
<rect width="4" height="48" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="16" y="19" fill="var(--sm-blue-text)" dominant-baseline="central">E0 (Root)</text>
<text class="node-sub" x="16" y="34" fill="var(--sm-blue-sub)">precursor_hash = 0x00...00</text>
</g>

<g id="fiber-a-update" transform="translate(60, 340)">
<rect width="240" height="48" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#crypto-shadow)"/>
<rect width="4" height="48" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="16" y="19" fill="var(--sm-blue-text)" dominant-baseline="central">E2 (Update)</text>
<text class="node-sub" x="16" y="34" fill="var(--sm-blue-sub)">BLAKE3(canonical envelope E0)</text>
</g>

<!-- Fiber Beta Sub-box -->
<rect x="350" y="225" width="280" height="187" rx="8" fill="none" stroke="var(--sm-green-stroke)" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.7"/>
<rect x="365" y="216" width="100" height="18" rx="9" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1"/>
<text class="tier-title" x="415" y="225" fill="var(--sm-green-text)" dominant-baseline="central" text-anchor="middle">Fiber Beta</text>

<!-- Link from B1 up to B0 -->
<path d="M 490,340 L 490,305" class="edge-dashed" stroke="var(--sm-green-stroke)" marker-end="url(#crypto-arrow-green)"/>
<g>
<rect class="badge-bg" x="433" y="310" width="114" height="18" rx="9"/>
<text class="edge-label badge-txt" x="490" y="319" dominant-baseline="central" text-anchor="middle">precursor_hash</text>
</g>

<g id="fiber-b-root" transform="translate(370, 250)">
<rect width="240" height="48" rx="7" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.8" filter="url(#crypto-shadow)"/>
<rect width="4" height="48" rx="2" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="16" y="19" fill="var(--sm-green-text)" dominant-baseline="central">E1 (Root)</text>
<text class="node-sub" x="16" y="34" fill="var(--sm-green-sub)">precursor_hash = 0x00...00</text>
</g>

<g id="fiber-b-update" transform="translate(370, 340)">
<rect width="240" height="48" rx="7" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.8" filter="url(#crypto-shadow)"/>
<rect width="4" height="48" rx="2" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="16" y="19" fill="var(--sm-green-text)" dominant-baseline="central">E3 (Update)</text>
<text class="node-sub" x="16" y="34" fill="var(--sm-green-sub)">BLAKE3(canonical envelope E1)</text>
</g>

<!-- Bottom Section Right: Orthogonality Annotation -->
<rect x="670" y="175" width="330" height="261" rx="10" fill="none" stroke="var(--sm-purple-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="685" y="164" width="220" height="22" rx="11" fill="var(--sm-purple-bg)" stroke="var(--sm-purple-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="795" y="175" fill="var(--sm-purple-text)" dominant-baseline="central" text-anchor="middle">Orthogonality Guarantee</text>

<g transform="translate(695, 205)">
<rect width="280" height="165" rx="8" fill="var(--sm-purple-bg)" stroke="var(--sm-purple-stroke)" stroke-width="1.5" filter="url(#crypto-shadow)"/>
<rect width="5" height="165" rx="2.5" fill="var(--sm-purple-stroke)"/>
<text class="node-title" x="16" y="24" fill="var(--sm-purple-text)" dominant-baseline="central">Physical ⊥ Logical</text>
<text class="callout-body" x="16" y="52">Physical H_k commits to frame order;</text>
<text class="callout-body" x="16" y="70">CRC32C checks enclosed envelope bytes.</text>
<text class="callout-body" x="16" y="96">Predecessor hashes link envelopes</text>
<text class="callout-body" x="16" y="114">within one fiber and generation.</text>
<text class="callout-body" x="16" y="140">Migration remints IDs and rechains</text>
<text class="callout-body" x="16" y="158">retained events in the new generation.</text>
</g>

</svg>
</div>

**Two scopes of integrity:** one continuous [BLAKE3 hasher](https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/crates/pardosa/src/file.rs#L233-L272) yields `H_k = BLAKE3(F_0 || … || F_k)` over recorded frame bytes. Fiber-local precursor hashes commit to canonical predecessor envelopes within a generation: the [commitment function](https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/crates/pardosa/src/encoding.rs#L998-L1010) hashes the fixed 81-byte header followed directly by payload bytes, excluding the wire payload-length field and frame length/checksum. Each physical node displays the prefix digest after that frame; each logical arrow carries the predecessor-envelope commitment. The 1.0 migration design remints and rechains retained events and computes fresh commitments. An independently trusted anchor enables comparison with an earlier observed prefix; the unkeyed hashes establish recorded-link integrity rather than authorship or cross-generation provenance.

---

## The 5-State Lifecycle State Machine

Pardosa implements a five-state fiber admission model. These are storage states; an application assigns domain meanings such as deletion to its own facts:

1. **`Undefined`**: No fiber is defined in the current storage state.
2. **`Defined`**: The fiber is active, exists, and accepts updates.
3. **`Detached`**: The head carries the detached marker; history remains available and rescue returns the fiber to `Defined`.
4. **`Purged`**: Fiber events are excluded from the migration target; source disposal and separate audit retention remain application-owned.
5. **`Locked`**: A migration-local lock/prune state with policy-controlled rescue. It is excluded from reopened fiber states, not a permanent domain-key ban.

### The 10 Legal Transitions

Pardosa encodes exactly **10 legal state transitions**. General transition methods return `Result`; an action attempting an unlisted transition returns `Err(IllegalStateTransition)` at runtime. A narrower type-level constraint applies to reopened fibers: `ReopenedFiberState` has no `Locked` variant, and validation rejects a raw `Locked` state on reopen:

The ten arrows match the [implemented transition function](https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/crates/pardosa/src/store.rs#L183-L240). Migration retention below follows the specified target policies, separately from the live manager's availability.

<div class="pardosa-lifecycle-diagram" style="margin: 2rem 0; padding: 1.5rem 1rem; border-radius: 0.75rem; border: 1px solid var(--gray-200, #e2e8f0); background: var(--body-background, #ffffff); overflow-x: auto;">
<svg id="state-diagram" role="img" aria-labelledby="state-title state-desc" viewBox="0 0 1060 510" width="100%" height="auto" style="display: block; min-width: 780px; max-width: 1060px; margin: 0 auto; overflow: visible;">
<title id="state-title">Five storage states and ten legal transitions</title>
<desc id="state-desc">Undefined, Defined, Detached, Locked and Purged are storage states. Rescue returns Detached or Locked to Defined; Purged excludes events from the migration target, not from independent copies.</desc>
<defs>
<marker id="arrow-slate" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-slate-fill" />
</marker>
<marker id="arrow-blue" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-blue-fill" />
</marker>
<marker id="arrow-amber" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-amber-fill" />
</marker>
<marker id="arrow-purple" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-purple-fill" />
</marker>
<marker id="arrow-rose" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
<path d="M 0 1.5 L 8 5 L 0 8.5 z" class="arrow-rose-fill" />
</marker>
<filter id="shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
<feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.08"/>
</filter>
</defs>
<style>
:root {
--sm-edge-halo: var(--body-background, #ffffff);
--sm-badge-bg: var(--gray-100, #f8fafc);
--sm-badge-border: var(--gray-200, #cbd5e1);
--sm-badge-text: var(--body-font-color, #1e293b);
--sm-slate-bg: #f8fafc;
--sm-slate-stroke: #475569;
--sm-slate-text: #475569;
--sm-slate-sub: #64748b;
--sm-blue-bg: #eff6ff;
--sm-blue-stroke: #2563eb;
--sm-blue-text: #1d4ed8;
--sm-blue-sub: #2563eb;
--sm-amber-bg: #fffbeb;
--sm-amber-stroke: #d97706;
--sm-amber-text: #b45309;
--sm-amber-sub: #d97706;
--sm-purple-bg: #f5f3ff;
--sm-purple-stroke: #7c3aed;
--sm-purple-text: #6d28d9;
--sm-purple-sub: #7c3aed;
--sm-rose-bg: #fff1f2;
--sm-rose-stroke: #e11d48;
--sm-rose-text: #be123c;
--sm-rose-sub: #e11d48;
}
@media (prefers-color-scheme: dark) {
:root:not([data-theme="light"]) {
--sm-edge-halo: var(--body-background, #2e3440);
--sm-badge-bg: var(--gray-100, #3b4252);
--sm-badge-border: var(--gray-200, #434c5e);
--sm-badge-text: var(--body-font-color, #f1f5f9);
--sm-slate-bg: #1e293b;
--sm-slate-stroke: #64748b;
--sm-slate-text: #cbd5e1;
--sm-slate-sub: #94a3b8;
--sm-blue-bg: #172554;
--sm-blue-stroke: #3b82f6;
--sm-blue-text: #93c5fd;
--sm-blue-sub: #60a5fa;
--sm-amber-bg: #451a03;
--sm-amber-stroke: #f59e0b;
--sm-amber-text: #fde68a;
--sm-amber-sub: #fbbf24;
--sm-purple-bg: #2e1065;
--sm-purple-stroke: #a855f7;
--sm-purple-text: #d8b4fe;
--sm-purple-sub: #c084fc;
--sm-rose-bg: #4c0519;
--sm-rose-stroke: #f43f5e;
--sm-rose-text: #fecdd3;
--sm-rose-sub: #fb7185;
}
}
:root[data-theme="dark"] {
--sm-edge-halo: var(--body-background, #2e3440);
--sm-badge-bg: var(--gray-100, #3b4252);
--sm-badge-border: var(--gray-200, #434c5e);
--sm-badge-text: var(--body-font-color, #f1f5f9);
--sm-slate-bg: #1e293b;
--sm-slate-stroke: #64748b;
--sm-slate-text: #cbd5e1;
--sm-slate-sub: #94a3b8;
--sm-blue-bg: #172554;
--sm-blue-stroke: #3b82f6;
--sm-blue-text: #93c5fd;
--sm-blue-sub: #60a5fa;
--sm-amber-bg: #451a03;
--sm-amber-stroke: #f59e0b;
--sm-amber-text: #fde68a;
--sm-amber-sub: #fbbf24;
--sm-purple-bg: #2e1065;
--sm-purple-stroke: #a855f7;
--sm-purple-text: #d8b4fe;
--sm-purple-sub: #c084fc;
--sm-rose-bg: #4c0519;
--sm-rose-stroke: #f43f5e;
--sm-rose-text: #fecdd3;
--sm-rose-sub: #fb7185;
}
.arrow-slate-fill { fill: var(--sm-slate-stroke); }
.arrow-blue-fill { fill: var(--sm-blue-stroke); }
.arrow-amber-fill { fill: var(--sm-amber-stroke); }
.arrow-purple-fill { fill: var(--sm-purple-stroke); }
.arrow-rose-fill { fill: var(--sm-rose-stroke); }
.state-title { font-size: 15px; font-weight: 700; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.state-sub { font-size: 11px; font-weight: 500; opacity: 0.9; font-family: system-ui, -apple-system, sans-serif; }
.edge-label { font-size: 11.5px; font-weight: 600; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
.edge-path { fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.edge-halo { fill: none; stroke: var(--sm-edge-halo); stroke-width: 8; stroke-linecap: round; stroke-linejoin: round; }
.badge-bg { fill: var(--sm-badge-bg); stroke: var(--sm-badge-border); stroke-width: 1.2; }
.badge-txt { fill: var(--sm-badge-text); }
</style>
<path d="M 360,85 L 360,157" class="edge-path" stroke="var(--sm-blue-stroke)" marker-end="url(#arrow-blue)"/>
<path d="M 280,172 C 190,130 90,130 90,187 C 90,244 190,244 280,202" class="edge-path" stroke="var(--sm-blue-stroke)" marker-end="url(#arrow-blue)"/>
<path d="M 440,173 C 485,153 555,153 597,173" class="edge-path" stroke="var(--sm-amber-stroke)" marker-end="url(#arrow-amber)"/>
<path d="M 600,201 C 555,221 485,221 443,201" class="edge-path" stroke="var(--sm-blue-stroke)" marker-end="url(#arrow-blue)"/>
<path d="M 760,172 C 850,130 970,130 970,187 C 970,244 850,244 760,202" class="edge-path" stroke="var(--sm-amber-stroke)" marker-end="url(#arrow-amber)"/>
<path d="M 705,214 L 705,397" class="edge-path" stroke="var(--sm-purple-stroke)" marker-end="url(#arrow-purple)"/>
<path d="M 620,214 C 595,270 455,340 423,397" class="edge-path" stroke="var(--sm-rose-stroke)" marker-end="url(#arrow-rose)"/>
<path d="M 620,400 C 595,344 455,274 423,217" class="edge-halo"/>
<path d="M 620,400 C 595,344 455,274 423,217" class="edge-path" stroke="var(--sm-blue-stroke)" marker-end="url(#arrow-blue)"/>
<path d="M 600,427 L 443,427" class="edge-path" stroke="var(--sm-rose-stroke)" marker-end="url(#arrow-rose)"/>
<path d="M 335,400 L 335,217" class="edge-path" stroke="var(--sm-blue-stroke)" marker-end="url(#arrow-blue)"/>
<g id="edge-1">
<rect class="badge-bg" x="317" y="109" width="86" height="24" rx="12"/>
<text class="edge-label badge-txt" x="360" y="121" dominant-baseline="central" text-anchor="middle">1. Create</text>
</g>
<g id="label-update">
<rect id="rect-update" class="badge-bg" x="46" y="175" width="88" height="24" rx="12"/>
<text id="text-update" class="edge-label badge-txt" x="90" y="187" dominant-baseline="central" text-anchor="middle">2. Update</text>
</g>
<g id="edge-3">
<rect class="badge-bg" x="477" y="137" width="86" height="24" rx="12"/>
<text class="edge-label badge-txt" x="520" y="149" dominant-baseline="central" text-anchor="middle">3. Detach</text>
</g>
<g id="edge-4">
<rect class="badge-bg" x="477" y="213" width="86" height="24" rx="12"/>
<text class="edge-label badge-txt" x="520" y="225" dominant-baseline="central" text-anchor="middle">4. Rescue</text>
</g>
<g id="label-migrate-keep">
<rect id="rect-migrate-keep" class="badge-bg" x="897" y="175" width="146" height="24" rx="12"/>
<text id="text-migrate-keep" class="edge-label badge-txt" x="970" y="187" dominant-baseline="central" text-anchor="middle">5. Migrate(Keep)</text>
</g>
<g id="edge-6">
<rect class="badge-bg" x="612" y="294" width="186" height="24" rx="12"/>
<text class="edge-label badge-txt" x="705" y="306" dominant-baseline="central" text-anchor="middle">6. Migrate(LockAndPrune)</text>
</g>
<g id="edge-7">
<rect class="badge-bg" x="506" y="243" width="138" height="24" rx="12"/>
<text class="edge-label badge-txt" x="575" y="255" dominant-baseline="central" text-anchor="middle">7. Migrate(Purge)</text>
</g>
<g id="edge-8">
<rect class="badge-bg" x="532" y="343" width="86" height="24" rx="12"/>
<text class="edge-label badge-txt" x="575" y="355" dominant-baseline="central" text-anchor="middle">8. Rescue</text>
</g>
<g id="edge-9">
<rect class="badge-bg" x="451" y="415" width="138" height="24" rx="12"/>
<text class="edge-label badge-txt" x="520" y="427" dominant-baseline="central" text-anchor="middle">9. Migrate(Purge)</text>
</g>
<g id="edge-10">
<rect class="badge-bg" x="292" y="294" width="86" height="24" rx="12"/>
<text class="edge-label badge-txt" x="335" y="306" dominant-baseline="central" text-anchor="middle">10. Create</text>
</g>
<g id="state-undefined" transform="translate(280, 35)">
<rect id="rect-undefined" width="160" height="50" rx="8" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="2" filter="url(#shadow)"/>
<rect width="6" height="50" rx="3" fill="var(--sm-slate-stroke)"/>
<text id="text-undefined" class="state-title" x="20" y="25" fill="var(--sm-slate-text)" dominant-baseline="central">Undefined</text>
<text class="state-sub" x="20" y="40" fill="var(--sm-slate-sub)">Initial State</text>
</g>
<g id="state-defined" transform="translate(280, 160)">
<rect id="rect-defined" width="160" height="54" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2.5" filter="url(#shadow)"/>
<rect width="6" height="54" rx="3" fill="var(--sm-blue-stroke)"/>
<text id="text-defined" class="state-title" x="20" y="27" fill="var(--sm-blue-text)" dominant-baseline="central">Defined</text>
<text class="state-sub" x="20" y="43" fill="var(--sm-blue-sub)">Accepts Updates</text>
</g>
<g id="state-detached" transform="translate(600, 160)">
<rect id="rect-detached" width="160" height="54" rx="8" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="2.5" filter="url(#shadow)"/>
<rect width="6" height="54" rx="3" fill="var(--sm-amber-stroke)"/>
<text id="text-detached" class="state-title" x="20" y="27" fill="var(--sm-amber-text)" dominant-baseline="central">Detached</text>
<text class="state-sub" x="20" y="43" fill="var(--sm-amber-sub)">Detached Head</text>
</g>
<g id="state-locked" transform="translate(600, 400)">
<rect id="rect-locked" width="160" height="54" rx="8" fill="var(--sm-purple-bg)" stroke="var(--sm-purple-stroke)" stroke-width="2.5" filter="url(#shadow)"/>
<rect width="6" height="54" rx="3" fill="var(--sm-purple-stroke)"/>
<text id="text-locked" class="state-title" x="20" y="27" fill="var(--sm-purple-text)" dominant-baseline="central">Locked</text>
<text class="state-sub" x="20" y="43" fill="var(--sm-purple-sub)">Migration-Local</text>
</g>
<g id="state-purged" transform="translate(280, 400)">
<rect id="rect-purged" width="160" height="54" rx="8" fill="var(--sm-rose-bg)" stroke="var(--sm-rose-stroke)" stroke-width="2.5" filter="url(#shadow)"/>
<rect width="6" height="54" rx="3" fill="var(--sm-rose-stroke)"/>
<text id="text-purged" class="state-title" x="20" y="27" fill="var(--sm-rose-text)" dominant-baseline="central">Purged</text>
<text class="state-sub" x="20" y="43" fill="var(--sm-rose-sub)">Excluded from Target</text>
</g>
</svg>
</div>

| # | Action | Operational Semantics |
|---|---|---|
| 1 | `Create` | `Undefined` → `Defined`. |
| 2 | `Update` | Appending a new state-modifying event to an active fiber. |
| 3 | `Detach` | `Defined` → `Detached`; marks the fiber head detached. |
| 4 | `Rescue` | `Detached` → `Defined`. |
| 5 | `Migrate(Keep)` | `Detached` → `Detached`; carries retained history into the target. |
| 6 | `Migrate(LockAndPrune)` | `Detached` → `Locked`; named rescue policy controls target retention. |
| 7 | `Migrate(Purge)` | `Detached` → `Purged`; excludes fiber events from the target. |
| 8 | `Rescue` | `Locked` → `Defined`; returns the fiber to the active storage state. |
| 9 | `Migrate(Purge)` | `Locked` → `Purged`; excludes retained fiber events from the target. |
| 10 | `Create` | `Purged` → `Defined`; this storage transition does not select domain-key reuse policy. |

---

## Consumer Idempotency & Deterministic Projections

In event-driven architectures, downstream systems build read models, search indexes, in-memory view models, and pre-rendered caches by projecting the event stream. Pardosa supplies ordered events and event identity; consumers define payloads that carry the facts needed by their views, while adapters define deterministic projections and coordinate sink delivery, identity retention and recovery. Payload completeness for a particular view is consumer-defined, not guaranteed by an envelope or schema descriptor. Rebuilding a view and suppressing a retry are separate mechanisms:

<div class="consumer-proj-container" id="consumer-reconstruction">
  <section class="cp-layer" aria-labelledby="consumer-facts-title">
    <h3 id="consumer-facts-title">Complete facts enable independent consumers</h3>
    <p>Illustrative issue-status facts, in order within one dragline (<a href="https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/docs/spec/pardosa-1.0.md#c38--invariant">C3.8</a>). Each carries the data needed for this view—not just an ID that requires a producer lookup.</p>
    <div class="cp-facts">
      <div class="cp-fact"><strong>E₁ · first fact</strong><br><code>issue: A, status: open</code></div>
      <div class="cp-fact"><strong>E₂ · next fact</strong><br><code>issue: A, status: closed</code></div>
    </div>
    <p class="cp-result">Ordered facts → independent consumers → consumer-defined views</p>
    <p><strong>What changes:</strong> a read-model adapter or search-index adapter can use these facts at its own pace, without a synchronous callback to the producer. This is event-carried state transfer, not a prescription for one shared view.</p>
  </section>
  <section class="cp-layer" aria-labelledby="consumer-rules-title">
    <h3 id="consumer-rules-title">The adapter defines how facts are processed</h3>
    <p>Pardosa provides order, dragline-local cursors (<a href="https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/docs/spec/pardosa-1.0.md#c522--surface">C5.22</a>) and event identity (<a href="https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/docs/spec/pardosa-1.0.md#c419--surface">C4.19</a>). The adapter owns the fold, sink writes, retained identities and recovery coordination.</p>
    <div class="cp-paths">
      <section class="cp-path" aria-labelledby="consumer-replay-title">
        <h4 id="consumer-replay-title">Path A · Fresh reconstruction</h4>
        <p><strong>Rule:</strong> same initial state, same ordered facts, same deterministic fold. Set A’s status from each fact; do not use arrival time or producer queries.</p>
        <ol>
          <li>Start each independent run at <code>S₀ = {}</code>.</li>
          <li>Fold E₁ → <code>{A: open}</code>.</li>
          <li>Fold E₂ → <code>{A: closed}</code>.</li>
        </ol>
        <p class="cp-result">First build = fresh replay → <code>{A: closed}</code></p>
        <p>Rebuild from S₀, not by applying the log again to the finished model. Equal results do not prove duplicate sink invocations were suppressed.</p>
      </section>
      <section class="cp-path" aria-labelledby="consumer-retry-title">
        <h4 id="consumer-retry-title">Path B · Bounded retry suppression</h4>
        <p><strong>Rule:</strong> check the event identity retained by the adapter before invoking its sink. Both deliveries here carry E₂’s same identity.</p>
        <ol>
          <li><strong>First E₂:</strong> handle the fact, upsert <code>A: closed</code>, retain E₂’s identity.</li>
          <li><strong>Repeated E₂, identity still retained:</strong> recognize and drop the delivery → <strong>no sink invocation</strong>.</li>
        </ol>
        <p class="cp-result">Retained identity → retry gate → delivery dropped</p>
        <p>Outside the adapter’s replay window, no suppression guarantee is made. Coordinating sink writes, identity retention and checkpoints across a crash is adapter-owned; engine metadata alone does not make recovery exactly-once.</p>
      </section>
    </div>
    <p><strong>Keep the paths separate:</strong> fresh reconstruction processes the ordered facts into a new view; the retry gate skips an already-handled delivery only while its identity remains retained.</p>
  </section>
</div>

### Resume and Adapter Boundaries

The engine replays one recorded order per artefact ([C3.8](https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/docs/spec/pardosa-1.0.md#c38--invariant)); it does not prescribe how concurrent fibers interleave. Resume cursors are dragline-local, regenerated during migrations, and invalid across migrations ([C5.22](https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/docs/spec/pardosa-1.0.md#c522--surface)). Persisting a cursor alone does not close the crash gap between an external action and recording its completion.

Read models, search indexes, analytical stores and **static cache stores** can consume facts at their own pace. A **consumer-side adapter (for example, a cache renderer)** owns its view transformation, sink writes, retained event identities and checkpoint/recovery coordination. The worked paths above show why deterministic reconstruction is not duplicate suppression, and why neither engine ordering nor integrity metadata supplies exactly-once sink recovery.

---

## Line Migration & Audit Boundaries

The **1.0 line migration design** removes selected histories from a new target generation. The implemented state-transition model above includes migration actions; the [live migration manager at the inspected revision](https://github.com/acje/pardosa/blob/bed69b854e3cf84c8e36c354feca3f36db2112b4/crates/pardosa/src/migration.rs#L284-L402) explicitly refuses live migration operations. The specified target construction is:

1. **Separation of Line and Audit**: A line contains the active operational stream. An optional audit log captures raw events separately under strict access controls.
2. **Target Construction**: A migration selects `Keep`, `Purge` or `LockAndPrune` for each fiber:
   - The target is a new line generation (`<new_stem>.pgno` and `<new_stem>.meta`).
   - Events belonging to purged fibers are physically excluded from the new container file.
   - Retained events receive fresh event/fiber IDs and are densely rechained from genesis; precursor commitments and local cursors are regenerated.
   - A fresh physical rolling BLAKE3 commitment is computed sequentially over the new container.
   - The old line version must also be removed; exclusion from the new file alone does not erase it. Separate audit copies, backups and downstream views require their own retention handling.
