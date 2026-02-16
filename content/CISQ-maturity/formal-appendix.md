---
title: "CISQ formal notation appendix"
aliases:
  - "/CISQ-maturity/formal-appendix/"
---
# CISQ formal notation appendix

[Back to improvements](/CISQ-maturity/improvements/)

## Scope

This appendix defines minimal formal semantics for the CISQ primary qualities and composition.

## Domain and predicates

Let $x$ be an assessed target (information object or system behavior).

- $A(x)$: Availability holds for $x$
- $I(x)$: Integrity holds for $x$
- $C(x)$: Control holds for $x$
- $Au(x)$: Authenticity holds for $x$

A composed quality $Q_S$ is defined by a subset $S \subseteq \{A, I, C, Au\}$ and evaluates to true when all included predicates hold:
$$
Q_S(x) = \bigwedge_{p \in S} p(x)
$$

## Composition operator

Define composition as set union over predicate symbols:
$$
Q_{S_1} \oplus Q_{S_2} = Q_{S_1 \cup S_2}
$$

### Properties

- Commutative: $Q_{S_1} \oplus Q_{S_2} = Q_{S_2} \oplus Q_{S_1}$
- Associative: $(Q_{S_1} \oplus Q_{S_2}) \oplus Q_{S_3} = Q_{S_1} \oplus (Q_{S_2} \oplus Q_{S_3})$
- Idempotent: $Q_S \oplus Q_S = Q_S$
- Identity element: $Q_{\emptyset}$
- Closure: $S_1 \cup S_2 \subseteq \{A,I,C,Au\}$

## Normative interpretation constraints

- Unknown provenance implies $Au(x)=\text{false}$ unless corroborating evidence exists.
- Shared operation in cloud/partner environments can still satisfy $C(x)$ if control boundary and authority are explicitly enumerated.
- Availability is assessed over a declared interval $T$ and service objective $\theta$; $A(x)$ is true only if the objective is met during $T$.

## Composition table (symbolic + prose)

| CISQ quality | Symbolic composition | Predicate form |
|---|---|---|
| Availability | $Q_{\{A\}}$ | $A(x)$ |
| Integrity | $Q_{\{I\}}$ | $I(x)$ |
| Control | $Q_{\{C\}}$ | $C(x)$ |
| Authenticity | $Q_{\{Au\}}$ | $Au(x)$ |
| Authorization | $Q_{\{A,C\}}$ | $A(x) \land C(x)$ |
| Durability | $Q_{\{I,C\}}$ | $I(x) \land C(x)$ |
| Credibility | $Q_{\{C,Au\}}$ | $C(x) \land Au(x)$ |
| Assurance | $Q_{\{A,I\}}$ | $A(x) \land I(x)$ |
| Traceability | $Q_{\{I,Au\}}$ | $I(x) \land Au(x)$ |
| Utility | $Q_{\{A,I,C\}}$ | $A(x) \land I(x) \land C(x)$ |
| Confidentiality | $Q_{\{A,C,Au\}}$ | $A(x) \land C(x) \land Au(x)$ |
| Non-repudiation | $Q_{\{I,C,Au\}}$ | $I(x) \land C(x) \land Au(x)$ |
| Certifiability | $Q_{\{A,I,Au\}}$ | $A(x) \land I(x) \land Au(x)$ |
| Reliability | $Q_{\{A,I,C,Au\}}$ | $A(x) \land I(x) \land C(x) \land Au(x)$ |

## Examples and counterexamples

- Example (positive): Signed transaction with verified chain of custody and auditable execution can satisfy $I$, $Au$, and $C$.
- Counterexample: Unsigned log export from unknown source cannot satisfy $Au$ even if format is correct.
- Counterexample: Service with undefined SLO cannot claim $A$ in a reproducible way.
