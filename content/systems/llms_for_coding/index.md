---
title: "LLMs for coding, we´re holding it wrong"
aliases:
  - "/llms_for_coding/"

date: 2026-05-21
lastmod: 2026-05-22
draft: false
homeFeatured: true
weight: 60
---

## LLMs for coding, we´re holding it wrong

Here are some perhaps counterintuitive lessons I have picked up, in no particular order, during my first ~1M lines of code;

Note of warning. If you havent internalised [Stop Looking at Your Code](https://www.oreilly.com/radar/steve-yegge-wants-you-to-stop-looking-at-your-code/) then this will not make any sense.

- This post was not written using an LLM. Unlike all my code.
- LLM is not AI, it is pattern recognition. I tend to align with Richard S. Sutton and Yann LeCun on this topic.
- Code should not have comments. 😱 It is a source of drift. See “dumb zone”.
- Rust is a good target for LLMs exactly because of its constraints. Other languages may be even better, but I haven’t tried yet. Pony may be even better? It is all about early mechanical feedback. Compile time feedback trumps runtime feedback.
- Use all the linters and constraints your toolchain makes available. The work you need to do when cleaning up a codebase that hit its peak entropy is orders of magnitude larger than the work your agents need to do to work with the added constraints. Unless of course you just give up at this point.
- If you are of the conviction that you do not want to use AI, then be aware that it has never been controversial to not use something that does not exist
- LLMs are pattern recognition over historical human information output. The anthropomorphism is built in. Do not fall for it.
- Coding with an LLM is mostly about managing the goal and the SNR of the context
- The “smart zone” and “dumb zone” of an LLM is not a very useful mental model. The dumb stuff is largely the noise of your context sitting in the “smart zone”. Bad news; it is on you. Good news; this is actionable
- Building tools to structure documentation is helpful

“Smart zone” / “Dumb zone” is real, but only part of the picture; The SNR (Signal to Noise Ratio) in the context is at least part of the picture, together with non perfect weights from the training
and normal transformer based neural network behavior

Principles for better results. You have more than one job.

- Job 1: Define the goal. What does good look like?
- Job 2: Manage SNR. Prune the available information that might end up in a context like a gardener removes weed.
- Job 3: Rephrase negatives as the opposite positive. Pattern recognition does not do well with negatives! Or rather “Pattern recognition works well with descriptions of the pattern”
- Job 4: manage Agent autonomy and ability to do feedback when they get stuck. This is Mission command with back brief in practice

Things I have found my self making to help LLMs code better;

- Comment-free a tool to remove comments in rust; will probably be integrated with upcoming adr-srv to allow strict doc comments that link to ADRs
- Adr-fmt a tool to lint ADRs; about to be replaced by adr-srv
- Library “Cherry-pit” to encode DDD, EDA and Hexagonal architecture, I do not want to guide an LLM through this exercise more than once
- Library “Pardosa” to encode how an event stream should work
- Actor Enclave Model (TBD), a framework to orchestrate components such that communication security model becomes fully capability based

All of these are constraints to reduce the chance a LLMs do not do the obvious wrong thing. It is just such an exhaustive task to enumerate all the classes of wrong.

The tooling and libraries are mostly living here; I do not live at the very edge of agentic engineering, but hopefully some of these ideas are worth following.

[Solon story (Repository)](https://github.com/acje/solon/blob/main/docs/STORY.md)
[Agents (Repository)](https://github.com/acje/.config)
