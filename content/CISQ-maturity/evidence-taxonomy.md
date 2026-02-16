---
title: "CISQ evidence taxonomy and scoring instructions"
aliases:
  - "/CISQ-maturity/evidence-taxonomy/"
---
# CISQ evidence taxonomy and scoring instructions

[Back to improvements](/CISQ-maturity/improvements/)

## Evidence types

- Test evidence: unit/integration/e2e tests, conformance tests
- Audit evidence: internal/external audit reports, control attestations
- Operational metrics: SLO reports, incidents, MTTR, error budgets
- Cryptographic evidence: signatures, attestations, verified chains
- Governance evidence: policies, risk acceptance, ownership registers
- Expert judgment: documented rationale by accountable reviewer

## Evidence quality tiers

- Tier 1: narrative only (weak)
- Tier 2: narrative + single artifact (moderate)
- Tier 3: multiple independent artifacts (strong)
- Tier 4: continuous measurement + independent verification (very strong)

## Scoring instructions

1. Score each primary quality first.
2. Assign confidence based on strongest recurring evidence tier.
3. Record at least one evidence item per quality.
4. Downgrade confidence when evidence is stale (> 12 months) or non-representative.
5. Compute composed qualities using rubric aggregation rules.

## Minimum evidence for high confidence

- Availability: 3+ months SLO and incident trend data
- Integrity: tamper detection controls plus verified restoration path
- Control: privileged access review and boundary documentation
- Authenticity: cryptographic or provenance evidence with revocation path
