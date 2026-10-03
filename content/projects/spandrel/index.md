---
title: "Spandrel: Modular DDD/CQRS/EDA Substrate"
description: "Unbundled application-side domain traits, projection fold pipelines, and resource-bounded serving"
weight: 30
draft: true
homeFeatured: true
homePrefix: "TODO:"
---

> **Status Notice: Specification & Target Design Phase (TODO)**<br/>
> Spandrel is currently in its formal specification and architectural design phase. It defines the unbundled substrate contracts and neutral domain traits required before implementing production Rust crates. Construction follows clean-room discipline: the specification and neutral test vectors are authored prior to implementation.

## Spandrel: Modular DDD/CQRS/EDA Substrate

Modern web frameworks tend to be monolithic. They bind domain business logic tightly to specific object-relational mappers (ORMs), assume synchronous request-response relational databases, and conflate HTTP request handling with state mutation and view rendering. When engineering teams attempt to adopt Domain-Driven Design (DDD), Command Query Responsibility Segregation (CQRS), and Event-Driven Architecture (EDA) in Rust, they are often forced to choose between heavyweight, all-or-nothing enterprise frameworks or assembling ad-hoc, brittle glue code across dozens of disparate crates.

`Spandrel` provides an **unbundled, modular substrate** for CQRS/DDD/EDA applications in Rust. Rather than acting as an invasive framework that dictates application control flow, Spandrel offers composable, high-performance primitives: neutral domain traits, change-driven projection fold pipelines, admission regulators, bounded work queues, and zero-query static HTTP serving.

<style>
  .spandrel-container {
    --sp-bg: #ffffff;
    --sp-text: #0f172a;
    --sp-text-muted: #475569;
    --sp-code-bg: rgba(15, 23, 42, 0.06);
    --sp-code-text: #0f172a;

    --sp-slate-border: #64748b;
    --sp-slate-bg: rgba(100, 116, 139, 0.05);
    --sp-slate-tag-bg: #475569;
    --sp-slate-tag-text: #ffffff;

    --sp-blue-border: #2563eb;
    --sp-blue-bg: rgba(37, 99, 235, 0.04);
    --sp-blue-tag-bg: #1d4ed8;
    --sp-blue-tag-text: #ffffff;

    --sp-purple-border: #7c3aed;
    --sp-purple-bg: rgba(124, 58, 237, 0.04);
    --sp-purple-tag-bg: #6d28d9;
    --sp-purple-tag-text: #ffffff;

    --sp-green-border: #059669;
    --sp-green-bg: rgba(5, 150, 105, 0.06);
    --sp-green-tag-bg: #047857;
    --sp-green-tag-text: #ffffff;

    --sp-cyan-border: #0891b2;
    --sp-cyan-bg: rgba(8, 145, 178, 0.05);
    --sp-cyan-tag-bg: #0e7490;
    --sp-cyan-tag-text: #ffffff;

    --sp-amber-border: #d97706;
    --sp-amber-bg: rgba(217, 119, 6, 0.05);
    --sp-amber-tag-bg: #b45309;
    --sp-amber-tag-text: #ffffff;

    --sp-rose-border: #e11d48;
    --sp-rose-bg: rgba(225, 29, 72, 0.05);
    --sp-rose-tag-bg: #be123c;
    --sp-rose-tag-text: #ffffff;

    --sp-connector-bg: rgba(241, 245, 249, 0.95);
    --sp-connector-border: #cbd5e1;

    box-sizing: border-box;
    width: 100%;
    max-width: 100%;
    margin: 2rem 0;
    padding: 1rem;
    background: var(--sp-bg);
    border: 1.5px solid var(--sp-slate-border);
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 0.875rem;
    line-height: 1.5;
    color: var(--sp-text);
    overflow-x: hidden;
  }

  :root[data-theme="dark"] .spandrel-container,
  :root[data-theme$="dark"] .spandrel-container {
    --sp-bg: #0f172a;
    --sp-text: #f1f5f9;
    --sp-text-muted: #94a3b8;
    --sp-code-bg: rgba(0, 0, 0, 0.4);
    --sp-code-text: #f8fafc;

    --sp-slate-border: #64748b;
    --sp-slate-bg: rgba(100, 116, 139, 0.15);
    --sp-slate-tag-bg: #334155;
    --sp-slate-tag-text: #f8fafc;

    --sp-blue-border: #3b82f6;
    --sp-blue-bg: rgba(59, 130, 246, 0.12);
    --sp-blue-tag-bg: #1d4ed8;
    --sp-blue-tag-text: #eff6ff;

    --sp-purple-border: #8b5cf6;
    --sp-purple-bg: rgba(139, 92, 246, 0.12);
    --sp-purple-tag-bg: #5b21b6;
    --sp-purple-tag-text: #f5f3ff;

    --sp-green-border: #10b981;
    --sp-green-bg: rgba(16, 185, 129, 0.12);
    --sp-green-tag-bg: #065f46;
    --sp-green-tag-text: #ecfdf5;

    --sp-cyan-border: #06b6d4;
    --sp-cyan-bg: rgba(6, 182, 212, 0.12);
    --sp-cyan-tag-bg: #0e7490;
    --sp-cyan-tag-text: #ecfeff;

    --sp-amber-border: #f59e0b;
    --sp-amber-bg: rgba(245, 158, 11, 0.12);
    --sp-amber-tag-bg: #92400e;
    --sp-amber-tag-text: #fef3c7;

    --sp-rose-border: #f43f5e;
    --sp-rose-bg: rgba(244, 63, 94, 0.12);
    --sp-rose-tag-bg: #9f1239;
    --sp-rose-tag-text: #ffe4e6;

    --sp-connector-bg: rgba(30, 41, 59, 0.9);
    --sp-connector-border: #475569;
  }

  @media (prefers-color-scheme: dark) {
    :root[data-theme="auto"] .spandrel-container,
    :root:not([data-theme="light"]):not([data-theme="dark"]) .spandrel-container {
      --sp-bg: #0f172a;
      --sp-text: #f1f5f9;
      --sp-text-muted: #94a3b8;
      --sp-code-bg: rgba(0, 0, 0, 0.4);
      --sp-code-text: #f8fafc;

      --sp-slate-border: #64748b;
      --sp-slate-bg: rgba(100, 116, 139, 0.15);
      --sp-slate-tag-bg: #334155;
      --sp-slate-tag-text: #f8fafc;

      --sp-blue-border: #3b82f6;
      --sp-blue-bg: rgba(59, 130, 246, 0.12);
      --sp-blue-tag-bg: #1d4ed8;
      --sp-blue-tag-text: #eff6ff;

      --sp-purple-border: #8b5cf6;
      --sp-purple-bg: rgba(139, 92, 246, 0.12);
      --sp-purple-tag-bg: #5b21b6;
      --sp-purple-tag-text: #f5f3ff;

      --sp-green-border: #10b981;
      --sp-green-bg: rgba(16, 185, 129, 0.12);
      --sp-green-tag-bg: #065f46;
      --sp-green-tag-text: #ecfdf5;

      --sp-cyan-border: #06b6d4;
      --sp-cyan-bg: rgba(6, 182, 212, 0.12);
      --sp-cyan-tag-bg: #0e7490;
      --sp-cyan-tag-text: #ecfeff;

      --sp-amber-border: #f59e0b;
      --sp-amber-bg: rgba(245, 158, 11, 0.12);
      --sp-amber-tag-bg: #92400e;
      --sp-amber-tag-text: #fef3c7;

      --sp-rose-border: #f43f5e;
      --sp-rose-bg: rgba(244, 63, 94, 0.12);
      --sp-rose-tag-bg: #9f1239;
      --sp-rose-tag-text: #ffe4e6;

      --sp-connector-bg: rgba(30, 41, 59, 0.9);
      --sp-connector-border: #475569;
    }
  }

  .spandrel-container,
  .spandrel-container * {
    box-sizing: border-box;
  }

  .sp-card {
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    background: var(--sp-bg);
    border: 1.5px solid var(--sp-slate-border);
    transition: border-color 0.2s ease;
    min-width: 0;
  }

  .sp-card-slate { border-color: var(--sp-slate-border); background: var(--sp-slate-bg); }
  .sp-card-blue { border-color: var(--sp-blue-border); background: var(--sp-blue-bg); }
  .sp-card-purple { border-color: var(--sp-purple-border); background: var(--sp-purple-bg); }
  .sp-card-green { border-color: var(--sp-green-border); background: var(--sp-green-bg); }
  .sp-card-cyan { border-color: var(--sp-cyan-border); background: var(--sp-cyan-bg); }
  .sp-card-amber { border-color: var(--sp-amber-border); background: var(--sp-amber-bg); }
  .sp-card-rose { border-color: var(--sp-rose-border); background: var(--sp-rose-bg); }

  .sp-card-title-bar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(100, 116, 139, 0.2);
  }

  .sp-title-group {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    min-width: 0;
  }

  .sp-title {
    font-weight: 600;
    font-size: 0.9375rem;
    color: var(--sp-text);
  }

  .sp-tag {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.025em;
    text-transform: uppercase;
    white-space: nowrap;
  }

  .sp-tag-slate { background: var(--sp-slate-tag-bg); color: var(--sp-slate-tag-text); }
  .sp-tag-blue { background: var(--sp-blue-tag-bg); color: var(--sp-blue-tag-text); }
  .sp-tag-purple { background: var(--sp-purple-tag-bg); color: var(--sp-purple-tag-text); }
  .sp-tag-green { background: var(--sp-green-tag-bg); color: var(--sp-green-tag-text); }
  .sp-tag-cyan { background: var(--sp-cyan-tag-bg); color: var(--sp-cyan-tag-text); }
  .sp-tag-amber { background: var(--sp-amber-tag-bg); color: var(--sp-amber-tag-text); }
  .sp-tag-rose { background: var(--sp-rose-tag-bg); color: var(--sp-rose-tag-text); }

  .sp-section-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--sp-text-muted);
    margin: 0.625rem 0 0.375rem 0;
  }

  .sp-grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 0.75rem;
  }

  .sp-grid-3 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.75rem;
  }

  .sp-grid-4 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 0.75rem;
  }

  .sp-stack-compact {
    display: flex;
    flex-direction: column;
    gap: 0.625rem;
  }

  .sp-field {
    border-radius: 6px;
    padding: 0.625rem 0.75rem;
    border: 1px solid rgba(100, 116, 139, 0.25);
    background: var(--sp-bg);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-width: 0;
  }

  .sp-field-slate { border-left: 3.5px solid var(--sp-slate-border); }
  .sp-field-blue { border-left: 3.5px solid var(--sp-blue-border); }
  .sp-field-purple { border-left: 3.5px solid var(--sp-purple-border); }
  .sp-field-green { border-left: 3.5px solid var(--sp-green-border); }
  .sp-field-cyan { border-left: 3.5px solid var(--sp-cyan-border); }
  .sp-field-amber { border-left: 3.5px solid var(--sp-amber-border); }
  .sp-field-rose { border-left: 3.5px solid var(--sp-rose-border); }

  .sp-field-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--sp-text-muted);
    margin-bottom: 0.25rem;
  }

  .sp-field-val {
    font-size: 0.8125rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 0.375rem;
    color: var(--sp-text);
  }

  .sp-field-val code {
    background: var(--sp-code-bg);
    color: var(--sp-code-text);
    padding: 0.15rem 0.35rem;
    border-radius: 3px;
    font-size: 0.8125rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    word-break: break-all;
    overflow-wrap: break-word;
  }

  .sp-field-desc {
    font-size: 0.72rem;
    color: var(--sp-text-muted);
    line-height: 1.35;
  }

  .sp-flow-arrow {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0.5rem 0;
  }

  .sp-arrow-line {
    width: 2px;
    height: 14px;
    background: var(--sp-slate-border);
  }

  .sp-arrow-badge {
    background: var(--sp-connector-bg);
    border: 1px solid var(--sp-connector-border);
    border-radius: 12px;
    padding: 0.2rem 0.75rem;
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--sp-text-muted);
    margin: 2px 0;
    text-align: center;
    max-width: 100%;
    word-break: break-word;
  }

  .sp-arrow-head {
    font-size: 0.75rem;
    color: var(--sp-slate-border);
    line-height: 1;
  }

  .sp-connector-block {
    background: var(--sp-connector-bg);
    border: 1.5px dashed var(--sp-connector-border);
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    min-width: 0;
  }

  .sp-connector-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--sp-connector-border);
  }

  .sp-connector-title {
    font-weight: 700;
    font-size: 0.8125rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--sp-text);
  }

  .sp-connector-subtitle {
    font-size: 0.75rem;
    color: var(--sp-text-muted);
  }

  .sp-connector-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 0.75rem;
  }

  .sp-conn-card {
    display: flex;
    align-items: flex-start;
    gap: 0.625rem;
    padding: 0.625rem;
    border-radius: 6px;
    background: var(--sp-bg);
    border: 1px solid rgba(100, 116, 139, 0.2);
    min-width: 0;
  }

  .sp-conn-num {
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

  .sp-num-slate { background: #475569; }
  .sp-num-blue { background: #2563eb; }
  .sp-num-purple { background: #7c3aed; }
  .sp-num-green { background: #059669; }
  .sp-num-cyan { background: #0891b2; }
  .sp-num-amber { background: #d97706; }
  .sp-num-rose { background: #e11d48; }

  .sp-conn-content {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    min-width: 0;
  }

  .sp-conn-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--sp-text);
  }

  .sp-conn-detail {
    font-size: 0.75rem;
    color: var(--sp-text);
  }

  .sp-conn-detail code {
    background: var(--sp-code-bg);
    color: var(--sp-code-text);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-size: 0.75rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    word-break: break-all;
    overflow-wrap: break-word;
  }

  .sp-conn-desc {
    font-size: 0.7rem;
    color: var(--sp-text-muted);
    line-height: 1.35;
  }

  .sp-callout-badge {
    border-radius: 6px;
    padding: 0.625rem 0.875rem;
    margin-top: 0.875rem;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    min-width: 0;
  }

  .sp-callout-cyan {
    border: 1.5px solid var(--sp-cyan-border);
    background: var(--sp-cyan-bg);
  }

  .sp-callout-amber {
    border: 1.5px solid var(--sp-amber-border);
    background: var(--sp-amber-bg);
  }

  .sp-callout-green {
    border: 1.5px solid var(--sp-green-border);
    background: var(--sp-green-bg);
  }

  .sp-callout-blue {
    border: 1.5px solid var(--sp-blue-border);
    background: var(--sp-blue-bg);
  }

  .sp-callout-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.8125rem;
    font-weight: 600;
    color: var(--sp-text);
    flex-wrap: wrap;
  }

  .sp-callout-desc {
    font-size: 0.75rem;
    color: var(--sp-text-muted);
  }

  @media (max-width: 640px) {
    .sp-grid-2,
    .sp-grid-3,
    .sp-grid-4,
    .sp-connector-grid {
      grid-template-columns: 1fr;
    }
    .sp-card-title-bar,
    .sp-callout-badge,
    .sp-connector-header {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>

<div class="spandrel-container">
  <div class="sp-grid-2">
    <!-- Card 1: Client Interaction -->
    <div class="sp-card sp-card-cyan">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-cyan">Client Interaction</span>
          <span class="sp-title">Edge Clients &amp; Browsers</span>
        </div>
        <span class="sp-tag sp-tag-cyan">HTTP Boundary</span>
      </div>
      <div class="sp-section-label">Request Interfaces</div>
      <div class="sp-stack-compact">
        <div class="sp-field sp-field-amber">
          <div class="sp-field-label">Command Ingestion (Mutating)</div>
          <div class="sp-field-val"><code>HTTP POST / PUT</code></div>
          <div class="sp-field-desc">Dispatches mutating commands to bounded admission work queue.</div>
        </div>
        <div class="sp-field sp-field-cyan">
          <div class="sp-field-label">Query Path (Read-Only)</div>
          <div class="sp-field-val"><code>HTTP GET</code></div>
          <div class="sp-field-desc">Direct static buffer read with zero query latency and zero lock contention.</div>
        </div>
      </div>
    </div>

    <!-- Card 2: Spandrel Substrate Primitives -->
    <div class="sp-card sp-card-blue">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-blue">Substrate Primitives</span>
          <span class="sp-title">Spandrel Runtime Engine</span>
        </div>
        <span class="sp-tag sp-tag-blue">Domain-Neutral</span>
      </div>
      <div class="sp-section-label">Core Substrate Modules</div>
      <div class="sp-stack-compact">
        <div class="sp-field sp-field-amber">
          <div class="sp-field-label">Admission Regulator &amp; Work Queue</div>
          <div class="sp-field-val"><code>FLEET-RES-01 Bounds</code></div>
          <div class="sp-field-desc">Independent item and byte limits shedding load via HTTP 429/503 backpressure.</div>
        </div>
        <div class="sp-field sp-field-blue">
          <div class="sp-field-label">Projection Fold Driver</div>
          <div class="sp-field-val"><code>Change-Driven Fold Stream</code></div>
          <div class="sp-field-desc">Follows committed events and folds state into typed view models asynchronously.</div>
        </div>
        <div class="sp-field sp-field-cyan">
          <div class="sp-field-label">Pre-Rendered Static Cache Store</div>
          <div class="sp-field-val"><code>O(1) Memory / Disk Cache</code></div>
          <div class="sp-field-desc">Serves pre-rendered HTML pages directly from memory-mapped static buffers.</div>
        </div>
      </div>
    </div>

    <!-- Card 3: Application Domain -->
    <div class="sp-card sp-card-purple">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-purple">Application Domain</span>
          <span class="sp-title">gh-report (or Domain Service)</span>
        </div>
        <span class="sp-tag sp-tag-purple">Domain Logic</span>
      </div>
      <div class="sp-section-label">Business Invariants &amp; Rendering</div>
      <div class="sp-stack-compact">
        <div class="sp-field sp-field-purple">
          <div class="sp-field-label">Domain Rules &amp; Aggregate Logic</div>
          <div class="sp-field-val"><code>Invariants &amp; State Transitions</code></div>
          <div class="sp-field-desc">Enforces domain boundaries, executes command handlers, and emits candidate facts.</div>
        </div>
        <div class="sp-field sp-field-purple">
          <div class="sp-field-label">Askama View Model Renderer</div>
          <div class="sp-field-val"><code>Compiled Type-Safe HTML</code></div>
          <div class="sp-field-desc">Transforms folded domain view models into static HTML artifacts ahead of read requests.</div>
        </div>
      </div>
    </div>

    <!-- Card 4: Stream Storage: Pardosa -->
    <div class="sp-card sp-card-green">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-green">Stream Storage</span>
          <span class="sp-title">Pardosa Storage Engine</span>
        </div>
        <span class="sp-tag sp-tag-green">Durable Dragline</span>
      </div>
      <div class="sp-section-label">Append-Only Commit Log</div>
      <div class="sp-stack-compact">
        <div class="sp-field sp-field-green">
          <div class="sp-field-label">Append-Only Dragline Log</div>
          <div class="sp-field-val"><code>Single-Writer Fencing &amp; CAS</code></div>
          <div class="sp-field-desc">Linearizable event storage with byte-level BLAKE3 framing and durable disk flush.</div>
        </div>
        <div class="sp-field sp-field-green">
          <div class="sp-field-label">Event Carried State Transfer</div>
          <div class="sp-field-val"><code>Fiber Event Notification</code></div>
          <div class="sp-field-desc">Streams committed events asynchronously to projection fold listeners.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Flow Direction Connectors Block -->
  <div class="sp-connector-block">
    <div class="sp-connector-header">
      <span class="sp-connector-title">End-to-End Command &amp; Query Data Flow</span>
      <span class="sp-connector-subtitle">Complete lifecycle from ingress to static response</span>
    </div>
    <div class="sp-connector-grid">
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-amber">1</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">Command Ingress &amp; Enqueue</div>
          <div class="sp-conn-detail"><code>Client HTTP POST/PUT</code> ➔ <code>Admission Regulator</code></div>
          <div class="sp-conn-desc">Command admitted to bounded queue with resource bounds (HTTP 202).</div>
        </div>
      </div>
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-purple">2</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">Domain Execution &amp; Log Commit</div>
          <div class="sp-conn-detail"><code>gh-report Invariants</code> ➔ <code>Pardosa Dragline</code></div>
          <div class="sp-conn-desc">Aggregate validates state and appends immutable event with CAS single-writer fencing.</div>
        </div>
      </div>
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-blue">3</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">Change-Driven Fold &amp; Render</div>
          <div class="sp-conn-detail"><code>Fold Driver</code> ➔ <code>Askama</code> ➔ <code>Static Cache</code></div>
          <div class="sp-conn-desc">Substrate consumes committed event, updates projection state, and renders HTML.</div>
        </div>
      </div>
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-cyan">4</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">Zero-Query Response</div>
          <div class="sp-conn-detail"><code>Client HTTP GET</code> ➔ <code>Static Cache Store</code></div>
          <div class="sp-conn-desc">Direct O(1) memory lookup serves pre-rendered HTML with zero database queries.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Highlighted Badge for Zero-Query Latency -->
  <div class="sp-callout-badge sp-callout-cyan">
    <div class="sp-callout-title">
      <span class="sp-tag sp-tag-cyan">Zero-Query Latency</span>
      <strong>Direct O(1) Memory Lookup</strong>
      <code>0 DB Queries · 0 Dynamic Renders · 0 Locks</code>
    </div>
    <div class="sp-callout-desc">
      HTTP GET requests bypass application databases entirely; read responses stream from pre-rendered static buffers.
    </div>
  </div>
</div>

---

## The Strategic Problem: Monolithic Framework Coupling vs. Unbundled Substrates

Enterprise application development in Rust faces a fundamental impedance mismatch:

1. **Framework Entanglement**: Mainstream web frameworks encourage embedding business invariants directly inside route handlers, database transaction blocks, or template engines. When data models evolve or deployment targets shift from servers to edge daemons, the entire application stack must be rewritten.
2. **The Query-at-Request Anti-Pattern**: Traditional web services query the database dynamically upon every incoming HTTP GET request. As data complexity grows, requests trigger expensive join cascades, relational locking, or distributed cache invalidation bugs. Even with Redis or Memcached, query latencies degrade under load.
3. **Lack of Composable EDA Building Blocks**: In the Rust ecosystem, while high-performance networking (`tokio`, `hyper`, `axum`) and fast templating (`askama`) exist as isolated libraries, there is a lack of cohesive, unbundled primitives for folding event streams into pre-rendered read views with explicit resource bounds.

Spandrel resolves this by unbundling application infrastructure into clean, autonomous tiers.

---

## Three-Tier Separation of Concerns

Spandrel establishes a strict, three-tier separation of concerns across the application architecture:

<div class="spandrel-container">
  <!-- 3-Tier Architectural Stack -->
  <div class="sp-section-label">3-Tier Architectural Stack</div>

  <!-- Tier 1: Application Layer -->
  <div class="sp-card sp-card-purple">
    <div class="sp-card-title-bar">
      <div class="sp-title-group">
        <span class="sp-tag sp-tag-purple">Tier 1</span>
        <span class="sp-title">Application Layer · e.g. gh-report</span>
      </div>
      <span class="sp-tag sp-tag-purple">Domain &amp; Routing</span>
    </div>
    <div class="sp-grid-2">
      <div class="sp-field sp-field-purple">
        <div class="sp-field-label">Domain Invariants</div>
        <div class="sp-field-val"><code>Business Rules &amp; Aggregates</code></div>
        <div class="sp-field-desc">Owns domain business rules, domain commands, and state validation.</div>
      </div>
      <div class="sp-field sp-field-purple">
        <div class="sp-field-label">Command Handlers</div>
        <div class="sp-field-val"><code>Dispatch Policies &amp; Work Units</code></div>
        <div class="sp-field-desc">Executes command admission policies and maps intents to domain mutations.</div>
      </div>
      <div class="sp-field sp-field-purple">
        <div class="sp-field-label">Askama HTML Templates</div>
        <div class="sp-field-val"><code>Typed View Models</code></div>
        <div class="sp-field-desc">Defines concrete compile-time Askama templates rendered during fold operations.</div>
      </div>
      <div class="sp-field sp-field-purple">
        <div class="sp-field-label">Security &amp; Routing</div>
        <div class="sp-field-val"><code>Identity &amp; Endpoint Policies</code></div>
        <div class="sp-field-desc">Declares authentication, authorization, session boundaries, and URL route mappings.</div>
      </div>
    </div>
  </div>

  <!-- Flow Arrow: Tier 1 to Tier 2 -->
  <div class="sp-flow-arrow">
    <div class="sp-arrow-line"></div>
    <div class="sp-arrow-badge">Tier 1 Implements Traits &amp; Uses Substrate Primitives</div>
    <div class="sp-arrow-head">▼</div>
  </div>

  <!-- Tier 2: Substrate Layer -->
  <div class="sp-card sp-card-blue">
    <div class="sp-card-title-bar">
      <div class="sp-title-group">
        <span class="sp-tag sp-tag-blue">Tier 2</span>
        <span class="sp-title">Substrate Layer · Spandrel</span>
      </div>
      <span class="sp-tag sp-tag-blue">Neutral Infrastructure</span>
    </div>
    <div class="sp-grid-2">
      <div class="sp-field sp-field-blue">
        <div class="sp-field-label">Neutral Domain Traits</div>
        <div class="sp-field-val"><code>Read Ports &amp; Event Descriptors</code></div>
        <div class="sp-field-desc">Provides unbundled domain traits, entity identifiers, and neutral event interfaces.</div>
      </div>
      <div class="sp-field sp-field-amber">
        <div class="sp-field-label">Admission Regulators</div>
        <div class="sp-field-val"><code>Bounded Work Queues</code></div>
        <div class="sp-field-desc">Enforces explicit item and byte limits with cooperative backpressure rejection.</div>
      </div>
      <div class="sp-field sp-field-blue">
        <div class="sp-field-label">Projection Fold Drivers</div>
        <div class="sp-field-val"><code>Schedulers &amp; Stream Listeners</code></div>
        <div class="sp-field-desc">Coordinates asynchronous transformation of event streams into in-memory projection states.</div>
      </div>
      <div class="sp-field sp-field-cyan">
        <div class="sp-field-label">Static HTTP Serving</div>
        <div class="sp-field-val"><code>High-Throughput O(1) Serving</code></div>
        <div class="sp-field-desc">Delivers pre-rendered HTML responses directly from memory-mapped disk buffers.</div>
      </div>
    </div>
  </div>

  <!-- Flow Arrow: Tier 2 to Tier 3 -->
  <div class="sp-flow-arrow">
    <div class="sp-arrow-line"></div>
    <div class="sp-arrow-badge">Decoupled Boundaries: Zero Cargo Dependency</div>
    <div class="sp-arrow-head">▼</div>
  </div>

  <!-- Tier 3: Stream Layer -->
  <div class="sp-card sp-card-green">
    <div class="sp-card-title-bar">
      <div class="sp-title-group">
        <span class="sp-tag sp-tag-green">Tier 3</span>
        <span class="sp-title">Stream Layer · Pardosa</span>
      </div>
      <span class="sp-tag sp-tag-green">Append-Only Dragline</span>
    </div>
    <div class="sp-grid-3">
      <div class="sp-field sp-field-green">
        <div class="sp-field-label">Durable Dragline Stream</div>
        <div class="sp-field-val"><code>Append-Only Log Files</code></div>
        <div class="sp-field-desc">Immutable event storage using fiber semantics and sequential container files.</div>
      </div>
      <div class="sp-field sp-field-green">
        <div class="sp-field-label">CAS Single-Writer Fencing</div>
        <div class="sp-field-val"><code>Linearizable Sequencing</code></div>
        <div class="sp-field-desc">Prevents split-brain mutations via atomic compare-and-swap sequence fences.</div>
      </div>
      <div class="sp-field sp-field-green">
        <div class="sp-field-label">BLAKE3 Framing &amp; Recovery</div>
        <div class="sp-field-val"><code>Cryptographic Checksums</code></div>
        <div class="sp-field-desc">Guarantees byte-level frame integrity and crash-safe frame reconstruction.</div>
      </div>
    </div>
  </div>

  <!-- Ownership & Zero-Direct-Dependency Callout Block -->
  <div class="sp-connector-block">
    <div class="sp-connector-header">
      <span class="sp-connector-title">Ownership &amp; Zero-Direct-Dependency Guarantees</span>
      <span class="sp-connector-subtitle">Rigorous architectural decoupling across Cargo workspaces</span>
    </div>
    <div class="sp-connector-grid">
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-purple">✓</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">Tier 1 Implements &amp; Uses Tier 2</div>
          <div class="sp-conn-detail"><code>gh-report</code> ➔ <code>Spandrel</code></div>
          <div class="sp-conn-desc">Application implements neutral traits (ReadPort, Fold) and consumes substrate runtime primitives.</div>
        </div>
      </div>
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-green">✓</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">Tier 1 Appends Events to Tier 3</div>
          <div class="sp-conn-detail"><code>gh-report</code> ➔ <code>Pardosa</code></div>
          <div class="sp-conn-desc">Application command handlers commit validated candidate events directly into Pardosa's dragline.</div>
        </div>
      </div>
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-blue">⚡</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">ZERO Direct Cargo Dependency</div>
          <div class="sp-conn-detail"><code>Spandrel</code> ⇏ <code>Pardosa (0 Cargo deps)</code></div>
          <div class="sp-conn-desc">Spandrel maintains complete compile-time decoupling from Pardosa; interacts strictly via generic traits.</div>
        </div>
      </div>
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-cyan">↻</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">Tier 3 Streams Events to Tier 2</div>
          <div class="sp-conn-detail"><code>Pardosa</code> ➔ <code>Spandrel</code></div>
          <div class="sp-conn-desc">Committed event frames are streamed asynchronously to substrate fold drivers via event subscriptions.</div>
        </div>
      </div>
    </div>
  </div>
</div>

1. **Application Layer (e.g. `gh-report`)**:
   - Owns domain business rules, domain commands, and state validation.
   - Defines concrete Askama HTML templates and typed view models.
   - Declares authentication, authorization, and endpoint routing.
2. **Substrate Layer (`Spandrel`)**:
   - Provides domain-neutral interfaces: read ports, entity identifiers, and event descriptors.
   - Implements resource-bounded admission regulators and priority work queues.
   - Drives projection fold pipelines, coordinating the transformation of stream events into state.
   - Manages high-performance HTTP serving directly from pre-rendered memory or disk buffers.
   - **Zero Dependency Guarantee**: Spandrel core crates maintain zero direct Cargo dependencies on Pardosa or specific storage engines, ensuring complete technological decoupling.
3. **Stream Layer (`Pardosa`)**:
   - Acts as the immutable, append-only commit log.
   - Provides per-aggregate linearizability via Compare-And-Swap (CAS) single-writer fencing.
   - Guarantees byte-level frame integrity via BLAKE3 checksums and crash-safe file flush protocols.

---

## Change-Driven Projection Fold Pipeline

The core architectural flow in Spandrel is the **Change-Driven Projection Fold Pipeline**. It eliminates runtime database querying by turning page rendering into an asynchronous, change-driven event fold:

<div class="spandrel-container">
  <div class="sp-section-label">4-Stage Pipeline Stepper</div>
  <div class="sp-grid-4">
    <!-- Stage 1: Stream Ingestion -->
    <div class="sp-card sp-card-green">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-green">Stage 1</span>
          <span class="sp-title">Stream Ingestion</span>
        </div>
        <span class="sp-tag sp-tag-green">Pardosa</span>
      </div>
      <div class="sp-field sp-field-green">
        <div class="sp-field-label">Committed Event</div>
        <div class="sp-field-val"><code>Pardosa Dragline</code></div>
        <div class="sp-field-desc">Immutable event record committed with CAS single-writer fencing and flushed to append-only storage.</div>
      </div>
    </div>

    <!-- Stage 2: Projection Fold Driver -->
    <div class="sp-card sp-card-blue">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-blue">Stage 2</span>
          <span class="sp-title">Projection Fold Driver</span>
        </div>
        <span class="sp-tag sp-tag-purple">Substrate + App</span>
      </div>
      <div class="sp-stack-compact">
        <div class="sp-field sp-field-blue">
          <div class="sp-field-label">1. Stream Listener</div>
          <div class="sp-field-val"><code>Subscription Stream Listener</code></div>
          <div class="sp-field-desc">Tail follower receives committed event frame.</div>
        </div>
        <div class="sp-field sp-field-blue">
          <div class="sp-field-label">2. State Accumulator</div>
          <div class="sp-field-val"><code>Fold State Accumulator</code></div>
          <div class="sp-field-desc">Deterministic in-memory fold updates state.</div>
        </div>
        <div class="sp-field sp-field-purple">
          <div class="sp-field-label">3. View Model Render</div>
          <div class="sp-field-val"><code>Askama View Model Render</code></div>
          <div class="sp-field-desc">Compiled templates render HTML ahead of time.</div>
        </div>
      </div>
    </div>

    <!-- Stage 3: Static Cache Store -->
    <div class="sp-card sp-card-cyan">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-cyan">Stage 3</span>
          <span class="sp-title">Static Cache Store</span>
        </div>
        <span class="sp-tag sp-tag-cyan">Storage</span>
      </div>
      <div class="sp-field sp-field-cyan">
        <div class="sp-field-label">Pre-Rendered HTML Page</div>
        <div class="sp-field-val"><code>In-Memory / Fast Disk</code></div>
        <div class="sp-field-desc">Fully formed HTML page buffered in memory or memory-mapped files ready for instantaneous HTTP transmission.</div>
      </div>
    </div>

    <!-- Stage 4: Zero-Query HTTP Serving -->
    <div class="sp-card sp-card-cyan">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-cyan">Stage 4</span>
          <span class="sp-title">HTTP Serving</span>
        </div>
        <span class="sp-tag sp-tag-cyan">O(1) Edge</span>
      </div>
      <div class="sp-stack-compact">
        <div class="sp-field sp-field-cyan">
          <div class="sp-field-label">Client Query</div>
          <div class="sp-field-val"><code>HTTP GET Request</code></div>
          <div class="sp-field-desc">Browser or client requests view endpoint.</div>
        </div>
        <div class="sp-field sp-field-cyan">
          <div class="sp-field-label">Zero-Query Response</div>
          <div class="sp-field-val"><code>Instant HTTP 200 Response</code></div>
          <div class="sp-field-desc">Instant delivery via O(1) direct memory lookup.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Performance, Latency & Zero-Query Callout Badges Block -->
  <div class="sp-connector-block">
    <div class="sp-connector-header">
      <span class="sp-connector-title">Read Path Performance Invariants &amp; Guarantees</span>
      <span class="sp-connector-subtitle">Elimination of runtime query degradation</span>
    </div>
    <div class="sp-connector-grid">
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-cyan">⚡</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">O(1) Zero-Copy Read</div>
          <div class="sp-conn-detail"><code>Direct Memory Buffer Access</code></div>
          <div class="sp-conn-desc">Static page bytes streamed directly to socket buffers without runtime memory allocation.</div>
        </div>
      </div>
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-green">0</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">Zero Database Queries</div>
          <div class="sp-conn-detail"><code>0 SQL · 0 KV Lookups · 0 Joins</code></div>
          <div class="sp-conn-desc">No database query engine is contacted during HTTP GET request execution.</div>
        </div>
      </div>
      <div class="sp-conn-card">
        <div class="sp-conn-num sp-num-blue">🔒</div>
        <div class="sp-conn-content">
          <div class="sp-conn-label">Zero Request-Time Locks</div>
          <div class="sp-conn-detail"><code>Lockless Serving Path</code></div>
          <div class="sp-conn-desc">Read threads operate completely unhindered by write locks or transactional concurrency.</div>
        </div>
      </div>
    </div>
  </div>
</div>

### The Four Pipeline Stages

1. **Stream Ingestion**: When an aggregate mutation commits to the stream layer, the event is emitted to subscribed listeners.
2. **State Folding**: Spandrel's projection driver routes the event to registered fold accumulators. The accumulator updates its typed in-memory projection state deterministically.
3. **Static View Rendering**: The updated projection state triggers immediate rendering through the application's compiled Askama template. The resulting static HTML page is published to an optimized cache store (in-memory buffer or memory-mapped file).
4. **Zero-Query HTTP Serving**: When an HTTP GET request arrives from a user or browser, the HTTP serving layer fetches the pre-rendered artifact directly from cache. **Zero database queries, zero template rendering, and zero locks occur at request time.** Serving achieves predictable $O(1)$ read response times under arbitrary traffic load.

---

## Invariants & Demarcation: Guarantees That Hold

Distributed systems require precise semantic boundaries. Spandrel formalizes critical demarcation invariants and resource safety contracts:

### 1. Ingestion Demarcation: Acceptance $\neq$ Completion $\neq$ Commit

Spandrel strictly enforces three distinct lifecycle checkpoints for all command mutations:

$$\text{Acceptance} \neq \text{Completion} \neq \text{Commit}$$

<div class="spandrel-container">
  <div class="sp-section-label">Three Sequential Mutation Checkpoints</div>
  <div class="sp-grid-3">
    <!-- Checkpoint 1: Acceptance -->
    <div class="sp-card sp-card-amber">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-amber">Checkpoint 1</span>
          <span class="sp-title">Acceptance</span>
        </div>
        <span class="sp-tag sp-tag-amber">HTTP 202 Enqueue</span>
      </div>
      <div class="sp-stack-compact">
        <div class="sp-field sp-field-amber">
          <div class="sp-field-label">Ingestion State</div>
          <div class="sp-field-val"><code>Bounded Work Queue</code></div>
          <div class="sp-field-desc">Admitted to work queue under FLEET-RES-01 item and byte bounds.</div>
        </div>
        <div class="sp-field sp-field-slate">
          <div class="sp-field-label">Mutation Status</div>
          <div class="sp-field-val"><code>No Mutation Yet</code></div>
          <div class="sp-field-desc">Command is scheduled; aggregate state remains completely unchanged.</div>
        </div>
      </div>
    </div>

    <!-- Checkpoint 2: Completion -->
    <div class="sp-card sp-card-purple">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-purple">Checkpoint 2</span>
          <span class="sp-title">Completion</span>
        </div>
        <span class="sp-tag sp-tag-purple">Validated Fact</span>
      </div>
      <div class="sp-stack-compact">
        <div class="sp-field sp-field-purple">
          <div class="sp-field-label">Domain Execution</div>
          <div class="sp-field-val"><code>Aggregate Logic Executed</code></div>
          <div class="sp-field-desc">Domain invariants validated; business logic produces candidate events.</div>
        </div>
        <div class="sp-field sp-field-purple">
          <div class="sp-field-label">Mutation Status</div>
          <div class="sp-field-val"><code>Uncommitted Candidate</code></div>
          <div class="sp-field-desc">Events are generated in memory but not yet durably stored or observable.</div>
        </div>
      </div>
    </div>

    <!-- Checkpoint 3: Commit -->
    <div class="sp-card sp-card-green">
      <div class="sp-card-title-bar">
        <div class="sp-title-group">
          <span class="sp-tag sp-tag-green">Checkpoint 3</span>
          <span class="sp-title">Commit</span>
        </div>
        <span class="sp-tag sp-tag-green">Durable Dragline Log</span>
      </div>
      <div class="sp-stack-compact">
        <div class="sp-field sp-field-green">
          <div class="sp-field-label">Storage Fencing</div>
          <div class="sp-field-val"><code>CAS Fencing &amp; Disk Flush</code></div>
          <div class="sp-field-desc">Appended to append-only log with single-writer fencing and flushed to disk.</div>
        </div>
        <div class="sp-field sp-field-green">
          <div class="sp-field-label">Mutation Status</div>
          <div class="sp-field-val"><code>Observable Fact</code></div>
          <div class="sp-field-desc">Event is permanent, durable, and immediately observable by projection folds.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Reconciliation of Unknown Outcomes Callout -->
  <div class="sp-callout-badge sp-callout-amber">
    <div class="sp-callout-title">
      <span class="sp-tag sp-tag-amber">Recovery Protocol</span>
      <strong>Reconciliation of Unknown Outcomes (FLEET-RES-01)</strong>
      <code>Status: Indeterminate (Never Assumed Failure)</code>
    </div>
    <div class="sp-callout-desc">
      If a network disconnect, process restart, or timeout occurs during stream append, Spandrel treats the outcome as <strong>Indeterminate</strong> rather than assuming failure. The subsystem initiates reconciliation against the stream rather than issuing duplicate mutations.
    </div>
  </div>
</div>

- **Acceptance (HTTP 202 / Enqueue)**: The command has passed admission regulation and entered a bounded work queue. No state mutation has yet occurred.
- **Completion**: The domain aggregate has executed business logic, validated invariants, and produced candidate events.
- **Commit**: The event has successfully been appended to the append-only stream log with CAS fencing and flushed to disk. Only committed events are observable by projection folds.
- **Reconciliation of Unknown Outcomes**: If a network disconnect, process restart, or timeout occurs during stream append, Spandrel treats the outcome as **Indeterminate**, never assuming failure. The subsystem initiates reconciliation against the stream rather than issuing duplicate mutations.

### 2. Explicit Resource Contracts (FLEET-RES-01)

To prevent resource exhaustion, Spandrel components enforce explicit resource bounds:

- **Separate Accounting for Items and Heap Bytes**: Bounded channels alone do not bound memory. A queue holding 100 small messages consumes kilobytes; holding 100 multi-megabyte payloads exhausts RAM. Spandrel accounts for item count and allocated payload bytes independently.
- **Admission Regulation & Backpressure**: When queue item or byte capacity reaches maximum thresholds, incoming commands are shed with explicit backpressure (`HTTP 429 Too Many Requests` or `HTTP 503 Service Unavailable`).
- **Supervised Shutdown & Cancellation**: Dropping asynchronous task handles does not guarantee task termination. Spandrel utilizes cooperative cancellation tokens, ensures in-flight tasks drain within explicit timeout budgets, and releases all permits deterministically via RAII guards.
