---
title: "CISQ interoperability crosswalk"
aliases:
  - "/CISQ-maturity/interoperability-crosswalk/"
---
# CISQ interoperability crosswalk

[Back to improvements](/CISQ-maturity/improvements/)

This crosswalk maps CISQ qualities to representative STRIDE threats and commonly associated ISO/IEC 27001 Annex A and NIST SP 800-53 control families.

| CISQ quality | Typical STRIDE alignment | ISO/IEC 27001 Annex A (representative) | NIST SP 800-53 families (representative) |
|---|---|---|---|
| Availability | Denial of Service | Business continuity, ICT readiness, backup, monitoring | CP, SC, SI, IR |
| Integrity | Tampering | Data integrity, secure development, change management | SI, SA, CM, AU |
| Control | Elevation of Privilege | Access control, privileged access management, segregation of duties | AC, IA, CM, AU |
| Authenticity | Spoofing | Identity management, authentication, certificates, key management | IA, SC, AU |
| Confidentiality | Information Disclosure | Cryptography, data masking, transfer protection, data handling | AC, SC, MP, PL |
| Non-repudiation | Repudiation | Logging, evidentiary records, digital signatures | AU, IA, SC |
| Traceability | Repudiation / Tampering | Logging and monitoring, event correlation | AU, SI, IR |
| Reliability | Multi-category | Governance + technical + continuity controls | PM, RA, CP, AC, SC, SI |

## Usage notes

- This mapping is intentionally many-to-many; it is not a control equivalence claim.
- Final compliance mapping should reference organization-specific Statements of Applicability.
- Use this table during context establishment and control design, not as a certification checklist.
