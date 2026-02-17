---
title: "CISQ model improvements for final release"
aliases:
  - "/CISQ-maturity/improvements/"
---
# CISQ model improvements

[Back to CISQ maturity levels]({{< relref "CISQ-maturity/_index.md" >}})

## Academic review of the current CISQ model

For final release quality, three gaps should be closed:

1. Formal rigor is not yet sufficient for reproducible, independent analysis.
2. Empirical evidence is not yet strong enough to establish practical reliability across teams.
3. Quantitative operational use is limited without explicit scoring and uncertainty handling.

The three improvements below address these gaps directly.

## Improvement 1: Formal semantics and composition rules

Current definitions are intuitive and readable, but they remain mostly natural-language descriptions. Without formal semantics, independent analysts may apply the same quality labels differently.

### Final-release expansion

For final release, define a minimal formal layer that keeps the model understandable:

- Define each primary quality as a predicate over an assessed target $x$:
  - $A(x)$ for Availability
  - $I(x)$ for Integrity
  - $C(x)$ for Control
  - $Au(x)$ for Authenticity
- Define composition as set and predicate combination, with each composed quality mapped to the conjunction of its required predicates.
- State algebraic properties explicitly (commutativity of composition, identity element, and closure over the quality set).
- Specify edge cases:
  - Unknown source provenance
  - Partial control in multi-tenant/cloud systems
  - Time-bounded availability
- Provide a one-page normative interpretation guide to minimize analyst drift.

### Deliverables

- [Formal notation appendix in the model documentation]({{< relref "CISQ-maturity/formal-appendix.md" >}})
- [Composition table with symbolic and prose definitions]({{< relref "CISQ-maturity/formal-appendix.md" >}})
- [Normative interpretation guide with examples and counterexamples]({{< relref "CISQ-maturity/formal-appendix.md" >}}#examples-and-counterexamples)

## Improvement 2: Empirical validation and interoperability mapping

A conceptual model becomes robust when different assessors can apply it consistently and when results connect to existing standards and operating practices.

### Final-release expansion

For final release, run a lightweight but rigorous validation program:

- Build a crosswalk from CISQ qualities to practical control references:
  - ISO/IEC 27001 Annex A controls
  - NIST SP 800-53 control families
  - Typical STRIDE categories where relevant
- Select a representative corpus of incidents and architecture decisions.
- Have multiple independent reviewers classify each case using CISQ.
- Measure inter-rater agreement (e.g., Cohen’s $\kappa$ for pairwise agreement).
- Analyze disagreement patterns and refine definitions where ambiguity is recurrent.

### Deliverables

- [Public crosswalk table (CISQ ↔ ISO/NIST/STRIDE)]({{< relref "CISQ-maturity/interoperability-crosswalk.md" >}})
- [Validation report with agreement metrics and observed ambiguities]({{< relref "CISQ-maturity/validation-report.md" >}})
- [Revision notes for definitions updated from empirical findings]({{< relref "CISQ-maturity/revision-notes.md" >}})

## Improvement 3: Quantitative scoring and uncertainty model

The current model supports conceptual clarity, but security programs also need measurable trends, prioritization, and explicit uncertainty handling.

### Final-release expansion

For final release, add a scoring profile without removing the qualitative model:

- Keep binary interpretation where applicable, but introduce a bounded score for each quality, e.g. $0$ to $5$.
- Add confidence for each score (e.g., low/medium/high, or numeric interval).
- Represent a system as a vector:

$$
S = \left[(A, c_A), (I, c_I), (C, c_C), (Au, c_{Au})\right]
$$
  where $c$ denotes confidence.

- Define clear aggregation rules for composed qualities and trend tracking over time.
- Require evidence type tags for each score (test result, audit artifact, operational metric, expert judgment).

### Deliverables

- [CISQ scoring rubric with thresholds and confidence definitions]({{< relref "CISQ-maturity/scoring-rubric.md" >}})
- [Evidence taxonomy and scoring instructions]({{< relref "CISQ-maturity/evidence-taxonomy.md" >}})
- [Dashboard-ready data model for periodic assessments]({{< relref "CISQ-maturity/assessment-data-model.md" >}})

## Final release criteria

The CISQ model should be considered ready for final release when all conditions are met:

1. Formal semantics are published and internally consistent.
2. Crosswalk and validation results are documented and reproducible.
3. Quantitative scoring and confidence guidance are available with worked examples.
4. At least two complete end-to-end case studies are published (one enterprise service, one distributed/public artifact scenario).

### Published case studies

- [Enterprise service case study]({{< relref "CISQ-maturity/case-study-enterprise-service.md" >}})
- [Distributed/public artifact case study]({{< relref "CISQ-maturity/case-study-distributed-artifact.md" >}})

## Suggested publication order

1. Publish formal appendix and revised terminology.
2. Publish interoperability crosswalk and validation report.
3. Publish scoring rubric and assessment templates.
4. Publish case studies and adoption guidance.

## Summary

These improvements preserve CISQ’s conceptual strengths while making it more scientific, more interoperable with existing governance frameworks, and more actionable in real-world security engineering.

[Return to CISQ maturity levels]({{< relref "CISQ-maturity/_index.md" >}})
