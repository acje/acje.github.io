---
title: "Information sharing is not a solved problem"
aliases:
  - "/information_sharing/"

---

## Information sharing is not a solved problem

**Under construction**

Technical article about a secure, cross-organizational platform for timely information-sharing depicted below.

![Information sharing](information_sharing_clean.png)

## A Common Challenge

When asked, "How can we share this information with X?", technical leads, architects, developers, and administrators invariably ask in return: "What are the requirements?"

This follow-up question is rarely answered fully. Stakeholders often have vague or conflicting priorities regarding performance, completeness, correctness, [security]({{< relref "systems/CISQ-maturity/index.md" >}}), maintenance, and budget.

The design presented here aims to solve these technical requirements holistically, leaving only the budget to be determined, and reducing costs through economies of scale.

## Requirements

**Secure.** Availability, integrity, authenticity, and control must be protected. See [security]({{< relref "systems/CISQ-maturity/index.md" >}}) for details.

**Timely delivery.** Applications often require up-to-date information. Daily batch transfers may introduce unacceptable latency.

**Efficient resource usage.** While nightly full downloads are acceptable for small datasets, this approach is inefficient at scale.

**Discoverability and semantic validity.** Users must be able to find and interpret data correctly. This is essential for any large-scale data platform.

**Completeness and correctness.** The same dataset should be available at both the source and the destination. This is a complex requirement to describe and implement due to physical constraints. Einstein's special relativity dictates that information cannot travel faster than the speed of light, meaning immediate consistency across distributed locations is impossible.

However, it is possible to achieve _eventual consistency_, where the destination eventually reflects the state of the source. This is the optimal solution within known physical limits. To guarantee eventual consistency, we rely on two principles:

1. **At-least-once delivery:** The source must ensure every message is delivered to the destination at least once. In a distributed system, this guarantee must be maintained for each destination independently.
2. **Idempotence:** The destination must be able to process duplicate messages without changing the result.

By combining _at-least-once delivery_ with _idempotence_, we achieve _exactly-once semantics_, ensuring the dataset is successfully replicated at the destination.

![Information sharing between organizations](information_sharing.png)

## Characteristics of the design

todo

## Necessities for a national robust information sharing infrastructure

(this doom chapter was entirely written by gemini 3 following some heavy prompt engineering. I use LLMs a lot to style text and connect with fields outside my area of expertise like epidemiology and behavioral economics. This chapter ended up with a lot of references within my field of expertise which I need to check out, so I have left it here for now although I don´t like to have pure AI text on my site. - Proper Author)

To escape the cycle of recurring systemic failures and strategic dependency, we must rethink our infrastructure through the lens of high-reliability theory. As Ken Thompson demonstrated in _Reflections on Trusting Trust_ (1984), a system's security is illusory if the tools used to build it are compromised; therefore, verified provenance in our software supply chain is a prerequisite for trust, protecting against the kind of hidden fragility Nassim Taleb warns can lead to catastrophic collapse. This technical autonomy is inseparable from political agency. Shoshana Zuboff’s analysis in _The Age of Surveillance Capitalism_ suggests that ceding infrastructure to hyperscale monopolies is not merely an outsourcing decision but a surrender of governance, necessitating a shift back to hosting environments where the organization retains full jurisdictional control.

Conceptually, we must accept Charles Perrow's thesis in _Normal Accidents_ that failure in tightly coupled systems is inevitable. Rather than striving for impossible perfection, we should emulate High Reliability Organizations (HROs) by designing for resilience and rigorous operational vetting. This requires a departure from monolithic architectures toward the "share nothing" principles of Carl Hewitt’s Actor Model (1973). By isolating components in a manner that prevents the "accidental complexity" of shared state described by Fred Brooks, and strictly enforcing Saltzer and Schroeder’s principle of _Least Privilege_ (1975) through capability-based interfaces, we can construct systems where individual faults are contained, preventing minor errors from cascading into national crises.

## More to Read

- [Digital Sovereignty]({{< relref "systems/digital_sovereignty/index.md" >}})
- [Fiber semantics. Event sourcing for complex domains (Repository)](https://github.com/acje/Fiber-semantics)
