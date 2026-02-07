---
title: "Digital Sovereignty"
description: "A roadmap to reduce systemic digital risk via politically mandated supply chains, hosting, and operations, paired with isolation-first architectures."

date: 2026-01-22
lastmod: 2026-02-06

---

# Digital Sovereignty

*Break digital vassalage. Use politics and architecture to reshape the systems that run our infrastructure and services. By targeting the ecosystem, every sector of society gains.*

Published 2026-01-22, Updated 2026-02-06

## The Risk We Built

Our infrastructure runs on brittle, shared systems. They fail together. The cocktail of pervasiveness, commonality, and fragility creates conditions of systemic vulnerabilities, prone to cascading failures. We must set out to chart an ecosystem that drives common vulnerabilities to tolerable levels. Describing how existing information systems can be sufficiently patched and remodeled to become secure is not a goal; in fact, it is assumed to be impossible. A real rupture needs to happen, and the old systems will not likely cross the chasm. Still, the defeatism that prevails in parts of the IT industry—that we simply cannot have inherently secure systems—is equally rejected in this article. It will be asserted that such an ecosystem consists of five principal necessities. By targeting the ecosystem, every sector of society gains. This must be done through politically mandated, verifiable, and trusted supply chains, hosting, and operations. Further, this must be combined with architecture principles that limit blast radius by employing isolation as a defense-in-depth strategy and rigidly enforce least-privilege interfaces at all levels.

## Fragile Systems, Everywhere

The geopolitical rules are changing. We do not yet know them. The systems and attitudes that got us here are unlikely to carry us through. For the purpose of this article, I will defer the naming of the coming period to the historians. When considering this looming challenge it is important to realize that the adversaries and their capabilities are not the significant source of the problem. The adversary is inevitable. The big problem is our own creation of a target-rich environment of critically important systems with common vulnerabilities. There will eventually be an adversary with the means and motivation to exploit the vulnerabilities against us. The additional risk posed by a nation-state adversary is not its ability to penetrate and exploit information systems, but its ability to coordinate with other events. The list of historic attacks exploiting systemic weaknesses is long: Stuxnet, NotPetya, WannaCry, HeartBleed, SolarWinds, Colonial Pipeline operations, Ukraine energy grid attacks, and Salt Typhoon telecom attacks, to name a few famous examples. These attacks come in uneven waves. Their impact tracks the field of targets more than the skill of the attacker.

### Self-Organized Criticality

Forest fires teach a hard rule: small sparks, big damage. The nature of the spark does not matter. The buildup in the ecosystem does. The spark is inevitable. Mathematician Per Bak and others named it: self‑organized criticality.

Pervasive digital transformation can unfortunately achieve the same. We seed every sector with insecure systems, thereby creating a situation where even a single mode of attack or shared vulnerability may trigger a ripple effect through our society. This could end up tearing down critical infrastructure and services like energy, communication, healthcare, finance, transportation, and water supply. In the worst-case scenario these will coordinate in time with other adversarial events.

The fix is simple—not easy. Use politics and architecture to reshape the ecosystem that makes our systems. Three political and two architectural necessities follow. They will not erase risk; they will cut it to levels fit for critical infrastructure and services.

### Critical or Not, Built the Same

Critical systems add rigor and isolation. Yet they use many of the same components as non‑critical ones. When the functional needs are the same, there is rarely any gain in using lower‑grade software components or services in non‑critical systems. The hardware may vary somewhat more in quantity and sometimes also in quality, but most system attributes are software‑defined these days.

## Where the Fight Is Won

Where we act matters. Act at the digital ecosystem level to lift outcomes across the board.
The digital ecosystem supplies parts and people. From it we build systems. Systems face security events that create security outcomes dependent on system resilience and organizational response. Let us define the terms.

The *digital ecosystem* consists of all the available services, components, and trained personnel that go into creating *information systems*. The systems themselves are created from what is available at their time of creation and what can reasonably be retrofitted during their period of maintenance, which may span decades. These information systems cause *security events* such as unexpected downtime due to internal, natural, or adversarial actions affecting the system. Depending on the system's ability to withstand these events and the organization's ability to plan for and react to these events, we get *security outcomes*. In this article, we will look at actions we can take at the ecosystem level to create a situation where all new and actively maintained systems can be made to produce meaningfully better security outcomes. When we intervene at this level, we are more likely to maximize impact compared to intervening at lower levels of this model.

Digital ecosystem → Information systems → Security events → Security outcomes

We must change the ecosystem that shapes our systems. Three political and two architectural necessities will carry pervasive digitization with less risk.

## Five Hard Necessities

We group necessities into politics and architecture. The political necessities will often require multinational action. Architecture may also need political help to advance at an acceptable pace, but these mandates must leave room for change. These five necessities make digital systems meaningfully more secure by strengthening our digital sovereignty and ability to defend our information systems.

### Political Necessities

Strategic and operational means to sustain our ability to build and maintain

- Trusted supply chains
- Trusted hosting
- Trusted operations

### Architectural Necessities

Tactical means to create defendable systems

- Maximally isolated components of least capability
- Least-privilege interfaces

## Political Necessities Explained

*A rising tide lifts all boats*

We have created multinational organizations like ESA, CERN, and the ITER project to advance capabilities in space, science, and energy. Yet we build our societies, and even the aforementioned organizations, on digital components and services that are often built by a single, anonymous, unpaid individual, or sometimes single-sourced from a foreign company. The absurdity of this situation seems to be lost on policymakers and the industry alike. In a world of nations seeking to secure leverage for their own geopolitical power by means of controlling our supply chains, hosting, and operations, this is going to become a huge vulnerability. It simply is not sustainable for small, medium, or super powers to depend on such components and services. The vulnerability of the individual and the leverage wielded by a company dominating the delivery of a critical component is just unacceptable. This has always been the case, but now it is obvious. Politicians and top bureaucrats talk about exit strategies. An exit to what exactly? The entire industry is an entangled mesh of honey traps and velcro.

## Capabilities and Market Failures

Some cornerstone digital capabilities must be built together, across borders. Others must be built at home. Organizations can only stand on what is made. These cornerstones do not rise from free markets or from globalization. Behavioral economics shows why the market does not create the necessary components for secure and sovereign information systems.

The gains are scattered and late. The costs are close and now. This pulls buyers toward the cheap and the quick, not the resilient. Status quo bias and switching costs hold the old dependencies in place, even when exit is possible.

## 1. Trusted supply chains

Of the three political necessities, this is the most potent for two reasons:

- Not a lot has been done to improve the robustness of supply chains, whereas hosting and operations are more mature
- The components available across supply chains are not delivering the necessary capabilities to build defendable information systems. But the solutions are emerging in the form of WebAssembly and the actor model.

In this document, the supply chain encompasses hardware, software, and critical services that enable the creation and operation of information systems. These services include identity and access management, code and package repositories, container registries across major clouds, and build systems such as GitHub Actions.

These supply chains rely heavily on national or multi‑national technology companies but also on small ad-hoc groups or even individual open‑source contributors who may be unpaid, unidentified, and vulnerable to pressure from nation‑state actors.

### Solutions to the supply chain challenge

Define a sovereign stack baseline: runtimes, frameworks, build systems, and registries with verifiable provenance.
Publish reference implementations and compliance tests; make certification cheap and repeatable.
Seed adoption through public services, then expand to regulated sectors.
Require hosting/operations to support Wasm isolation and actor‑based service boundaries.

- Set defaults through procurement in public and critical infrastructure builds; make these defaults the easiest path to pass audits.

- Create a trusted supply chain; require provenance and reproducible builds.

- Make risk visible: “systemic‑risk labels” on components and hosting providers; tie procurement points to lower‑risk stacks.

- Coordinate investment: pooled, multinational funding for reference runtimes, verification tools, and actor frameworks; reduce the upfront cost hump.

- Realign incentives: liability and insurance discounts for default architectures; penalties for shared‑risk dependencies not under control by a certified multinational or national organization.

## 2. Trusted hosting

Trusted hosting is sort of a new problem. We used to keep out data in our own buildings, but then the cloud happened. The cloud may or may not be cheaper. That discussion is really not very intelligible because it primarily depends on the technical debt, technical skill and appropriate framing of the transition by management of the cloud customer. The pricing model of the cloud provider is just adaptation to the market. The cloud is not really about cost but about speed, or opportunity cost, if you insist.

### Solutions to the hosting challenge

Many cloud customers has experienced that once they have built an organization capable of building their own software rather than operating bought software, the cloud is not all that necessary. The agency gained form being able to build can be used to transition to any type of hosting, including your own. If however one has done a lift and shift ov legacy systems from the basement to the cloud it will be equally obvious that the lack of agency makes the cloud about at painful as the basement.

The solution to the hosting problem is relatively simple for those who used the cloud transition to build agency.

## 3. Trusted operations

Lastly we need to secure trusted operations and this is perhaps the lowest hanging fruit. Generally nations have been able to operate their own systems with vetted personnel for the most critical infrastructure and services by now. There is however some common flaws. Many providers of more complex systems has a tendency to require som kind of remote management solution. Some organizations also do not have the internal technical capacity to operate all their own infrastructure and services, and typically rely on third party providers to manage parts of their systems. This creates a market for common resources with wide spread access across many organizations.

### Solutions to the operations challenge

Vet personnel and build in house skills. This one is not hard to do.

## Architectural Necessities Explained

Scope is to point out the two most long term unappreciated aspects of computer engineering, not to enumerate every technical lever readily available to us. Hence there will not be a rich discussion about distributed computing. That topic is well covered and understood, albite complex.

## 4. Maximally isolated components of least capability

My previous series on Substack;
[Liberal democracies need a new compute stack. Part 1](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute)
[Part 2](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-2fd),
[Part 3](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-523) and
[Part 4](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-d56)
may serve as a more comprehensive introduction to this topic. I will describe it more briefly here.

### Solutions to Maximally isolated components of least capability

- Set defaults through procurement: mandate Wasm + actor‑based isolation in public and critical infrastructure builds; make it the easiest path to pass audits.
- Create a trusted supply chain: certify Wasm runtimes, actor libraries, compilers, and toolchains; require provenance and reproducible builds.
- Make risk visible: “systemic‑risk labels” on components and hosting providers; tie procurement points to lower‑risk stacks.
- Coordinate investment: pooled, multinational funding for reference runtimes, verification tools, and actor frameworks; reduce the upfront cost hump.
- Realign incentives: liability and insurance discounts for isolation‑first architectures; penalties for shared‑risk dependencies.
- Why WebAssembly + actor model fits the defensibility  goal because everything is sandboxed and there are no implicit interfaces

Wasm enables portable, sandboxed components with strong isolation, reducing blast radius and dependency on a single vendor.
The actor model enforces least‑privilege interfaces and message‑passing boundaries; failures do not cascade easily.
Together they match the “isolation‑first” architecture in the Digital Sovereignty roadmap, while fitting the political need for trusted supply chains, hosting, and operations.
Practical roadmap (policy + architecture)

Define a sovereign stack baseline: Wasm runtimes, actor frameworks, build systems, and registries with verifiable provenance.
Publish reference implementations and compliance tests; make certification cheap and repeatable.
Seed adoption through public services, then expand to regulated sectors.
Require hosting/operations to support Wasm isolation and actor‑based service boundaries.

Non-solutions

- Third party code - technically ok, but impractical to control
- Library - not sandboxed
- Script language (Lua, embedded JS engine) - inefficient

## 5. Least-privilege Interfaces

### Solutions to Least-privilege Interfaces

Clearly define interfaces derived from function signatures of exposed functions.

## Final thoughts

Formal verification as explored in the 60ies and 70ies was never going to be a big part of secure information systems and the later strategy of "enumerating badness", that is the creation of software that catalogs anything that is unwanted such as viruses, worms, software behavior was never going to be more than a temporary stop gap.

Defeatism is not necessary in information security. We been through formal verification and got overwhelmed by complexity. Enumerating badness and got overwhelmed by badness.

## More to Read

[Liberal democracies need a new compute stack. Part 1 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute)

[Liberal democracies need a new compute stack. Part 2 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-2fd)

[Liberal democracies need a new compute stack. Part 3 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-523)

[Liberal democracies need a new compute stack. Part 4 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-d56)

[Maturity levels in the CISQ security model](https://acje.github.io/CISQ-maturity)
