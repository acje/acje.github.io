# Amendment — CISQ Maturity Model: validation findings and proof methods

> This amendment documents a formal validation audit of the **15-term** Composing Information
> Security Qualities (CISQ) maturity taxonomy in
> [`content/systems/CISQ-maturity/index.md`](content/systems/CISQ-maturity/index.md). It explains
> the five proof methods used (in detail), applies them to every term, and reports the finding:
> **two terms are logically equivalent to existing terms rather than distinct qualities.** The
> underlying capability model has **15 lattice cells but 13 distinct qualities.**

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
set is excluded). The post assigns one named quality per subset and claims (:37) the result is
both **complete** and **non-overlapping** — but adds "this has not yet been formally proven."
This amendment supplies that proof attempt and its result.

---

## 2. The five proof methods

The audit applies five complementary proof methods. M1–M4 are the original four; necessity
(M2) is split out from sufficiency (M3) so the subtraction form carries its own weight.

### M1 — Proof by Adversarial Counterexample (Threat Mapping)
Instead of proving a quality exists, prove that **every unique subset produces a distinct
failure mode when one link is attacked**. If two combinations produced the exact same threat,
one of them would be redundant. This is the distinctness/separability gate: it fails if two
subsets map to the same operational failure class.

### M2 — Necessity Testing (Subtraction)
The chain-link premise, checked one link at a time: **if I remove one quality from the formula,
does the capability collapse?** This is the "without-X" argument the post uses for
Non-repudiation. It proves each listed link is *load-bearing*. If removing a link does **not**
collapse the capability, that link is inert and the composition is over-specified.

### M3 — Sufficiency Testing (Isolation)
The converse: **if I have ONLY these qualities and deliberately set the excluded ones to zero,
does the core capability still hold?** This is sharp for compositions that exclude a primary.
If the capability fails when an excluded primary is zeroed, that excluded primary was actually
required — the composition is under-specified.

### M4 — Orthogonal Distinction (Pairwise Contrast)
Take two compositions that share most ingredients and differ by exactly **one** quality, then
contrast them side by side to isolate what that single differing link contributes. This is the
tool for separating adjacent-looking terms (e.g. Credibility vs Traceability) and for showing a
link genuinely adds something.

### M5 — Operational Construction (Architecture Walkthrough)
Prove a composition by **building a minimal real-world system, control by control**, showing how
adding each primary unlocks the next tier of capability. This is the realizability gate: if a
faithful build cannot stop at the stated composition (it necessarily overshoots or undershoots),
the composition is false.

---

## 3. Application to all 15 terms

Legend: **PASS** (survives) · **PASS\*** (survives, with a definitional caveat) · **AT-RISK**
(survives only if a definition is tightened — redeemable) · **FAIL** (the term is not a distinct
quality as defined).

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
| 9 | Durability | I⊕C | PASS | **FAIL** | **FAIL** | **FAIL** | **FAIL** | Control is inert (see §5.2) |
| 10 | Credibility | C⊕Au | **FAIL** | **FAIL** | **FAIL** | **FAIL** | **FAIL** | Integrity is required but excluded (see §5.1) |
| 11 | Certifiability | A⊕I⊕Au | PASS | PASS | PASS | PASS | PASS | |
| 12 | Assurance | A⊕Au | AT-RISK | AT-RISK | PASS\* | PASS | PASS | scope as "evidence of behavior," not correctness |
| 13 | Traceability | I⊕Au | AT-RISK | PASS | PASS | AT-RISK | PASS | the post's own Authenticity definition subsumes it |
| 14 | Usefulness | A⊕I | AT-RISK | AT-RISK | PASS\* | PASS | PASS | "format" vs "completeness"; Availability link is weak |
| 15 | Reliability | A⊕I⊕C⊕Au | PASS | PASS | PASS | PASS | PASS | the full-set composition; strongest construction |

The result is binary and decisive at exactly two cells: **Credibility** and **Durability**.
The other 13 terms are distinct and survivable with definitional tightening (the AT-RISK cases
are redeemable by making an existing definition explicit — they are *not* composition failures).

---

## 4. The findings

### 4.1 Credibility is logically equivalent to Non-repudiation

Definitions, as the post states them:
- **Credibility**: "Ability to **verify** information and behavior."
- **Non-repudiation**: "Assurance of the **correctness, completeness, and origin** of information
  and behavior."

Every row of the post's own Credibility controls — cryptographic signatures, certificate pinning,
PKI validation, trusted timestamping, tamper-evident logging — is **tamper-evident**. A signature
verifies *both* origin *and* intact payload. Verifying that the payload is unaltered **is**
Integrity's function. The post makes this exact point for Non-repudiation: *"Without Integrity: the
origin is known, but the payload may have been altered — the actor can claim, 'That isn't what I
sent.'"*

Therefore:

> **Lemma (mechanism identity).** Verifying information and behavior requires detecting that
> content has been modified — which is an **Integrity** function. Signatures and tamper-evident
> logging already perform it.
>
> **Corollary (set identity).** Credibility ⊕ Integrity = Non-repudiation, because
> {C, Au} ∪ {I} = {I, C, Au}, which is exactly the documented Non-repudiation composition.

Because Integrity is a *necessary* link for "verify information and behavior," Credibility's real
requirement set is **{Integrity, Control, Authenticity}** — identical to Non-repudiation. The two
terms are **co-extensive**: you cannot realize one without realizing the other. They are the same
capability under two labels.

**Conclusion — Credibility ≡ Non-repudiation.** The C⊕Au cell does not name a new quality; it
names Non-repudiation minus the Integrity it cannot in fact shed. (Controls corroborate: the
Credibility control list is the Non-repudiation control list.)

### 4.2 Durability is logically equivalent to Integrity

Definitions, as the post states them:
- **Durability**: "Ability to **withstand degradation of the integrity** of information and
  behavior."
- **Integrity**: "Preserving correctness and completeness ... preventing, detecting, and recovering
  from unauthorized or accidental changes."

Withstanding degradation is delivered by **redundancy and error-correction** — the post's own
Durability controls are "automatic rebuilding, forward error correction (FEC), error correction
codes (ECC)." These preserve correctness/completeness with **no agency**. The decisive falsifier:

> **Necessity counterexample.** Amazon S3 publishes 11-nines durability while the customer holds
> **zero** control (no agency, no authority) over the underlying storage medium. RAID-5, ECC and
> erasure coding behave the same: they resist corruption mathematically, with no control over the
> medium. Removing **Control** from Durability does **not** collapse the capability.

Because Control is non-necessary (M2 fails), and no Authenticity or Availability is required
either, Durability's real requirement set is **{Integrity}** — identical to Integrity.
"Withstand degradation of integrity" is Integrity *under degradation stress*; the underlying
property is the same.

**Conclusion — Durability ≡ Integrity.** The I⊕C cell over-specifies a single-requirement
quality. (Note this is an equivalence of *capability/property*; the two terms retain a *threat-label*
difference — tampering vs data corruption — but both are Integrity failures under a different
attack vector, so they still denote the same property.)

### 4.3 Consequence: 15 cells, 13 distinct qualities

Applying both collapse relations over the full lattice (computed from the 15 non-empty subsets):

| Distinct effective composition | Terms sharing it |
|---|---|
| {Integrity} | Integrity, **Durability** |
| {Integrity, Control, Authenticity} | Non-repudiation, **Credibility** |

**15 lattice cells → 13 distinct qualities**, with exactly two redundant-cell pairs. The post's
"completeness and non-overlapping concepts" claim (:37) therefore holds for the **lattice
geometry** (15 cells, since it is the full power set) but **not for distinct capabilities** (13).
Two cells are logical aliases.

### 4.4 The mirror symmetry of the two defects

| Cell | Defect | Direction | Collapses to |
|---|---|---|---|
| Credibility (C⊕Au) | **under-specified** — omits a mandatory link (Integrity) | expands up | Non-repudiation |
| Durability (I⊕C) | **over-specified** — includes an inert link (Control) | contracts down | Integrity |

One omission, one over-inclusion. Both defects resolve to a *duplicate*, not a new quality — this
is why the taxonomy is not simply "two wrong labels" but "two non-distinct labels."

---

## 5. The subtraction (necessity) proofs, term by term

M2 (subtraction), extended to every composition as the post does for Non-repudiation. For a
composition to stand, removing any listed link must collapse it. (**Atomic links 1–4 have no link
to remove; they are the references.**)

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
- **Durability (I⊕C):** without I → nothing to withstand degradation of; **without C → durability
  survives (S3/RAID/ECC, zero control) — M2 FAILS.** See §4.2.
- **Credibility (C⊕Au):** without C → no custody of verification context; without Au → cannot verify
  source. But **Integrity is required and excluded — M2 FAILS** (the excluded link is necessary). See §4.1.
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

## 6. Resolution fork and recommendation

The findings above are a logical consequence of the post's *current definitions*. That leaves two
internally consistent ways to read and fix the taxonomy:

### Option A — Reduce to 13 distinct qualities (accept the equivalences)
Treat Credibility ≡ Non-repudiation and Durability ≡ Integrity as true. Then the taxonomy has
**13 genuinely distinct qualities**; the two redundant cells are recognised as aliases and either
removed from the term table (`:217–233`) or annotated ("Credibility = Non-repudiation; Durability =
Integrity"), and the :37 claim is amended to "**13 distinct qualities** over a 15-cell lattice."
- **Virtue:** honest to the current definitions; introduces no new vocabulary.
- **Cost:** surrenders the clean 15-distinct uniformity and the "15 variants" framing.

### Option B — Relabel to 15 distinct qualities (change two definitions)
Replace the two mis-fitted *definitions* with meanings that genuinely load only their cell's
primaries, e.g. **Ownership** for C⊕Au (legitimate possession vested in a genuine principal) and
**Recoverability** for I⊕C (the ability to use control to restore integrity). Then the equivalences
no longer hold, and the taxonomy keeps 15 distinct cells.
- **Virtue:** preserves the 15-distinct + non-overlapping elegance.
- **Cost:** introduces new terms and changes the post's vocabulary for two cells.

### Recommendation
Either way, **the equivalence cannot be left unstated** — it is a provable consequence of the
current definitions, and the "non-overlapping" claim is currently false (two cells are duplicate). If
the priority is fidelity to the existing vocabulary, take **Option A**. If the priority is the
15-cell one-term-per-subset structure, take **Option B** (which must remove the equivalence by
changing the definitions). The amendment documents the finding and the methods either way.

---

## 7. Notes and provenance

- The audit source is the post at `content/systems/CISQ-maturity/index.md` (all line/section
  references are to that file; the composition, threat, and term table is at `:217–233`).
- The post introduces the chain-link / "links in a chain" framing of ⊕ and the worked
  Non-repudiation subtraction (the "example" this audit extends to every composition).
- Supporting working notes (per-method breakdowns, the reconciled validation matrix, the
  relabeling candidates, and the equivalence verification) are retained in the repository's
  gitignored `.ooda/` scratch directory and are not part of this committed amendment.
- The `2⁴ − 1 = 15` / `2^4` duplicate-collapse computations were verified over the full
  power set of {A, I, C, Au}.
