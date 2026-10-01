---
title: "Pardosa: Event-Driven Storage with Fiber Semantics"
description: "Append-only line storage enforcing event-driven correctness, auditability, and verifiable deletion"
weight: 20
homeFeatured: true
---

## Pardosa: Event-Driven Storage with Fiber Semantics

Modern distributed applications increasingly adopt Event-Driven Architecture (EDA) to decouple services and scale ingestion. However, when complex enterprise systems migrate to event sourcing, they frequently run into severe correctness hazards: split-brain concurrent mutations, silent aggregate state corruption, and the architectural inability to satisfy legal deletion mandates (such as GDPR "right to be forgotten") without corrupting immutable event histories.

`Pardosa` is an append-only event-driven storage engine implemented in Rust, built specifically upon the principles of **Fiber Semantics**. It is designed for enterprise domains where **correctness, strict auditability, and deterministic deletion policies matter far more than raw ingestion volume**. Pardosa guarantees per-aggregate linearizability and single-writer fencing, backed by a formal 5-state lifecycle state machine.

<div class="pardosa-architecture-diagram" style="margin: 2rem 0; padding: 1.5rem 1rem; border-radius: 0.75rem; border: 1px solid var(--gray-200, #e2e8f0); background: var(--body-background, #ffffff); overflow-x: auto;">
<svg id="architecture-diagram" viewBox="0 0 1020 370" width="100%" height="auto" style="display: block; min-width: 780px; max-width: 1020px; margin: 0 auto; overflow: visible;">
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
<text class="tier-title" x="130" y="25" fill="var(--sm-amber-text)" dominant-baseline="central" text-anchor="middle">Single-Writer Ingestion</text>

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
<text class="node-title" x="20" y="27" fill="var(--sm-amber-text)" dominant-baseline="central">Domain Command</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-amber-sub)">Precursor Hash &amp; Payload</text>
</g>

<g id="node-cas" transform="translate(45, 150)">
<rect width="250" height="58" rx="8" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-amber-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-amber-text)" dominant-baseline="central">CAS Single-Writer Fencing</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-amber-sub)">Per-Fiber Head Verification</text>
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
<text class="node-sub" x="20" y="44" fill="var(--sm-blue-sub)">Linearized Domain Aggregate</text>
</g>

<g id="node-blake" transform="translate(385, 150)">
<rect width="250" height="58" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-blue-text)" dominant-baseline="central">BLAKE3 Framing &amp; Checksum</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-blue-sub)">Envelope &amp; Rolling Hash Fold</text>
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
<text class="node-sub" x="20" y="44" fill="var(--sm-cyan-sub)">Real-Time Read Models &amp; CQRS</text>
</g>

<g id="node-ecst" transform="translate(725, 150)">
<rect width="250" height="58" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-green-text)" dominant-baseline="central">Event Carried State Transfer</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-green-sub)">Decoupled Broadcast Channel</text>
</g>

<g id="node-audit" transform="translate(725, 240)">
<rect width="250" height="58" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2" filter="url(#arch-shadow)"/>
<rect width="6" height="58" rx="3" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="20" y="27" fill="var(--sm-green-text)" dominant-baseline="central">Immutable Audit Trails</text>
<text class="node-sub" x="20" y="44" fill="var(--sm-green-sub)">Verifiable Cryptographic Proofs</text>
</g>

</svg>
</div>

---

## Domain State Governance & Verifiable Deletion

High-integrity enterprise applications require event storage that enforces two foundational invariants:

1. **Domain State Governance**: In enterprise systems, business entities transition through structured lifecycles governed by formal domain rules. Without aggregate-level fencing and state-transition admission control, concurrent mutations risk overwriting entity state and committing illegal transitions. Pardosa enforces first-class aggregate fencing and deterministic lifecycle admission directly at the storage boundary, guaranteeing that every committed event represents a validated, sequential state transition for that specific entity.
2. **The Immutability vs. Deletion Paradox**: Event-sourced systems require immutable historical streams for auditability, replayability, and provenance. However, regulated enterprises operate under strict legal mandates (such as GDPR Article 17, healthcare data privacy standards, and statutory retention expirations) requiring verifiable, physical data deletion. Traditional workarounds—such as breaking audit trails via out-of-band record patching, or encrypting payloads and discarding keys (crypto-shredding)—leave metadata exposed, historical commitments unverifiable, and physical storage un-reclaimed.

Pardosa resolves this tension by separating physical append-only container files (**draglines**) from aggregate lifecycle governance (**fibers**) and introducing cryptographically auditable, verifiable **line migrations**.

---

## Fiber Semantics: Entities as Ordered Event Chains

In Fiber Semantics, the lifecycle history of each domain entity is modeled as an independent **fiber**:

- **Definition**: A fiber is a singly linked list of immutable events belonging to a unique, domain-scoped identifier (`fiber_id`).
- **Chain Topology**: Rather than storing events in a forward array that must be rewritten on mutation, each event in a fiber explicitly references its immediate predecessor through a `precursor` pointer (a 16-byte predecessor event ID and a 32-byte BLAKE3 precursor hash).
- **Head-Anchored Traversal**: The active state of a fiber is always anchored at its newest event (the head). Reading an entity's current state requires inspecting only the head; traversing backward reconstructs historical state transitions without requiring full-log scans.

---

## Draglines: Append-Only Interleaved Commit Streams

While domain entities exist logically as independent fibers, disk I/O and network replication achieve maximum efficiency through sequential streaming. Pardosa unifies these models through the **dragline**:

<div class="pardosa-dragline-diagram" style="margin: 2rem 0; padding: 1.5rem 1rem; border-radius: 0.75rem; border: 1px solid var(--gray-200, #e2e8f0); background: var(--body-background, #ffffff); overflow-x: auto;">
<svg id="dragline-diagram" viewBox="0 0 1020 450" width="100%" height="auto" style="display: block; min-width: 780px; max-width: 1020px; margin: 0 auto; overflow: visible;">
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
<rect x="20" y="25" width="980" height="130" rx="10" fill="none" stroke="var(--sm-slate-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="35" y="14" width="300" height="22" rx="11" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="185" y="25" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle">Physical Dragline (Append-Only Stream)</text>

<!-- Physical Sequential Append Links -->
<path d="M 170,95 L 198,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>
<path d="M 330,95 L 358,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>
<path d="M 490,95 L 518,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>
<path d="M 650,95 L 678,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>
<path d="M 810,95 L 838,95" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#drag-arrow-slate)"/>

<!-- Physical Frame Cards -->
<g id="phys-e1" transform="translate(45, 63)">
<rect width="125" height="64" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="16" y="24" fill="var(--sm-blue-text)" dominant-baseline="central">E1: Id=A</text>
<text class="node-sub" x="16" y="44" fill="var(--sm-blue-sub)">seq=0 (Create)</text>
</g>

<g id="phys-e2" transform="translate(205, 63)">
<rect width="125" height="64" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="16" y="24" fill="var(--sm-green-text)" dominant-baseline="central">E2: Id=B</text>
<text class="node-sub" x="16" y="44" fill="var(--sm-green-sub)">seq=0 (Create)</text>
</g>

<g id="phys-e3" transform="translate(365, 63)">
<rect width="125" height="64" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="16" y="24" fill="var(--sm-blue-text)" dominant-baseline="central">E3: Id=A</text>
<text class="node-sub" x="16" y="44" fill="var(--sm-blue-sub)">seq=1 (Update)</text>
</g>

<g id="phys-e4" transform="translate(525, 63)">
<rect width="125" height="64" rx="8" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-amber-stroke)"/>
<text class="node-title" x="16" y="24" fill="var(--sm-amber-text)" dominant-baseline="central">E4: Id=C</text>
<text class="node-sub" x="16" y="44" fill="var(--sm-amber-sub)">seq=0 (Create)</text>
</g>

<g id="phys-e5" transform="translate(685, 63)">
<rect width="125" height="64" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="16" y="24" fill="var(--sm-green-text)" dominant-baseline="central">E5: Id=B</text>
<text class="node-sub" x="16" y="44" fill="var(--sm-green-sub)">seq=1 (Update)</text>
</g>

<g id="phys-e6" transform="translate(845, 63)">
<rect width="125" height="64" rx="8" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="2" filter="url(#drag-shadow)"/>
<rect width="5" height="64" rx="2.5" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="16" y="24" fill="var(--sm-blue-text)" dominant-baseline="central">E6: Id=A</text>
<text class="node-sub" x="16" y="44" fill="var(--sm-blue-sub)">seq=2 (Detach)</text>
</g>

<!-- Bottom Section: Logical Singly-Linked Fiber Histories -->
<rect x="20" y="180" width="980" height="245" rx="10" fill="none" stroke="var(--sm-slate-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="35" y="169" width="340" height="22" rx="11" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="205" y="180" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle">Logical Singly-Linked Fiber Histories</text>

<!-- Fiber A Track -->
<rect x="35" y="210" width="85" height="22" rx="11" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="77" y="221" fill="var(--sm-blue-text)" dominant-baseline="central" text-anchor="middle">Fiber A</text>

<!-- Precursor Backward Dashed Arrows for Fiber A -->
<!-- E6 (840) to E3 (490) -->
<path d="M 840,223 C 740,195 590,195 498,223" class="edge-halo"/>
<path d="M 840,223 C 740,195 590,195 498,223" class="edge-dashed" stroke="var(--sm-blue-stroke)" marker-end="url(#drag-arrow-blue)"/>
<g>
<rect class="badge-bg" x="625" y="190" width="80" height="20" rx="10"/>
<text class="edge-label badge-txt" x="665" y="200" dominant-baseline="central" text-anchor="middle">precursor</text>
</g>

<!-- E3 (365) to E1 (170) -->
<path d="M 365,223 C 300,195 230,195 178,223" class="edge-halo"/>
<path d="M 365,223 C 300,195 230,195 178,223" class="edge-dashed" stroke="var(--sm-blue-stroke)" marker-end="url(#drag-arrow-blue)"/>
<g>
<rect class="badge-bg" x="235" y="190" width="80" height="20" rx="10"/>
<text class="edge-label badge-txt" x="275" y="200" dominant-baseline="central" text-anchor="middle">precursor</text>
</g>

<g id="logic-e1" transform="translate(45, 203)">
<rect width="125" height="50" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-blue-text)" dominant-baseline="central">E1: Create</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-blue-sub)">seq=0 (Root)</text>
</g>

<g id="logic-e3" transform="translate(365, 203)">
<rect width="125" height="50" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-blue-text)" dominant-baseline="central">E3: Update</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-blue-sub)">seq=1</text>
</g>

<g id="logic-e6" transform="translate(845, 203)">
<rect width="125" height="50" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-blue-text)" dominant-baseline="central">E6: Detach</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-blue-sub)">seq=2 (Head)</text>
</g>

<!-- Fiber B Track -->
<rect x="35" y="285" width="85" height="22" rx="11" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="77" y="296" fill="var(--sm-green-text)" dominant-baseline="central" text-anchor="middle">Fiber B</text>

<!-- Precursor Backward Dashed Arrow for Fiber B: E5 (685) to E2 (330) -->
<path d="M 685,298 C 580,270 430,270 338,298" class="edge-halo"/>
<path d="M 685,298 C 580,270 430,270 338,298" class="edge-dashed" stroke="var(--sm-green-stroke)" marker-end="url(#drag-arrow-green)"/>
<g>
<rect class="badge-bg" x="475" y="265" width="80" height="20" rx="10"/>
<text class="edge-label badge-txt" x="515" y="275" dominant-baseline="central" text-anchor="middle">precursor</text>
</g>

<g id="logic-e2" transform="translate(205, 278)">
<rect width="125" height="50" rx="7" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-green-text)" dominant-baseline="central">E2: Create</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-green-sub)">seq=0 (Root)</text>
</g>

<g id="logic-e5" transform="translate(685, 278)">
<rect width="125" height="50" rx="7" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-green-text)" dominant-baseline="central">E5: Update</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-green-sub)">seq=1 (Head)</text>
</g>

<!-- Fiber C Track -->
<rect x="35" y="360" width="85" height="22" rx="11" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="77" y="371" fill="var(--sm-amber-text)" dominant-baseline="central" text-anchor="middle">Fiber C</text>

<g id="logic-e4" transform="translate(525, 353)">
<rect width="125" height="50" rx="7" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="1.8" filter="url(#drag-shadow)"/>
<rect width="4" height="50" rx="2" fill="var(--sm-amber-stroke)"/>
<text class="node-title" x="14" y="20" fill="var(--sm-amber-text)" dominant-baseline="central">E4: Create</text>
<text class="node-sub" x="14" y="36" fill="var(--sm-amber-sub)">seq=0 (Root)</text>
</g>

<g>
<rect class="badge-bg" x="670" y="368" width="165" height="22" rx="11"/>
<text class="edge-label badge-txt" x="752" y="379" dominant-baseline="central" text-anchor="middle">Root Frame (precursor=0x00)</text>
</g>

<!-- Projection Drop Lines from Physical Stream down to Logical Chains -->
<path d="M 107,127 L 107,203" class="edge-dashed" stroke="var(--sm-blue-stroke)" opacity="0.35"/>
<path d="M 267,127 L 267,278" class="edge-dashed" stroke="var(--sm-green-stroke)" opacity="0.35"/>
<path d="M 427,127 L 427,203" class="edge-dashed" stroke="var(--sm-blue-stroke)" opacity="0.35"/>
<path d="M 587,127 L 587,353" class="edge-dashed" stroke="var(--sm-amber-stroke)" opacity="0.35"/>
<path d="M 747,127 L 747,278" class="edge-dashed" stroke="var(--sm-green-stroke)" opacity="0.35"/>
<path d="M 907,127 L 907,203" class="edge-dashed" stroke="var(--sm-blue-stroke)" opacity="0.35"/>

</svg>
</div>

- **Interleaving**: Events from thousands of concurrent fibers are committed sequentially onto a shared dragline.
- **Per-Aggregate Linearizability**: Sequential consistency is enforced strictly per fiber. Single-writer fencing using Compare-And-Swap (CAS) ensures that an append succeeds if and only if the event's declared `precursor` matches the active head of that fiber. If a concurrent writer attempts to append to the same fiber simultaneously, the CAS check fails immediately, preventing aggregate state corruption.
- **Atomic Durability**: Frames are appended with strict atomic durability (`write` $\rightarrow$ `fsync` $\rightarrow$ `atomic rename` $\rightarrow$ `parent dir fsync`), guaranteeing crash resilience against power loss or operating system faults.

---

## Physical Data Structure: On-Disk Dragline Layout

Pardosa separates line state into an artefact pair on disk:

1. **`<stem>.meta` (Descriptor File)**: Stores line metadata, schema commitments, domain namespace scope, and partition ownership.
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

    --dl-green-border: #059669;
    --dl-green-bg: rgba(5, 150, 105, 0.06);
    --dl-green-tag-bg: #047857;
    --dl-green-tag-text: #ffffff;

    --dl-emerald-border: #059669;
    --dl-emerald-bg: rgba(5, 150, 105, 0.12);
    --dl-emerald-tag-bg: #059669;
    --dl-emerald-tag-text: #ffffff;
    --dl-emerald-highlight-border: #047857;
    --dl-emerald-highlight-bg: rgba(5, 150, 105, 0.14);

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

    --dl-green-border: #10b981;
    --dl-green-bg: rgba(16, 185, 129, 0.12);
    --dl-green-tag-bg: #065f46;
    --dl-green-tag-text: #ecfdf5;

    --dl-emerald-border: #10b981;
    --dl-emerald-bg: rgba(16, 185, 129, 0.18);
    --dl-emerald-tag-bg: #059669;
    --dl-emerald-tag-text: #ffffff;
    --dl-emerald-highlight-border: #34d399;
    --dl-emerald-highlight-bg: rgba(16, 185, 129, 0.22);

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

      --dl-green-border: #10b981;
      --dl-green-bg: rgba(16, 185, 129, 0.12);
      --dl-green-tag-bg: #065f46;
      --dl-green-tag-text: #ecfdf5;

      --dl-emerald-border: #10b981;
      --dl-emerald-bg: rgba(16, 185, 129, 0.18);
      --dl-emerald-tag-bg: #059669;
      --dl-emerald-tag-text: #ffffff;
      --dl-emerald-highlight-border: #34d399;
      --dl-emerald-highlight-bg: rgba(16, 185, 129, 0.22);

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
  .dl-tag-green { background: var(--dl-green-tag-bg); color: var(--dl-green-tag-text); }
  .dl-tag-emerald { background: var(--dl-emerald-tag-bg); color: var(--dl-emerald-tag-text); }

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
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 0.625rem;
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
  .dl-field-green { border-left: 3px solid var(--dl-green-border); }

  .dl-field-emerald-highlight {
    border: 1.5px solid var(--dl-emerald-highlight-border);
    border-left: 4px solid var(--dl-emerald-highlight-border);
    background: var(--dl-emerald-highlight-bg);
  }

  .dl-field-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--dl-text-muted);
    margin-bottom: 0.25rem;
  }

  .dl-emerald-label {
    color: var(--dl-emerald-highlight-border);
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

  .dl-emerald-desc {
    color: var(--dl-text);
    font-weight: 500;
  }

  .dl-digest-badge {
    border-radius: 6px;
    padding: 0.625rem 0.875rem;
    margin-top: 0.875rem;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
  }

  .dl-digest-slate {
    border: 1px solid var(--dl-slate-border);
    background: var(--dl-slate-bg);
  }

  .dl-digest-emerald {
    border: 1.5px solid var(--dl-emerald-highlight-border);
    background: var(--dl-emerald-highlight-bg);
  }

  .dl-digest-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8125rem;
  }

  .dl-digest-title code {
    background: var(--dl-code-bg);
    color: var(--dl-code-text);
    padding: 0.15rem 0.4rem;
    border-radius: 3px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-weight: 600;
  }

  .dl-digest-desc {
    font-size: 0.75rem;
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

  .dl-connector-block {
    background: var(--dl-connector-bg);
    border: 1.5px dashed var(--dl-connector-border);
    border-radius: 8px;
    padding: 1rem;
    margin: 1.25rem 0;
  }

  .dl-connector-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--dl-connector-border);
  }

  .dl-connector-title {
    font-weight: 700;
    font-size: 0.8125rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--dl-text);
  }

  .dl-connector-subtitle {
    font-size: 0.75rem;
    color: var(--dl-text-muted);
  }

  .dl-connector-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 0.75rem;
  }

  .dl-conn-card {
    display: flex;
    align-items: flex-start;
    gap: 0.625rem;
    padding: 0.625rem;
    border-radius: 6px;
    background: var(--dl-bg);
    border: 1px solid rgba(100, 116, 139, 0.2);
  }

  .dl-conn-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    font-size: 0.72rem;
    font-weight: 700;
    color: #ffffff;
    flex-shrink: 0;
    margin-top: 1px;
  }

  .dl-conn-physical .dl-conn-num { background: #475569; }
  .dl-conn-logical .dl-conn-num { background: #059669; }
  .dl-conn-causal .dl-conn-num { background: #047857; }
  .dl-conn-rolling .dl-conn-num { background: #0f766e; }

  .dl-conn-content {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }

  .dl-conn-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--dl-text);
  }

  .dl-conn-detail {
    font-size: 0.75rem;
    color: var(--dl-text);
  }

  .dl-conn-detail code {
    background: var(--dl-code-bg);
    color: var(--dl-code-text);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-size: 0.75rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }

  .dl-conn-desc {
    font-size: 0.7rem;
    color: var(--dl-text-muted);
    line-height: 1.35;
  }

  @media (max-width: 640px) {
    .dl-grid-envelope {
      grid-template-columns: 1fr 1fr;
    }
    .dl-grid-2 {
      grid-template-columns: 1fr;
    }
    .dl-connector-grid {
      grid-template-columns: 1fr;
    }
  }

  .consumer-proj-container {
    --cp-bg: #ffffff;
    --cp-text: #0f172a;
    --cp-text-muted: #475569;
    --cp-code-bg: rgba(15, 23, 42, 0.06);
    --cp-code-text: #0f172a;

    --cp-slate-border: #64748b;
    --cp-slate-bg: rgba(100, 116, 139, 0.05);
    --cp-slate-tag-bg: #475569;
    --cp-slate-tag-text: #ffffff;

    --cp-blue-border: #2563eb;
    --cp-blue-bg: rgba(37, 99, 235, 0.04);
    --cp-blue-tag-bg: #1d4ed8;
    --cp-blue-tag-text: #ffffff;

    --cp-purple-border: #7c3aed;
    --cp-purple-bg: rgba(124, 58, 237, 0.04);
    --cp-purple-tag-bg: #6d28d9;
    --cp-purple-tag-text: #ffffff;

    --cp-green-border: #059669;
    --cp-green-bg: rgba(5, 150, 105, 0.06);
    --cp-green-tag-bg: #047857;
    --cp-green-tag-text: #ffffff;

    --cp-cyan-border: #0891b2;
    --cp-cyan-bg: rgba(8, 145, 178, 0.05);
    --cp-cyan-tag-bg: #0e7490;
    --cp-cyan-tag-text: #ffffff;

    --cp-amber-border: #d97706;
    --cp-amber-bg: rgba(217, 119, 6, 0.05);
    --cp-amber-tag-bg: #b45309;
    --cp-amber-tag-text: #ffffff;

    --cp-connector-bg: rgba(241, 245, 249, 0.95);
    --cp-connector-border: #cbd5e1;

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
    overflow-x: hidden;
  }

  :root[data-theme="dark"] .consumer-proj-container,
  :root[data-theme$="dark"] .consumer-proj-container {
    --cp-bg: #0f172a;
    --cp-text: #f1f5f9;
    --cp-text-muted: #94a3b8;
    --cp-code-bg: rgba(0, 0, 0, 0.4);
    --cp-code-text: #f8fafc;

    --cp-slate-border: #64748b;
    --cp-slate-bg: rgba(100, 116, 139, 0.15);
    --cp-slate-tag-bg: #334155;
    --cp-slate-tag-text: #f8fafc;

    --cp-blue-border: #3b82f6;
    --cp-blue-bg: rgba(59, 130, 246, 0.12);
    --cp-blue-tag-bg: #1d4ed8;
    --cp-blue-tag-text: #eff6ff;

    --cp-purple-border: #8b5cf6;
    --cp-purple-bg: rgba(139, 92, 246, 0.12);
    --cp-purple-tag-bg: #5b21b6;
    --cp-purple-tag-text: #f5f3ff;

    --cp-green-border: #10b981;
    --cp-green-bg: rgba(16, 185, 129, 0.12);
    --cp-green-tag-bg: #065f46;
    --cp-green-tag-text: #ecfdf5;

    --cp-cyan-border: #06b6d4;
    --cp-cyan-bg: rgba(6, 182, 212, 0.12);
    --cp-cyan-tag-bg: #0e7490;
    --cp-cyan-tag-text: #ecfeff;

    --cp-amber-border: #f59e0b;
    --cp-amber-bg: rgba(245, 158, 11, 0.12);
    --cp-amber-tag-bg: #92400e;
    --cp-amber-tag-text: #fef3c7;

    --cp-connector-bg: rgba(30, 41, 59, 0.9);
    --cp-connector-border: #475569;
  }

  @media (prefers-color-scheme: dark) {
    :root[data-theme="auto"] .consumer-proj-container,
    :root:not([data-theme="light"]):not([data-theme="dark"]) .consumer-proj-container {
      --cp-bg: #0f172a;
      --cp-text: #f1f5f9;
      --cp-text-muted: #94a3b8;
      --cp-code-bg: rgba(0, 0, 0, 0.4);
      --cp-code-text: #f8fafc;

      --cp-slate-border: #64748b;
      --cp-slate-bg: rgba(100, 116, 139, 0.15);
      --cp-slate-tag-bg: #334155;
      --cp-slate-tag-text: #f8fafc;

      --cp-blue-border: #3b82f6;
      --cp-blue-bg: rgba(59, 130, 246, 0.12);
      --cp-blue-tag-bg: #1d4ed8;
      --cp-blue-tag-text: #eff6ff;

      --cp-purple-border: #8b5cf6;
      --cp-purple-bg: rgba(139, 92, 246, 0.12);
      --cp-purple-tag-bg: #5b21b6;
      --cp-purple-tag-text: #f5f3ff;

      --cp-green-border: #10b981;
      --cp-green-bg: rgba(16, 185, 129, 0.12);
      --cp-green-tag-bg: #065f46;
      --cp-green-tag-text: #ecfdf5;

      --cp-cyan-border: #06b6d4;
      --cp-cyan-bg: rgba(6, 182, 212, 0.12);
      --cp-cyan-tag-bg: #0e7490;
      --cp-cyan-tag-text: #ecfeff;

      --cp-amber-border: #f59e0b;
      --cp-amber-bg: rgba(245, 158, 11, 0.12);
      --cp-amber-tag-bg: #92400e;
      --cp-amber-tag-text: #fef3c7;

      --cp-connector-bg: rgba(30, 41, 59, 0.9);
      --cp-connector-border: #475569;
    }
  }

  .consumer-proj-container * {
    box-sizing: border-box;
  }

  .cp-card {
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    background: var(--cp-bg);
    border: 1.5px solid var(--cp-slate-border);
    transition: border-color 0.2s ease;
    min-width: 0;
  }

  .cp-card-blue { border-color: var(--cp-blue-border); background: var(--cp-blue-bg); }
  .cp-card-green { border-color: var(--cp-green-border); background: var(--cp-green-bg); }
  .cp-card-purple { border-color: var(--cp-purple-border); background: var(--cp-purple-bg); }
  .cp-card-cyan { border-color: var(--cp-cyan-border); background: var(--cp-cyan-bg); }
  .cp-card-amber { border-color: var(--cp-amber-border); background: var(--cp-amber-bg); }

  .cp-card-title-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(100, 116, 139, 0.2);
  }

  .cp-title-group {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    min-width: 0;
  }

  .cp-title {
    font-weight: 600;
    font-size: 0.9375rem;
    color: var(--cp-text);
  }

  .cp-tag {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.025em;
    text-transform: uppercase;
    white-space: nowrap;
  }

  .cp-tag-slate { background: var(--cp-slate-tag-bg); color: var(--cp-slate-tag-text); }
  .cp-tag-blue { background: var(--cp-blue-tag-bg); color: var(--cp-blue-tag-text); }
  .cp-tag-green { background: var(--cp-green-tag-bg); color: var(--cp-green-tag-text); }
  .cp-tag-purple { background: var(--cp-purple-tag-bg); color: var(--cp-purple-tag-text); }
  .cp-tag-cyan { background: var(--cp-cyan-tag-bg); color: var(--cp-cyan-tag-text); }
  .cp-tag-amber { background: var(--cp-amber-tag-bg); color: var(--cp-amber-tag-text); }

  .cp-section-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--cp-text-muted);
    margin: 0.625rem 0 0.375rem 0;
  }

  .cp-grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 0.75rem;
  }

  .cp-grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 0.75rem;
  }

  .cp-stack-compact {
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
  }

  .cp-field {
    border-radius: 6px;
    padding: 0.625rem 0.75rem;
    border: 1px solid rgba(100, 116, 139, 0.25);
    background: var(--cp-bg);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0;
  }

  .cp-field-slate { border-left: 3.5px solid var(--cp-slate-border); }
  .cp-field-blue { border-left: 3.5px solid var(--cp-blue-border); }
  .cp-field-green { border-left: 3.5px solid var(--cp-green-border); }
  .cp-field-purple { border-left: 3.5px solid var(--cp-purple-border); }
  .cp-field-cyan { border-left: 3.5px solid var(--cp-cyan-border); }
  .cp-field-amber { border-left: 3.5px solid var(--cp-amber-border); }

  .cp-field-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--cp-text-muted);
    margin-bottom: 0.25rem;
  }

  .cp-field-val {
    font-size: 0.8125rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.375rem;
    color: var(--cp-text);
  }

  .cp-field-val code {
    background: var(--cp-code-bg);
    color: var(--cp-code-text);
    padding: 0.15rem 0.35rem;
    border-radius: 3px;
    font-size: 0.8125rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    word-break: break-all;
    overflow-wrap: break-word;
  }

  .cp-field-desc {
    font-size: 0.72rem;
    color: var(--cp-text-muted);
    line-height: 1.35;
  }

  .cp-connector-block {
    background: var(--cp-connector-bg);
    border: 1.5px dashed var(--cp-connector-border);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    min-width: 0;
  }

  .cp-connector-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--cp-connector-border);
  }

  .cp-connector-title {
    font-weight: 700;
    font-size: 0.8125rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--cp-text);
  }

  .cp-connector-subtitle {
    font-size: 0.75rem;
    color: var(--cp-text-muted);
  }

  .cp-connector-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 0.75rem;
  }

  .cp-conn-card {
    display: flex;
    align-items: flex-start;
    gap: 0.625rem;
    padding: 0.625rem;
    border-radius: 6px;
    background: var(--cp-bg);
    border: 1px solid rgba(100, 116, 139, 0.2);
    min-width: 0;
  }

  .cp-conn-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    font-size: 0.72rem;
    font-weight: 700;
    flex-shrink: 0;
  }

  .cp-num-blue { background: var(--cp-blue-tag-bg); color: #ffffff; }
  .cp-num-green { background: var(--cp-green-tag-bg); color: #ffffff; }
  .cp-num-purple { background: var(--cp-purple-tag-bg); color: #ffffff; }
  .cp-num-cyan { background: var(--cp-cyan-tag-bg); color: #ffffff; }

  .cp-conn-content {
    min-width: 0;
    flex: 1;
  }

  .cp-conn-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--cp-text);
    margin-bottom: 0.15rem;
  }

  .cp-conn-detail {
    font-size: 0.75rem;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.25rem;
  }

  .cp-conn-detail code {
    background: var(--cp-code-bg);
    color: var(--cp-code-text);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-size: 0.72rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  }

  .cp-conn-desc {
    font-size: 0.7rem;
    color: var(--cp-text-muted);
    line-height: 1.35;
  }

  @media (max-width: 640px) {
    .cp-grid-3 {
      grid-template-columns: 1fr;
    }
    .cp-grid-2 {
      grid-template-columns: 1fr;
    }
    .cp-connector-grid {
      grid-template-columns: 1fr;
    }
  }

</style>

<div class="dragline-container">
  <!-- Container Header Block -->
  <div class="dl-card dl-card-header">
    <div class="dl-card-title-bar">
      <div class="dl-title-group">
        <span class="dl-tag dl-tag-slate">Offset 0x00..0x0B · 12 Bytes</span>
        <span class="dl-title">Container Header · Storage Format Identity</span>
      </div>
      <span class="dl-tag dl-tag-slate">Immutable Prefix</span>
    </div>
    <div class="dl-grid-2">
      <div class="dl-field dl-field-slate">
        <div class="dl-field-label">Magic Identifier (8B)</div>
        <div class="dl-field-val"><code>PARDOSA\x01</code> <span class="dl-field-hex">[0x50, 0x41, 0x52, 0x44, 0x4F, 0x53, 0x41, 0x01]</span></div>
        <div class="dl-field-desc">Immutable engine signature identifying dragline container format</div>
      </div>
      <div class="dl-field dl-field-slate">
        <div class="dl-field-label">Format Version (4B)</div>
        <div class="dl-field-val"><code>1 LE</code> <span class="dl-field-hex">[0x01, 0x00, 0x00, 0x00]</span></div>
        <div class="dl-field-desc">32-bit unsigned little-endian integer format version</div>
      </div>
    </div>
  </div>
  <!-- Flow Boundary: Container Header to Frame 0 -->
  <div class="dl-flow-arrow">
    <div class="dl-arrow-line"></div>
    <div class="dl-arrow-badge">Initial Append Boundary: Offset 0x0C</div>
    <div class="dl-arrow-head">▼</div>
  </div>
  <!-- FRAME 0 -->
  <div class="dl-card dl-card-frame">
    <div class="dl-card-title-bar">
      <div class="dl-title-group">
        <span class="dl-tag dl-tag-slate">FRAME 0</span>
        <span class="dl-title">Offset 0x0C · Event 0 : Genesis on Fiber A</span>
      </div>
      <span class="dl-tag dl-tag-blue">Genesis Root</span>
    </div>
    <div class="dl-section-label">Physical Framing (8 Bytes Framing Overhead)</div>
    <div class="dl-grid-2">
      <div class="dl-field dl-field-slate">
        <div class="dl-field-label">frame_length_0 (4B)</div>
        <div class="dl-field-val"><code>u32 LE</code> <span class="dl-field-hex">81 + N₀ Bytes</span></div>
        <div class="dl-field-desc">Byte length of enclosed Envelope 0 payload</div>
      </div>
      <div class="dl-field dl-field-slate">
        <div class="dl-field-label">CRC32C Checksum (4B)</div>
        <div class="dl-field-val"><code>Castagnoli (SSE4.2)</code> <span class="dl-field-hex">IEEE 802.3</span></div>
        <div class="dl-field-desc">Hardware checksum detecting torn writes and disk bit-rot</div>
      </div>
    </div>
    <!-- Inner Envelope 0 Card (Strictly Contained) -->
    <div class="dl-card dl-card-envelope">
      <div class="dl-card-title-bar">
        <div class="dl-title-group">
          <span class="dl-tag dl-tag-blue">Envelope 0</span>
          <span class="dl-title">Fiber A Genesis Aggregate · Invariant C4.19</span>
        </div>
        <span class="dl-tag dl-tag-purple">85 + payload_length_0 Bytes</span>
      </div>
      <div class="dl-section-label">EnvelopeHeader Fields (81 Bytes Fixed Layout)</div>
      <div class="dl-grid-envelope">
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">event_id (16B)</div>
          <div class="dl-field-val"><code>0x01.. [E0]</code></div>
          <div class="dl-field-desc">UUID / ULID Identity</div>
        </div>
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">fiber_id (16B)</div>
          <div class="dl-field-val"><code>0xAA.. [Fiber A]</code></div>
          <div class="dl-field-desc">Aggregate Stream ID</div>
        </div>
        <div class="dl-field dl-field-slate">
          <div class="dl-field-label">detached (1B)</div>
          <div class="dl-field-val"><code>0x00</code> (Active)</div>
          <div class="dl-field-desc">Lifecycle status flag</div>
        </div>
        <div class="dl-field dl-field-green">
          <div class="dl-field-label">precursor (16B)</div>
          <div class="dl-field-val"><code>[0u8; 16]</code></div>
          <div class="dl-field-desc">Root Genesis (Null Pointer)</div>
        </div>
        <div class="dl-field dl-field-green">
          <div class="dl-field-label">precursor_hash (32B)</div>
          <div class="dl-field-val"><code>[0u8; 32]</code></div>
          <div class="dl-field-desc">Root Genesis (Zero Hash)</div>
        </div>
      </div>
      <div class="dl-section-label">Domain Event Payload (N₀ Bytes)</div>
      <div class="dl-grid-2">
        <div class="dl-field dl-field-purple">
          <div class="dl-field-label">payload_length_0 (4B)</div>
          <div class="dl-field-val"><code>u32 LE</code> <span class="dl-field-hex">N₀</span></div>
          <div class="dl-field-desc">32-bit integer length of Genesis payload</div>
        </div>
        <div class="dl-field dl-field-purple">
          <div class="dl-field-label">payload_bytes (N₀ B)</div>
          <div class="dl-field-val"><code>GenesisState</code></div>
          <div class="dl-field-desc">Initial state machine admission payload</div>
        </div>
      </div>
    </div>
    <!-- Bottom Badge: Physical Rolling Digest H0 -->
    <div class="dl-digest-badge dl-digest-slate">
      <div class="dl-digest-title">
        <span class="dl-tag dl-tag-green">H₀</span>
        <strong>Physical Rolling Digest H₀ (32B):</strong>
        <code>BLAKE3(Frame 0)</code>
      </div>
      <div class="dl-digest-desc">Base container commitment for sequential tamper-evidence</div>
    </div>
  </div>
  <!-- Inter-Frame Connector Block -->
  <div class="dl-connector-block">
    <div class="dl-connector-header">
      <span class="dl-connector-title">Inter-Frame Linkages &amp; Transitions</span>
      <span class="dl-connector-subtitle">Append progression, causal binding &amp; tamper verification</span>
    </div>
    <div class="dl-connector-grid">
      <div class="dl-conn-card dl-conn-physical">
        <div class="dl-conn-num">1</div>
        <div class="dl-conn-content">
          <div class="dl-conn-label">Physical Sequential Append</div>
          <div class="dl-conn-detail">Offset: <code>0x0C + L₀ + 8</code></div>
          <div class="dl-conn-desc">Advances past Frame 0 framing (8B) and envelope payload (L₀ bytes)</div>
        </div>
      </div>
      <div class="dl-conn-card dl-conn-logical">
        <div class="dl-conn-num">2</div>
        <div class="dl-conn-content">
          <div class="dl-conn-label">Logical Precursor Link</div>
          <div class="dl-conn-detail">Points to <code>E0 [0x01..]</code></div>
          <div class="dl-conn-desc">Enforces single-writer linearizability on Fiber A via CAS head check</div>
        </div>
      </div>
      <div class="dl-conn-card dl-conn-causal">
        <div class="dl-conn-num">3</div>
        <div class="dl-conn-content">
          <div class="dl-conn-label">Causal Commitment (Invariant C5.40)</div>
          <div class="dl-conn-detail"><code>BLAKE3(Envelope 0)</code></div>
          <div class="dl-conn-desc">Cryptographic parent commitment prevents silent aggregate history rewrite</div>
        </div>
      </div>
      <div class="dl-conn-card dl-conn-rolling">
        <div class="dl-conn-num">4</div>
        <div class="dl-conn-content">
          <div class="dl-conn-label">Physical Rolling Fold (Invariant C5.26)</div>
          <div class="dl-conn-detail"><code>BLAKE3(H₀ ∥ Frame 1)</code></div>
          <div class="dl-conn-desc">Sequential tamper-evidence accumulated across all physical frames</div>
        </div>
      </div>
    </div>
    <div class="dl-flow-arrow">
      <div class="dl-arrow-line"></div>
      <div class="dl-arrow-head">▼</div>
    </div>
  </div>
  <!-- FRAME 1 -->
  <div class="dl-card dl-card-frame">
    <div class="dl-card-title-bar">
      <div class="dl-title-group">
        <span class="dl-tag dl-tag-slate">FRAME 1</span>
        <span class="dl-title">Offset 0x0C + L₀ + 8 · Event 1 : State Mutation on Fiber A</span>
      </div>
      <span class="dl-tag dl-tag-emerald">Fiber A Mutation</span>
    </div>
    <div class="dl-section-label">Physical Framing (8 Bytes Framing Overhead)</div>
    <div class="dl-grid-2">
      <div class="dl-field dl-field-slate">
        <div class="dl-field-label">frame_length_1 (4B)</div>
        <div class="dl-field-val"><code>u32 LE</code> <span class="dl-field-hex">81 + N₁ Bytes</span></div>
        <div class="dl-field-desc">Byte length of enclosed Envelope 1 payload</div>
      </div>
      <div class="dl-field dl-field-slate">
        <div class="dl-field-label">CRC32C Checksum (4B)</div>
        <div class="dl-field-val"><code>Castagnoli (SSE4.2)</code> <span class="dl-field-hex">IEEE 802.3</span></div>
        <div class="dl-field-desc">Hardware checksum detecting torn writes and disk bit-rot</div>
      </div>
    </div>
    <!-- Inner Envelope 1 Card (Strictly Contained) -->
    <div class="dl-card dl-card-envelope">
      <div class="dl-card-title-bar">
        <div class="dl-title-group">
          <span class="dl-tag dl-tag-blue">Envelope 1</span>
          <span class="dl-title">Fiber A State Mutation · Invariant C4.19</span>
        </div>
        <span class="dl-tag dl-tag-purple">85 + payload_length_1 Bytes</span>
      </div>
      <div class="dl-section-label">EnvelopeHeader Fields (81 Bytes Fixed Layout)</div>
      <div class="dl-grid-envelope">
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">event_id (16B)</div>
          <div class="dl-field-val"><code>0x02.. [E1]</code></div>
          <div class="dl-field-desc">UUID / ULID Identity</div>
        </div>
        <div class="dl-field dl-field-blue">
          <div class="dl-field-label">fiber_id (16B)</div>
          <div class="dl-field-val"><code>0xAA.. [Fiber A]</code></div>
          <div class="dl-field-desc">Aggregate Stream ID</div>
        </div>
        <div class="dl-field dl-field-slate">
          <div class="dl-field-label">detached (1B)</div>
          <div class="dl-field-val"><code>0x00</code> (Active)</div>
          <div class="dl-field-desc">Lifecycle status flag</div>
        </div>
        <div class="dl-field dl-field-emerald-highlight">
          <div class="dl-field-label dl-emerald-label">precursor (16B) · Link</div>
          <div class="dl-field-val"><code>0x01.. [E0]</code></div>
          <div class="dl-field-desc dl-emerald-desc">Points to E0 (Linear predecessor)</div>
        </div>
        <div class="dl-field dl-field-emerald-highlight">
          <div class="dl-field-label dl-emerald-label">precursor_hash (32B) · Causal</div>
          <div class="dl-field-val"><code>BLAKE3(Envelope 0)</code></div>
          <div class="dl-field-desc dl-emerald-desc">Cryptographic parent commitment</div>
        </div>
      </div>
      <div class="dl-section-label">Domain Event Payload (N₁ Bytes)</div>
      <div class="dl-grid-2">
        <div class="dl-field dl-field-purple">
          <div class="dl-field-label">payload_length_1 (4B)</div>
          <div class="dl-field-val"><code>u32 LE</code> <span class="dl-field-hex">N₁</span></div>
          <div class="dl-field-desc">32-bit integer length of Mutation payload</div>
        </div>
        <div class="dl-field dl-field-purple">
          <div class="dl-field-label">payload_bytes (N₁ B)</div>
          <div class="dl-field-val"><code>AccountUpdated</code></div>
          <div class="dl-field-desc">Committed state transition payload</div>
        </div>
      </div>
    </div>
    <!-- Bottom Badge: Physical Rolling Digest H1 (Emerald Highlighted) -->
    <div class="dl-digest-badge dl-digest-emerald">
      <div class="dl-digest-title">
        <span class="dl-tag dl-tag-emerald">H₁</span>
        <strong>Physical Rolling Digest H₁ (32B):</strong>
        <code>BLAKE3(H₀ ∥ Frame 1)</code>
      </div>
      <div class="dl-digest-desc">Sequential Tamper-Evidence (Invariant C5.26) · Folded sequentially across frames</div>
    </div>
  </div>
</div>

### 1. Container Header (12 Bytes)
At file offset `0x00000000` of `<stem>.pgno`, the container header establishes format identity:
- **Magic Bytes (`0x00..0x07`, 8 bytes)**: Fixed byte sequence `PARDOSA\x01` (`[0x50, 0x41, 0x52, 0x44, 0x4F, 0x53, 0x41, 0x01]`).
- **Format Version (`0x08..0x0B`, 4 bytes)**: 32-bit little-endian integer (`1` = `0x01, 0x00, 0x00, 0x00`).

Any file lacking this 12-byte signature is rejected during container initialization.

### 2. Frame Framing (Invariant C3.4)
Every commit to the dragline is framed with length demarcations and hardware-accelerated checksums:
- **Length Prefix (4 bytes)**: 32-bit little-endian unsigned integer declaring the byte length of the enclosed frame payload.
- **Frame Payload (`frame_length` bytes)**: The unpadded event envelope.
- **CRC32C Checksum (4 bytes)**: Castagnoli polynomial checksum (IEEE 802.3 / SSE4.2 CRC32C) computed over the frame payload bytes. Torn writes, truncated disk blocks, or silent disk bit-rot are detected prior to envelope parsing.

### 3. Event Envelope Header (Invariant C4.19)
The frame payload contains an unpadded, fixed 81-byte `EnvelopeHeader` followed by the domain event payload:

| Field | Offset | Width | Type | Description |
|---|---|---|---|---|
| `event_id` | `0x00` | 16 bytes | `[u8; 16]` | Globally unique event identifier (UUID/ULID). |
| `fiber_id` | `0x10` | 16 bytes | `[u8; 16]` | Scoped domain entity / aggregate identifier. |
| `detached` | `0x20` | 1 byte | `bool` (`u8`) | Lifecycle flag: `0x00` = active, `0x01` = soft-deleted. |
| `precursor` | `0x21` | 16 bytes | `[u8; 16]` | Predecessor `event_id` on this fiber (`[0u8; 16]` for root). |
| `precursor_hash` | `0x31` | 32 bytes | `[u8; 32]` | 256-bit BLAKE3 cryptographic hash of precursor event. |
| `payload_length` | `0x51` | 4 bytes | `u32` LE | Byte length $N$ of domain event payload. |
| `payload_bytes` | `0x55` | $N$ bytes | `[u8; N]` | Serialized domain-specific event payload. |

Total unpadded envelope length is exactly $81 + 4 + N = 85 + \text{payload\_length}$ bytes.

### 4. Physical vs. Logical Cryptographic Commitments

Pardosa maintains two complementary, orthogonal cryptographic chains:

<div class="pardosa-crypto-diagram" style="margin: 2rem 0; padding: 1.5rem 1rem; border-radius: 0.75rem; border: 1px solid var(--gray-200, #e2e8f0); background: var(--body-background, #ffffff); overflow-x: auto;">
<svg id="crypto-diagram" viewBox="0 0 1020 410" width="100%" height="auto" style="display: block; min-width: 780px; max-width: 1020px; margin: 0 auto; overflow: visible;">
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
<text class="tier-title" x="200" y="25" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle">Physical Integrity Chain (Invariant C5.26)</text>

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
<text class="node-sub" x="16" y="40" fill="var(--sm-slate-sub)">H_0 = BLAKE3(F_0)</text>
</g>

<g id="frame-1" transform="translate(235, 62)">
<rect width="130" height="56" rx="8" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="2" filter="url(#crypto-shadow)"/>
<rect width="5" height="56" rx="2.5" fill="var(--sm-slate-stroke)"/>
<text class="node-title" x="16" y="22" fill="var(--sm-slate-text)" dominant-baseline="central">Frame 1</text>
<text class="node-sub" x="16" y="40" fill="var(--sm-slate-sub)">H_1 = BLAKE3(H_0||F_1)</text>
</g>

<g id="frame-2" transform="translate(425, 62)">
<rect width="130" height="56" rx="8" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="2" filter="url(#crypto-shadow)"/>
<rect width="5" height="56" rx="2.5" fill="var(--sm-slate-stroke)"/>
<text class="node-title" x="16" y="22" fill="var(--sm-slate-text)" dominant-baseline="central">Frame 2</text>
<text class="node-sub" x="16" y="40" fill="var(--sm-slate-sub)">H_2 = BLAKE3(H_1||F_2)</text>
</g>

<g id="frame-3" transform="translate(615, 62)">
<rect width="130" height="56" rx="8" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="2" filter="url(#crypto-shadow)"/>
<rect width="5" height="56" rx="2.5" fill="var(--sm-slate-stroke)"/>
<text class="node-title" x="16" y="22" fill="var(--sm-slate-text)" dominant-baseline="central">Frame 3</text>
<text class="node-sub" x="16" y="40" fill="var(--sm-slate-sub)">H_3 = BLAKE3(H_2||F_3)</text>
</g>

<g id="frame-proof" transform="translate(805, 62)">
<rect width="175" height="56" rx="8" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="2.2" filter="url(#crypto-shadow)"/>
<rect width="5" height="56" rx="2.5" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="16" y="22" fill="var(--sm-green-text)" dominant-baseline="central">Log Commitment</text>
<text class="node-sub" x="16" y="40" fill="var(--sm-green-sub)">Rolling Digest Proof</text>
</g>

<!-- Bottom Section Left: Logical Precursor Chains (Invariant C5.40) -->
<rect x="20" y="175" width="630" height="215" rx="10" fill="none" stroke="var(--sm-slate-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="35" y="164" width="340" height="22" rx="11" fill="var(--sm-slate-bg)" stroke="var(--sm-slate-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="205" y="175" fill="var(--sm-slate-text)" dominant-baseline="central" text-anchor="middle">Logical Precursor Chains (Invariant C5.40)</text>

<!-- Fiber Alpha Sub-box -->
<rect x="40" y="200" width="280" height="175" rx="8" fill="none" stroke="var(--sm-blue-stroke)" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.7"/>
<rect x="55" y="191" width="105" height="18" rx="9" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1"/>
<text class="tier-title" x="107" y="200" fill="var(--sm-blue-text)" dominant-baseline="central" text-anchor="middle">Fiber Alpha</text>

<!-- Link from A1 up to A0 -->
<path d="M 180,305 L 180,277" class="edge-dashed" stroke="var(--sm-blue-stroke)" marker-end="url(#crypto-arrow-blue)"/>
<g>
<rect class="badge-bg" x="125" y="278" width="110" height="18" rx="9"/>
<text class="edge-label badge-txt" x="180" y="287" dominant-baseline="central" text-anchor="middle">precursor_hash</text>
</g>

<g id="fiber-a-root" transform="translate(60, 222)">
<rect width="240" height="48" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#crypto-shadow)"/>
<rect width="4" height="48" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="16" y="19" fill="var(--sm-blue-text)" dominant-baseline="central">E0 (Root)</text>
<text class="node-sub" x="16" y="34" fill="var(--sm-blue-sub)">precursor_hash = 0x00...00</text>
</g>

<g id="fiber-a-update" transform="translate(60, 305)">
<rect width="240" height="48" rx="7" fill="var(--sm-blue-bg)" stroke="var(--sm-blue-stroke)" stroke-width="1.8" filter="url(#crypto-shadow)"/>
<rect width="4" height="48" rx="2" fill="var(--sm-blue-stroke)"/>
<text class="node-title" x="16" y="19" fill="var(--sm-blue-text)" dominant-baseline="central">E2 (Update)</text>
<text class="node-sub" x="16" y="34" fill="var(--sm-blue-sub)">precursor_hash = BLAKE3(E0)</text>
</g>

<!-- Fiber Beta Sub-box -->
<rect x="350" y="200" width="280" height="175" rx="8" fill="none" stroke="var(--sm-green-stroke)" stroke-width="1.2" stroke-dasharray="3 3" opacity="0.7"/>
<rect x="365" y="191" width="100" height="18" rx="9" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1"/>
<text class="tier-title" x="415" y="200" fill="var(--sm-green-text)" dominant-baseline="central" text-anchor="middle">Fiber Beta</text>

<!-- Link from B1 up to B0 -->
<path d="M 490,305 L 490,277" class="edge-dashed" stroke="var(--sm-green-stroke)" marker-end="url(#crypto-arrow-green)"/>
<g>
<rect class="badge-bg" x="435" y="278" width="110" height="18" rx="9"/>
<text class="edge-label badge-txt" x="490" y="287" dominant-baseline="central" text-anchor="middle">precursor_hash</text>
</g>

<g id="fiber-b-root" transform="translate(370, 222)">
<rect width="240" height="48" rx="7" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.8" filter="url(#crypto-shadow)"/>
<rect width="4" height="48" rx="2" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="16" y="19" fill="var(--sm-green-text)" dominant-baseline="central">E1 (Root)</text>
<text class="node-sub" x="16" y="34" fill="var(--sm-green-sub)">precursor_hash = 0x00...00</text>
</g>

<g id="fiber-b-update" transform="translate(370, 305)">
<rect width="240" height="48" rx="7" fill="var(--sm-green-bg)" stroke="var(--sm-green-stroke)" stroke-width="1.8" filter="url(#crypto-shadow)"/>
<rect width="4" height="48" rx="2" fill="var(--sm-green-stroke)"/>
<text class="node-title" x="16" y="19" fill="var(--sm-green-text)" dominant-baseline="central">E3 (Update)</text>
<text class="node-sub" x="16" y="34" fill="var(--sm-green-sub)">precursor_hash = BLAKE3(E1)</text>
</g>

<!-- Bottom Section Right: Orthogonality Annotation -->
<rect x="670" y="175" width="330" height="215" rx="10" fill="none" stroke="var(--sm-purple-stroke)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.6"/>
<rect x="685" y="164" width="220" height="22" rx="11" fill="var(--sm-purple-bg)" stroke="var(--sm-purple-stroke)" stroke-width="1.2"/>
<text class="tier-title" x="795" y="175" fill="var(--sm-purple-text)" dominant-baseline="central" text-anchor="middle">Orthogonality Guarantee</text>

<g transform="translate(695, 205)">
<rect width="280" height="165" rx="8" fill="var(--sm-purple-bg)" stroke="var(--sm-purple-stroke)" stroke-width="1.5" filter="url(#crypto-shadow)"/>
<rect width="5" height="165" rx="2.5" fill="var(--sm-purple-stroke)"/>
<text class="node-title" x="16" y="24" fill="var(--sm-purple-text)" dominant-baseline="central">Physical ⊥ Logical</text>
<text class="callout-body" x="16" y="52">Physical commitments (H_k) verify</text>
<text class="callout-body" x="16" y="70">disk file framing &amp; detect bit-flips.</text>
<text class="callout-body" x="16" y="96">Logical precursor hash chains secure</text>
<text class="callout-body" x="16" y="114">entity provenance across fibers.</text>
<text class="callout-body" x="16" y="140">Pruning purged fibers never breaks</text>
<text class="callout-body" x="16" y="158">surviving entity precursor chains.</text>
</g>

</svg>
</div>

- **Physical Rolling Commitment (Invariant C5.26)**: A running 256-bit BLAKE3 hash digest computed sequentially across all container frames in `<stem>.pgno`. Each frame $k$ is folded into the rolling commitment:
  $$\mathcal{H}_k = \text{BLAKE3}(\mathcal{H}_{k-1} \parallel \text{Frame}_k)$$
  This guarantees immediate tamper-evidence for the physical stream: missing frames, reordered writes, or bit flips corrupt the rolling digest.
- **Logical Precursor Chain (Invariant C5.40)**: Independent, fiber-scoped hash linkage. Each event's `precursor_hash` contains the BLAKE3 digest of the preceding event on the same `fiber_id`.
- **Orthogonality**: Because physical commitments track file framing and logical commitments track aggregate state transitions, events from distinct fibers interleave freely without invalidating entity provenance. During line migrations, purged fibers can be pruned from `<stem>.pgno` without breaking the precursor chains of surviving fibers.

---

## The 5-State Lifecycle State Machine

At the core of Pardosa is an explicit, formal state machine governing every fiber's lifecycle. An aggregate does not merely exist or get deleted; it transitions across five strictly defined states:

1. **`Undefined`**: The entity has never existed within the domain namespace.
2. **`Defined`**: The fiber is active, exists, and accepts updates.
3. **`Detached`**: The fiber is soft-deleted; it remains on the dragline for historical auditability and can be rescued or migrated.
4. **`Purged`**: The fiber has been permanently removed from the line following an auditable migration, satisfying regulatory deletion mandates while preserving optional audit records.
5. **`Locked`**: The fiber has been pruned and frozen; the identifier cannot be reused, preventing replay attacks or accidental recreation.

### The 10 Legal Transitions

Pardosa encodes exactly **10 legal state transitions**. Any action attempting an unlisted transition is rejected at compile time and runtime by the `IllegalStateTransition` error:

<div class="pardosa-lifecycle-diagram" style="margin: 2rem 0; padding: 1.5rem 1rem; border-radius: 0.75rem; border: 1px solid var(--gray-200, #e2e8f0); background: var(--body-background, #ffffff); overflow-x: auto;">
<svg id="state-diagram" viewBox="0 0 1060 510" width="100%" height="auto" style="display: block; min-width: 780px; max-width: 1060px; margin: 0 auto; overflow: visible;">
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
<circle cx="210" cy="60" r="8" fill="var(--sm-slate-stroke)"/>
<path d="M 218,60 L 277,60" class="edge-path" stroke="var(--sm-slate-stroke)" marker-end="url(#arrow-slate)"/>
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
<text class="state-sub" x="20" y="43" fill="var(--sm-blue-sub)">Active &amp; Linearized</text>
</g>
<g id="state-detached" transform="translate(600, 160)">
<rect id="rect-detached" width="160" height="54" rx="8" fill="var(--sm-amber-bg)" stroke="var(--sm-amber-stroke)" stroke-width="2.5" filter="url(#shadow)"/>
<rect width="6" height="54" rx="3" fill="var(--sm-amber-stroke)"/>
<text id="text-detached" class="state-title" x="20" y="27" fill="var(--sm-amber-text)" dominant-baseline="central">Detached</text>
<text class="state-sub" x="20" y="43" fill="var(--sm-amber-sub)">Soft-Deleted</text>
</g>
<g id="state-locked" transform="translate(600, 400)">
<rect id="rect-locked" width="160" height="54" rx="8" fill="var(--sm-purple-bg)" stroke="var(--sm-purple-stroke)" stroke-width="2.5" filter="url(#shadow)"/>
<rect width="6" height="54" rx="3" fill="var(--sm-purple-stroke)"/>
<text id="text-locked" class="state-title" x="20" y="27" fill="var(--sm-purple-text)" dominant-baseline="central">Locked</text>
<text class="state-sub" x="20" y="43" fill="var(--sm-purple-sub)">Frozen Tombstone</text>
</g>
<g id="state-purged" transform="translate(280, 400)">
<rect id="rect-purged" width="160" height="54" rx="8" fill="var(--sm-rose-bg)" stroke="var(--sm-rose-stroke)" stroke-width="2.5" filter="url(#shadow)"/>
<rect width="6" height="54" rx="3" fill="var(--sm-rose-stroke)"/>
<text id="text-purged" class="state-title" x="20" y="27" fill="var(--sm-rose-text)" dominant-baseline="central">Purged</text>
<text class="state-sub" x="20" y="43" fill="var(--sm-rose-sub)">Permanently Scrubbed</text>
</g>
</svg>
</div>

| # | Action | Source State | Target State | Operational Semantics |
|---|---|---|---|---|
| 1 | `Create` | `Undefined` | `Defined` | Initial creation of an entity from an empty state. |
| 2 | `Update` | `Defined` | `Defined` | Appending a new state-modifying event to an active fiber. |
| 3 | `Detach` | `Defined` | `Detached` | Soft-deleting an aggregate; marks head as detached. |
| 4 | `Rescue` | `Detached` | `Defined` | Reversing a soft delete; returns the fiber to active status. |
| 5 | `Migrate(Keep)` | `Detached` | `Detached` | Retains the soft-deleted fiber across a line migration. |
| 6 | `Migrate(LockAndPrune)` | `Detached` | `Locked` | Prunes fiber history, retaining only the tombstone; prevents reuse. |
| 7 | `Migrate(Purge)` | `Detached` | `Purged` | Verifiably scrubs all event payloads and keys from the active line. |
| 8 | `Rescue` | `Locked` | `Defined` | Administrative rescue of a locked fiber under an explicit audit policy. |
| 9 | `Migrate(Purge)` | `Locked` | `Purged` | Permanently purges a previously locked fiber during migration. |
| 10 | `Create` | `Purged` | `Defined` | Re-allocates the domain identifier cleanly following a complete purge. |

---

## Consumer Idempotency & Deterministic Projections

In event-driven architectures, downstream systems build read models, search indexes, in-memory view models, and pre-rendered caches by projecting the event stream. Pardosa guarantees deterministic consumption and effectively exactly-once processing through authoritative core engine invariants and architectural demarcation rather than relying on external database transactions:

<div class="consumer-proj-container">
  <div class="cp-card cp-card-blue" style="margin-bottom: 1rem;">
    <div class="cp-card-title-bar">
      <div class="cp-title-group">
        <span class="cp-tag cp-tag-blue">Pipeline Architecture</span>
        <span class="cp-title">Pardosa Dragline ➔ Monotonic Cursor ➔ Consumer Adapter Fold</span>
      </div>
      <span class="cp-tag cp-tag-slate">Demarcated Pipeline</span>
    </div>
    <div class="cp-field-desc">
      Architectural demarcation separating engine-level append guarantees from downstream read-model projections. Downstream adapters fold immutable event facts autonomously with zero RPC callbacks and zero relational multi-row transaction coupling.
    </div>
  </div>
  <div class="cp-grid-3">
    <!-- Stage 1: Pardosa Core Engine -->
    <div class="cp-card cp-card-blue">
      <div class="cp-card-title-bar">
        <div class="cp-title-group">
          <span class="cp-tag cp-tag-blue">Stage 1</span>
          <span class="cp-title">Pardosa Dragline</span>
        </div>
        <span class="cp-tag cp-tag-slate">Core Engine</span>
      </div>
      <div class="cp-section-label">Log Guarantees (C3.8 · C4.19)</div>
      <div class="cp-stack-compact">
        <div class="cp-field cp-field-blue">
          <div class="cp-field-label">Total Replay Order (C3.8)</div>
          <div class="cp-field-val"><code>&lt;stem&gt;.pgno Append Log</code></div>
          <div class="cp-field-desc">Immutable physical total order over all events [E₁, E₂, ..., E_N] within the container.</div>
        </div>
        <div class="cp-field cp-field-blue">
          <div class="cp-field-label">Cryptographic Identity (C4.19)</div>
          <div class="cp-field-val"><code>81B Header · BLAKE3</code></div>
          <div class="cp-field-desc">16B event_id and 32B BLAKE3 precursor commitment hash per event envelope.</div>
        </div>
        <div class="cp-field cp-field-blue">
          <div class="cp-field-label">Sequential Streaming API</div>
          <div class="cp-field-val"><code>stream_from(cursor)</code></div>
          <div class="cp-field-desc">Linear non-blocking frame dispatch to registered consumer adapters.</div>
        </div>
      </div>
    </div>
    <!-- Stage 2: Monotonic Resume Cursor -->
    <div class="cp-card cp-card-green">
      <div class="cp-card-title-bar">
        <div class="cp-title-group">
          <span class="cp-tag cp-tag-green">Stage 2</span>
          <span class="cp-title">Monotonic Cursor</span>
        </div>
        <span class="cp-tag cp-tag-green">Invariant C5.22</span>
      </div>
      <div class="cp-section-label">Cursor Guarantees (C5.22)</div>
      <div class="cp-stack-compact">
        <div class="cp-field cp-field-green">
          <div class="cp-field-label">Physical Frame Boundary</div>
          <div class="cp-field-val"><code>u64 Byte Offset</code></div>
          <div class="cp-field-desc">Monotonic 64-bit physical byte offset pointing strictly to verified frame boundaries.</div>
        </div>
        <div class="cp-field cp-field-green">
          <div class="cp-field-label">Valid by Construction</div>
          <div class="cp-field-val"><code>Zero-Scan Resumption</code></div>
          <div class="cp-field-desc">Unaligned offsets are unrepresentable; resumes immediately without log parsing.</div>
        </div>
        <div class="cp-field cp-field-green">
          <div class="cp-field-label">Lifecycle Scope</div>
          <div class="cp-field-val"><code>Dragline-Local Scope</code></div>
          <div class="cp-field-desc">Bound to container lifetime; regenerated during migrations with no cross-line leakage.</div>
        </div>
      </div>
    </div>
    <!-- Stage 3: Consumer Adapter Fold -->
    <div class="cp-card cp-card-purple">
      <div class="cp-card-title-bar">
        <div class="cp-title-group">
          <span class="cp-tag cp-tag-purple">Stage 3</span>
          <span class="cp-title">Consumer Adapter</span>
        </div>
        <span class="cp-tag cp-tag-purple">Projection Fold</span>
      </div>
      <div class="cp-section-label">Adapter Ownership (Demarcation)</div>
      <div class="cp-stack-compact">
        <div class="cp-field cp-field-purple">
          <div class="cp-field-label">Pure Deterministic Fold</div>
          <div class="cp-field-val"><code>State_N = fold(State₀, [E₁..E_N])</code></div>
          <div class="cp-field-desc">Pure reduction function transforms immutable event stream into typed view models.</div>
        </div>
        <div class="cp-field cp-field-purple">
          <div class="cp-field-label">ECST Autonomy</div>
          <div class="cp-field-val"><code>Self-Contained Facts</code></div>
          <div class="cp-field-desc">Events carry complete domain transition facts; zero synchronous RPC callback queries.</div>
        </div>
        <div class="cp-field cp-field-purple">
          <div class="cp-field-label">Idempotency &amp; Dedup</div>
          <div class="cp-field-val"><code>16B event_id / Upsert Keys</code></div>
          <div class="cp-field-desc">Deduplication windows and natural upsert keys eliminate side effects across retries.</div>
        </div>
      </div>
    </div>
  </div>
  <!-- Connector / Progression Bar -->
  <div class="cp-connector-block">
    <div class="cp-connector-header">
      <div class="cp-connector-title">End-to-End Projection Lifecycle</div>
      <div class="cp-connector-subtitle">Sequential Fact Propagation Across Demarcation Boundary</div>
    </div>
    <div class="cp-connector-grid">
      <div class="cp-conn-card">
        <div class="cp-conn-num cp-num-blue">1</div>
        <div class="cp-conn-content">
          <div class="cp-conn-label">Frame Append &amp; Commit</div>
          <div class="cp-conn-detail"><code>Single-Writer CAS</code> ➔ <code>.pgno</code></div>
          <div class="cp-conn-desc">Linearizable append logs frame with CRC32C framing and rolling BLAKE3 commitment.</div>
        </div>
      </div>
      <div class="cp-conn-card">
        <div class="cp-conn-num cp-num-green">2</div>
        <div class="cp-conn-content">
          <div class="cp-conn-label">Cursor Query &amp; Dispatch</div>
          <div class="cp-conn-detail"><code>stream_from(cursor)</code> ➔ <code>Events [E_k]</code></div>
          <div class="cp-conn-desc">Consumer adapter queries stream from its persisted monotonic byte offset (C5.22).</div>
        </div>
      </div>
      <div class="cp-conn-card">
        <div class="cp-conn-num cp-num-purple">3</div>
        <div class="cp-conn-content">
          <div class="cp-conn-label">Deterministic State Fold</div>
          <div class="cp-conn-detail"><code>State_N = fold(State_{N-1}, E_N)</code></div>
          <div class="cp-conn-desc">Adapter folds self-contained facts (ECST) into view models without RPC callbacks.</div>
        </div>
      </div>
      <div class="cp-conn-card">
        <div class="cp-conn-num cp-num-cyan">4</div>
        <div class="cp-conn-content">
          <div class="cp-conn-label">Autonomous Read Serving</div>
          <div class="cp-conn-detail"><code>Read Models</code> ➔ <code>O(1) Queries</code></div>
          <div class="cp-conn-desc">Downstream consumers (e.g. Spandrel static cache) serve reads with zero write contention.</div>
        </div>
      </div>
    </div>
  </div>
</div>

### Core Engine Invariants

1. **Deterministic Event Folds (Invariant C3.8)**: An artefact holds exactly one total order over all events it carries on `<stem>.pgno`, and replaying it yields that identical order every time. Replaying the identical sequence of dragline frames produces identical projection state bit-for-bit:
   $$\text{State}_N = \text{fold}(\text{State}_0, [E_1, E_2, \dots, E_N])$$
   Projections rely strictly on immutable event facts—timestamps, precursors, and state payloads—eliminating dependencies on consumer arrival time, wall-clock skew, network transit delays, or execution environment non-determinism. Downstream read models can rebuild their entire state deterministically from genesis ($\text{State}_0$) or incrementally from any verified checkpoint frame.
2. **Dragline-Local Resume Cursors (Invariant C5.22)**: Pardosa exposes a resume cursor that is dragline-local and valid by construction. Monotonic 64-bit physical byte offsets point directly to verified frame boundaries within `<stem>.pgno`. Cursors are valid by construction: a consumer cannot construct or advance to an unaligned offset or an uncommitted frame. When resuming after restarts or failovers, consumers invoke `stream_from(cursor)` to resume streaming directly from that byte boundary without scanning logs, indexing tables, or re-processing previously committed frames. Cursors are regenerated during migrations and have no meaning across migrations.
3. **Cryptographic Event Identity & Commitments (Invariant C4.19)**: Every event envelope carries a fixed 81-byte wire header containing a globally unique 16-byte `event_id` (128-bit UUID), a 16-byte `fiber_id`, a 1-byte detachment flag, a 16-byte `precursor` UUID, and a 32-byte BLAKE3 `precursor_hash` commitment (both frame-level digest and fiber precursor hash). Combined with hardware-accelerated CRC32C framing, this cryptographic commitment enables unconditional deduplication: downstream consumer adapters can detect re-delivered frames and eliminate duplicate side-effects unconditionally.

### Event Carried State Transfer (ECST)

- **Self-Contained Domain Facts**: Events emitted by Pardosa carry full state transition facts rather than thin notifications (e.g., entity IDs requiring subsequent queries). Downstream consumers receive all data necessary to project their read models without executing synchronous callback queries or RPC round-trips to the producer or source datastore.
- **Autonomous Projections**: Read models (in-memory view models, search indexes, analytical column stores, Spandrel static cache stores) consume the dragline independently at their own pace. If a consumer crashes, restarts, or lags during bulk backpressure, write ingestion into the Pardosa dragline remains completely unaffected.

### Adapter Demarcation & Side-Effect Elimination

To maintain clean architectural boundaries and prevent coupling engine storage to external sinks, Pardosa enforces strict demarcation between core engine responsibilities and consumer-side adapter responsibilities:

| Responsibility | Pardosa Core Engine | Consumer-Side Adapter (e.g., Spandrel) |
|---|---|---|
| **Log Storage & Framing** | Physical append log (`.pgno`), frame CRC32C, BLAKE3 rolling commitments | Downstream read models (SQLite, memory maps, search indexes, static HTML caches) |
| **Ordering & Cursors** | Total log order (C3.8), dragline-local cursor offsets (C5.22) | Cursor offset persistence, checkpoint retention, replay coordination |
| **Identity & Mapping** | 16-byte `event_id`, 16-byte `fiber_id`, precursor causal chains | Domain aggregate IDs (`IssueId`, `AccountId`), in-memory `FiberIndex` mapping |
| **State Transformation** | Raw frame envelope serialization, byte-level framing validation | Pure projection fold functions (`State_N = fold(State_{N-1}, E_N)`), view models |
| **Side-Effect Elimination** | Unconditional deduplication metadata (C4.19 BLAKE3 commitments) | Idempotent upserts, bounded dedup filters, zero RPC callbacks |

Downstream consumer adapters achieve side-effect elimination and effectively exactly-once processing through:
- **Pure Mathematical Folds**: Downstream projections model state accumulation as pure, deterministic functions over immutable events: $\text{State}_N = \text{fold}(\text{State}_{N-1}, E_N)$. Reprocessing the log from genesis or from a verified checkpoint cursor yields identical bit-level state.
- **Cryptographic Deduplication (C4.19)**: For sinks with external side effects (e.g., message queues, webhook dispatchers, search indexes), adapters use the 16-byte `event_id` or 32-byte BLAKE3 precursor hash as natural idempotency tokens. Duplicate deliveries within a replay window are identified and dropped as no-ops prior to external invocation.
- **Adapter-Owned Cursor Persistence**: Adapters record their dragline-local cursor alongside their projected view model. On crash recovery, the adapter reads its persisted cursor and calls `stream_from(cursor)` to resume exactly where processing halted without requiring engine-level multi-row database transactions.

---

## Regulatory Compliance & Verifiable Deletion

In enterprise architectures, compliance cannot be an afterthought. Pardosa satisfies privacy legislation (such as GDPR Article 17) through **auditable line migrations**:

1. **Separation of Line and Audit**: A line contains the active operational stream. An optional audit log captures raw events separately under strict access controls.
2. **Cryptographic Integrity**: Payloads and envelope headers are hashed using BLAKE3. Tampering with any historical event on a fiber breaks the precursor hash chain immediately.
3. **Physical Purging via Line Migration**: When an operator executes a line migration with `Migrate(Purge)` on detached fibers:
   - Pardosa constructs a new, compacted line version (`<new_stem>.pgno` and `<new_stem>.meta`).
   - Events belonging to purged fibers are physically excluded from the new container file.
   - Active fibers are preserved, retaining their exact logical precursor hash relationships.
   - A fresh physical rolling BLAKE3 commitment is computed sequentially over the new container.
   - The old line version is verifiably scrubbed from disk, providing provable physical data destruction while preserving cryptographic proof of the migration transaction itself.

