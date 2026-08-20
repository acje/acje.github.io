---
title: "The yank that gave it away"
aliases:
  - "/watching_a_supply_chain_attack/"

date: 2026-08-20
lastmod: 2026-08-20
draft: false
homeFeatured: true
weight: 80
---

## The yank that gave it away

I was not looking for a supply chain attack. I was working on [gh-report](https://github.com/Mattilsynet/gh-report), a Rust project that has nothing to do with `arrayref`, on a task that had nothing to do with `arrayref`, and my build went red.

`cargo deny` had failed. The reason was that a dependency the project had pinned for months — `arrayref 0.3.9`, checksum `76a2e8…fecb` — had just been yanked out from under it. `deny.toml` sets `yanked = "deny"` under `[advisories]`, listed explicitly even though it is already the default, precisely so that a future relaxation would be visible in a diff. It fired.

I had never chosen `arrayref`. Nobody does. It is a transitive dependency; it came along with `blake3`, because that is what a hash function pulls in. It sat in the lock file being boring for months.

First, credit where it belongs. Discovery goes to the Research Team at Nextron Systems GmbH; the postmortem thanks them "for initially discovering this and reporting it to us", and that report reached crates.io at 07:15 UTC. Remediation goes to crates.io and the Rust Security Response Team, who deleted the malicious versions, un-yanked the maliciously-yanked ones and locked the account. The authoritative account is theirs: [Supply chain attack on arrayref](https://blog.rust-lang.org/2026/08/20/supply-chain-attack-on-arrayref/) (Manish Goregaokar, on behalf of security-response). I did notify the crates.io security team once my agents had characterised what they were seeing. I make no claim on the discovery, and by the time I reported it the professionals were already working the incident. Nothing below changes that ordering.

### The irony the whole thing rests on

The attacker had to yank `arrayref` 0.3.5 through 0.3.9. That is the mechanism. A poisoned 0.3.10 sitting quietly alongside five healthy releases converts nobody; consumers stay where their lock files put them. Yank the modern release history and resolution, tooling and supply-chain gates all start pushing people up onto the one live modern version. The yank *is* the delivery.

And the yank is what set off my alarm. The same act that was supposed to force me onto the poisoned version is the act that made an unrelated project, on an unrelated task, refuse to build. `0.3.4` and older were left alone, which tells you the shape of it — you do not leave the ancient releases live if you are honestly deprecating; you leave them live if you are targeting modern consumers.

### The part that actually mattered

Here is the obvious response to "cargo deny says your dependency is yanked": bump to the newest version. It is what a tired human does at 09:00. It is what a careless agent does. In this case it walks straight into `arrayref 0.3.10`, which is the entire point of yanking the alternatives.

**hopper did not do the obvious thing.** It went and looked at what had replaced the yanked versions, noticed that 0.3.10 had appeared four minutes after `arrayref` acquired a brand-new dependency it had never had in its life, and kept pulling. **moltke** consolidated the finding and presented it. Then a third pass verified it independently — against the crates.io API and the manifest read out of the unpacked tarball — rather than taking moltke's word for it.

![moltke's consolidated finding: an independent verification of an in-progress supply chain attack on the arrayref crate, showing the typosquatted proc-macro1 publisher, the 07:15:00Z publication of arrayref 0.3.10, the yanked 0.3.5 through 0.3.9, and the dependency on proc-macro1 1.0.107 read from the crate manifest](moltke-summary.png)

*The consolidated finding, verified independently against the crates.io API and the unpacked tarball manifest. The decisive line is `[dependencies.proc-macro1] version = "1.0.107"` — read out of the manifest, not inferred.*

Two numbers on that screenshot are worth stopping on. `proc-macro1` had **9 downloads**. Nine. At the moment of detection the payload crate's blast radius was still essentially nil. `arrayref`, the crate it had just been attached to, had **244,989,384**. That asymmetry is the whole business model of a supply chain attack: you do not need anyone to install your crate, you need one crate that everybody already installs to install it for you.

The value here was not that a language model is clever. It was a gate configured to fail loudly, plus agents that treated a red gate as a question rather than a chore.

Asked to justify the verdict rather than state it, the fleet laid out its reasoning signal by signal.

![moltke's evidence table for a verdict of MALICIOUS at high confidence, listing six independent signals: a typosquat publisher, a stolen identity copied from proc-macro2, an account takeover, no reviewable source for the published version, the payload shape implied by the dependency closure, and the yank itself as the delivery vector](moltke-evidence.png)

*The evidence behind the verdict. `moltke-summary.png` above is what it found; this is why it was sure.*

Two rows carry most of the weight. **Account takeover**: `droundy` "published arrayref 0.3.10 and yanked 0.3.5-0.3.9 — its entire clean history — in a 40-second window, no reason given". Forty seconds is not a maintainer having second thoughts about five releases; it is a script running. And **stolen identity**: `proc-macro1`'s description was copy-pasted verbatim from `proc-macro2`, pinned to `1.0.107` — `proc-macro2`'s exact current version *in this project's own lock file*. A version number chosen to read as unremarkable in a lock file diff, and the fleet caught that it matched the real crate the project was already resolving.

### A rate limit is not a negative finding

The most transferable lesson in the whole record is a 403. The fleet asked whether a RustSec advisory existed yet. Every probe came back HTTP 403, rate limit exceeded — code search, commits list twice, contents-API fallback.

The section was recorded as **Indeterminate**. Not "no advisory exists".

A failure to observe is not an observation of absence. An error, a permission denial, a rate limit — collapse any of those into a negative finding and you get a confident wrong answer with every check apparently green. My agent instructions carry that as an explicit rule; this is the first time I have watched it bite in the wild, on a question that mattered, under time pressure.

The situation also moved under the observation. Between two checks four minutes apart, `append-only-vec` 0.1.7–0.1.8 went from yanked to un-yanked. Neither check was wrong. The world changed between them, and the record is timestamped enough to show that.

### What it got right, and what it missed

The strongest single result is the **payload shape** row. A crate with a ten-year zero-dependency history had suddenly acquired a transitive `ureq` + `rustls` + `base64` closure — an HTTP client, a TLS stack and an encoder — inside a *proc-macro*. From that shape alone the fleet inferred compile-time network egress: code that runs during the build, in CI and on every developer's machine. Hours later the postmortem confirmed it. The crate "had a build script that was downloading a malicious payload". `ureq` + `rustls` **is** downloading.

What it did not do is read the build script source. It reasoned from the dependency graph to the mechanism rather than observing the code that implemented it. Right answer, indirect evidence — and worth naming, because an inference that happens to land is not a confirmation.

Where it genuinely fell short was scope. The postmortem names six malicious crates — "This crate proc-macro1 and others like it (proc-macro-en, aovine, arone, aronenao, tinymember) have been deleted." The fleet had `proc-macro1` and missed all five of the others. That is a scoping failure, and scoping is the job I keep saying is mine and not the agent's — see {{< relref "systems/llms_for_coding/index.md" >}}. "Characterise this incident" was too loose a goal; I got a precise, well-evidenced answer about one crate when the question that mattered was how many there were.

The practical advice is the Rust team's, not mine: "We recommend you check your local dependencies to ensure these crates were not pulled in." Their postmortem hands you a ready-made `find ~/.cargo/registry/cache` command, which is a better check than anything my fleet ran, because it asks about *you* rather than about crates.io.

What saved this build was not intelligence. It was a strict gate on a boring transitive dependency, and an agent that read a red light as a question. Longer term I would rather not be inferring intent from yank patterns at all; provenance ought to be a property of the artefact, not an inference from the registry's edit history. That is a different post: {{< relref "workbench/pervasive_supply_chain_provenance/index.md" >}}.
