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

## Watching my software factory handle a live supply chain attack

I was not looking for a supply chain attack. I was working on [gh-report](https://github.com/Mattilsynet/gh-report), a Rust project that has nothing to do with `arrayref`, on a task that had nothing to do with `arrayref`, and my build went red.

`cargo deny` had fired. The reason was that a dependency the project had pinned for months — `arrayref 0.3.9` had just been yanked out from under it.

I had never chosen `arrayref`. It is a transitive dependency; it came along with `blake3` which I use for my Pardosa event stream library.

First, credit where it belongs. Discovery goes to the Research Team at Nextron Systems GmbH; the postmortem thanks them "for initially discovering this and reporting it to us", and that report reached crates.io at 07:15 UTC. Remediation goes to crates.io and the Rust Security Response Team, who deleted the malicious versions, un-yanked the maliciously-yanked ones and locked the account. The authoritative account is at: [Supply chain attack on arrayref](https://blog.rust-lang.org/2026/08/20/supply-chain-attack-on-arrayref/) (Manish Goregaokar, on behalf of security-response). I did notify the crates.io security team once my agents had characterised what they were seeing. I make no claim on the discovery, and by the time I reported it the professionals were already working the incident. Nothing below changes that ordering.

The attacker had to yank `arrayref` 0.3.5 through 0.3.9. That is the mechanism. A poisoned 0.3.10 sitting quietly alongside five healthy releases converts nobody in the short term, and time is not on the attacker's side here; consumers stay where their lock files put them. Yank the modern release history and things will start moving at much higher speeds. Tooling and supply-chain gates all start pushing people up onto the one live modern version. The yank *is* the delivery.

### The agents fell for it, then caught themselves

At the time of the attack I was using Opus 5 (writing) and Sol (review) for most of my work. Normally I´d use Sonnet 5 but a Pardosa clean-room rewrite was about to start and I felt like bringing some sharper tools for that job. If this made any difference I do not know, but Opus 5 is about to save my day here. Probably helped by the invariants partly enforced mechanically and partly guided through prompt engineering in what together resembles the software factory setup.

Here is the obvious response to "cargo deny says your dependency is yanked": bump to the newest version. It is what a tired human does. It is what a careless agent does. In this case it walks straight into `arrayref 0.3.10`, which is the entire point of yanking the alternatives.

The trap worked. Agent **Hopper**, the agent that writes the code, ran `cargo update -p arrayref --precise 0.3.10`, and the lock file moved onto the poisoned version. No cleverness saved anyone here.

What stopped it was the next step, the unglamorous one: read the diff before you commit.

![two terminal panes: the first shows cargo update -p arrayref --precise 0.3.10 updating arrayref v0.3.9 to v0.3.10 while adding proc-macro1 v1.0.107 and ureq v2.12.1; the second shows git diff --stat reporting 33 insertions and 2 deletions in Cargo.lock, followed by the verdict line "This is a hard stop. Rolling back immediately."](hopper-hard-stop.png)

*The origin of the whole story: the obvious command, its consequences, and the review step that refused them.*

Thirty-three insertions and two deletions, for a patch-level version bump. A patch bump moves two or three lines. Thirty-three lines is a different kind of change, and the shape of it is the tell: a version bump does not add an HTTP client.

Cargo had already said as much a moment earlier, in its own output — `Adding proc-macro1 v1.0.107`, `Adding ureq v2.12.1`. The information was on screen before the diff was. It still took the review step to act on it, which is roughly the argument for having a review step.

"This is a hard stop. Rolling back immediately." The rollback happened before any commit, so the poisoned lock file never entered the history.

### The investigation

What had replaced the yanked versions, and the fact that 0.3.10 carried a brand-new dependency `arrayref` had never had in its life — on a crate published four minutes earlier. The orchestration agent **Moltke** took that question into its own session and worked it out signal by signal. My software factory runs on mission command principles, hence Moltke, and when an agent gets a "Surprise" that is a back brief. This is helpful to prevent the agents from getting cornered and becoming too creative and dangerous.

![moltke's evidence table for a verdict of MALICIOUS at high confidence, listing six independent signals: a typosquat publisher, a stolen identity copied from proc-macro2, an account takeover, no reviewable source for the published version, the payload shape implied by the dependency closure, and the yank itself as the delivery vector](moltke-evidence.png)

*The reasoning behind the verdict, inside moltke's own session: six independent signals, assembled before anything was reported upward.*

Two rows carry most of the weight. **Account takeover**: `droundy` "published arrayref 0.3.10 and yanked 0.3.5-0.3.9 — its entire clean history — in a 40-second window, no reason given". Forty seconds is not a maintainer having second thoughts about five releases; it is a script running. And **stolen identity**: `proc-macro1`'s description was copy-pasted verbatim from `proc-macro2`, pinned to `1.0.107` — `proc-macro2`'s exact current version *in this project's own lock file*. A version number chosen to read as unremarkable in a lock file diff, and the agents caught that it matched the real crate the project was already resolving.

What reached me, one level up in the build context, was not that table but a consolidated verdict — detailed reasoning stays down in the subagent session, and the level above re-verified it rather than accepting it. I only read these details much later as I was working on Pardosa, remember, this gh-report maintenance was running in a different terminal.

![moltke's consolidated finding: an independent verification of an in-progress supply chain attack on the arrayref crate, showing the typosquatted proc-macro1 publisher, the 07:15:00Z publication of arrayref 0.3.10, the yanked 0.3.5 through 0.3.9, and the dependency on proc-macro1 1.0.107 read from the crate manifest](moltke-summary.png)

*The third pass, at the top level: "Stop — moltke's finding is real. I verified it independently against the crates.io API and the crate manifest itself." The decisive line is `[dependencies.proc-macro1] version = "1.0.107"` — read out of the manifest, not inferred.*

Two numbers on that screenshot are worth stopping on. `proc-macro1` had **9 downloads**. Nine. At the moment of detection the payload crate's blast radius was still essentially nil. `arrayref`, the crate it had just been attached to, had **244,989,384**. That asymmetry is the whole business model of a supply chain attack: you do not need anyone to install your crate, you need one crate that everybody already installs to install it for you.

The value here was not that a language model is clever. It was a gate configured to fail loudly, and a review step the agent was not allowed to skip.

### The setup

Two names have been doing work in this post without introduction, so: I run [opencode](https://opencode.ai) with a set of named agents, each a separate subagent with its own context, dispatched for one role. The roster follows Boyd's OODA loop — copernicus observes, feynman orients, moltke decides, hopper and linus act. **hopper** is the one that writes code and commits. **moltke** is the one that decides and commands. That is why the three screenshots above are three different sessions; Hopper discovers, Moltke actually tasks Copernicus to gather information (not shown). Moltke then diagnoses and hands back to the opencode Build context I typically use to interact. This creates an orchestrator of orchestrators situation with build and Moltke, which may be too much, but essentially means I can run for hours unattended if needed. Because the build context simply asks Moltke to march and if moltke returns or compacts that has relatively small consequences. The beads keep memory of what we are doing, the hundreds of ADRs are managed by my adr-fmt tool and keeps the course steady, graphify connects some dots, git keeps the history at proper distance form the context.

Agents live here: <https://github.com/acje/.config>.

My agents inferred the payload from the dependency closure and never opened it. SafeDep did: [Malicious Rust Crate arrayref Runs a Build-Time Payload](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/) has the `build.rs` source, the decoded endpoints, the per-platform payloads and the IOCs.
