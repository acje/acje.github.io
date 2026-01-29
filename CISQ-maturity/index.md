# Maturity levels in the CISQ security model

| ![CISQ security model version 1.0](CISQ-simplified-large.png)  |
|                      :--:                                      |
|  *CISQ security model v1.0, Maturity level 2 simplified*       |

## Introducing the model

The Composing Information Security Qualities (CISQ) model is created by combining insights and definitions from the [CIA triad](https://en.wikipedia.org/wiki/Information_security#CIA_triad), [Parkerian Hexad](https://en.wikipedia.org/wiki/Parkerian_Hexad), and [STRIDE threat model](https://en.wikipedia.org/wiki/STRIDE_model). The result is a model of four pillar security qualities and eleven composed security qualities. Each security quality has a corresponding threat category inspired by the STRIDE threat model. You can read more about previous work on the model here: [CISQ-Model of security qualities](https://acje.github.io/CISQ-model). Please note that previous work on this model may deviate somewhat, as we have made changes to use the most familiar terms for qualities and threats.

The CISQ model describes *security qualities*: positive, naturally emerging qualities we want to preserve in information objects or in the information and behavior of information systems. The CISQ model does not describe systemic qualities that emerge in the relations between components or within systems, nor does it deal with human-made concepts like legal, ethical, or societal issues. This is why the simplified view of the CISQ model is flanked by these two distinct concepts.

The CISQ security model can be a bit daunting at first. To make the model more approachable, this document presents a step-by-step maturity model, starting with the four pillars and then building on them in a systematic manner.

## How to use the model

The CISQ model structures the vocabulary of security qualities. These are qualities we want to protect when working with information systems. When performing a risk assessment, as mandated by ISO/IEC 27005, the CISQ model may help when establishing the context and identifying risks. If you use threat modeling to identify risks, CISQ can replace or enhance the STRIDE model.

## Maturity level one

At the first level, the four pillar qualities are evaluated in the context of the system. These qualities are important to evaluate for any system, and they form the foundation for all the other security concepts at any maturity level. Note that we talk about the *control quality* here, borrowed from the Parkerian Hexad, not to be confused with security controls.

| ![CISQ security model version 1.0](CISQ-maturity-l1.png) |
|                      :--:                                |
|  *Maturity level one of the CISQ security model*         |

The four pillar security qualities are:

**Availability** - Timely access to information and behavior

*Corresponding threat category*: Denial of service

*Typical security controls*: Redundancy, capacity planning, rate limiting, traffic scrubbing and shaping (e.g., ACLs, WAFs), load balancing

**Integrity** - Preserving correctness and completeness of information and behavior

*Corresponding threat category*: Tampering

*Typical security controls*: Input validation, hashing, session management, separation of duties

**Control** - Power to physically or logically influence information and behavior

*Corresponding threat category*: Elevation of privilege

*Typical security controls*: Principle of least privilege, patch management, logging and auditing

**Authenticity** - Information and behavior originate from their purported source

*Corresponding threat category*: Spoofing

*Typical security controls*: Multi-factor authentication (MFA), signatures, certificates

## Maturity level two

At maturity level two, we introduce some common higher-order qualities that are composed of the control quality and two of the other three pillar qualities from maturity level one.

| ![CISQ security model version 1.0](CISQ-maturity-l2.png) |
|                      :--:                                |
|  *Maturity level two of the CISQ security model*         |

Maturity level two can be represented in the simplified view.

| ![CISQ security model version 1.0](CISQ-transformation.png)                                       |
|                      :--:                                                                         |
|  *CISQ security model has a base view implementing all maturity levels and a simplified overview* |

Together with related perspectives, this is a useful representation and starting point for most teams managing information systems. The higher maturity levels are meant for security professionals and infrastructure or platform teams focusing on a deeper understanding of their security posture.

| ![CISQ security model version 1.0](CISQ-L2-Overview.png)           |
|                      :--:                                          |
|  *CISQ security model v1.0, Maturity level 2, simplified overview* |

**Utility** – Ability to maintain information and behavior

*Corresponding threat category*: Information contortion

*Typical security controls*: API management, semantic versioning, type checks, independently deployable components

**Confidentiality** - Access to information and behavior is limited exclusively to authorized entities

*Corresponding threat category*: Information disclosure

*Typical security controls*: Encryption, access control lists (ACLs), data loss prevention (DLP), data classification policies

**Non-repudiation** - (Accountability) Assurance of the correctness, completeness, and origin of information and behavior

*Corresponding threat category*: Repudiation

*Typical security controls*: Signatures, public key infrastructure (PKI), audit trails and logs, message authentication codes (MACs), digital contracts, hashing, trusted third parties

## Maturity level three

At maturity level three, we introduce more accurate definitions of concepts. Increasing your depth of conceptual understanding may help you develop and categorize security controls (not to be confused with the *control quality* in the CISQ model).

| ![CISQ security model version 1.0](CISQ-maturity-l3.png) |
|                      :--:                                |
|  *Maturity level three of the CISQ security model*       |

**Authority** – Power to grant access to information and behavior

*Corresponding threat category*: Traffic manipulation

*Typical security controls*: DDoS protection, rate limiting

**Durability** – Ability to withstand degradation of the integrity of information and behavior

*Corresponding threat category*: Data corruption

*Typical security controls*: Automatic rebuilding, forward error correction (FEC), error correction codes (ECC)

**Credibility** – Ability to verify information and behavior

*Corresponding threat category*: Misinformation

*Typical security controls*:

**Certifiability** – Ability to prove the validity of information and behavior

*Corresponding threat category*:

*Typical security controls*:

**Assurance** – (Assurability) Ability to positively confirm information and behavior

*Corresponding threat category*:

*Typical security controls*:

**Traceability** – Ability to discover where and how information and behavior were produced

*Corresponding threat category*:

*Typical security controls*:

**Usefulness** – Ability to work with the format of information and behavior

*Corresponding threat category*:

*Typical security controls*:

## Maturity level four

At level four, we define the sole quality composing all four pillar qualities. The most prominent systems to create technical guarantees for all four qualities would be smart contracts running on blockchains. However, it is not necessary that all qualities are technical guarantees. Many organizations deliver very good reliability as a combination of technical, process, and organizational measures. Financial institutions are typical examples of such systems where all aspects come together to create a level of trust where customers are happy to turn over control of their assets to these organizations.

**Reliability** – Trustworthy information and behavior

*Corresponding threat category*:

*Typical security controls*:

## Resources

[Download Excalidraw file](CISQ.excalidraw)
