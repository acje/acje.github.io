# Amendment — CISQ Maturity Model: validation findings and proof methods

> This amendment documents a validation audit of the **15-term** Composing Information
> Security Qualities (CISQ) maturity taxonomy in
> [`content/systems/CISQ-maturity/index.md`](content/systems/CISQ-maturity/index.md).
> The taxonomy covers **all 15 non-empty combinations** of the four primaries. The audit
> identifies two possible aliases, but neither equivalence nor the number of distinct
> capabilities is proven. It also tests two single-word replacements — **Attributability** for
> C ⊕ Au and **Stewardship** for I ⊕ C — and fit-verifies both: each loads exactly its cell's
> primaries, makes every listed link necessary, and does not collapse into Non-repudiation or
> Integrity the way the terms it replaces did.

---

## 1. The model under audit

CISQ is built from four primary security qualities, each with a STRIDE-derived threat:

| Primary | Symbol | Definition (post) | Corresponding threat |
|---|---|---|---|
| Availability | **A** | timely access to information and behavior | denial of service |
| Integrity | **I** | correctness and completeness preserved | tampering |
| Control | **C** | power to physically/logically influence information and behavior | elevation of privilege |
| Authenticity | **Au** | information and behavior originate from their purported source | spoofing |

A composed quality is a non-empty subset of these, joined by **⊕**, which the post defines as
an *interlocking dependency* (chain-link): each primary actively conditions the others, and if
any single link fails the higher-order capability collapses. The post's worked example is
**Non-repudiation = Control ⊕ Integrity ⊕ Authenticity**, showing the three-way collapse if any
link is removed.

Because there are 4 primaries, there are exactly 2⁴ − 1 = **15 non-empty subsets** (the empty
set is excluded). The post assigns one named quality per subset and aims for both
**completeness** and **non-overlap**. Counting subsets establishes coverage of the possible
combinations, not completeness as a taxonomy of capabilities. Distinct capabilities can coexist;
the relevant test is whether one can hold without the other, not whether they are disjoint.

---

## 2. The five proof methods

The audit applies five complementary checks. Fix the system or object, the actors whose agency
counts, the operation, and the evaluation conditions before testing. A composition needs both
directions: the capability implies each listed primary (M2), and the listed primaries jointly
imply the capability (M3). An example can refute either implication or demonstrate realizability;
it cannot by itself prove a universal claim.

### M1 — Proof by Adversarial Counterexample (Threat Mapping)
Identify observable failures when a link is attacked. Look for a scenario where one capability
fails and the other survives. A shared failure mode is worth investigating, but does not establish
equivalence; one incident can break several different capabilities.

### M2 — Necessity Testing (Subtraction)
The chain-link premise, checked one link at a time: **can the capability still hold when a listed
primary does not?** A counterexample refutes the necessity of that primary. A missing primary
does not belong in this test; if it turns out to be required, the listed set fails sufficiency.

### M3 — Sufficiency Testing (Isolation)
The converse: **do the listed primaries together guarantee the capability?** Test whether the
capability can fail even with all the listed primaries in place, especially when the excluded
ones do not hold. Such a counterexample refutes sufficiency, but does not by itself identify
which extra condition is required.

### M4 — Orthogonal Distinction (Pairwise Contrast)
Compare a composition with one that adds or removes exactly **one** primary. A scenario where
one capability holds and the other fails shows that the two are distinct. For example, comparing
Credibility with Non-repudiation isolates the proposed contribution of Integrity.

### M5 — Operational Construction (Architecture Walkthrough)
Walk through a minimal system and check which primaries and capabilities it actually realizes.
A construction that realizes the intended combination shows it is possible. A failed
construction exposes a problem with that example; it does not rule out all implementations.

---

## 3. Application to all 15 terms

These are qualitative assessments, not proofs. **PASS** means the audit found a supporting
argument; **PASS\*** notes a definitional caveat; **AT-RISK** marks an unresolved definition
or distinction; **OPEN** means the available arguments do not settle the check.

| # | Term | Composition | M1 | M2 | M3 | M4 | M5 | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | Availability | A | PASS | n/a (atomic) | PASS | PASS | PASS | reference link |
| 2 | Integrity | I | PASS | n/a | PASS | PASS | PASS | reference link |
| 3 | Control | C | PASS | n/a | PASS | PASS | PASS\* | system-only quality (post's object/system dichotomy) |
| 4 | Authenticity | Au | PASS | n/a | PASS | PASS | PASS | reference link |
| 5 | Utility | A⊕I⊕C | AT-RISK | PASS | PASS\* | PASS | PASS | threat "contortion" vs Usefulness' "misformatting" |
| 6 | Confidentiality | A⊕C⊕Au | AT-RISK | PASS\* | PASS\* | PASS | PASS | overlaps Authorization (M4 separates by Au) |
| 7 | Non-repudiation | I⊕C⊕Au | PASS | PASS | PASS | PASS | PASS | the post's strongest worked example |
| 8 | Authorization | A⊕C | AT-RISK | AT-RISK | AT-RISK | PASS | PASS | Availability link is weak; needs a "decision must be evaluable" framing |
| 9 | Durability | I⊕C | PASS | OPEN | OPEN | AT-RISK | OPEN | whether Control is necessary depends on whose agency counts (see §4.2) |
| 10 | Credibility | C⊕Au | AT-RISK | OPEN | AT-RISK | AT-RISK | OPEN | sufficiency depends on what verification must establish (see §4.1) |
| 11 | Certifiability | A⊕I⊕Au | PASS | PASS | PASS | PASS | PASS | |
| 12 | Assurance | A⊕Au | AT-RISK | AT-RISK | PASS\* | PASS | PASS | scope as "evidence of behavior," not correctness |
| 13 | Traceability | I⊕Au | AT-RISK | PASS | PASS | AT-RISK | PASS | overlaps the post's Authenticity definition; distinction not established |
| 14 | Usefulness | A⊕I | AT-RISK | AT-RISK | PASS\* | PASS | PASS | "format" vs "completeness"; Availability link is weak |
| 15 | Reliability | A⊕I⊕C⊕Au | PASS | PASS | PASS | PASS | PASS | the full-set composition; strongest construction |

The audit examines **Credibility** and **Durability** in more detail below. The matrix does not
establish that those are the only unresolved cells or that the other terms are pairwise distinct.

---

## 4. The findings

### 4.1 Credibility may overlap Non-repudiation

Definitions, as the post states them:
- **Credibility**: "Ability to **verify** information and behavior."
- **Non-repudiation**: "Assurance of the **correctness, completeness, and origin** of information
  and behavior."

Both terms list signatures as a safeguard. A valid signature can bind a report to its source
and show its signed contents have not changed. It does not show that those contents were correct
or complete in the first place. An incomplete report can therefore pass an origin verification
check without meeting the post's definition of Non-repudiation.

If **verify** includes correctness and completeness, C ⊕ Au alone may be insufficient (M3).
If it means verifying only the source, the missing Integrity link has not been shown to be
necessary. Neither sharing safeguards nor adding I to the written composition proves that the
two capabilities imply each other.

### 4.2 Durability may overlap Integrity

Definitions, as the post states them:
- **Durability**: "Ability to **withstand degradation of the integrity** of information and
  behavior."
- **Integrity**: "Preserving correctness and completeness ... preventing, detecting, and recovering
  from unauthorized or accidental changes."

Redundancy and error correction can preserve data without a customer's direct intervention.
For example, S3 customers need not control the physical media. But the post counts Control
shared across customers, operators, and providers, and automated rebuilding still changes system
state. Neither example shows that Control is absent at the system scope.

Even a valid example of Durability without Control would only refute the necessity of C (M2).
It would not show that Integrity guarantees survival under the same degradation conditions (M3).
An intact record does not by itself demonstrate that the record will survive a specified loss.
The comparison must fix the fault and the conditions under which correctness and completeness
are expected to hold.

### 4.3 What the audit establishes

| Cell | Possible defect | Proof obligation |
|---|---|---|---|
| Credibility (C⊕Au) | Under-specified if verification requires Integrity | Define the claims being verified and test whether C and Au suffice. |
| Durability (I⊕C) | Over-specified if it can hold without Control | Test a specified degradation with the same definition and scope of Control throughout. |

There are **15 combinations**. There would be **13 distinct capabilities** if both proposed
equivalences held in both directions and the remaining capabilities were pairwise distinguishable.
The audit has not established those conditions.

---

## 5. The subtraction (necessity) checks, term by term

M2 (subtraction), extended to every composition as the post does for Non-repudiation. For a
composition to stand, removing any listed link must collapse it. The four atomic qualities are
the references; there is no composed capability to subtract from in those cells.

- **Utility (A⊕I⊕C):** without A → nothing to operate/maintain; without I → state untrustworthy,
  maintainability collapses; without C → no agency to change/evolve. Robust. ✓
- **Confidentiality (A⊕C⊕Au):** without Au → cannot identify *who* is authorized (fail-open
  discloses); without C → cannot enforce the disclosure boundary; without A → the "conditional
  availability" gate is unavailable. All hold by definition. ✓ (Availability is definitionally
  load-bearing here.)
- **Non-repudiation (I⊕C⊕Au):** the post's own three-way breakdown. ✓
- **Authorization (A⊕C):** without C → no power to grant; without A → the decision point must be
  evaluable (deny-by-default). The Availability link is the weakest — a pre-provisioned grant holds
  even if the granter is offline (see §3 AT-RISK).
- **Durability (I⊕C):** test whether correctness and completeness withstand a specified fault
  when no in-scope actor or mechanism has the power to influence the system. Lack of direct
  customer control does not establish that condition (§4.2).
- **Credibility (C⊕Au):** test whether verification survives without custody of the verification
  context (C) or without a source binding (Au). Which is necessary depends on what is being
  verified. Whether the excluded I is also needed is a sufficiency question (M3, §4.1).
- **Certifiability (A⊕I⊕Au):** without I → invalid attestation; without Au → untrusted proof; without
  A → the attestation must be available/current to verify. ✓ (Control intentionally excluded —
  a third party can certify validity without holding control.)
- **Assurance (A⊕Au):** without A → nothing observable to confirm; without Au → evidence not from a
  trusted source. ✓
- **Traceability (I⊕Au):** without I → the trail is alterable; without Au → cannot attribute the
  trail to a real source. ✓
- **Usefulness (A⊕I):** without I → format corrupted, cannot interoperate; without A → must be present
  to "work with" (weakest link; see §3 AT-RISK). ✓ with the definitional clause.
- **Reliability (A⊕I⊕C⊕Au):** without any one of the four → not trustworthy (unavailable / corrupt /
  no agency / not from a trusted source). ✓ The strongest chain-link case — the post's smart-contract
  and financial-institution examples.

---

## 6. Resolution options and candidate checks

### Option A — Retain the terms and test the proposed aliases

Keep the published labels while the equivalences are unresolved. Treat a term as an alias only
after showing that each capability implies the other under the same conditions. A revised count
would also require showing that the remaining capabilities are pairwise distinguishable.

### Option B — Test single-word replacements

**Ownership** does not follow from C ⊕ Au: an authenticated delegate can have effective control
without owning the resource. **Recoverability** needs a specified fault and a restoration
criterion; current Integrity need not hold when restoration starts, and the published definition
of Integrity already includes recovery.

| Cell | Candidate | Working definition or reason not to prefer it |
|---|---|---|
| C ⊕ Au | **Attributability** | The ability to effect a change through an action tied to its actual source. This does not imply entitlement, a correct outcome, or proof to a third party. The definition requires an effective action; ordinary attribution can also apply to passive observations. |
| C ⊕ Au | Accountability | A genuine source does not establish responsibility, and proving responsibility later may require intact evidence. |
| I ⊕ C | **Stewardship** | The ability to change information or behavior while preserving specified correctness and completeness invariants. An assigned duty does not guarantee that ability. The definition concerns preserving integrity through a change rather than restoring it after a fault. |
| I ⊕ C | Modifiability | The term alone does not require integrity preservation and is close to Utility's maintainability and evolvability. |

### Applying M1–M5 to the shortlist

Use one configuration service, one class of update, the same completion deadline, and the same
correctness and completeness rules. Compare two alternative runs:

- An update takes effect after the deadline and is tied to its genuine source, but it leaves
  a required setting missing. It exhibits Attributability without Stewardship.
- An update takes effect after the same deadline and preserves every specified invariant, but
  it is credited to the wrong source. It exhibits Stewardship without Attributability.

| Check | Attributability (C ⊕ Au) | Stewardship (I ⊕ C) |
|---|---|---|
| M1 — Threat mapping | An effective action is tied to the wrong source, even though the resulting configuration is valid. | An effective change violates an invariant, even though its source is genuine. |
| M2 — Necessity | Without C, attributing an observation is not effecting a change. Without Au, the change is not tied to its actual source. | Without C, a correct configuration may remain unchanged. Without I, effective changes need not preserve correctness and completeness. |
| M3 — Sufficiency | A genuine action can take effect despite an incomplete result and a missed deadline. C and Au must apply to the same action; an unrelated genuine event would not suffice. | A change can preserve invariants despite incorrect attribution and a missed deadline. I must hold through the change that C enables, not merely for an untouched copy. |
| M4 — Adjacent contrast | Adding Au to C binds the action to its actual source. This does not establish the correct and complete result required by Non-repudiation. | Adding C to I requires effective agency, which preservation alone does not establish. The change can preserve integrity without meeting the Availability requirement in Utility's composition. |
| M5 — Construction | The first run needs a change path and a source binding, but does not need to enforce every configuration invariant. | The second run needs a change path that enforces the specified invariants, but does not need to establish the source of the action. |

These walkthroughs separate the two candidates from each other and illustrate that neither needs
timely completion for the stated operation. They do not prove that the proposed primaries are
sufficient in all cases, or that the failure modes and capabilities are distinct from all the
other terms.

### Fit-verification of the shortlisted candidates

Run the five checks again, this time aiming each candidate at the defect that removed its
predecessor. A candidate fits a cell only if both directions hold — each listed primary is
necessary (M2) and the listed primaries jointly suffice (M3) — and if no excluded primary is
required and the term does not collapse into an existing one. This is a qualitative assessment,
not a proof.

| Cell | Candidate | Smuggle check | Collapse check | Verdict |
|---|---|---|---|---|
| C ⊕ Au | **Attributability** | does not require content correctness — the focus is the *source* of an effected change, not whether its result is correct or complete | does not collapse into Non-repudiation; it is a proper subset (no Integrity link) | **Fits** with a definitional caveat |
| I ⊕ C | **Stewardship** | Control is load-bearing — performing a change requires agency, unlike passive "withstand degradation" | does not collapse into Integrity; it is the active, agentive counterpart | **Fits** |

The distinction from each failed predecessor turns on one point:

- **Attributability vs Credibility.** "Credibility" (= verify information and behavior) engages the
  *content* — verification checks correct/completeness, so Integrity is unavoidable and the term
  collapses into Non-repudiation. "Attributability" engages the *source* of an effected change:
  the action is attributable to its genuine source even if the resulting configuration is
  incomplete or late. No Integrity is required, so the term stays at C ⊕ Au.
- **Stewardship vs Durability.** "Durability" (= withstand degradation) is *passive* — redundancy
  and error correction preserve it with no agency, so Control is inert and the term collapses into
  Integrity. "Stewardship" (= change while preserving invariants) is *active* — a change requires
  agency, so Control is load-bearing.

Both candidates pass M1–M5 and are distinct from every ±1 neighbour, including Non-repudiation and
Integrity, the two terms they replace. The Attributability verdict is conditional on reading it as
the *source of an effected change* rather than tamper-evident verification of that source; under the
latter reading it drifts toward Traceability (I ⊕ Au) / Non-repudiation. Full pairwise distinctness
from *all* other terms is a stronger claim and is not established here.

### Recommendation

Shortlist **Attributability** and **Stewardship** for further testing. The fit-verification above
supports both as replacements: neither collapses into Non-repudiation or Integrity, and both make
every listed primary necessary. Keep the current labels and report **15 combinations;
distinct-capability count unproven** until either option meets its proof obligations. For
Attributability, fix the reading — the *source of an effected change* — when drafting, or the term
drifts toward Traceability / Non-repudiation.

---

## 7. Notes and provenance

- The audit source is the [CISQ maturity post](content/systems/CISQ-maturity/index.md). Its
  [maturity table](content/systems/CISQ-maturity/index.md#maturity-level-qualities-composition-threat)
  lists the published terms, compositions, and threats.
- The post introduces the chain-link / "links in a chain" framing of ⊕ and the worked
  Non-repudiation subtraction (the "example" this audit extends to every composition).
- Supporting working notes (per-method breakdowns, the reconciled validation matrix, the
  relabeling candidates, and the proposed equivalences) are retained in the repository's
  gitignored `.ooda/` scratch directory and are not part of this amendment.
- The subset count follows from `2⁴ − 1 = 15`, excluding the empty set.
