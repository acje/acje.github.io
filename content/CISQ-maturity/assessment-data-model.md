---
title: "CISQ assessment data model"
aliases:
  - "/CISQ-maturity/assessment-data-model/"
---
# CISQ assessment data model

[Back to improvements](/CISQ-maturity/improvements/)

## Purpose

A dashboard-ready schema for periodic CISQ assessments.

## Entity schema

```yaml
assessment:
  assessment_id: string
  system_id: string
  timestamp_utc: datetime
  assessor: string
  scope: string
  qualities:
    availability:
      score: integer   # 0..5
      confidence: enum # low|medium|high
      evidence_refs: [string]
    integrity:
      score: integer
      confidence: enum
      evidence_refs: [string]
    control:
      score: integer
      confidence: enum
      evidence_refs: [string]
    authenticity:
      score: integer
      confidence: enum
      evidence_refs: [string]
  composed:
    non_repudiation:
      score: integer
      confidence: enum
    confidentiality:
      score: integer
      confidence: enum
    reliability:
      score: integer
      confidence: enum
  notes: string
```

## Derived-field rules

- `score(composed) = min(score(required_primaries))`
- `confidence(composed) = min(confidence(required_primaries))`
- `delta = current_score - prior_score` per quality and reporting period

## Reporting views

- Radar chart for primary qualities
- Heatmap for composed quality trend by quarter
- Confidence drift alerts when confidence drops without score change
