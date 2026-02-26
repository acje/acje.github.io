---
title: "Digital sovereignty – National robust information sharing"
description: "Exploring how to implement a robust system for information sharing in the Norwegian public sector"
aliases:
  - "/national_robust_information_sharing/"
date: 2026-02-25
lastmod: 2026-02-25
---

## Digital Sovereignty – National Robust Information Sharing

### Pitch

Norway needs a national information sharing backbone as critical public infrastructure. A robust, standardized model for secure information sharing will reduce duplication of effort, improve service quality, and strengthen national digital sovereignty. This is not primarily a technology project; it is a state-capacity project.

By launching a joint pilot between DigDir and Mattilsynet, the government can demonstrate rapid, practical results: faster information flow, fewer integration failures, and lower long-term operating costs. The pilot can then scale into a national pattern that ministries and agencies can adopt without reinventing the wheel.

### Challenge

Information sharing across organizations is now essential to public value creation and should be treated as a core component of national digital sovereignty. At present, however, fragmented approaches generate avoidable errors, slow delivery, and high integration costs. A standardized national design can address these structural weaknesses and support the needs of large public institutions. Today, data sharing resembles water distribution without reliable infrastructure: quality is inconsistent, losses accumulate, and significant manual effort is required to keep services running.

### Opportunity

A standardized national model for robust information sharing would allow the vast majority of use cases to follow one trusted implementation pattern. This article proposes a pilot between the Norwegian Digitalisation Agency (DigDir) and the Norwegian Food Safety Authority (Mattilsynet) to establish a practical proof of concept with national scaling potential. Mattilsynet contributes operational expertise from its internal use of the NATS service mesh for systems integration, while DigDir contributes governance expertise in information quality and national data stewardship. Together, they are well positioned to demonstrate a model that others can adopt.

### Difficulty

Perhaps counterintuitively, the main barriers are no longer technical. Advances in service mesh technology and a more mature understanding of data products make implementation increasingly feasible. Yet national-scale deployment remains difficult to deploy in practice. The most significant constraints are institutional incentives and cross-organizational coordination, discussed below. For technical background, see [Information sharing is not a solved problem]({{< relref "systems/information_sharing/index.md" >}}).

## Diagnosis

When challenges recur over time, effective policy begins with diagnosis. To date, many interventions in the field of cross-organizational information sharing have addressed symptoms rather than underlying structural causes.

### The Incentive Structure

Consider two middle managers attempting to establish information sharing between their organizations. Each faces specific delivery requirements, fixed budgets, and performance metrics tied to short-term results. Under these conditions, both are incentivized to optimize only for the immediate bilateral need. Investments in shared foundations create near-term local costs, while benefits are distributed across institutions and realized later. Those who bear the cost are therefore unlikely to receive credit for the broader gain. In this incentive structure, producing a common good is often institutionally viable only when strong leadership commitment and sufficient organizational slack are available.

### The Coordination Challenge

Even where incentives are aligned, coordination remains a major challenge. Robust information sharing requires at least two organizations to be ready at the same time, with compatible priorities and implementation choices. Timing can usually be managed when urgency is clear; alignment of intentions is harder. Each institution carries a historically evolved technology stack, constrained capacity for absorbing new tools, and a legacy portfolio that shapes what is feasible in practice. These constraints differ across organizations and often collide during integration efforts, producing delays, rework, and avoidable cost.

As noted above, service mesh technology has advanced significantly. NATS, particularly relevant for data sharing due to native publish-subscribe capabilities, is already used by large and mature fintech and telecommunications organizations. It has, however, seen limited adoption in the Norwegian public sector.

## How to Win

### Fast Tracking

The fastest route is to identify a political actor with both mandate and implementation authority to sponsor a coordinated national effort. In practice, this will often be a ministry-level initiative with clear cross-sector governance. Such sponsorship can rebalance incentives and reduce coordination friction by funding common foundations rather than isolated one-off integrations.

The political context is favorable. Since the COVID-19 pandemic, and especially following the full-scale invasion of Ukraine, digital sovereignty has moved from a niche concern to a mainstream national priority across Europe. In this environment, credible measures that strengthen sovereign digital capacity, preparedness, and institutional resilience are likely to command broad political support.

### Scaling

The establishment of a successful pilot significantly de-risks subsequent onboarding. With a validated integration pattern and operational common infrastructure in place, the barriers to entry for additional organizations are substantially lowered. This creates a positive feedback loop: as participation grows, the marginal cost of each new connection decreases, while the collective value of the data sharing network increases efficiently.

## More to read

[Digital Sovereignty]({{< relref "systems/digital_sovereignty/index.md" >}})

[Information sharing is not a solved problem]({{< relref "systems/information_sharing/index.md" >}})
