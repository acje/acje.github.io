# Maturity levels in the CISQ security model

| ![CISQ security model version 1.0](CISQ.png) |
|                      :--:                    |
|  The CISQ security model version 1.0         |

## Introducing the model

In this post I will lay down how an organization can reason about the security of an information system by traversing maturity levels of the CISQ security model. You can read mode about the model here;
[CISQ-Model of security qualities](https://acje.github.io/CISQ-model)

The CISQ security model can be a bit daunting at first. With its four pilar qualities and a further eleven composed security qualities it totals 15 different concepts.

## Maturity level one

At the first level the four pilar qualities are evaluated in the context of the system. These qualities will be important to evaluate for any system and they make up the foundations for all the other security concepts at any maturity level.

The four pilar security qualities are:

**Availability** - Timely access to information and behavior

**Integrity** - Preserving correctness and completeness of information and behavior

**Control** - Power to physically or logically influence information and behavior

**Authenticity** - Origin of information and behavior is from its purported source

Every security quality has a corresponding threat; denial of service, tampering, elevation of privilege, spoofing.

## Maturity level two

At maturity level two we introduce some common higher order qualities that are composed of two or three pilar qualities from maturity level one.

| ![CISQ security model version 1.0](CISQ-maturity-l2.png) |
|                      :--:                                |
|  Maturity level two of the CISQ security model           |

**Utility** - Usefulness of information and behavior

**Confidentiality** - Access to information and behavior being exclusively limited to authorized entities

**Accountability** - Assurance of the correctness, completeness and origin of information and behavior

The security qualities at level two has these corresponding threats; Information contortion, information disclosure, non-repudiation.

## Maturity level three

Maturity level three is TODO.

At maturity level three we introduce more accurate definition of concepts. Increasing your depth of conceptual understanding may help develop and categorize security controls (not to be confused with the *control quality* in the CISQ model).

**Reliability** – Trustworthy information and behavior

**Sustainability** - Ability to maintain information and behavior

**Authority** - Power to grant access to information and behavior

**Durability** - Ability to withstand integrity degradation of information and behavior

**Credibility** - Verified information and behavior

**Certifiability** - Ability to prove validity of information and behavior

**Assurance** - Positive declaration of information and behavior

**Traceability** - Ability to discover where and how information and behavior was made
