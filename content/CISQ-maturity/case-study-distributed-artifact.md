---
title: "CISQ case study: distributed software artifact"
aliases:
  - "/CISQ-maturity/case-study-distributed-artifact/"
---
# CISQ case study: distributed software artifact

[Back to improvements](/CISQ-maturity/improvements/)

## Context

An open-source command-line tool is distributed via public package registries and release binaries. Consumers include enterprise CI pipelines.

## Scope and assumptions

- Scope: artifact publication and verification lifecycle
- Assessment period: latest major release cycle
- Objective: maximize integrity/authenticity in public distribution context

## Primary quality assessment

- Availability: 3 (Medium)
  - Evidence: mirror uptime and release hosting continuity
- Integrity: 5 (High)
  - Evidence: reproducible builds, checksums, tamper detection
- Control: 2 (Medium)
  - Evidence: shared maintainer model with limited infrastructure control
- Authenticity: 4 (High)
  - Evidence: signed tags, release signatures, maintainer key policy

## Composed quality outcomes

- Traceability ($I\oplus Au$): 4 (High)
- Certifiability ($A\oplus I\oplus Au$): 3 (Medium)
- Reliability ($A\oplus I\oplus C\oplus Au$): 2 (Medium)

## Key findings

1. Integrity and authenticity are strong despite limited centralized control.
2. Reliability is constrained by control and hosting dependency concentration.
3. Consumer trust improves significantly with transparent provenance records.

## Improvement actions

- Add secondary release mirrors with documented failover ownership.
- Require threshold signing for maintainer release approvals.
- Publish machine-readable provenance attestations with each release.

## Reassessment trigger

Reassess after threshold signing rollout and mirror failover test completion.
