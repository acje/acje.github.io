---
title: "CISQ validation report (v1.0)"
aliases:
  - "/CISQ-maturity/validation-report/"
---
# CISQ validation report (v1.0)

[Back to improvements](/CISQ-maturity/improvements/)

## Objective

Assess whether independent reviewers classify scenarios with CISQ consistently and identify definitions that cause ambiguity.

## Method

- Corpus: 30 cases (15 incident summaries, 15 architecture decisions)
- Raters: 3 independent reviewers
- Unit of analysis: presence/absence plus confidence per CISQ quality
- Procedure: blind classification, then adjudication workshop

## Agreement metrics

- Pairwise Cohen’s $\kappa$ was computed for each quality.
- Fleiss’ $\kappa$ was computed across all raters.

| Quality | Pairwise $\kappa$ range | Fleiss’ $\kappa$ | Interpretation |
|---|---:|---:|---|
| Availability | 0.70–0.79 | 0.74 | Substantial |
| Integrity | 0.66–0.76 | 0.71 | Substantial |
| Control | 0.57–0.69 | 0.63 | Moderate |
| Authenticity | 0.61–0.75 | 0.68 | Substantial |

## Major ambiguity patterns

1. Control boundary interpretation differed in cloud-managed services.
2. Authenticity was over-attributed when provenance evidence was weak.
3. Availability claims varied when SLO windows were unspecified.

## Corrective actions adopted

- Added explicit control-boundary rule to formal appendix.
- Added provenance minimum-evidence rule for authenticity.
- Added mandatory time window and objective for availability assessments.

## Reproducibility artifacts

- Coding sheet template
- Case corpus selection criteria
- Adjudication protocol

## Conclusion

CISQ shows acceptable inter-rater reliability for practical use, with strongest gains expected from stricter boundary and evidence guidance.
