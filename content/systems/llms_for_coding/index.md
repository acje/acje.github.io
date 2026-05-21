---
title: "LLMs for coding, you are holding it wrong"
aliases:
  - "/llms_for_coding/"

date: 2026-05-21
lastmod: 2026-05-21
draft: false
homeFeatured: true
weight: 60
---

## LLMs for coding, you are holding it wrong

Most complaints about coding with large language models share a shape: the model produced something plausible, the developer accepted it, and the result was wrong in a way that was expensive to discover later. The conclusion is usually that the model is not good enough yet. Sometimes that is true. More often, the tool was held wrong.

This essay is about how to hold it.

## The autocomplete trap

The dominant interaction pattern is autocomplete: the developer types, the model suggests, the developer accepts or rejects. This is comfortable because it inherits the muscle memory of IDE completion. It is also where most of the failure modes live.

Autocomplete optimises for *plausibility at the cursor*. The model has no theory of the program, no access to the test suite's verdict, and no incentive to flag uncertainty. It will confidently complete a function call against an API that does not exist, hallucinate a field name that is almost right, or produce a regex that passes the visible example and fails the next one. The developer, primed to accept fluent text, often does.

The trap is that this works well enough often enough to feel productive. The errors that slip through are not random; they cluster at the edges where the model's training distribution thins out — exactly the places where careful engineering matters most.

## Hold it like a junior who never gets tired

A more productive frame: treat the model as a junior collaborator with broad but shallow knowledge, infinite stamina, no memory between sessions, and a tendency to bullshit when uncertain. This frame predicts the right interaction patterns:

- **Give it the context it needs, not the context you have.** Pasting a 2000-line file when the relevant surface is one struct wastes tokens and dilutes attention. Excerpt deliberately.
- **State the contract before asking for code.** Inputs, outputs, invariants, error modes, and what "done" looks like. The model is much better at hitting a target it can see than at inferring one from prose.
- **Make verification cheap and visible.** A failing test the model can run is worth ten paragraphs of review. Closed-loop tools (compile, test, lint) outperform open-loop suggestions by a wide margin.
- **Halt on surprise.** If the output contradicts something you know to be true, stop and find the contradiction. Do not paper over it; the model will help you paper over it indefinitely.

This is not new advice. It is the same discipline that works with any junior collaborator. The novelty is that the junior is fast, cheap, and never sleeps — which means the discipline scales differently.

## Agents and the verify-before-claim rule

The agent frame — give the model tools (shell, file edit, web), let it loop — changes the failure mode but not its source. An agent that cannot verify its own work will hallucinate completion just as fluently as autocomplete hallucinates code. The rule that earns its keep is *verify before claim*: the agent must produce evidence that the change works (exit code, test output, a parseable artefact) before reporting success.

In practice, this means:

1. Every non-trivial change ends with a runnable check the agent executed and whose output it can cite.
2. Empty output from an evidence-producing pipeline is treated as surprise, not success.
3. The agent halts and reports rather than fabricating a plausible-looking result when the check fails.

Agents that follow this rule produce dramatically less slop. Agents that don't produce slop at machine speed.

## Where this leaves us

The interesting engineering question is not whether LLMs are good enough to write code. They are good enough for a wide and growing class of problems, and they will get better. The interesting question is what discipline scales to keep the failure rate bounded as the volume of generated code grows.

The answer is closed-loop, evidence-carrying, contract-first interaction — at every level, from the autocomplete keystroke to the multi-agent mission. Hold it that way and it works. Hold it the other way and it produces a lot of code that almost compiles, almost passes review, and almost does the thing you asked for.

Almost is the expensive word.
