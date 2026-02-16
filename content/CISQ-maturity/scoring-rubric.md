---
title: "CISQ scoring rubric"
aliases:
  - "/CISQ-maturity/scoring-rubric/"
---
# CISQ scoring rubric

[Back to improvements](/CISQ-maturity/improvements/)

## Scoring model

Each primary quality receives a score from 0 to 5 and a confidence level.

- 0: Not demonstrated
- 1: Ad hoc controls; frequent failure modes
- 2: Basic controls present; inconsistent execution
- 3: Defined controls; reliable for common scenarios
- 4: Quantitatively managed; robust under stress
- 5: Optimized and continuously improved with strong evidence

Confidence levels:

- Low: mostly expert judgment, limited artifact support
- Medium: mixed evidence and partial operational validation
- High: repeatable metrics, audits, and production evidence

## System profile

$$
S = \left[(A, c_A), (I, c_I), (C, c_C), (Au, c_{Au})\right]
$$

## Aggregation rules

- Composed quality score = minimum of required primary quality scores.
- Composed quality confidence = minimum confidence among required primary qualities.
- Trend tracking uses rolling quarterly averages with change deltas.

## Worked example

- Availability: 4 (High)
- Integrity: 3 (High)
- Control: 2 (Medium)
- Authenticity: 3 (Medium)

Then:

- Non-repudiation ($I\oplus C\oplus Au$) = score 2, confidence Medium
- Reliability ($A\oplus I\oplus C\oplus Au$) = score 2, confidence Medium
