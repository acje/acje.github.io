---
title: "CISQ case study: enterprise payment service"
aliases:
  - "/CISQ-maturity/case-study-enterprise-service/"
---
# CISQ case study: enterprise payment service

[Back to improvements](/CISQ-maturity/improvements/)

## Context

A regional payment API processes card-not-present transactions for e-commerce merchants. The service runs across two cloud regions and integrates with fraud scoring and settlement systems.

## Scope and assumptions

- Scope: payment authorization and capture workflows
- Assessment period: previous two quarters
- SLO target: 99.95% monthly availability

## Primary quality assessment

- Availability: 4 (High)
  - Evidence: SLO compliance reports, failover drill records
- Integrity: 4 (High)
  - Evidence: signed event streams, idempotency controls, reconciliation checks
- Control: 3 (Medium)
  - Evidence: PAM reviews, break-glass logs; residual vendor dependency risk
- Authenticity: 4 (High)
  - Evidence: mTLS, token binding, hardware-backed key rotation

## Composed quality outcomes

- Non-repudiation ($I\oplus C\oplus Au$): 3 (Medium)
- Confidentiality ($A\oplus C\oplus Au$): 3 (Medium)
- Reliability ($A\oplus I\oplus C\oplus Au$): 3 (Medium)

## Key findings

1. Control boundary with third-party fraud provider reduced confidence.
2. Reliability bottleneck was control maturity, not availability or integrity.
3. Incident recovery quality improved after quarterly game days.

## Improvement actions

- Enforce just-in-time elevated access for operations roles.
- Add contractual attestation requirements for fraud provider controls.
- Expand immutable audit pipeline retention from 90 to 180 days.

## Reassessment trigger

Run reassessment after provider attestation and next access-review cycle.
