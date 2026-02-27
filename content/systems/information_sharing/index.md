---
title: "Information sharing is not a solved problem"
aliases:
  - "/information_sharing/"

---

## Information sharing is not a solved problem

**Under construction**

Technical article about a secure, cross-organizational platform for timely information-sharing depicted below.

![Information sharing](information_sharing_clean.png)

## The question is always the same

"How can we share this information with X." The follow-up by the tech lead, architect, developer, or administrator is also always the same: What are the requirements?

And that is a question rarely, if ever, answered fully. Performance, completeness, correctness, [security]({{< relref "systems/CISQ-maturity/index.md" >}}), maintenance, budget? Everyone has their own subset of requirements, which they are usually only partially aware of. What if we could solve for everything except budget, once, and drive down the cost through economies of scale?

That is the strategy underlying the following design.

![Information sharing between organizations](information_sharing.png)

## Characteristics of the design

todo

## Necessities for a national robust information sharing infrastructure

(this doom chapter was entirely written by gemini 3 following some heavy prompt engineering. I use LLMs a lot to style text and connect with fields outside my area of expertise like epidemiology and behavioral economics. This chapter ended up with a lot of references within my field of expertise which I need to check out, so I have left it here for now although I don´t like to have pure AI text on my site. - Proper Author)

To escape the cycle of recurring systemic failures and strategic dependency, we must rethink our infrastructure through the lens of high-reliability theory. As Ken Thompson demonstrated in *Reflections on Trusting Trust* (1984), a system's security is illusory if the tools used to build it are compromised; therefore, verified provenance in our software supply chain is a prerequisite for trust, protecting against the kind of hidden fragility Nassim Taleb warns can lead to catastrophic collapse. This technical autonomy is inseparable from political agency. Shoshana Zuboff’s analysis in *The Age of Surveillance Capitalism* suggests that ceding infrastructure to hyperscale monopolies is not merely an outsourcing decision but a surrender of governance, necessitating a shift back to hosting environments where the organization retains full jurisdictional control.

Conceptually, we must accept Charles Perrow's thesis in *Normal Accidents* that failure in tightly coupled systems is inevitable. Rather than striving for impossible perfection, we should emulate High Reliability Organizations (HROs) by designing for resilience and rigorous operational vetting. This requires a departure from monolithic architectures toward the "share nothing" principles of Carl Hewitt’s Actor Model (1973). By isolating components in a manner that prevents the "accidental complexity" of shared state described by Fred Brooks, and strictly enforcing Saltzer and Schroeder’s principle of *Least Privilege* (1975) through capability-based interfaces, we can construct systems where individual faults are contained, preventing minor errors from cascading into national crises.

## More to Read

- [Digital Sovereignty]({{< relref "systems/digital_sovereignty/index.md" >}})
- [Fiber semantics. Event sourcing for complex domains (Repository)](https://github.com/acje/Fiber-semantics)
