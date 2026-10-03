---
title: "Software Factory SDLC (sf-sdlc)"
description: "Authoritative engineering lifecycle and monotonic quality ratchet for software fleets"
weight: 10
homeFeatured: true
---

## Software Factory SDLC (sf-sdlc)

Multi-repository software fleets inevitably suffer from structural entropy: architectural drift, divergent dependency baselines, silent quality regressions, and what can only be termed *compliance theatre*. In the absence of an authoritative, mechanically enforced lifecycle, organizational standards devolve into static wiki pages, subjective code review debates, and disconnected audit checklists that teams satisfy symbolically rather than structurally.

`sf-sdlc` establishes a rigorous, normative software engineering lifecycle and an automated quality ratchet designed specifically for modern autonomous agent and human engineering fleets. It defines how software moves from initial intent to retirement, governs technical trade-offs through an explicit priority hierarchy, and enforces baseline hygiene across repositories using high-speed, read-only mechanical checkers.

<style>
  .sdlc-container {
    --sdlc-bg: #ffffff;
    --sdlc-text: #0f172a;
    --sdlc-text-muted: #475569;
    --sdlc-code-bg: rgba(15, 23, 42, 0.06);
    --sdlc-code-text: #0f172a;

    --sdlc-slate-border: #64748b;
    --sdlc-slate-bg: rgba(100, 116, 139, 0.05);
    --sdlc-slate-tag-bg: #475569;
    --sdlc-slate-tag-text: #ffffff;

    --sdlc-blue-border: #2563eb;
    --sdlc-blue-bg: rgba(37, 99, 235, 0.04);
    --sdlc-blue-tag-bg: #1d4ed8;
    --sdlc-blue-tag-text: #ffffff;

    --sdlc-purple-border: #7c3aed;
    --sdlc-purple-bg: rgba(124, 58, 237, 0.04);
    --sdlc-purple-tag-bg: #6d28d9;
    --sdlc-purple-tag-text: #ffffff;

    --sdlc-green-border: #059669;
    --sdlc-green-bg: rgba(5, 150, 105, 0.06);
    --sdlc-green-tag-bg: #047857;
    --sdlc-green-tag-text: #ffffff;

    --sdlc-cyan-border: #0891b2;
    --sdlc-cyan-bg: rgba(8, 145, 178, 0.05);
    --sdlc-cyan-tag-bg: #0e7490;
    --sdlc-cyan-tag-text: #ffffff;

    --sdlc-amber-border: #d97706;
    --sdlc-amber-bg: rgba(217, 119, 6, 0.05);
    --sdlc-amber-tag-bg: #b45309;
    --sdlc-amber-tag-text: #ffffff;

    --sdlc-rose-border: #e11d48;
    --sdlc-rose-bg: rgba(225, 29, 72, 0.05);
    --sdlc-rose-tag-bg: #be123c;
    --sdlc-rose-tag-text: #ffffff;

    --sdlc-connector-bg: rgba(241, 245, 249, 0.95);
    --sdlc-connector-border: #cbd5e1;

    box-sizing: border-box;
    width: 100%;
    max-width: 100%;
    margin: 2rem 0;
    padding: 1rem;
    background: var(--sdlc-bg);
    border: 1.5px solid var(--sdlc-slate-border);
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 0.875rem;
    line-height: 1.5;
    color: var(--sdlc-text);
    overflow-x: hidden;
  }

  :root[data-theme="dark"] .sdlc-container,
  :root[data-theme$="dark"] .sdlc-container {
    --sdlc-bg: #0f172a;
    --sdlc-text: #f1f5f9;
    --sdlc-text-muted: #94a3b8;
    --sdlc-code-bg: rgba(0, 0, 0, 0.4);
    --sdlc-code-text: #f8fafc;

    --sdlc-slate-border: #64748b;
    --sdlc-slate-bg: rgba(100, 116, 139, 0.15);
    --sdlc-slate-tag-bg: #334155;
    --sdlc-slate-tag-text: #f8fafc;

    --sdlc-blue-border: #3b82f6;
    --sdlc-blue-bg: rgba(59, 130, 246, 0.12);
    --sdlc-blue-tag-bg: #1d4ed8;
    --sdlc-blue-tag-text: #eff6ff;

    --sdlc-purple-border: #8b5cf6;
    --sdlc-purple-bg: rgba(139, 92, 246, 0.12);
    --sdlc-purple-tag-bg: #5b21b6;
    --sdlc-purple-tag-text: #f5f3ff;

    --sdlc-green-border: #10b981;
    --sdlc-green-bg: rgba(16, 185, 129, 0.12);
    --sdlc-green-tag-bg: #065f46;
    --sdlc-green-tag-text: #ecfdf5;

    --sdlc-cyan-border: #06b6d4;
    --sdlc-cyan-bg: rgba(6, 182, 212, 0.12);
    --sdlc-cyan-tag-bg: #0e7490;
    --sdlc-cyan-tag-text: #ecfeff;

    --sdlc-amber-border: #f59e0b;
    --sdlc-amber-bg: rgba(245, 158, 11, 0.12);
    --sdlc-amber-tag-bg: #92400e;
    --sdlc-amber-tag-text: #fef3c7;

    --sdlc-rose-border: #f43f5e;
    --sdlc-rose-bg: rgba(244, 63, 94, 0.12);
    --sdlc-rose-tag-bg: #9f1239;
    --sdlc-rose-tag-text: #ffe4e6;

    --sdlc-connector-bg: rgba(30, 41, 59, 0.9);
    --sdlc-connector-border: #475569;
  }

  @media (prefers-color-scheme: dark) {
    :root[data-theme="auto"] .sdlc-container,
    :root:not([data-theme="light"]):not([data-theme="dark"]) .sdlc-container {
      --sdlc-bg: #0f172a;
      --sdlc-text: #f1f5f9;
      --sdlc-text-muted: #94a3b8;
      --sdlc-code-bg: rgba(0, 0, 0, 0.4);
      --sdlc-code-text: #f8fafc;

      --sdlc-slate-border: #64748b;
      --sdlc-slate-bg: rgba(100, 116, 139, 0.15);
      --sdlc-slate-tag-bg: #334155;
      --sdlc-slate-tag-text: #f8fafc;

      --sdlc-blue-border: #3b82f6;
      --sdlc-blue-bg: rgba(59, 130, 246, 0.12);
      --sdlc-blue-tag-bg: #1d4ed8;
      --sdlc-blue-tag-text: #eff6ff;

      --sdlc-purple-border: #8b5cf6;
      --sdlc-purple-bg: rgba(139, 92, 246, 0.12);
      --sdlc-purple-tag-bg: #5b21b6;
      --sdlc-purple-tag-text: #f5f3ff;

      --sdlc-green-border: #10b981;
      --sdlc-green-bg: rgba(16, 185, 129, 0.12);
      --sdlc-green-tag-bg: #065f46;
      --sdlc-green-tag-text: #ecfdf5;

      --sdlc-cyan-border: #06b6d4;
      --sdlc-cyan-bg: rgba(6, 182, 212, 0.12);
      --sdlc-cyan-tag-bg: #0e7490;
      --sdlc-cyan-tag-text: #ecfeff;

      --sdlc-amber-border: #f59e0b;
      --sdlc-amber-bg: rgba(245, 158, 11, 0.12);
      --sdlc-amber-tag-bg: #92400e;
      --sdlc-amber-tag-text: #fef3c7;

      --sdlc-rose-border: #f43f5e;
      --sdlc-rose-bg: rgba(244, 63, 94, 0.12);
      --sdlc-rose-tag-bg: #9f1239;
      --sdlc-rose-tag-text: #ffe4e6;

      --sdlc-connector-bg: rgba(30, 41, 59, 0.9);
      --sdlc-connector-border: #475569;
    }
  }

  .sdlc-container,
  .sdlc-container * {
    box-sizing: border-box;
  }

  .sdlc-card {
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    background: var(--sdlc-bg);
    border: 1.5px solid var(--sdlc-slate-border);
    transition: border-color 0.2s ease;
    min-width: 0;
  }

  .sdlc-card-slate { border-color: var(--sdlc-slate-border); background: var(--sdlc-slate-bg); }
  .sdlc-card-blue { border-color: var(--sdlc-blue-border); background: var(--sdlc-blue-bg); }
  .sdlc-card-purple { border-color: var(--sdlc-purple-border); background: var(--sdlc-purple-bg); }
  .sdlc-card-green { border-color: var(--sdlc-green-border); background: var(--sdlc-green-bg); }
  .sdlc-card-cyan { border-color: var(--sdlc-cyan-border); background: var(--sdlc-cyan-bg); }
  .sdlc-card-amber { border-color: var(--sdlc-amber-border); background: var(--sdlc-amber-bg); }
  .sdlc-card-rose { border-color: var(--sdlc-rose-border); background: var(--sdlc-rose-bg); }

  .sdlc-card-title-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(100, 116, 139, 0.2);
  }

  .sdlc-title-group {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    min-width: 0;
  }

  .sdlc-title {
    font-weight: 600;
    font-size: 0.9375rem;
    color: var(--sdlc-text);
  }

  .sdlc-tag {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.025em;
    text-transform: uppercase;
    white-space: nowrap;
  }

  .sdlc-tag-slate { background: var(--sdlc-slate-tag-bg); color: var(--sdlc-slate-tag-text); }
  .sdlc-tag-blue { background: var(--sdlc-blue-tag-bg); color: var(--sdlc-blue-tag-text); }
  .sdlc-tag-purple { background: var(--sdlc-purple-tag-bg); color: var(--sdlc-purple-tag-text); }
  .sdlc-tag-green { background: var(--sdlc-green-tag-bg); color: var(--sdlc-green-tag-text); }
  .sdlc-tag-cyan { background: var(--sdlc-cyan-tag-bg); color: var(--sdlc-cyan-tag-text); }
  .sdlc-tag-amber { background: var(--sdlc-amber-tag-bg); color: var(--sdlc-amber-tag-text); }
  .sdlc-tag-rose { background: var(--sdlc-rose-tag-bg); color: var(--sdlc-rose-tag-text); }

  .sdlc-section-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--sdlc-text-muted);
    margin: 0.625rem 0 0.375rem 0;
  }

  .sdlc-grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 0.75rem;
  }

  .sdlc-grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.75rem;
  }

  .sdlc-grid-7 {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.75rem;
  }

  .sdlc-stack-compact {
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
  }

  .sdlc-field {
    border-radius: 6px;
    padding: 0.625rem 0.75rem;
    border: 1px solid rgba(100, 116, 139, 0.25);
    background: var(--sdlc-bg);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0;
  }

  .sdlc-field-slate { border-left: 3.5px solid var(--sdlc-slate-border); }
  .sdlc-field-blue { border-left: 3.5px solid var(--sdlc-blue-border); }
  .sdlc-field-purple { border-left: 3.5px solid var(--sdlc-purple-border); }
  .sdlc-field-green { border-left: 3.5px solid var(--sdlc-green-border); }
  .sdlc-field-cyan { border-left: 3.5px solid var(--sdlc-cyan-border); }
  .sdlc-field-amber { border-left: 3.5px solid var(--sdlc-amber-border); }
  .sdlc-field-rose { border-left: 3.5px solid var(--sdlc-rose-border); }

  .sdlc-field-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--sdlc-text-muted);
    margin-bottom: 0.25rem;
  }

  .sdlc-field-val {
    font-size: 0.8125rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.375rem;
    color: var(--sdlc-text);
  }

  .sdlc-field-val code {
    background: var(--sdlc-code-bg);
    color: var(--sdlc-code-text);
    padding: 0.15rem 0.35rem;
    border-radius: 3px;
    font-size: 0.8125rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    word-break: break-all;
  }

  .sdlc-field-desc {
    font-size: 0.72rem;
    color: var(--sdlc-text-muted);
    line-height: 1.35;
  }

  .sdlc-flow-arrow {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0.5rem 0;
  }

  .sdlc-arrow-line {
    width: 2px;
    height: 14px;
    background: var(--sdlc-slate-border);
  }

  .sdlc-arrow-badge {
    background: var(--sdlc-connector-bg);
    border: 1px solid var(--sdlc-connector-border);
    border-radius: 12px;
    padding: 0.2rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--sdlc-text-muted);
    margin: 2px 0;
    text-align: center;
  }

  .sdlc-arrow-head {
    font-size: 0.75rem;
    color: var(--sdlc-text-muted);
    line-height: 1;
  }

  .sdlc-connector-block {
    background: var(--sdlc-connector-bg);
    border: 1.5px dashed var(--sdlc-connector-border);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    min-width: 0;
  }

  .sdlc-connector-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--sdlc-connector-border);
  }

  .sdlc-connector-title {
    font-weight: 700;
    font-size: 0.8125rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--sdlc-text);
  }

  .sdlc-connector-subtitle {
    font-size: 0.75rem;
    color: var(--sdlc-text-muted);
  }

  .sdlc-connector-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.75rem;
  }

  .sdlc-conn-card {
    display: flex;
    align-items: flex-start;
    gap: 0.625rem;
    padding: 0.625rem;
    border-radius: 6px;
    background: var(--sdlc-bg);
    border: 1px solid rgba(100, 116, 139, 0.2);
    min-width: 0;
  }

  .sdlc-conn-num {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    font-size: 0.72rem;
    font-weight: 700;
    color: #ffffff;
    flex-shrink: 0;
    margin-top: 1px;
  }

  .sdlc-num-slate { background: #475569; }
  .sdlc-num-blue { background: #2563eb; }
  .sdlc-num-purple { background: #7c3aed; }
  .sdlc-num-green { background: #059669; }
  .sdlc-num-cyan { background: var(--sdlc-cyan-tag-bg); }
  .sdlc-num-amber { background: var(--sdlc-amber-tag-bg); }
  .sdlc-num-rose { background: #e11d48; }

  .sdlc-conn-content {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    min-width: 0;
  }

  .sdlc-conn-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--sdlc-text);
  }

  .sdlc-conn-detail {
    font-size: 0.75rem;
    color: var(--sdlc-text);
  }

  .sdlc-conn-detail code {
    background: var(--sdlc-code-bg);
    color: var(--sdlc-code-text);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-size: 0.75rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    word-break: break-all;
  }

  .sdlc-conn-desc {
    font-size: 0.7rem;
    color: var(--sdlc-text-muted);
    line-height: 1.35;
  }

  @media (max-width: 640px) {
    .sdlc-grid-2,
    .sdlc-grid-3,
    .sdlc-grid-7,
    .sdlc-connector-grid {
      grid-template-columns: 1fr;
    }
    .sdlc-card-title-bar {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>

<div class="sdlc-container">
  <div class="sdlc-grid-2">
    <!-- Card 1: Multi-Repository Software Fleet -->
    <div class="sdlc-card sdlc-card-slate">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-slate">Fleet Boundary</span>
          <span class="sdlc-title">Multi-Repository Software Fleet</span>
        </div>
        <span class="sdlc-tag sdlc-tag-slate">Anonymous Consumers</span>
      </div>
      <div class="sdlc-section-label">Fleet Repositories (Independent State Machines)</div>
      <div class="sdlc-stack-compact">
        <div class="sdlc-field sdlc-field-slate">
          <div class="sdlc-field-label">Consumer Repo A</div>
          <div class="sdlc-field-val"><code>gh-report</code></div>
          <div class="sdlc-field-desc">Autonomous agent fleet member exposing read-only verification surface</div>
        </div>
        <div class="sdlc-field sdlc-field-slate">
          <div class="sdlc-field-label">Consumer Repo B</div>
          <div class="sdlc-field-val"><code>internal-service</code></div>
          <div class="sdlc-field-desc">Production domain service implementing 7-phase loop with pinned toolchain</div>
        </div>
        <div class="sdlc-field sdlc-field-slate">
          <div class="sdlc-field-label">Consumer Repo N</div>
          <div class="sdlc-field-val"><code>fleet-member-N</code></div>
          <div class="sdlc-field-desc">Domain-neutral fleet member onboarded onto quality ratchet without bespoke config</div>
        </div>
      </div>
    </div>
    <!-- Card 2: Software Factory SDLC Engine -->
    <div class="sdlc-card sdlc-card-blue">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-blue">Governing Core</span>
          <span class="sdlc-title">Software Factory SDLC Engine</span>
        </div>
        <span class="sdlc-tag sdlc-tag-blue">Normative Standard</span>
      </div>
      <div class="sdlc-section-label">Core Architectural Pillars</div>
      <div class="sdlc-grid-2">
        <div class="sdlc-field sdlc-field-green">
          <div class="sdlc-field-label">Priority Hierarchy</div>
          <div class="sdlc-field-val"><code>5 Tiers</code></div>
          <div class="sdlc-field-desc">Maintainability &gt; Correctness &gt; Response &gt; Energy &gt; Features</div>
        </div>
        <div class="sdlc-field sdlc-field-purple">
          <div class="sdlc-field-label">Lifecycle Loop</div>
          <div class="sdlc-field-val"><code>7 Phases</code></div>
          <div class="sdlc-field-desc">Continuous feedback loop from framing through evolution &amp; retirement</div>
        </div>
        <div class="sdlc-field sdlc-field-amber">
          <div class="sdlc-field-label">The Ratchet Doctrine</div>
          <div class="sdlc-field-val"><code>Monotonic Floor</code></div>
          <div class="sdlc-field-desc">Opt-in incubation elevating to non-negotiable hygiene floors</div>
        </div>
        <div class="sdlc-field sdlc-field-blue">
          <div class="sdlc-field-label">Compiled Tooling</div>
          <div class="sdlc-field-val"><code>Rust (Sub-Second)</code></div>
          <div class="sdlc-field-desc">High-speed checkers, comment-free, adr-fmt, and CI tripwires</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Directional Linkage / Connector Block -->
  <div class="sdlc-connector-block">
    <div class="sdlc-connector-header">
      <span class="sdlc-connector-title">Bidirectional Fleet Coordination &amp; Conformance</span>
      <span class="sdlc-connector-subtitle">Mechanical enforcement decoupled from domain runtime</span>
    </div>
    <div class="sdlc-connector-grid">
      <div class="sdlc-conn-card">
        <div class="sdlc-conn-num sdlc-num-blue">▼</div>
        <div class="sdlc-conn-content">
          <div class="sdlc-conn-label">Mechanical Conformance (Engine → Fleet)</div>
          <div class="sdlc-conn-detail"><code>Read-Only Checks &amp; Exact-Byte Baselines</code></div>
          <div class="sdlc-conn-desc">Checker validates target repositories against normative references without mutating code</div>
        </div>
      </div>
      <div class="sdlc-conn-card">
        <div class="sdlc-conn-num sdlc-num-cyan">▲</div>
        <div class="sdlc-conn-content">
          <div class="sdlc-conn-label">Situation Evidence (Fleet → Engine)</div>
          <div class="sdlc-conn-detail"><code>Streaming Telemetry (TSV/JSONL) &amp; Tri-State Exits</code></div>
          <div class="sdlc-conn-desc">Unfiltered exit codes (0/1/2) and machine records stream to orchestrators for ratchet evaluation</div>
        </div>
      </div>
    </div>
  </div>
</div>

---

## The Strategic Problem: Fleet Governance vs. Compliance Theatre

Traditional software development lifecycles (SDLCs) fail across multi-repository organizations for three distinct structural reasons:

1. **Epistemic Divergence & Architectural Drift**: As repositories proliferate, individual teams make localized compromises. Toolchains diverge, error handling conventions drift, linter configurations soften, and security invariants erode. Without continuous verification against a shared standard, the fleet fragments into incompatible architectural dialects.
2. **Compliance Theatre**: When organizational standards are defined as narrative policies rather than compiled rules, compliance becomes performative. Engineers write speculative unit tests to hit arbitrary coverage targets, approve pull requests based on familiarity, and maintain documentation that bears no verifiable relationship to the code running in production.
3. **The Fragility of Blanket Enforcement**: When leadership attempts to enforce a new quality standard uniformly across dozens of active repositories, the initiative typically collapses under the weight of broken builds and delivery friction. A top-down mandate either breaks non-compliant services immediately or gets diluted with blanket exemptions that permanently compromise the standard.

`sf-sdlc` replaces narrative policy with compiled, deterministic conformance. Repositories are treated as verifiable state machines governed by exact-byte baselines and monotonic quality gates.

---

## The Strict Priority Hierarchy

When architectural options, resource constraints, or review criteria conflict, `sf-sdlc` mandates an unambiguous, five-tier decision hierarchy. Every engineering decision—from type design to runtime telemetry—resolves strictly in this order:

Maintainability > Correctness by design > Response times > Energy efficiency in code > Features

<div class="sdlc-container">
  <!-- Tier 1: Maintainability -->
  <div class="sdlc-card sdlc-card-green">
    <div class="sdlc-card-title-bar">
      <div class="sdlc-title-group">
        <span class="sdlc-tag sdlc-tag-green">Priority 1</span>
        <span class="sdlc-title">Maintainability · Pure Trunk &amp; Low Cognitive Overhead</span>
      </div>
      <span class="sdlc-tag sdlc-tag-green">Dominant Priority</span>
    </div>
    <div class="sdlc-grid-2">
      <div class="sdlc-field sdlc-field-green">
        <div class="sdlc-field-label">Integration Cadence</div>
        <div class="sdlc-field-val"><code>Pure Trunk Integration</code></div>
        <div class="sdlc-field-desc">Small, reversible, deployable increments committed directly to trunk. No long-lived feature branches.</div>
      </div>
      <div class="sdlc-field sdlc-field-green">
        <div class="sdlc-field-label">Architectural Rule</div>
        <div class="sdlc-field-val"><code>Simplicity &gt; Speculative Abstraction</code></div>
        <div class="sdlc-field-desc">Low cognitive overhead dominates clever local optimizations or speculative generalization.</div>
      </div>
    </div>
  </div>

  <!-- Flow Arrow -->
  <div class="sdlc-flow-arrow">
    <div class="sdlc-arrow-line"></div>
    <div class="sdlc-arrow-badge">Dominates Priority 2</div>
    <div class="sdlc-arrow-head">▼</div>
  </div>

  <!-- Tier 2: Correctness by Design -->
  <div class="sdlc-card sdlc-card-blue">
    <div class="sdlc-card-title-bar">
      <div class="sdlc-title-group">
        <span class="sdlc-tag sdlc-tag-blue">Priority 2</span>
        <span class="sdlc-title">Correctness by Design · Make Illegal States Unrepresentable</span>
      </div>
      <span class="sdlc-tag sdlc-tag-blue">Structural Verification</span>
    </div>
    <div class="sdlc-grid-2">
      <div class="sdlc-field sdlc-field-blue">
        <div class="sdlc-field-label">Type-Driven Modeling</div>
        <div class="sdlc-field-val"><code>Algebraic Data Types &amp; State Machines</code></div>
        <div class="sdlc-field-desc">Closed enums and private invariant constructors eliminate split-brain and invalid states at compile time.</div>
      </div>
      <div class="sdlc-field sdlc-field-blue">
        <div class="sdlc-field-label">Validation Boundary</div>
        <div class="sdlc-field-val"><code>Parse at Boundary, Trust Inward</code></div>
        <div class="sdlc-field-desc">Validation occurs once at untrusted input boundaries; internal domain code trusts valid types unconditionally.</div>
      </div>
    </div>
  </div>

  <!-- Flow Arrow -->
  <div class="sdlc-flow-arrow">
    <div class="sdlc-arrow-line"></div>
    <div class="sdlc-arrow-badge">Dominates Priority 3</div>
    <div class="sdlc-arrow-head">▼</div>
  </div>

  <!-- Tier 3: Response Times -->
  <div class="sdlc-card sdlc-card-cyan">
    <div class="sdlc-card-title-bar">
      <div class="sdlc-title-group">
        <span class="sdlc-tag sdlc-tag-cyan">Priority 3</span>
        <span class="sdlc-title">Response Times · Optimized Read Paths &amp; Prompt EDA</span>
      </div>
      <span class="sdlc-tag sdlc-tag-cyan">Latency Sensitive</span>
    </div>
    <div class="sdlc-grid-2">
      <div class="sdlc-field sdlc-field-cyan">
        <div class="sdlc-field-label">Read Optimization</div>
        <div class="sdlc-field-val"><code>Read Path Dominance</code></div>
        <div class="sdlc-field-desc">Read access paths are optimized first to minimize system latency and maximize user utility.</div>
      </div>
      <div class="sdlc-field sdlc-field-cyan">
        <div class="sdlc-field-label">Fact Propagation</div>
        <div class="sdlc-field-val"><code>Event-Driven Architecture (EDA)</code></div>
        <div class="sdlc-field-desc">Events propagate promptly across context boundaries via Event Carried State Transfer (ECST).</div>
      </div>
    </div>
  </div>

  <!-- Flow Arrow -->
  <div class="sdlc-flow-arrow">
    <div class="sdlc-arrow-line"></div>
    <div class="sdlc-arrow-badge">Dominates Priority 4</div>
    <div class="sdlc-arrow-head">▼</div>
  </div>

  <!-- Tier 4: Energy Efficiency in Code -->
  <div class="sdlc-card sdlc-card-amber">
    <div class="sdlc-card-title-bar">
      <div class="sdlc-title-group">
        <span class="sdlc-tag sdlc-tag-amber">Priority 4</span>
        <span class="sdlc-title">Energy Efficiency in Code · Bounded Resource Burn</span>
      </div>
      <span class="sdlc-tag sdlc-tag-amber">Resource Stewardship</span>
    </div>
    <div class="sdlc-grid-2">
      <div class="sdlc-field sdlc-field-amber">
        <div class="sdlc-field-label">Hardware Conservation</div>
        <div class="sdlc-field-val"><code>Zero Hot Loops &amp; Polling Burn</code></div>
        <div class="sdlc-field-desc">Eliminate redundant polling, unmetered heap allocations, and idle CPU/network utilization.</div>
      </div>
      <div class="sdlc-field sdlc-field-amber">
        <div class="sdlc-field-label">Resource Contracts</div>
        <div class="sdlc-field-val"><code>Explicit Unit &amp; Memory Budgets</code></div>
        <div class="sdlc-field-desc">Enforce bounded queues, concurrency limits, and RAII resource release on error and cancellation.</div>
      </div>
    </div>
  </div>

  <!-- Flow Arrow -->
  <div class="sdlc-flow-arrow">
    <div class="sdlc-arrow-line"></div>
    <div class="sdlc-arrow-badge">Dominates Priority 5</div>
    <div class="sdlc-arrow-head">▼</div>
  </div>

  <!-- Tier 5: Features -->
  <div class="sdlc-card sdlc-card-slate">
    <div class="sdlc-card-title-bar">
      <div class="sdlc-title-group">
        <span class="sdlc-tag sdlc-tag-slate">Priority 5</span>
        <span class="sdlc-title">Features · Subordinate to All Higher Tiers</span>
      </div>
      <span class="sdlc-tag sdlc-tag-slate">Subordinate</span>
    </div>
    <div class="sdlc-grid-2">
      <div class="sdlc-field sdlc-field-slate">
        <div class="sdlc-field-label">Scope Discipline</div>
        <div class="sdlc-field-val"><code>Justified by Explicit Requirement</code></div>
        <div class="sdlc-field-desc">New capabilities rank lowest. Never justified if they degrade maintainability or type safety.</div>
      </div>
      <div class="sdlc-field sdlc-field-slate">
        <div class="sdlc-field-label">Arbitration Rule</div>
        <div class="sdlc-field-val"><code>Zero Compromise on Higher Tiers</code></div>
        <div class="sdlc-field-desc">Features may not introduce illegal states, violate latency budgets, or leak unmetered memory.</div>
      </div>
    </div>
  </div>
</div>

### Rationale & Trade-off Arbitration

1. **Maintainability (Priority 1)**: Software spend is dominated by long-term maintenance and comprehension costs. `sf-sdlc` mandates pure trunk-based development: work integrates directly onto trunk in small, reversible, independently deployable increments without long-lived feature branches. Simplicity, readability, and low cognitive overhead strictly dominate speculative abstractions or clever local optimizations.
2. **Correctness by design (Priority 2)**: Defensive runtime assertions and scattered conditional checks indicate architectural failure. Correctness must be guaranteed at the type level. Systems must use algebraic data types, closed enumerations, explicit state machines, and private invariant constructors to make illegal domain states structurally unrepresentable. Validation occurs strictly at untrusted input boundaries; once admitted, domain data is trusted unconditionally.
3. **Response times (Priority 3)**: In modern distributed architectures, read latency dominates system utility and user experience. Systems must optimize read-side access paths first. State changes propagate promptly across bounded contexts via Event-Driven Architecture (EDA) and Event Carried State Transfer (ECST), decoupling write ingestion from read queries.
4. **Energy efficiency in code (Priority 4)**: Hardware burn and cloud compute footprint are direct consequences of software design. Code must eliminate redundant polling, idle CPU spinning, unmetered serialization cycles, and unbounded heap allocations. Systems respect explicit resource contracts (bounding concurrent tasks, queue capacity, and heap buffers).
5. **Features (Priority 5)**: New functionality, speculative hooks, and optional configuration parameters rank lowest. A feature is never justified if it degrades maintainability, introduces invalid states into the domain model, degrades read latency, or leaks memory.

---

## The 7-Phase SDLC Control Loop

`sf-sdlc` structures software development into seven continuous, feedback-coupled phases. Each phase defines concrete inputs, verification responsibilities, and unambiguous transition gates:

<div class="sdlc-container">
  <!-- 7-Phase Lifecycle Grid -->
  <div class="sdlc-section-label">7-Stage Continuous Pipeline</div>
  <div class="sdlc-grid-7">
    <!-- Phase 1: Framing -->
    <div class="sdlc-card sdlc-card-slate">
      <div class="sdlc-card-title-bar">
        <span class="sdlc-tag sdlc-tag-slate">Phase 1</span>
        <span class="sdlc-title">Framing</span>
      </div>
      <div class="sdlc-field sdlc-field-slate">
        <div class="sdlc-field-label">Intent &amp; Invariants</div>
        <div class="sdlc-field-val"><code>Operational Bounds</code></div>
        <div class="sdlc-field-desc">Establish intent, boundary constraints, and non-negotiables before touching code.</div>
      </div>
    </div>
    <!-- Phase 2: Design & Planning -->
    <div class="sdlc-card sdlc-card-purple">
      <div class="sdlc-card-title-bar">
        <span class="sdlc-tag sdlc-tag-purple">Phase 2</span>
        <span class="sdlc-title">Design &amp; Planning</span>
      </div>
      <div class="sdlc-field sdlc-field-purple">
        <div class="sdlc-field-label">ADRs &amp; Contracts</div>
        <div class="sdlc-field-val"><code>State Machines</code></div>
        <div class="sdlc-field-desc">Formalize domain interfaces, explicit state transitions, and immutable ADRs via adr-fmt.</div>
      </div>
    </div>
    <!-- Phase 3: Building -->
    <div class="sdlc-card sdlc-card-blue">
      <div class="sdlc-card-title-bar">
        <span class="sdlc-tag sdlc-tag-blue">Phase 3</span>
        <span class="sdlc-title">Building</span>
      </div>
      <div class="sdlc-field sdlc-field-blue">
        <div class="sdlc-field-label">Kent Beck TDD</div>
        <div class="sdlc-field-val"><code>Clean Trunk</code></div>
        <div class="sdlc-field-desc">Execute red-green-refactor cycles; one axis of advance (Tidy First) committed to trunk.</div>
      </div>
    </div>
    <!-- Phase 4: Verification -->
    <div class="sdlc-card sdlc-card-green">
      <div class="sdlc-card-title-bar">
        <span class="sdlc-tag sdlc-tag-green">Phase 4</span>
        <span class="sdlc-title">Verification</span>
      </div>
      <div class="sdlc-field sdlc-field-green">
        <div class="sdlc-field-label">Three-Tier Cadence</div>
        <div class="sdlc-field-val"><code>Inner · Mid · Boundary</code></div>
        <div class="sdlc-field-desc">Inner (&lt;5s), Mid (reverse closure), and Boundary (workspace &amp; timeouts) verification.</div>
      </div>
    </div>
    <!-- Phase 5: Release -->
    <div class="sdlc-card sdlc-card-blue">
      <div class="sdlc-card-title-bar">
        <span class="sdlc-tag sdlc-tag-blue">Phase 5</span>
        <span class="sdlc-title">Release</span>
      </div>
      <div class="sdlc-field sdlc-field-blue">
        <div class="sdlc-field-label">Deterministic Binaries</div>
        <div class="sdlc-field-val"><code>Supply Chain</code></div>
        <div class="sdlc-field-desc">Reproducible, signed binaries verified with cargo-deny and cargo-audit provenance.</div>
      </div>
    </div>
    <!-- Phase 6: Operation & Learning -->
    <div class="sdlc-card sdlc-card-cyan">
      <div class="sdlc-card-title-bar">
        <span class="sdlc-tag sdlc-tag-cyan">Phase 6</span>
        <span class="sdlc-title">Operation &amp; Learning</span>
      </div>
      <div class="sdlc-field sdlc-field-cyan">
        <div class="sdlc-field-label">Runtime Telemetry</div>
        <div class="sdlc-field-val"><code>Latency &amp; Failure</code></div>
        <div class="sdlc-field-desc">Monitor real-world latency distributions and error telemetry feeding back to design.</div>
      </div>
    </div>
    <!-- Phase 7: Evolution & Retirement -->
    <div class="sdlc-card sdlc-card-amber">
      <div class="sdlc-card-title-bar">
        <span class="sdlc-tag sdlc-tag-amber">Phase 7</span>
        <span class="sdlc-title">Evolution &amp; Sunset</span>
      </div>
      <div class="sdlc-field sdlc-field-amber">
        <div class="sdlc-field-label">Lifecycle Completion</div>
        <div class="sdlc-field-val"><code>Schema Migrations</code></div>
        <div class="sdlc-field-desc">Auditable schema migrations, explicit component deprecation, and clean decommissioning.</div>
      </div>
    </div>
  </div>

  <!-- Dedicated Feedback Routing Card -->
  <div class="sdlc-connector-block">
    <div class="sdlc-connector-header">
      <span class="sdlc-connector-title">Closed-Loop Feedback Routing</span>
      <span class="sdlc-connector-subtitle">Mechanisms routing defects and runtime telemetry back to upstream phases</span>
    </div>
    <div class="sdlc-connector-grid">
      <div class="sdlc-conn-card">
        <div class="sdlc-conn-num sdlc-num-rose">1</div>
        <div class="sdlc-conn-content">
          <div class="sdlc-conn-label">Defect Detected · Phase 4 → Phase 3</div>
          <div class="sdlc-conn-detail"><code>Verification → Building</code></div>
          <div class="sdlc-conn-desc">TDD assertion or clippy gate failure halts progression; execution immediately re-enters red-green cycle.</div>
        </div>
      </div>
      <div class="sdlc-conn-card">
        <div class="sdlc-conn-num sdlc-num-purple">2</div>
        <div class="sdlc-conn-content">
          <div class="sdlc-conn-label">Design Flaw · Phase 4 → Phase 2</div>
          <div class="sdlc-conn-detail"><code>Verification → Design &amp; Planning</code></div>
          <div class="sdlc-conn-desc">Boundary verification surfaces unrepresentable state or resource contract gap; forces ADR revision.</div>
        </div>
      </div>
      <div class="sdlc-conn-card">
        <div class="sdlc-conn-num sdlc-num-slate">3</div>
        <div class="sdlc-conn-content">
          <div class="sdlc-conn-label">Strategic Shift · Phase 6 → Phase 1</div>
          <div class="sdlc-conn-detail"><code>Operation &amp; Learning → Framing</code></div>
          <div class="sdlc-conn-desc">Operational reality or market shift invalidates prior assumptions, re-framing fundamental intent.</div>
        </div>
      </div>
      <div class="sdlc-conn-card">
        <div class="sdlc-conn-num sdlc-num-cyan">4</div>
        <div class="sdlc-conn-content">
          <div class="sdlc-conn-label">Bottleneck Evidence · Phase 6 → Phase 2</div>
          <div class="sdlc-conn-detail"><code>Operation &amp; Learning → Design &amp; Planning</code></div>
          <div class="sdlc-conn-desc">Telemetry exposes latency spikes or queue saturation; triggers state machine and capacity redesign.</div>
        </div>
      </div>
      <div class="sdlc-conn-card">
        <div class="sdlc-conn-num sdlc-num-amber">5</div>
        <div class="sdlc-conn-content">
          <div class="sdlc-conn-label">Legacy Sunset · Phase 7 → Phase 1</div>
          <div class="sdlc-conn-detail"><code>Evolution &amp; Retirement → Framing</code></div>
          <div class="sdlc-conn-desc">Decommissioning legacy services reclaims fleet resource budget and simplifies system boundaries.</div>
        </div>
      </div>
    </div>
  </div>
</div>

1. **Framing**: Establish the fundamental intent, operational boundaries, and system invariant definitions before touching code. Distinguishes hard constraints from speculative requirements.
2. **Design & Planning**: Formalize domain interfaces, explicit state machine transitions, and resource contracts. Strategic decisions are committed to immutable Architectural Decision Records (ADRs) via `adr-fmt`.
3. **Building**: Execute implementation through strict Kent Beck test-driven development (TDD: red → green → refactor). Enforces "one axis of advance" (Tidy First): structural changes and behavioral changes never land in the same commit.
4. **Verification**: Enforce a rigid three-tier verification cadence:
   - **INNER**: Local crate-level tests and clippy checks for rapid TDD loops (< 5s).
   - **MID**: Reverse-dependent closure verification executed prior to sub-mission completion.
   - **BOUNDARY**: Full workspace compilation, all-features test suites under strict timeouts, linting, and formatting executed before epic merge.
5. **Release**: Produce reproducible, cryptographically signed artifacts with full supply-chain provenance (`cargo deny`, `cargo audit`).
6. **Operation & Learning**: Monitor real-world runtime metrics, latency profiles, and failure distributions. Telemetry feeds directly back into framing and design.
7. **Evolution & Retirement**: Manage schema evolution via auditable data migrations, explicit component deprecation, and clean data purging.

---

## The Ratchet Doctrine: Monotonic Quality Floor Elevation

Elevating quality across a multi-repository organization without stalling delivery requires a non-breaking, unidirectional mechanism. `sf-sdlc` achieves this through **The Ratchet Doctrine**.

<div class="sdlc-container">
  <div class="sdlc-grid-3">
    <!-- Phase 1: Incubation -->
    <div class="sdlc-card sdlc-card-amber">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-amber">Phase 1</span>
          <span class="sdlc-title">Opt-In Introduction</span>
        </div>
        <span class="sdlc-tag sdlc-tag-amber">Incubation</span>
      </div>
      <div class="sdlc-section-label">Non-Breaking Control Entry</div>
      <div class="sdlc-stack-compact">
        <div class="sdlc-field sdlc-field-slate">
          <div class="sdlc-field-label">Initiation</div>
          <div class="sdlc-field-val"><code>New Control Developed</code></div>
          <div class="sdlc-field-desc">Forward-looking, high-assurance rule designed (e.g. comment-free AST checks).</div>
        </div>
        <div class="sdlc-flow-arrow">
          <div class="sdlc-arrow-line"></div>
          <div class="sdlc-arrow-head">▼</div>
        </div>
        <div class="sdlc-field sdlc-field-amber">
          <div class="sdlc-field-label">Tier Designation</div>
          <div class="sdlc-field-val"><code>ControlTier::OptIn</code></div>
          <div class="sdlc-field-desc">Control enters as optional check; zero build failures imposed across active repositories.</div>
        </div>
      </div>
    </div>
    <!-- Phase 2: Deliberate Adoption -->
    <div class="sdlc-card sdlc-card-blue">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-blue">Phase 2</span>
          <span class="sdlc-title">Deliberate Fleet Adoption</span>
        </div>
        <span class="sdlc-tag sdlc-tag-blue">Fleet Uptake</span>
      </div>
      <div class="sdlc-section-label">Progressive Autonomous Adoption</div>
      <div class="sdlc-stack-compact">
        <div class="sdlc-field sdlc-field-slate">
          <div class="sdlc-field-label">Pioneer Adoption</div>
          <div class="sdlc-field-val"><code>Repo Alpha Opts In</code></div>
          <div class="sdlc-field-desc">Alpha repository configures check, resolves defects, and verifies stability.</div>
        </div>
        <div class="sdlc-field sdlc-field-slate">
          <div class="sdlc-field-label">Fleet Diffusion</div>
          <div class="sdlc-field-val"><code>Repo Beta Opts In</code></div>
          <div class="sdlc-field-desc">Broader fleet opts in during planned refactor cycles without deadline friction.</div>
        </div>
        <div class="sdlc-field sdlc-field-blue">
          <div class="sdlc-field-label">Fleet Convergence</div>
          <div class="sdlc-field-val"><code>Repo N Compliance</code></div>
          <div class="sdlc-field-desc">Final repositories achieve compliance; readiness monitored mechanically via telemetry.</div>
        </div>
      </div>
    </div>
    <!-- Phase 3: Ratchet Advancement -->
    <div class="sdlc-card sdlc-card-green">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-green">Phase 3</span>
          <span class="sdlc-title">Ratchet Advancement</span>
        </div>
        <span class="sdlc-tag sdlc-tag-green">Monotonic Floor</span>
      </div>
      <div class="sdlc-section-label">Permanent Elevation to Floor</div>
      <div class="sdlc-stack-compact">
        <div class="sdlc-field sdlc-field-green">
          <div class="sdlc-field-label">Precondition</div>
          <div class="sdlc-field-val"><code>100% Fleet Compliance</code></div>
          <div class="sdlc-field-desc">Every repository in the classification verified green on the opted-in control.</div>
        </div>
        <div class="sdlc-flow-arrow">
          <div class="sdlc-arrow-line"></div>
          <div class="sdlc-arrow-head">▼</div>
        </div>
        <div class="sdlc-field sdlc-field-blue">
          <div class="sdlc-field-label">Ratchet Promotion</div>
          <div class="sdlc-field-val"><code>Promote to ControlTier::Hygiene</code></div>
          <div class="sdlc-field-desc">The quality ratchet clicks forward; violation now immediately fails the build.</div>
        </div>
        <div class="sdlc-flow-arrow">
          <div class="sdlc-arrow-line"></div>
          <div class="sdlc-arrow-head">▼</div>
        </div>
        <div class="sdlc-field sdlc-field-green">
          <div class="sdlc-field-label">New Invariant</div>
          <div class="sdlc-field-val"><code>New Mandatory Quality Floor</code></div>
          <div class="sdlc-field-desc">Standard becomes immutable floor across all current and future repositories.</div>
        </div>
      </div>
    </div>
  </div>
</div>

The Ratchet operates via a two-tier control architecture:

1. **Hygiene Tier (`ControlTier::Hygiene`)**: The mandatory baseline enforced across all repositories in a target classification. Failure to satisfy a hygiene control fails the build immediately. Examples include pinned toolchains, zero compiler warnings (`-D warnings`), closed error enumerations, AST comment hygiene, and supply-chain vulnerability absence.
2. **Opt-In Tier (`ControlTier::OptIn`)**: Forward-looking, high-assurance controls introduced as optional checks. Repositories adopt them deliberately via `opt_in_controls` in their configuration when capacity permits.
3. **Advancement**: A control never enters the hygiene tier directly. It must incubate in `OptIn`. As individual repositories opt in and achieve compliance, the adoption rate is monitored. Once 100% of repositories in a class comply, the control is promoted to `Hygiene`. The ratchet clicks forward: the quality floor rises monotonically, and backsliding becomes structurally impossible.

---

## Delivered Rust Read-Only Conformance Checker

To prevent verification tooling from becoming a source of state corruption, the delivered `sf-sdlc` CLI is engineered as an ultra-fast, read-only conformance engine written in Rust (channel 1.98.0, edition 2024).

<div class="sdlc-container">
  <div class="sdlc-grid-3">
    <!-- Column 1: Inputs & Declarations -->
    <div class="sdlc-card sdlc-card-slate">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-slate">Column 1</span>
          <span class="sdlc-title">Inputs &amp; Declarations</span>
        </div>
        <span class="sdlc-tag sdlc-tag-slate">Inert State</span>
      </div>
      <div class="sdlc-section-label">Declared Baselines &amp; Codebases</div>
      <div class="sdlc-stack-compact">
        <div class="sdlc-field sdlc-field-slate">
          <div class="sdlc-field-label">Repository Configuration</div>
          <div class="sdlc-field-val"><code>sf-sdlc.toml</code></div>
          <div class="sdlc-field-desc">Declares target profile, opted-in controls, and local overrides.</div>
        </div>
        <div class="sdlc-field sdlc-field-slate">
          <div class="sdlc-field-label">Inert Reference Baselines</div>
          <div class="sdlc-field-val"><code>references/&lt;target&gt;/&lt;file&gt;.ref</code></div>
          <div class="sdlc-field-desc">Canonical exact-byte reference files storing normative standards.</div>
        </div>
        <div class="sdlc-field sdlc-field-slate">
          <div class="sdlc-field-label">Target Worktrees</div>
          <div class="sdlc-field-val"><code>Target Repository Trees</code></div>
          <div class="sdlc-field-desc">Target source trees evaluated in-place without write access.</div>
        </div>
      </div>
    </div>
    <!-- Column 2: Conformance Engine -->
    <div class="sdlc-card sdlc-card-blue">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-blue">Column 2</span>
          <span class="sdlc-title">Conformance Engine</span>
        </div>
        <span class="sdlc-tag sdlc-tag-blue">Read-Only Core</span>
      </div>
      <div class="sdlc-section-label">Rust Execution Pipeline (Sub-Second)</div>
      <div class="sdlc-stack-compact">
        <div class="sdlc-field sdlc-field-blue">
          <div class="sdlc-field-label">Config &amp; Profile Parser</div>
          <div class="sdlc-field-val"><code>Strict Schema Validation</code></div>
          <div class="sdlc-field-desc">Validates repository manifest and active quality tier rules.</div>
        </div>
        <div class="sdlc-field sdlc-field-blue">
          <div class="sdlc-field-label">Diff &amp; Baseline Engine</div>
          <div class="sdlc-field-val"><code>Exact-Byte &amp; Structural Diff</code></div>
          <div class="sdlc-field-desc">Deterministic comparison against canonical references.</div>
        </div>
        <div class="sdlc-field sdlc-field-green">
          <div class="sdlc-field-label">Rule Evaluators</div>
          <div class="sdlc-field-val"><code>Hygiene &amp; Opt-In Audit</code></div>
          <div class="sdlc-field-desc">Evaluates AST comment hygiene, toolchain pins, and tripwires.</div>
        </div>
      </div>
    </div>
    <!-- Column 3: Neutral Situation Evidence -->
    <div class="sdlc-card sdlc-card-cyan">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-cyan">Column 3</span>
          <span class="sdlc-title">Neutral Situation Evidence</span>
        </div>
        <span class="sdlc-tag sdlc-tag-cyan">Stream Separation</span>
      </div>
      <div class="sdlc-section-label">Stream-Separated Telemetry &amp; Exits</div>
      <div class="sdlc-stack-compact">
        <div class="sdlc-field sdlc-field-cyan">
          <div class="sdlc-field-label">stdout Stream</div>
          <div class="sdlc-field-val"><code>Streaming Machine Records</code></div>
          <div class="sdlc-field-desc">Unfiltered TSV / JSONL records for agent and orchestrator consumption.</div>
        </div>
        <div class="sdlc-field sdlc-field-amber">
          <div class="sdlc-field-label">stderr Stream</div>
          <div class="sdlc-field-val"><code>Diagnostic Traces &amp; Logs</code></div>
          <div class="sdlc-field-desc">Human-readable operational traces, warnings, and contextual diagnostics.</div>
        </div>
        <div class="sdlc-field sdlc-field-green">
          <div class="sdlc-field-label">Tri-State Exit Code</div>
          <div class="sdlc-field-val"><code>0 (Pass) | 1 (Defect) | 2 (Indet)</code></div>
          <div class="sdlc-field-desc">Explicit exit taxonomy; error is never folded into a negative finding.</div>
        </div>
      </div>
    </div>
  </div>
</div>

### Architectural Guarantees

- **Zero Destructive Mutation**: The checker is strictly read-only. It performs zero in-place file modifications, automated rewrites, or unprompted file synchronization. Write operations require explicit operator authorization and dedicated tooling.
- **Inert Reference Baselines**: Normative reference files (such as operational instructions or configuration templates) are stored within `sf-sdlc` under `references/<target>/<file>.ref`. The checker evaluates exact-byte equivalence between the target repository's files and the canonical reference.
- **Tri-State Exit Taxonomy**: Following fleet doctrine, the tool never folds errors or missing permissions into negative findings:
  - `0`: All assertions passed; target is fully conformant.
  - `1`: Domain defect detected; target violates a hygiene or opted-in control.
  - `2`: Indeterminate or environmental failure (missing files, invalid syntax, I/O error).
- **Stream Separation**: Structured, parseable machine-readable records stream exclusively to `stdout`. Human-readable diagnostic traces, progress indications, and error context route strictly to `stderr`.

---

## The Software Factory Tooling Ecosystem

`sf-sdlc` acts as the orchestrator for a suite of specialized, compiled Rust binaries and structural tools designed to execute in milliseconds:

<div class="sdlc-container">
  <!-- Top Orchestrator Card -->
  <div class="sdlc-card sdlc-card-blue">
    <div class="sdlc-card-title-bar">
      <div class="sdlc-title-group">
        <span class="sdlc-tag sdlc-tag-blue">Central Orchestrator</span>
        <span class="sdlc-title">sf-sdlc Linter &amp; Orchestrator</span>
      </div>
      <span class="sdlc-tag sdlc-tag-blue">Sub-Second Execution</span>
    </div>
    <div class="sdlc-field sdlc-field-blue">
      <div class="sdlc-field-label">Orchestration &amp; Conformance Scope</div>
      <div class="sdlc-field-val"><code>Mechanical Conformance &amp; Quality Ratchet</code></div>
      <div class="sdlc-field-desc">Central orchestrator invoking specialized Rust tooling, verifying exact-byte baselines, and streaming neutral situation evidence across the fleet.</div>
    </div>
  </div>

  <!-- Flow Connector -->
  <div class="sdlc-flow-arrow">
    <div class="sdlc-arrow-line"></div>
    <div class="sdlc-arrow-badge">Dispatches &amp; Integrates Substrates</div>
    <div class="sdlc-arrow-head">▼</div>
  </div>

  <div class="sdlc-grid-2">
    <!-- Pillar 1: Compiled Rust Tooling -->
    <div class="sdlc-card sdlc-card-slate">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-slate">Pillar 1</span>
          <span class="sdlc-title">Compiled Rust Tooling</span>
        </div>
        <span class="sdlc-tag sdlc-tag-slate">AST &amp; Types</span>
      </div>
      <div class="sdlc-section-label">High-Speed Specialized Binaries</div>
      <div class="sdlc-stack-compact">
        <div class="sdlc-field sdlc-field-green">
          <div class="sdlc-field-label">comment-free</div>
          <div class="sdlc-field-val"><code>AST Comment Hygiene &amp; Word Budgets</code></div>
          <div class="sdlc-field-desc">Strips plain non-doc comments (//, /* */); gates doc comments (///) behind 80/120 word limits.</div>
        </div>
        <div class="sdlc-field sdlc-field-purple">
          <div class="sdlc-field-label">adr-fmt</div>
          <div class="sdlc-field-val"><code>ADR Structure, Validation &amp; Citations</code></div>
          <div class="sdlc-field-desc">Validates ADR schema, accepted status, bidirectional markdown links, and code citation traces.</div>
        </div>
        <div class="sdlc-field sdlc-field-rose">
          <div class="sdlc-field-label">tripwires / non-exhaustive-check</div>
          <div class="sdlc-field-val"><code>Closed Error Enums Enforcement</code></div>
          <div class="sdlc-field-desc">CI tripwire blocking #[non_exhaustive] on public error enums to preserve domain error completeness.</div>
        </div>
      </div>
    </div>
    <!-- Pillar 2: Graph & Issue Substrates -->
    <div class="sdlc-card sdlc-card-slate">
      <div class="sdlc-card-title-bar">
        <div class="sdlc-title-group">
          <span class="sdlc-tag sdlc-tag-slate">Pillar 2</span>
          <span class="sdlc-title">Graph &amp; Issue Substrates</span>
        </div>
        <span class="sdlc-tag sdlc-tag-slate">Coordination</span>
      </div>
      <div class="sdlc-section-label">Structural Intelligence &amp; Task Memory</div>
      <div class="sdlc-stack-compact">
        <div class="sdlc-field sdlc-field-purple">
          <div class="sdlc-field-label">graphify</div>
          <div class="sdlc-field-val"><code>AST Knowledge Graph Engine</code></div>
          <div class="sdlc-field-desc">Extracts syntax trees, call graphs, and module dependencies into queryable graphify-out/graph.json.</div>
        </div>
        <div class="sdlc-field sdlc-field-blue">
          <div class="sdlc-field-label">beads / Dolt</div>
          <div class="sdlc-field-val"><code>Git-Backed Distributed Issue Tracking</code></div>
          <div class="sdlc-field-desc">Local-first issue tracking (bd) retaining tasks, dependency graphs, and audit trails without SaaS.</div>
        </div>
      </div>
    </div>
  </div>
</div>

- **`comment-free`**: A compiled AST-level Rust analyzer. It enforces the fleet's strict "zero plain comments" policy by stripping non-doc comments (`//` and `/* */`) from source code. It additionally acts as a quality gate on public doc comments (`///`), enforcing concise prose budgets (80-word advisory threshold, 120-word hard ceiling) so documentation remains focused contracts rather than wandering prose.
- **`adr-fmt`**: An architectural linter that parses, validates, and cross-references Architectural Decision Records. It guarantees valid metadata, enforces accepted statuses, checks bidirectional markdown links, and traces citations from code back to architectural decisions.
- **`tripwires` (`non-exhaustive-check`)**: A CI gate enforcing the fleet's closed error enum invariant. It mechanically scans public error enums to ensure they do not carry `#[non_exhaustive]`, ensuring that unhandled domain errors remain impossible to construct across semver lines.
- **`graphify`**: A structural knowledge graph engine that extracts syntax trees, call graphs, and module dependencies into a queryable graph (`graphify-out/graph.json`), enabling instant blast-radius calculation prior to refactoring.
- **`beads` (with embedded Dolt)**: Distributed, git-backed issue tracking (`bd`). Retains durable project task tracking, dependency trees, and audit logs locally without external SaaS dependencies.

---

## Fleet Boundary & Consumer Anonymity

A foundational design principle of `sf-sdlc` is **fleet boundary encapsulation**. 

Consumer applications—such as `gh-report` or internal services—are strictly **anonymous members** of the fleet. They consume the standards, run the read-only checker, and implement the lifecycle phases, but their domain-specific requirements never leak back into the definition of `sf-sdlc`. 

`sf-sdlc` remains an unpolluted, domain-neutral governing body. By maintaining this clean separation, the lifecycle rules remain universal, ensuring that any new repository added to the fleet can be immediately onboarded onto the quality ratchet.
