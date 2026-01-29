# Maturity levels in the CISQ security model

| ![CISQ security model version 1.0](CISQ-simplified-large.png)                   |
|                      :--:                                                       |
|  *A good place to start: CISQ security model v1.0, Maturity level 2 simplified* |

## Introducing the model

The Composing Information Security Qualities (CISQ) model is created by combining insights and definitions from the [CIA triad](https://en.wikipedia.org/wiki/Information_security#CIA_triad), [Parkerian Hexad](https://en.wikipedia.org/wiki/Parkerian_Hexad), and [STRIDE threat model](https://en.wikipedia.org/wiki/STRIDE_model). The result is a model of four primary security qualities and eleven composed security qualities. Each security quality has a corresponding threat category inspired by the STRIDE threat model. You can read more about previous work on the model here: [CISQ-Model of security qualities](https://acje.github.io/CISQ-model). Please note that previous work on this model may deviate somewhat, as we have made changes to use the most familiar terms for qualities and threats.

The CISQ model describes *security qualities*: positive, naturally emerging qualities we want to preserve in information objects or in the information and behavior of information systems. The CISQ model does not describe systemic qualities that emerge in the relationships between components or within systems, nor does it deal with human-made concepts like legal, ethical, or societal issues. This is why the simplified view of the CISQ model can also be flanked by these two distinct concepts, as shown below.

The CISQ security model can be a bit daunting at first. To make the model more approachable, this document presents a step-by-step maturity model, starting with the four primary qualities and then building on them in a systematic manner.

### Definition of “behavior”

Throughout this document the phrase “information and behavior” is central. Behavior here refers to state transitions and observable actions, in an information system.

## How to use the model

The CISQ model structures the vocabulary of security qualities. These are qualities we want to protect when working with information systems. When performing a risk assessment, as mandated by ISO/IEC 27005, the CISQ model may help when establishing the context and identifying risks. If you use threat modeling to identify risks, CISQ can replace or enhance the STRIDE model.

## Maturity level one

At the first level, the four primary qualities are evaluated in the context of the system. These qualities are important to evaluate for any system, and they form the foundation for all the other security concepts at any maturity level. Note that we refer to the *control quality* here—borrowed from the Parkerian Hexad—not to be confused with security controls.

| ![CISQ security model version 1.0](CISQ-maturity-l1.png) |
|                      :--:                                |
|  *Maturity level one of the CISQ security model*         |

### The four primary security qualities

**Availability** - Timely access to information and behavior

Availability ensures users and systems can access information and execute required behavior when needed, despite failures, demand spikes, or maintenance. It emphasizes capacity, resilience, and graceful degradation by keeping services responsive under stress and recovering quickly when components fail. Strong availability practices combine demand forecasting and capacity planning, health checks and monitoring, redundancy and failover, load balancing and backpressure, rate limiting and circuit breakers, retry/backoff and queuing, and disaster recovery/business continuity. By preserving availability, teams minimize downtime, sustain essential operations, and maintain user trust.

*Corresponding threat category*: Denial of service — disruption or resource exhaustion preventing timely access

*Typical security controls*: Redundancy, capacity planning, load balancing

**Integrity** - Preserving correctness and completeness of information and behavior

Integrity ensures information and system behavior remain correct, complete, and unaltered from their intended state across storage, transmission, and execution. It focuses on preventing, detecting, and recovering from unauthorized or accidental changes by maintaining invariants and verifying inputs, states, and outputs. Strong integrity practices combine validation and normalization, cryptographic hashes and signatures, transactional guarantees and idempotency, and separation of duties to reduce the chance and impact of tampering. By preserving integrity, teams can trust results, reason about changes, and safely automate decisions and actions.

*Corresponding threat category*: Tampering — unauthorized modification compromising correctness or completeness

*Typical security controls*: Input validation, hashing, session management, separation of duties

**Control** - Power to physically or logically influence information and behavior

CISQ’s primary control security quality mirrors "Possession or Control" in the Parkerian Hexad. At its core, the control security quality is all about agency. It concerns the extent to which someone or something can influence an information system. This quality is also special in that it does not apply to widely dispersed information objects and, as such, creates a dichotomy in the CISQ model, with information objects not under exclusive control on one side and information systems on the other side. In modern information systems, control is often shared with other teams and organizations that together exerts exclusive control. Typical situations include cloud hosting or smartphones, where manufacturers, hosting providers, operators, and users all have some degree of influence on the systems. Effectively managing control prevents unauthorized manipulation and limits the blast radius when barriers fail.

*Corresponding threat category*: Elevation of privilege — unauthorized gain of permissions enabling control, break‑glass workflows

*Typical security controls*: Principle of least privilege, patch management, logging and auditing, secure enclaves

**Authenticity** - Information and behavior originate from their purported source

Authenticity ensures information and system behavior truly originate from the claimed source and remain bound to that identity across creation, transmission, and execution. It focuses on identity proofing and binding, mutual verification, and provenance, resisting impersonation, spoofing, and forged artifacts. Strong authenticity practices combine robust identity lifecycle (enrollment, proofing, rotation, revocation), secure channels and token binding, and tamper‑evident logs to establish source and lineage. By preserving authenticity, teams can trust who or what produced actions and data, enabling accountable automation and safe delegation.

*Corresponding threat category*: Spoofing — impersonation of identities or sources

*Typical security controls*: Multi-factor authentication (MFA), signatures, certificate management and pinning, mutual transport layer security (mTLS)

## Maturity level two

At maturity level two, we introduce some common higher-order qualities that are composed of the control quality and two of the other three primary qualities from maturity level one.

| ![CISQ security model version 1.0](CISQ-maturity-l2.png) |
|                      :--:                                |
|  *Maturity level two of the CISQ security model*         |

Maturity level two can be represented in the simplified view.

| ![CISQ security model version 1.0](CISQ-transformation.png)                                       |
|                      :--:                                                                         |
|  *The CISQ security model has a base view covering all maturity levels and a simplified overview* |

Together with related perspectives, this is a useful representation and starting point for most teams managing information systems. The higher maturity levels are meant for security professionals and infrastructure or platform teams focusing on a deeper understanding of their security posture.

| ![CISQ security model version 1.0](CISQ-L2-Overview.png)           |
|                      :--:                                          |
|  *CISQ security model v1.0, Maturity level 2, simplified overview* |

**Utility** – Ability to maintain information and behavior

*Corresponding threat category*: Information contortion — distortion or incompatibility reducing ability to maintain or use

*Typical security controls*: API management, semantic versioning, type checks, independently deployable components

**Confidentiality** - Access to information and behavior is limited exclusively to authorized entities

*Corresponding threat category*: Information disclosure — unauthorized exposure of information or behavior

*Typical security controls*: Encryption, access control lists (ACLs), data loss prevention (DLP), data classification policies

**Non-repudiation** - Assurance of the correctness, completeness, and origin of information and behavior

*Corresponding threat category*: Repudiation — denial of actions or origins

*Typical security controls*: Signatures, public key infrastructure (PKI), audit trails and logs, message authentication codes (MACs), digital contracts, hashing, trusted third parties

## Maturity level three

At maturity level three, we introduce more accurate definitions of concepts. Increasing your depth of conceptual understanding may help you develop and categorize security controls (not to be confused with the *control quality* in the CISQ model).

| ![CISQ security model version 1.0](CISQ-maturity-l3.png) |
|                      :--:                                |
|  *Maturity level three of the CISQ security model*       |

**Authorization** – Power to grant access to information and behavior

*Corresponding threat category*: (review threat: Authorization is the capacity to grant access) Traffic manipulation — interception or alteration of communications affecting access decisions

*Typical security controls*: DDoS protection, rate limiting, traffic scrubbing and shaping (e.g., ACLs, WAFs)

**Durability** – Ability to withstand degradation of the integrity of information and behavior

*Corresponding threat category*: Data corruption — integrity degradation of stored or transmitted data

*Typical security controls*: Automatic rebuilding, forward error correction (FEC), error correction codes (ECC)

**Credibility** – Ability to verify information and behavior

*Corresponding threat category*: Misinformation — deceptive or misleading content undermining verification

*Typical security controls*: Cryptographic signatures, certificate pinning, PKI validation, trusted timestamping, source verification policies, tamper-evident logging, content validation workflows, reputation/trust lists

**Certifiability** – Ability to prove the validity of information and behavior

*Corresponding threat category*: Invalid attestation — unverifiable or untrusted proofs of validity

*Typical security controls*: Third‑party audits and certifications (ISO, SOC 2), attestation frameworks (TPM/TEE remote attestation), formal verification/conformance testing, reproducible builds, SBOMs and supply chain attestations, notarization/trusted registries

**Assurance** – Ability to positively confirm information and behavior

*Corresponding threat category*: Unverified behavior — insufficient evidence to confirm claims or outcomes

*Typical security controls*:

**Traceability** – Ability to discover where and how information and behavior were produced

*Corresponding threat category*: Obfuscation — concealed provenance or tampered production trails

*Typical security controls*: Structured logging with correlation IDs, distributed tracing (OpenTelemetry), append‑only/immutable logs, cryptographic log signing, data lineage catalogs, version control and change history, chain‑of‑custody procedures

**Usefulness** – Ability to work with the format of information and behavior

*Corresponding threat category*: Data misformatting — incompatible, ambiguous, or malformed representations

*Typical security controls*: Schema registries and data dictionaries, strict typing and validation, canonical data models, format normalization and conversion, API versioning, compatibility testing

## Maturity level four

At level four, we define the sole quality composing all four primary qualities. The most prominent systems to create technical guarantees for all four qualities would be smart contracts running on blockchains. However, it is not necessary for all qualities to be technical guarantees. Many organizations deliver very good reliability as a combination of technical, process, and organizational measures. Financial institutions are typical examples of such systems where all aspects come together to create a level of trust where customers are happy to hand over control of their assets to these organizations.

| ![CISQ security model version 1.0](CISQ-maturity-l4.png) |
|                      :--:                                |
|  *Maturity level four of the CISQ security model*        |

**Reliability** – Trustworthy information and behavior

*Corresponding threat category*: Dependability loss — systemic failures reducing trust in outcomes

*Typical security controls*: Transactional integrity, idempotency, distributed consensus, circuit breakers and retry/backoff, disaster recovery and business continuity plans, chaos engineering

## Resources

[Download Excalidraw file](CISQ.excalidraw)

## Qualities, Threat Categories, and MITRE ATT&CK Tactics

| Quality | Threat Category | MITRE ATT&CK Tactics |
|---|---|---|
| Availability | Denial of service | Impact |
| Integrity | Tampering | Execution, Impact |
| Control | Elevation of privilege | Discovery, Privilege Escalation, Persistence |
| Authenticity | Spoofing | Reconnaissance, Resource Development, Initial Access, Defense Evasion |
| Utility | Information contortion | Impact |
| Confidentiality | Information disclosure | Collection, Exfiltration, Lateral Movement |
| Non-repudiation | Repudiation | Defense Evasion |
| Authorization | Traffic manipulation | Credential Access, Command and Control |
| Durability | Data corruption | Impact |
| Credibility | Misinformation | Impact |
| Certifiability | Invalid attestation | Defense Evasion |
| Assurance | Unverified behavior | Defense Evasion |
| Traceability | Obfuscation | Defense Evasion |
| Usefulness | Data misformatting | Impact |
| Reliability | Dependability loss | Impact |
