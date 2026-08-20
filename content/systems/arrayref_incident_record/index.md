---
title: "crates.io / arrayref: a contemporaneous incident record"
aliases:
  - "/arrayref_incident_record/"

date: 2026-08-20
lastmod: 2026-08-20
draft: false
homeFeatured: true
weight: 90
---

## crates.io / arrayref: a contemporaneous incident record

**Original document title:** crates.io incident follow-up — `droundy` account compromise + `dtolney` impersonation

This is a contemporaneous record. My agents and I compiled it on 2026-08-20
between roughly 09:08Z and 12:08Z, while the incident was still moving, and it
is published here as written. It is not current advice, and it is not the
authoritative account — the authoritative account is the Rust Security Response
Team's postmortem, [Supply chain attack on
arrayref](https://blog.rust-lang.org/2026/08/20/supply-chain-attack-on-arrayref/).
Everything here was true as of its stated timestamp. Several items were
superseded within hours, and the document records those corrections as marked,
dated **UPDATE** blocks rather than editing the original claims away. That
self-correcting structure is the reason it is worth publishing at all: the value
is in seeing what was knowable at each moment, including where it was wrong.

The companion post, [Watching my software factory handle a live supply chain
attack]({{< relref "systems/watching_a_supply_chain_attack/index.md" >}}), is the
narrative version: how a `cargo deny` gate on an unrelated project caught the
yank, how my agents walked into the poisoned upgrade and then stopped themselves
reading the diff, and what the tooling did and did not get right. Read that one
first if you want the story. This one is the raw material behind it.

**Compiled:** 2026-08-20T09:08Z · **revised** 2026-08-20T09:26Z ·
**§5 re-verified** 2026-08-20T12:07–12:08Z

**Remediation state as of 2026-08-20T09:26Z (original record).** crates.io has
removed `proc-macro1`, deleted `arrayref 0.3.10`, and reverted the adversarial
yanks on `arrayref` and `append-only-vec`. **One crate appears to have been
missed: `internment` (§5.1).** Further residuals in §5.2–5.5.

> **UPDATE 2026-08-20T12:07Z — supersedes the 09:26Z state above.** The
> `internment` yank is **no longer outstanding**: 0.8.3–0.8.6 are live again and
> `max_version` is restored to 0.8.6 (§5.1). Of the five §5 items, four have
> moved: §5.1 **resolved**, §5.2 **resolved by outright deletion** (not
> un-yank), §5.3 **partially resolved** (account still exists and still asserts
> the name "David Tolnay", but now owns zero crates), §5.5 **resolved** — an
> official crates.io / Rust Security Response Team postmortem was published the
> same day. **§5.4 (RustSec advisory) is `Indeterminate`, not resolved** — the
> re-check was HTTP 403 rate-limited, which is absence of signal, not evidence
> of absence. Everything still open is in §5.4 and in the residual `dtolney`
> name claim in §5.3.

> **This document describes a live, moving situation.** Between the 09:08Z
> compilation and the 09:26Z revision, `arrayref` 0.3.5–0.3.9 and
> `append-only-vec` 0.1.7–0.1.8 were un-yanked — the latter *between two checks
> four minutes apart*. Every §5 item carries an as-of timestamp and a
> re-verification command; re-run them before acting. Sections 1–4 are the
> attack record as compiled at 09:08Z/09:26Z and are preserved as written;
> corrections and scope extensions from the 12:07Z pass appear as marked, dated
> **UPDATE** blocks, never as silent rewrites.

> **UPDATE 2026-08-20T12:07Z — §1–§4 under-scope the campaign.** Two gaps, both
> from the official postmortem (§5.5): (a) the attack was **broader than the
> four items in §1** — five further malicious crates were deleted
> (`proc-macro-en`, `aovine`, `arone`, `aronenao`, `tinymember`), none of which
> appear anywhere in this document's own observations; (b) the **executing
> payload was in `proc-macro1`'s own `build.rs`**, which this document never
> sampled. §3.2's "there is no `build.rs`" is correct *about `arrayref`'s
> manifest* and remains so — but a reader of §3 alone would not learn where the
> payload actually ran. See §3.2 and §5.5.

---

### 1. Summary

Between 01:25Z and 07:38Z on 2026-08-20, an attacker:

1. Created a crates.io account impersonating David Tolnay (`dtolney`, full-name
   field set to "David Tolnay").
2. Published `proc-macro1` — a crate impersonating `proc-macro2`, with
   `repository` pointing at a non-existent `github.com/dtolnay/proc-macro1`.
3. Published `arrayref 0.3.10` from the **legitimate** `droundy` account
   (245M downloads), adding a mandatory dependency on `proc-macro1`.
4. Yanked the modern release history of **three** `droundy` crates —
   `arrayref` 0.3.5–0.3.9, `internment` 0.8.3–0.8.6, `append-only-vec`
   0.1.7–0.1.8 — in each case leaving older releases live. For `arrayref` this
   forced downstream consumers toward the poisoned 0.3.10.
5. Published `append-only-vec 0.1.9` (4.5M downloads) and an `internment`
   version (14.4M downloads, since removed) in the same burst.

The `droundy` account (id 2402, created 2009-10-09) shows every sign of
takeover rather than malice by the owner: 37 crates, 17 years of history,
three touched inside a 23-minute window after ~5 days of no activity. A sweep
of all 37 found no other crate with yanked versions dating from the incident.

> **UPDATE 2026-08-20T12:07Z — scope correction.** The summary above is
> `droundy`/`dtolney`-scoped and understates the campaign. Per the official
> postmortem (§5.5), five further malicious crates were also deleted:
> `proc-macro-en`, `aovine`, `arone`, `aronenao`, `tinymember`. The
> `internment` publish left unnumbered in item 5 above is **0.8.7**. crates.io
> states it "locked the [`droundy`] account as a precaution" and is "attempting
> to contact them", and that "We do not believe the author of arrayref to be
> acting maliciously" — consistent with this section's takeover assessment. The
> initial report reached crates.io at 2026-08-20T07:15 UTC, credited to "the
> Research Team at Nextron Systems GmbH".

---

### 2. Timeline (UTC)

Publish times are crates.io API `created_at` fields. Yank times are not exposed
by the API; they are placed by the affected crate's `updated_at`, which falls
inside the burst in all three cases.

**Attack**

| Time | Event |
|---|---|
| `2026-08-20T01:25:58Z` | crates.io account `dtolney` created (GitHub avatar uid 318835712) |
| `2026-08-20T01:55:34Z` | `proc-macro1 1.0.106` published by `dtolney` |
| `2026-08-20T07:11:15Z` | `proc-macro1 1.0.107` published by `dtolney` |
| `2026-08-20T07:15:00Z` | `arrayref 0.3.10` published by `droundy`, depending on `proc-macro1 ^1.0.107` (4 min after that version appeared) |
| `2026-08-20T07:15Z` | `arrayref` 0.3.5–0.3.9 yanked by `droundy` |
| `2026-08-20T07:34:07Z` | `internment` touched by `droundy` — 0.8.3–0.8.6 yanked; a publish from this moment has since been removed |
| `2026-08-20T07:37:49Z` | `append-only-vec 0.1.9` published by `droundy`; 0.1.7–0.1.8 yanked |

**Remediation** (externally observed; crates.io will have exact times)

| Time | Event |
|---|---|
| by `2026-08-20T09:08Z` | `proc-macro1` removed entirely; `arrayref 0.3.10` deleted; malicious `internment` version deleted |
| by `2026-08-20T09:21Z` | `arrayref` 0.3.5–0.3.9 un-yanked |
| `09:21Z`–`09:24Z` | `append-only-vec` 0.1.7–0.1.8 un-yanked (observed to change between two checks four minutes apart) |
| open at `09:26Z` | `internment` 0.8.3–0.8.6 **still yanked** (§5.1) |

**Remediation — UPDATE 2026-08-20T12:07Z.** Rows below are added from the
12:07–12:08Z re-verification and the official postmortem (§5.5). The postmortem
gives exact deletion timestamps that the externally-observed table above could
only bracket; where they conflict, the postmortem times are authoritative.

| Time | Event | Source |
|---|---|---|
| `2026-08-20T07:15Z` | initial report received by crates.io; discovery credited to the Research Team at Nextron Systems GmbH | postmortem |
| `2026-08-20T08:41:40Z` | `arrayref@0.3.10` **deleted** (before this doc's 09:08Z compile — consistent with the record above) | postmortem |
| `2026-08-20T09:04:11Z` | `internment@0.8.7` (the malicious publish) **deleted** | postmortem |
| `2026-08-20T09:25:24Z` | `append-only-vec@0.1.9` **deleted** — ~1–2 min *before* this doc's 09:26Z revision, which is why §5.2 still recorded it live | postmortem |
| by `2026-08-20T12:07Z` | `internment` 0.8.3–0.8.6 **un-yanked**; `max_version` restored to 0.8.6 — §5.1 closed | direct API |
| by `2026-08-20T12:07Z` | `dtolney` owns **zero** crates (`proc-macro1` 404s); account itself still resolves 200 | direct API |
| `2026-08-20` | official crates.io / Rust Security Response Team postmortem published ("Supply chain attack on arrayref", Manish Goregaokar) | blog.rust-lang.org |

---

### 3. Evidence

#### 3.1 Impersonation account

```
GET https://crates.io/api/v1/users/dtolney
{
  "id": 438608,
  "login": "dtolney",
  "name": "David Tolnay",           <-- real name of the dtolnay maintainer
  "avatar": "https://avatars.githubusercontent.com/u/318835712?v=4",
  "url": "https://github.com/dtolney",
  "created_at": "2026-08-20T01:25:58.619057Z"
}
```

The `name` field is the strongest single signal: this is not an accidental
typo-registration, it is deliberate identity assumption. GitHub uid 318835712
indicates an account created immediately before use.

`proc-macro1`'s crate metadata additionally carried:
- `description`: verbatim copy of `proc-macro2`'s description
  ("A substitute implementation of the compiler's `proc_macro` API to decouple
  token-based lib…")
- `repository`: `https://github.com/dtolnay/proc-macro1` — a repository that
  does not exist under the real maintainer's account.

#### 3.2 The payload vector — `arrayref 0.3.10`

Read directly from the published tarball's normalised manifest
(`arrayref-0.3.10/Cargo.toml`):

```toml
[package]
name = "arrayref"
version = "0.3.10"
authors = ["David Roundy"]
build = false
repository = "https://github.com/droundy/arrayref"

[dependencies.proc-macro1]
version = "1.0.107"

[dev-dependencies.quickcheck]
version = "1.0"
```

Dependency delta versus the previous release:

| Version | normal deps | dev deps |
|---|---|---|
| `0.3.9` | **0** | `quickcheck ^1.0` |
| `0.3.10` | **`proc-macro1 ^1.0.107`** | `quickcheck ^1.0` |

`arrayref` is a macro crate for taking array references of slices. It has had
zero runtime dependencies for its entire 10-year history. A mandatory
dependency on a proc-macro token library has no plausible functional
justification. Because proc-macros execute during compilation, the payload runs
on CI runners and developer workstations at `cargo build` time — no runtime
invocation of the library is required.

There is no `build.rs`; the dependency **is** the vector.

> **UPDATE 2026-08-20T12:07Z — scope gap, not an error.** The statement above is
> correct about **`arrayref`'s** manifest (`build = false`, verified from the
> published tarball). But the official postmortem (§5.5) states `proc-macro1`
> "had a build script that was downloading a malicious payload" — i.e. the
> executing payload lived in **`proc-macro1`'s own `build.rs`**, a crate this
> document never sampled. Read §3.2 as: `arrayref 0.3.10` is the *delivery*
> mechanism; `proc-macro1`'s `build.rs` is where the payload *ran*.

Artefact hashes (tarball as served, since removed):

```
sha256  25ad700976873c76af785cb99b33c48db7df8b81f21d1e9e06b3676b9a9373ae
        arrayref-0.3.10.crate   (12051 bytes)
```

Additional anomaly: every file inside the 0.3.10 tarball is backdated to
`Jul 24 2006`, inconsistent with a `cargo publish` from a normal working tree.

#### 3.3 No corresponding source

`arrayref 0.3.10` has no matching tag or commit in
`github.com/droundy/arrayref`. The published artefact is not reproducible from
the declared repository.

#### 3.4 The yank is the delivery mechanism

`arrayref` 0.3.5 through 0.3.9 were yanked in the same window as the 0.3.10
publish. Yanking the entire supported history is what converts a poisoned
release into a forced upgrade: dependency resolution and supply-chain gates
(`cargo deny`, `cargo audit`) push consumers off the yanked versions and onto
0.3.10. Notably `0.3.4` and earlier were **left un-yanked**, consistent with
targeting modern consumers rather than an honest deprecation.

**These yanks were reverted by 2026-08-20T09:21Z** — `arrayref` 0.3.5–0.3.9
are live again and `max_version` is back to 0.3.9. The identical yank signature
on `internment` has **not** been reverted; see §5.1.

> **UPDATE 2026-08-20T12:07Z.** The `internment` yanks *have* since been
> reverted — 0.8.3–0.8.6 are live and `max_version` is 0.8.6. The final sentence
> above is the 09:26Z state, retained as the record. See §5.1.

---

### 4. Reproduction

```sh
UA="incident-report (your-contact@example.com)"

# impersonation account (still live at 09:26Z)
curl -s -A "$UA" https://crates.io/api/v1/users/dtolney

# the three affected crates: max_version + currently-yanked set
for c in arrayref internment append-only-vec; do
  echo "== $c"
  curl -s -A "$UA" "https://crates.io/api/v1/crates/$c" \
    | jq '.crate.max_version, ([.versions[] | select(.yanked)] | map(.num))'
done

# the payload dependency (404 since 0.3.10 was deleted; recorded for the record)
curl -s -A "$UA" https://crates.io/api/v1/crates/arrayref/0.3.10/dependencies

# full portfolio sweep for the yank signature
curl -s -A "$UA" 'https://crates.io/api/v1/crates?user_id=2402&per_page=100&sort=recent-updates'
```

---

### 5. Residual items for crates.io

All items were first verified at **2026-08-20T09:26Z** and **re-verified at
2026-08-20T12:07–12:08Z**. Each carries its own re-check command — the situation
moved twice during a 16-minute review. Status at 12:07Z:

| Item | Status at 09:26Z | Status at 12:07Z |
|---|---|---|
| 5.1 `internment` yanks | open | **Resolved** — un-yanked, `max_version` 0.8.6 |
| 5.2 `append-only-vec 0.1.9` | open (live, unaudited) | **Resolved** — version **deleted** outright, not un-yanked |
| 5.3 `dtolney` account | open | **Partially resolved** — owns 0 crates; account still live and still names "David Tolnay" |
| 5.4 RustSec advisory | open | **Indeterminate** — re-check HTTP 403 rate-limited; neither confirmed nor denied |
| 5.5 broader sweep | open (suggestion) | **Resolved** — official postmortem published; crates.io had already swept (5 more malicious crates) |

#### 5.1 `internment` 0.8.3–0.8.6 are still yanked — apparently missed

> **STATUS 2026-08-20T12:07Z: RESOLVED.** `curl
> https://crates.io/api/v1/crates/internment` returns `max_version: 0.8.6`,
> `updated_at: 2026-08-20T07:34:07.663686Z`, `yanked: []` — 0.8.3–0.8.6 are no
> longer in the yanked set and the 0.8.2 regression is undone. Regression check
> on the other two: `arrayref` `max_version` 0.3.9, `yanked: []`;
> `append-only-vec` `max_version` 0.1.8, `yanked: []` — neither has re-regressed
> on the yank front. The analysis below is the 09:26Z record.

This is the one outstanding item, and it looks like an oversight rather than a
decision.

The same adversarial yank signature was applied to three `droundy` crates in
the 07:15–07:38Z burst. Two have been reverted; `internment` has not:

| Crate | Downloads | Yanked in burst | State at 09:26Z |
|---|---|---|---|
| `arrayref` | 245M | 0.3.5–0.3.9 | **reverted** — all live, `max_version` 0.3.9 |
| `append-only-vec` | 4.5M | 0.1.7–0.1.8 | **reverted** — all live, `max_version` 0.1.9 |
| `internment` | 14.4M | **0.8.3–0.8.6** | **still yanked**, `max_version` regressed to **0.8.2** |

`internment`'s `updated_at` is `2026-08-20T07:34:07Z` — inside the compromise
window, between the `arrayref` and `append-only-vec` events. Its newest four
releases are yanked while `0.8.2` (2024-04-17) and older remain live: the exact
"yank the modern history, leave the old" shape seen on the other two crates,
and the same shape crates.io has already judged adversarial and reverted twice.

Effect: every consumer of `internment` 0.8.3+ with a supply-chain gate is
hard-blocked, and resolution silently drags them back to a two-year-old release.

Re-check:

```sh
curl -s -A "$UA" https://crates.io/api/v1/crates/internment \
  | jq '.crate.max_version, ([.versions[] | select(.yanked)] | map(.num))'
```

A full sweep of all 37 `droundy` crates found only two other crates with any
yanked versions — `display-as-template` (2018) and `david-set` (2017) — both
long predating the incident and unrelated.

#### 5.2 `append-only-vec 0.1.9` — publish from within the compromise window, unaudited

> **STATUS 2026-08-20T12:07Z: RESOLVED — by deletion, not by un-yank.**
> `curl https://crates.io/api/v1/crates/append-only-vec/0.1.9` returns **404**
> (`crate append-only-vec does not have a version 0.1.9`), and the full version
> list now tops out at `0.1.8` (`created_at` 2025-10-20): 0.1.9 is **entirely
> absent from the versions array**, not merely `yanked: true` — the same
> disposition as `arrayref 0.3.10`. The postmortem (§5.5) gives the deletion
> time as **2026-08-20T09:25:24Z**, ~1–2 min before this document's 09:26Z
> revision, which is why the text below still recorded it as live.
>
> **A 404 from the re-check commands here is therefore the resolved state, not a
> broken command.** Consequences: the dependency-set comparison against 0.1.8
> can no longer be performed (the version is gone; the `/dependencies` endpoint
> was not separately probed once the parent 404'd), and the `build.rs`/source
> audit called for below was never done and is now moot.

Downgraded from the 09:08Z revision but not withdrawn. The yanks on this crate
have been reverted, but `0.1.9` itself was **published at
`2026-08-20T07:37:49Z`** — 22 minutes into the burst, by the compromised
account — and is live and un-yanked.

Its declared dependencies are clean and identical to `0.1.8`
(`parking_lot ^0.12`, `scaling ^0.1.3`, both dev-only), so it does not carry
the `proc-macro1` vector. Its source has **not** been audited. On provenance
alone it warrants review: a clean dependency set does not exclude an inline or
`build.rs` payload, and a second vector cannot be ruled out.

`internment` and `tinyset` have no live version published in the window; the
malicious `internment` publish has already been removed.

#### 5.3 The `dtolney` impersonation account still exists

> **STATUS 2026-08-20T12:07Z: PARTIALLY RESOLVED — the account claim below is
> still open.** Direct checks:
> - `GET /api/v1/users/dtolney` → **200**, `id 438608`, `name` still `"David
>   Tolnay"`, `created_at` unchanged. The false-identity claim is **unresolved**.
> - `GET /api/v1/crates?user_id=438608&per_page=100` → `{"total":0,"crates":[]}`
>   — the account now owns **zero** crates.
> - `GET /api/v1/crates/proc-macro1` → **404** (`crate proc-macro1 does not
>   exist`).
> - `github.com/dtolney` → **200**; that GitHub account is unrelated to
>   crates.io and is still live.
>
> The postmortem (§5.5) states crates.io "locked the account as a precaution" —
> in the postmortem's own text that sentence is about the **`droundy`** account;
> the same wording is also consistent with what is observed here for `dtolney`
> (locked, not deleted: still resolving, zero crates). The evidence does not
> settle which account the phrase covers; treat the attribution as open.

`proc-macro1` was removed, but the account that published it was not. As of
09:26Z:

```json
{ "id": 438608, "login": "dtolney", "name": "David Tolnay",
  "created_at": "2026-08-20T01:25:58.619057Z" }
```

The `name` field still asserts the identity of the `dtolnay` maintainer. The
account retains publish capability and could re-publish under a different crate
name.

#### 5.4 RustSec advisory — status **Indeterminate** (was: "no advisory exists")

> **STATUS 2026-08-20T12:07Z: INDETERMINATE. This is the one item where the
> re-check produced no signal at all — do not read it as "no advisory exists".**
> Every probe returned **HTTP 403 — API rate limit exceeded**
> (`Authenticated requests get a higher rate limit`):
> - GitHub code search `q=proc-macro1 repo:rustsec/advisory-db` → 403
> - GitHub commits list on `rustsec/advisory-db` `since=2026-08-19` → 403, twice
>   (immediately, and again after a 5s sleep retry)
> - Contents-API fallback on `crates/proc-macro1` and `crates/arrayref` → 403
>
> The unauthenticated GitHub REST API is fully rate-limited from this egress IP.
> **A 403 is absence of signal, not a negative finding**: an advisory may or may
> not exist, and neither was established. The official postmortem (§5.5) does
> not settle it either — that post does not mention RUSTSEC or advisory-db at
> all.
>
> Settle it with an **authenticated** re-check (needs `gh auth login`, or
> `GH_TOKEN` in the environment):
>
> ```sh
> # another 403 here means still rate-limited — still Indeterminate, not "absent"
> gh api -H 'Accept: application/vnd.github+json' \
>   '/search/code?q=proc-macro1+repo:rustsec/advisory-db'
>
> gh api '/repos/rustsec/advisory-db/commits?since=2026-08-19'
>
> # direct existence probe: 200 = advisory filed, 404 = genuinely absent
> gh api '/repos/rustsec/advisory-db/contents/crates/proc-macro1'
> gh api '/repos/rustsec/advisory-db/contents/crates/arrayref'
>
> gh api /rate_limit   # confirm the budget before trusting any of the above
> ```

**Original 09:26Z finding, retained as the record:**

Checked at 09:26Z: zero references to `proc-macro1` in `rustsec/advisory-db`,
and the most recent advisory-db commit is `2026-08-18` (RUSTSEC-2026-0258, h2).
No advisory has been filed for this incident.

Given the crates involved (245M + 14.4M + 4.5M downloads) and that the attack
window is only ~2 hours old, an informational advisory would let downstream
supply-chain tooling flag any lockfile that captured `arrayref 0.3.10` during
the window, which yank-reversion alone does not surface.

> **UPDATE 2026-08-20 — settled with an authenticated re-check.** The
> `Indeterminate` above is now resolved on the evidence, in both directions.
> `rustsec/advisory-db` **issue #3161** exists — an **issue, not a PR** — titled
> "Malware: arrayref 0.3.10 executes a remote payload at build time via
> typosquatted proc-macro1". It was filed **2026-08-20T07:54:11Z** and closed
> **2026-08-20T09:34:17Z** by `djc` with `state_reason: not_planned`. No merged
> RUSTSEC advisory for `arrayref` or `proc-macro1` was found: `crates/arrayref`
> and `crates/proc-macro1` both 404, repo code search returned zero results, and
> no `RUSTSEC-2026-NNNN` id was observed.
>
> This document's own probes ran at **09:26Z**, so #3161 was **open** at that
> moment and closed about **eight minutes later**. Both halves matter. Writing
> "no advisory exists" from behind a 403 would have been **confidently wrong** —
> an issue with that precise title existed at that precise moment. And equally:
> it closed `not_planned` with nothing merged, so the *final* state is closer to
> "no advisory" than not. Neither half rescues the other into "the record was
> right all along". The record did not know, and what it wrote was that it did
> not know. Who filed #3161 was never observed and is not recorded here.

#### 5.5 Suggested broader check

> **STATUS 2026-08-20T12:07Z: RESOLVED — crates.io had already swept.** The
> official postmortem, *"Supply chain attack on arrayref"* (blog.rust-lang.org,
> 2026-08-20, by Manish Goregaokar on behalf of the security-response team,
> <https://blog.rust-lang.org/2026/08/20/supply-chain-attack-on-arrayref/>),
> covers remediation for `arrayref`, `internment`, and `append-only-vec` **and
> names five further malicious crates, all versions deleted**:
> `proc-macro-en`, `aovine`, `arone`, `aronenao`, `tinymember`. None of these
> appear anywhere in this document's own observations — the sweep suggested
> below was evidently run internally, independently of this recommendation, and
> found a materially broader campaign than §1 describes.
>
> Also from that post, and not otherwise in this document: the report reached
> crates.io at **2026-08-20T07:15 UTC**, credited to **the Research Team at
> Nextron Systems GmbH**; the malicious `internment` version was **0.8.7**;
> `proc-macro1` "had a build script that was downloading a malicious payload"
> (see §3.2); crates.io "locked the [`droundy`] account as a precaution" and is
> "attempting to contact them"; and "We do not believe the author of arrayref to
> be acting maliciously".
>
> Note: **`status.crates.io` does not carry this incident** — at 12:07Z it read
> "All Systems Operational" with "No incidents reported today" for Aug 20 2026.
> The status page is not a usable signal for this class of event.

**Original 09:26Z suggestion, retained as the record:**

The `dtolney` account published only `proc-macro1`, but the technique — a
plausible-looking `-1` sibling of a ubiquitous `-2` crate, introduced as a new
mandatory dependency of an unrelated high-download crate — generalises. Worth
sweeping for other recently-created accounts whose display name matches a
well-known maintainer, and for new mandatory dependencies added to long-stable
zero-dependency crates.

