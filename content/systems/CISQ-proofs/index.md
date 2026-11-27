---
title: "CISQ proofs: validating the security qualities"
description: "A proof atlas for the fifteenth term Composing Information Security Qualities (CISQ) model, applying five proof methods and mapping weak and strong logical equivalents."
aliases:
  - "/CISQ-proofs/"
date: 2026-11-27
lastmod: 2026-11-27
homeFeatured: true
weight: 100
---

## Validity, not acceptance

This page is a **proof atlas** for the *Composing Information Security Qualities* (CISQ) model
described in the companion [CISQ maturity levels](/systems/cisq-maturity/) post. It applies five
proof methods to all **fifteen** composed qualities and records, for each, its **weak and strong
logical equivalents** — the terms it is nearly the same as, and the terms it is genuinely
different from.

Two things are true at once here and worth stating up front:

1. **Each of the fifteen cells is a distinct subset** of the four primaries, so as a *lattice* the
   model has exactly 15 cells.
2. **Being a distinct subset is not the same as being a distinct capability.** Two cells can
   denote the same real-world capability under two labels. This page separates the *lattice*
   (15 cells) from the *capability set* (which the audit could not prove to be 15 distinct).

The conclusions are deliberately hedged. A counterexample *refutes* a claim; it does not *prove*
a universal. Where the evidence settles a check, the verdict is **PASS** or **PASS\***; where a
definition has to be tightened first, it is **AT-RISK**; where the available arguments do not
settle it, it is **OPEN**.

---

## The model under audit

CISQ is built from four primary security qualities, each with a STRIDE-derived threat:

| Primary | Symbol | Definition | Corresponding threat |
|---|---|---|---|
| Availability | **A** | timely access to information and behavior | denial of service |
| Integrity | **I** | correctness and completeness preserved | tampering |
| Control | **C** | power to physically or logically influence information and behavior | elevation of privilege |
| Authenticity | **Au** | information and behavior originate from their purported source | spoofing |

A composed quality is a non-empty subset joined by **⊕**, defined as an *interlocking dependency*
(chain-link): each primary actively conditions the others, and if any single link fails the
higher-order capability collapses. With four primaries there are exactly **2⁴ − 1 = 15**
non-empty subsets; the 16th variant (the empty set) is excluded.

Counting subsets establishes coverage of the *possible combinations*, not completeness as a
taxonomy of capabilities. Distinct capabilities can coexist; the relevant test is whether one can
hold without the other, not whether their subsets are disjoint.

### The fifteen qualities

| # | Quality | Composition | Threat | Verdict |
|---|---|---|---|---|
| 1 | Availability | A | Denial of service | PASS |
| 2 | Integrity | I | Tampering | PASS |
| 3 | Control | C | Elevation of privilege | PASS\* |
| 4 | Authenticity | Au | Spoofing | PASS |
| 5 | Utility | A ⊕ I ⊕ C | Information contortion | AT-RISK |
| 6 | Confidentiality | A ⊕ C ⊕ Au | Information disclosure | AT-RISK |
| 7 | Non-repudiation | I ⊕ C ⊕ Au | Repudiation | PASS |
| 8 | Authorization | A ⊕ C | Broken access control | AT-RISK |
| 9 | Stewardship | I ⊕ C | Corrupting change | FIT |
| 10 | Attributability | C ⊕ Au | Misattribution | FIT\* |
| 11 | Certifiability | A ⊕ I ⊕ Au | Invalid attestation | PASS |
| 12 | Assurance | A ⊕ Au | Unverified behavior | AT-RISK |
| 13 | Traceability | I ⊕ Au | Obfuscation | AT-RISK |
| 14 | Usefulness | A ⊕ I | Data misformatting | AT-RISK |
| 15 | Reliability | A ⊕ I ⊕ C ⊕ Au | Dependability loss | PASS |

> The two terms in **bold** — **Stewardship** and **Attributability** — are the relabeled cells.
> The audit found their predecessors (Durability and Credibility) were the two cells that did not
> survive as distinct under the current definitions. See §7. Their verdicts come from a
> fit-verification aimed specifically at the defects that removed the old labels.

---

## The five proof methods

Every check is run against a **fixed** system or object: the actors whose agency counts, the
operation, and the evaluation conditions. A composition needs **both directions**: the capability
implies each listed primary (M2), and the listed primaries jointly imply the capability (M3). An
example can refute either implication or demonstrate realizability; it cannot by itself prove a
universal claim.

### M1 — Adversarial counterexample (threat mapping)
Look for an observable failure when a link is attacked. Find a scenario where one capability fails
and the other survives. A shared failure mode is worth investigating but does *not* establish
equivalence — one incident can break several different capabilities.

### M2 — Necessity testing (subtraction)
The chain-link premise, checked one link at a time: **can the capability still hold when a listed
primary does not?** A counterexample refutes the necessity of that primary. A missing primary does
not belong in this test; if it turns out to be required, the listed set fails sufficiency instead.

### M3 — Sufficiency testing (isolation)
The converse: **do the listed primaries together guarantee the capability?** Test whether the
capability can fail even with all listed primaries in place, especially when the excluded ones do
not hold. Such a counterexample refutes sufficiency, but does not by itself identify which extra
condition is required.

### M4 — Orthogonal distinction (pairwise contrast)
Compare a composition with one that adds or removes exactly **one** primary. A scenario where one
capability holds and the other fails shows the two are distinct. Contrasting a cell with a ±1
neighbour isolates exactly what that single differing link contributes.

### M5 — Operational construction (architecture walkthrough)
Walk through a minimal system and check which primaries and capabilities it actually realizes. A
construction that realizes the intended combination shows it is possible. A failed construction
exposes a problem with that example; it does not rule out all implementations.

---

## Proofs for each quality

### 1. Availability — A
Timely access to information and behavior. Atomic reference link; there is no composition to
subtract from.
- **M1** — A denial-of-service or resource-exhaustion event breaks timely access. This is the
  model's reference failure.
- **M2 / M3** — Not applicable (single primary; nothing to subtract, and the primary is the
  capability). **M4** — Contrast with Usefulness (A⊕I) and Assurance (A⊕Au): those fail on
  format/evidence, not on timeliness, so availability is separable.
- **M5** — A load-balanced service with capacity planning and failover realizes availability
  without any of the other primaries.
- **Verdict: PASS** (reference link).

### 2. Integrity — I
Correctness and completeness preserved. Atomic reference link.
- **M1** — Tampering breaks correctness/completeness. Reference failure.
- **M2 / M3** — Not applicable. **M4** — Contrast with Stewardship (I⊕C) and Traceability (I⊕Au):
  stewardship needs a *change*, traceability needs a *trail*; neither is the integrity state alone.
- **M5** — Input validation, hashing and separation of duties preserve integrity with no agency
  requirement and no source binding.
- **Verdict: PASS** (reference link).

### 3. Control — C
Power to physically or logically influence information and behavior. Atomic link.
- **M1** — Elevation of privilege is the model's reference failure.
- **M2 / M3** — Not applicable. **M4** — Contrast with Authorization (A⊕C) and Stewardship (I⊕C):
  both scope control to a *grant* or a *preserving change*; bare control is the agency itself.
- **M5** — Least-privilege, patch management and secure enclaves realise control.
- **Verdict: PASS\*** (system-only quality). Control is special: it does not apply to widely
  dispersed information objects, creating the post's object/system dichotomy. This is a definitional
  scope caveat, not a composition defect.

### 4. Authenticity — Au
Information and behavior originate from their purported source. Atomic link.
- **M1** — Spoofing is the reference failure.
- **M2 / M3** — Not applicable. **M4** — Contrast with Attributability (C⊕Au) and Traceability
  (I⊕Au): authenticity needs no *effective change* and no *immutable trail*.
- **M5** — Identity proofing, MFA and mTLS realise authenticity.
- **Verdict: PASS** (reference link).

### 5. Utility — A ⊕ I ⊕ C
Ability to maintain information and behavior.
- **M1** — Information *contortion* (distortion/incompatibility) is its threat; this overlaps
  Usefulness' *misformatting* (see §6), a wording distinction not a capability one. **AT-RISK**.
- **M2** — Without A nothing is reachable to operate on; without I state is untrustworthy and
  maintenance collapses; without C there is no agency to change or evolve. All three hold. ✓
- **M3** — A⊕I⊕C generally suffices for maintainability, *provided* the definition of "maintain"
  excludes an availability of *input format* (else it drifts into Usefulness). **PASS\***.
- **M4** — Remove A and you get Stewardship (I⊕C, change-preservation without operability) —
  distinct. **M5** — Semantic versioning, type checks and independently deployable components
  realise it.
- **Verdict: AT-RISK** (definitional; the contortion/misformatting disjunction).

### 6. Confidentiality — A ⊕ C ⊕ Au
Information conditionally available to a set of authenticated entities.
- **M1** — Information disclosure. **AT-RISK** because it overlaps Authorization (its M4 contrast
  separates them only by Au).
- **M2** — Without Au you cannot identify who is authorised (fail-open discloses); without C you
  cannot enforce the disclosure boundary; without A the conditional-availability gate is
  unavailable. **PASS\***.
- **M3** — A⊕C⊕Au suffices *provided* "authenticated entities" is read as an actual access grant,
  else the Control link is doing the work alone. **PASS\***.
- **M4** — Contrast with Authorization (A⊕C): adding Au to A⊕C turns "power to grant" into
  "disclosure bounded to authenticated principals". Distinct. **M5** — Encryption, ACLs, DLP and
  data classification realise it.
- **Verdict: AT-RISK** (adjacency to Authorization).

### 7. Non-repudiation — I ⊕ C ⊕ Au
Assurance of the correctness, completeness and origin of information and behavior. The model's
strongest worked example.
- **M1** — Repudiation (denial of action or origin). **PASS**.
- **M2** — Without Integrity the origin is known but the payload may have been altered; without
  Authenticity the message is intact but its origin unverified; without Control an unauthorised
  party may have accessed keys or the environment. All three hold. ✓
- **M3** — I⊕C⊕Au suffices: the three-way collapse above is exactly what the post documents.
  **PASS**. **M4** — Contrast with Attributability (C⊕Au): non-repudiation adds Integrity, so
  it is strictly stronger. **M5** — Signatures, PKI, audit trails and MACs realise it.
- **Verdict: PASS** (the post's strongest chain-link case).

### 8. Authorization — A ⊕ C
Power to grant access to information and behavior.
- **M1** — Broken access control. **AT-RISK**.
- **M2** — Without C there is no power to grant; without A the decision must still be evaluable
  (deny-by-default). The Availability link is the *weakest*: a pre-provisioned grant holds even if
  the granter is offline. **AT-RISK**.
- **M3** — A⊕C holds only if the word "grant" implies the decision point is reachable; otherwise
  the Availability link is inert. **AT-RISK**.
- **M4** — Add Au to get Confidentiality (disclosure-scoped to authentic principals) — distinct.
  **M5** — RBAC/ABAC, deny-by-default, tenant isolation and entitlement reviews realise it.
- **Verdict: AT-RISK** (the Availability link needs a "decision must be evaluable" framing).

### 9. Stewardship — I ⊕ C
Ability to change information and behavior while preserving specified correctness and completeness
invariants. *(Relabeled from Durability; see §7.)*
- **M1** — A corrupting *change* (an effective change violating an invariant). Its shared mode with
  Tampering (I) is expected — Stewardship ⊇ I — but a shared mode is not equivalence. **Distinct.**
- **M2** — Without C a correct configuration may remain unchanged (no active change); without I
  changes need not preserve invariants. **Both necessary — and C is load-bearing**, which is
  exactly what the old "Durability" lacked. ✓
- **M3** — I⊕C suffices provided I holds *through* the change C enables, not merely for an
  untouched copy. **PASS\***. Neither A nor Au is required.
- **M4** — +C over Integrity turns passive correctness into active change-preservation; +I over
  Control turns generic agency into correctness-scoped agency. **Clean**. **M5** — A transactional,
  versioned change path that enforces invariants on every update realises it, without source
  binding (Au) or timeliness (A).
- **Verdict: FIT** (loads exactly {I, C}; C is the active agency that the passive "withstand
  degradation" label failed to carry).

### 10. Attributability — C ⊕ Au
Ability to effect a change through an action tied to its actual source. *(Relabeled from
Credibility; see §7.)*
- **M1** — Misattribution: an effective action is tied to the wrong source, even though the
  resulting configuration is valid. **Distinct** (from misinforming, from repudiation, from
  tampering).
- **M2** — Without C, attributing a passive observation is not effecting a change; without Au the
  change is not tied to its actual source. **Both necessary.** ✓
- **M3** — A genuine action can be attributable despite an incomplete result and a missed deadline,
  so no excluded primary (I, A) is required. **PASS\*** with the caveat that "actual source" must be
  read as *the source of an effected change*, not tamper-evident *verification* of that source
  (which would drag in I and drift toward Traceability/Non-repudiation).
- **M4** — +Au over Control binds power to a genuine source; +C over Authenticity turns a genuine
  source into one that *effects* a change. Contrast with Non-repudiation (I⊕C⊕Au) shows it is
  weaker — no content-correctness requirement. **Clean**. **M5** — An authenticated change path
  bound to a verified acting principal, without enforcing every configuration invariant, realises it.
- **Verdict: FIT\*** (loads exactly {C, Au}; the source-binding reading must be fixed — the caveat
  the audit flagged for the old "Credibility").

### 11. Certifiability — A ⊕ I ⊕ Au
Ability to prove the validity of information and behavior.
- **M1** — Invalid attestation. **PASS**.
- **M2** — Without I the attestation is invalid; without Au the proof is untrusted; without A the
  attestation must be available/current to verify. All hold. ✓
- **M3** — A⊕I⊕Au suffices; Control is *deliberately excluded* — a third party can certify validity
  without holding control. **PASS**. **M4** — Contrast with Non-repudiation (I⊕C⊕Au) and Reliability:
  certification needs no agency. **PASS**. **M5** — Third-party audits, TPM/TEE remote attestation,
  reproducible builds and SBOMs realise it.
- **Verdict: PASS**.

### 12. Assurance — A ⊕ Au
Ability to positively confirm information and behavior.
- **M1** — Unverified behavior. **AT-RISK**.
- **M2** — Without A there is nothing observable to confirm; without Au the evidence is not from a
  trusted source. **AT-RISK** (the Availability link is loose).
- **M3** — A⊕Au suffices only if Assurance is scoped as *evidence of behavior*, not correctness.
  **PASS\***. **M4** — Add I to get Certifiability (proof of validity); add C to get Confidentiality.
  **PASS**. **M5** — Conformance tests, runtime assertions and SLO/SLA health checks realise it.
- **Verdict: AT-RISK** (scope it as "evidence", not correctness, and the Availability link is
  sound).

### 13. Traceability — I ⊕ Au
Ability to discover where and how information and behavior were produced.
- **M1** — Obfuscation. **AT-RISK**.
- **M2** — Without I the trail is alterable; without Au the trail cannot be attributed to a real
  source. **PASS**. **M3** — I⊕Au suffices. **PASS**.
- **M4** — The model's own Authenticity definition ("information originate from their purported
  source") already includes provenance, so the distinctness of Traceability from Authenticity is
  **not established**. **AT-RISK**.
- **M5** — Structured logging, immutable logs, data lineage catalogs and chain-of-custody realise it.
- **Verdict: AT-RISK** (overlaps the post's Authenticity definition; the distinction must be made
  explicit).

### 14. Usefulness — A ⊕ I
Ability to work with the format of information and behavior.
- **M1** — Data misformatting. **AT-RISK**.
- **M2** — Without I the format is corrupted and cannot interoperate; without A it must be present
  to "work with" (weakest link). **AT-RISK**.
- **M3** — A⊕I suffices *provided* "work with" means representational compatibility and not
  completeness of content (which is Integrity). **PASS\***. **M4** — Add C to get Utility
  (maintainability); add Au to get Certifiability. **PASS**. **M5** — Schema registries, strict
  typing, canonical data models and compatibility testing realise it.
- **Verdict: AT-RISK** ("format" vs "completeness"; the Availability link needs shoring).

### 15. Reliability — A ⊕ I ⊕ C ⊕ Au
Trustworthy information and behavior. The full-set composition; the strongest construction.
- **M1** — Dependability loss. **PASS**.
- **M2** — Without any one of the four it is untrustworthy (unavailable / corrupt / no agency / not
  from a trusted source). **PASS**. **M3** — All four jointly suffice. **PASS**. **M4** — Removing
  any one primary yields exactly the four adjacent cells — all weaker. **PASS**. **M5** — The
  post's smart-contract and financial-institution examples realise it.
- **Verdict: PASS** (the full chain-link case; also the top of the lattice, so it entails every
  other quality).

---

## Weak and strong logical equivalents

Two relations matter. **Strong (co-extensive)** means two terms denote the *same* capability —
each implies the other. **Weak** means either they are *adjacent* (their compositions differ by
exactly one primary) or one is *strictly stronger/weaker* (a strict superset/subset, so one
entails the other). The composition order in the table is the post's order; the set relations are
order-independent.

> **Strong equivalence requires two distinct cells to denote one capability.** Because each of the
> 15 cells is a distinct subset of the four primaries, **no two *published* terms in the current
> model are co-extensive.** The two candidates the audit found (see §7) were *definitional* —
> Credibility and Durability — and the relabel was made precisely to remove them. So the strong
> column is empty for every term under the current labels; it is the *lattice* that guarantees
> distinctness, not the *capability semantics*, and the latter is not proven.

| Quality | Composition | Strong equivalent | Weak — adjacent (±1) | Weak — strictly stronger (entails it) |
|---|---|---|---|---|
| Availability | A | — | Usefulness, Authorization, Assurance | Utility, Confidentiality, Certifiability, Authorization, Assurance, Usefulness, Reliability |
| Integrity | I | — | Usefulness, Stewardship, Traceability | Utility, Non-repudiation, Certifiability, Stewardship, Traceability, Usefulness, Reliability |
| Control | C | — | Authorization, Stewardship, Attributability | Utility, Confidentiality, Non-repudiation, Authorization, Stewardship, Attributability, Reliability |
| Authenticity | Au | — | Assurance, Attributability, Traceability | Confidentiality, Non-repudiation, Certifiability, Assurance, Attributability, Traceability, Reliability |
| Utility | A ⊕ I ⊕ C | — | Stewardship, Authorization, Usefulness | Reliability |
| Confidentiality | A ⊕ C ⊕ Au | — | Attributability, Assurance, Authorization | Reliability |
| Non-repudiation | I ⊕ C ⊕ Au | — | Attributability, Stewardship, Traceability | Reliability |
| Authorization | A ⊕ C | — | Availability, Control, Confidentiality, Utility | Utility, Confidentiality, Reliability |
| Stewardship | I ⊕ C | — | Integrity, Control, Utility, Non-repudiation | Utility, Non-repudiation, Reliability |
| Attributability | C ⊕ Au | — | Control, Authenticity, Confidentiality, Non-repudiation | Confidentiality, Non-repudiation, Reliability |
| Certifiability | A ⊕ I ⊕ Au | — | Usefulness, Assurance, Traceability | Reliability |
| Assurance | A ⊕ Au | — | Availability, Authenticity, Certifiability, Confidentiality | Certifiability, Confidentiality, Reliability |
| Traceability | I ⊕ Au | — | Integrity, Authenticity, Certifiability, Non-repudiation | Certifiability, Non-repudiation, Reliability |
| Usefulness | A ⊕ I | — | Availability, Integrity, Utility, Certifiability | Utility, Certifiability, Reliability |
| Reliability | A ⊕ I ⊕ C ⊕ Au | — | Utility, Confidentiality, Non-repudiation, Certifiability | — (top of lattice) |

### Reading the table

- **Adjacent (weak, ±1):** the closest lattice neighbours — they share all but one primary. These
  are the terms most easily conflated with the one in question, and the audit's M4 contrasts are
  run against them. **Example:** Authorization and Confidentiality differ only by Au; Stewardship
  and Attributability share only C (they differ by I vs Au).
- **Strictly stronger (entails it):** a strict superset, so when that term holds, this one also
  holds. **Reliability is the top of the lattice** and entails every other quality; the four
  primaries are the bottom and are entailed by everything above them. **Example:** Non-repudiation
  (I⊕C⊕Au) is strictly stronger than Attributability (C⊕Au) — it adds Integrity, so it entails
  Attributability but not conversely.
- **Strictly weaker (entailed by it):** the mirror image — strict subsets. A cell implies all the
  terms whose composition is a subset of its own.
- **Strong equivalent:** empty for all published terms. The only co-extensive candidates the audit
  found were the two relabeled cells under their *old* definitions, resolved in §7.

### The one shared-link pair worth isolating

**Stewardship (I⊕C) and Attributability (C⊕Au) share only Control.** They differ by I vs Au. The
audit's walkthrough separates them cleanly: an update that takes effect but misses a required
setting exhibits **Attributability without Stewardship**; an update that preserves every invariant
but is credited to the wrong source exhibits **Stewardship without Attributability**. This is why
they are legitimately two distinct cells and not two names for one capability.

---

## The two relabeled cells

The audit flagged exactly two cells as not-yet-distinct and replaced their definitions. In both
cases the defect was a relationship between the term's composition and an *excluded* or *inert*
primary.

### Durability → Stewardship (I ⊕ C)

**Old definition:** "Ability to **withstand degradation** of the integrity" — *passive*. Redundancy
and error correction (FEC, ECC, S3's 11-nines) preserve data with no actor agency, so **Control is
inert** and the effective requirement set collapses to **{I} = Integrity**. Comparing with Integrity
fixed the fault and the survival conditions; the equivalence was a candidate, not proven.
**Relabel:** Stewardship is *active* — a change requires agency, so **Control is load-bearing** and
the cell no longer collapses.

### Credibility → Attributability (C ⊕ Au)

**Old definition:** "Ability to **verify** information and behavior" — engages the *content*.
Verification necessarily checks correctness/completeness, which is an **Integrity** function, so the
term was under-specified and its effective requirement set expanded to **{I, C, Au} =
Non-repudiation**. The exact set identity: `{C, Au} ∪ {I} = {I, C, Au}`.
**Relabel:** Attributability engages the *source* of an effected change, not content correctness —
"the action is attributable to its genuine source even if the resulting configuration is wrong". No
Integrity is required, so it stays at C⊕Au as a proper subset of Non-repudiation.

Neither equivalence is *proven* to have held; the audit establishes them as the two cells whose
definitions were most at risk and resolves them by relabel. Both new terms keep 15 distinct cells,
but it is the *fit-verification* — that each loads exactly its primaries and makes every listed
link necessary — that supports the relabel, not a proof of full pairwise distinctness.

---

## What is proven, and what is not

- **Proven:** there are **15 cells** — the non-empty subsets of the four primaries — and each is a
  distinct subset. This is set theory, not judgment.
- **Supported (qualitative):** all 15 compositions carry an M1–M5 argument; most are robust, and
  six carry a definitional caveat (**AT-RISK**) that tightening a definition could remove.
- **Not proven:** that the 15 cells correspond to **15 distinct capabilities**. The cells
  **Stewardship** and **Attributability** now load their primaries cleanly (the fit-verification
  finds them **FIT** / **FIT\***), but full pairwise distinctness of *all* terms from *all* others
  is a stronger claim than the audit establishes. The count remains **15 combinations;
  distinct-capability count not formally proven.**

The honest headline: the model is a sound *lattice* of 15 cells, and its vocabulary has been
tightened at the two cells that could have been aliases — but "15 non-overlapping qualities" is a
claim, not yet a theorem.

---

## Provenance

- The audit source is the [CISQ maturity levels](/systems/cisq-maturity/) post. Its
  [maturity table](/systems/cisq-maturity/#maturity-level-qualities-composition-threat) lists the
  published terms, compositions and threats; the [CISQ-model](/systems/cisq-model/) post gives the
  earlier vocabulary.
- The chain-link framing of ⊕ and the worked Non-repudiation subtraction come from the maturity
  post and are extended here to every composition.
- This proof atlas was produced and validated for the **acje/acje.github.io** repository. The
  repository also retains a root-level amendment (`CISQ-maturity-amendment.md`, outside the
  published site) that documents the same methods, matrix and candidate checks.
- The subset count follows from `2⁴ − 1 = 15`, excluding the empty set.
