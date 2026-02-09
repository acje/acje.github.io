---
title: "Digital Sovereignty"
description: "Why systemic risk demands a new digital ecosystem—and the five necessities to make it real. Linking resilience engineering, security, and political economy, behavioral economics"

date: 2026-01-22
lastmod: 2026-02-07

---

# Digital Sovereignty

*Break digital vassalage. Use politics and architecture to reshape the systems that run our infrastructure and services. By targeting the ecosystem, every sector of society gains.*

Published 2026-01-22, Updated 2026-02-08

## The Risk We Built

Our information systems run on brittle, shared components and services. They fail together. The cocktail of pervasiveness, commonality, and fragility creates conditions of systemic vulnerabilities prone to cascading failures. We must set out to chart an ecosystem that drives common vulnerabilities to tolerable levels. Describing how existing information systems can be sufficiently patched and remodeled to become secure is not a goal; in fact, it is assumed to be impossible. A real rupture needs to happen, and the old systems will not likely cross the chasm. Still, the defeatism that prevails in parts of the IT industry—that we simply cannot have inherently secure systems—is equally rejected in this article. It will be asserted that such an ecosystem consists of five principal necessities. By targeting the ecosystem, every sector of society gains. This must be done through politically mandated, verifiable, and trusted supply chains, hosting, and operations. Further, this must be combined with architectural principles that limit blast radius by employing isolation as a defense-in-depth strategy and rigidly enforce least-privilege interfaces at all levels.

## Fragile Systems, Everywhere

The geopolitical rules are changing. We do not yet know them. The systems and attitudes that got us here are unlikely to carry us through. When considering this looming challenge, it is important to realize that the adversaries and their capabilities are not the significant source of the problem. The adversary is inevitable. The significant problem is our own creation of a target-rich environment of critically important systems with shared and interconnected vulnerabilities. There will eventually be an adversary with the means and motivation and opportunity to exploit the vulnerabilities against us, at costs we have yet to experience. The additional risk posed by a nation-state adversary is not its ability to penetrate and exploit information systems, but its ability to coordinate with other events. The list of historic attacks exploiting systemic weaknesses is long: Stuxnet, NotPetya, WannaCry, Heartbleed, SolarWinds, the Colonial Pipeline attack, Ukraine energy grid attacks, and Salt Typhoon telecom attacks, to name a few famous examples. These attacks come in uneven waves. Their impact tracks the field of targets more than the skill of the attacker.

### Self-Organized Criticality

Forest fires teach a hard rule: small sparks, big damage. The nature of the spark does not matter. The buildup in the ecosystem does. The spark is inevitable. Mathematician Per Bak and others named it: self‑organized criticality. These systems are stabilized by managing the buildup of potential in the environment, not by suppressing trigger events.

Pervasive digital transformation can, unfortunately, achieve the same. We seed every sector with the same insecure components, shared services and architectures with weak forms of isolation, thereby creating a situation where even a single mode of attack or shared vulnerability may trigger a ripple effect through our society. This could end up tearing down critical infrastructure and services within defense, energy, communication, healthcare, finance, transportation, and water supply. In the worst-case scenario, these will coordinate in time with other adversarial events.

The fix is simple—not easy. Use politics and architecture to reshape the ecosystem that makes our systems. Three political and two architectural necessities follow. They will not erase risk; they will cut it to levels fit for critical infrastructure and services.

### Critical or Not, Built the Same

Critical systems add rigor and isolation. Yet they use many of the same components as non‑critical ones. When the functional needs are the same, there is rarely any gain in using lower‑grade software components or services in non‑critical systems. The hardware may vary somewhat more in quantity and sometimes also in quality, but most system attributes are software‑defined these days.

## Threat model

The threat model adopted here combines nation‑state coercion, software supply‑chain compromise, and infrastructure fragility. It is argued that these cannot be treated in isolation.

## Where the Fight Is Won

Where we act matters. Act at the digital ecosystem level to lift outcomes across the board.
The digital ecosystem supplies parts and people. From it we build systems. Systems face security events that create security outcomes dependent on system resilience and organizational response. Let us define the terms.

The *digital ecosystem* consists of all the available services, components, and trained personnel that go into creating *information systems*. The systems themselves are created from what is available at their time of creation and what can reasonably be retrofitted during their period of maintenance, which may span decades. These information systems cause *security events* such as unexpected downtime due to internal, natural, or adversarial actions affecting the system. Depending on the system's ability to withstand these events and the organization's ability to plan for and react to these events, we get *security outcomes*. In this article, we will look at actions we can take at the ecosystem level to create a situation where all new and actively maintained systems can be made to produce meaningfully better security outcomes. When we intervene at this level, we are more likely to maximize impact compared to intervening at lower levels of this model.

Digital ecosystem → Information systems → Security events → Security outcomes

We must change the ecosystem that shapes our systems. Three political and two architectural necessities will carry pervasive digitization with less risk.

## Five Hard Necessities

We group necessities into politics and architecture. The political necessities will often require multinational action. Architecture may also need political help to advance at an acceptable pace, but these mandates must leave room for change. These five necessities make digital systems meaningfully more secure by strengthening our digital sovereignty and ability to defend our information systems.

### Political Necessities

Strategic and operational means to sustain our ability to build and maintain systems.

- Trusted supply chains
- Trusted hosting
- Trusted operations

### Architectural Necessities

Tactical means to create defensible systems.

- Maximally isolated components of least capability
- Least-privilege interfaces

## Political Necessities Explained

*A rising tide lifts all boats.*

We have created multinational organizations like ESA, CERN, and the ITER project to advance capabilities in space, science, and energy. Yet we build our societies, and even the aforementioned organizations, on digital components and services that are often built by a single, anonymous, unpaid individual, or sometimes single-sourced from a foreign company. The strategic vulnerability inherent in this situation seems to be lost on policymakers and the industry alike. In a world of nations seeking to secure leverage for their own geopolitical power by means of controlling our supply chains, hosting, and operations, this is going to become a huge vulnerability. It simply is not sustainable for small, medium, or great powers to depend on such components and services. The vulnerability of the individual and the leverage wielded by a company dominating the delivery of a critical component are unacceptable. This has always been the case, but now it is obvious. Politicians and top bureaucrats talk about exit strategies. An exit to what exactly? The entire industry is an entangled mesh of honey traps and velcro.

## Capabilities and Market Failures

Some cornerstone digital capabilities must be built together, across borders. Others must be built at home. Organizations can only stand on what is made. These cornerstones do not rise from free markets or from globalization. Behavioral economics helps explain why markets often under-provide the necessary components for secure and sovereign information systems.

The gains are scattered and late. The costs are close and now. This pulls buyers toward the cheap and the quick, not the resilient. Status quo bias and switching costs hold the old dependencies in place, even when exit is possible.

## 1. Trusted supply chains

Of the three political necessities, this is the most potent for three reasons:

First, not a lot has been done to improve the robustness of supply chains, whereas hosting and operations are more mature. Second, the components available across supply chains today are not delivering the necessary capabilities to build defensible information systems. Some promising solutions are emerging on the horizon in the form of WebAssembly and the actor model. These also represent an opportunity to establish a new supply chain ecosystem for defensible information systems. This will be further explored in the section "Architectural Necessities Explained". Third, it is much less effort to modify an immature supply chain than a mature one based on complexity alone.

In this document, the supply chain encompasses hardware, software, and critical services that enable the creation and operation of information systems. These services include identity and access management, code and package repositories, container registries across major clouds, and build systems such as GitHub Actions.

These supply chains rely heavily on national or multinational technology companies but also on small ad hoc groups or even individual open‑source contributors who may be unpaid, unidentified, and vulnerable to pressure from nation‑state actors.

### Solutions to the supply chain challenge

- Define a sovereign stack baseline: runtimes, frameworks, build systems, and registries with verifiable provenance.
- Publish reference implementations and compliance tests; make certification cheap and repeatable.
- Seed adoption through public services, then expand to regulated sectors.
- Require hosting and operations to support Wasm isolation and actor‑based service boundaries.
- Set defaults through procurement in public and critical infrastructure builds; make these defaults the easiest path to pass audits.
- Create a trusted supply chain; require provenance and reproducible builds.
- Make risk visible: “systemic-risk labels” on components and hosting providers; tie procurement points to lower-risk stacks.
- Coordinate investment: pooled, multinational funding for reference runtimes, verification tools, and actor frameworks; reduce the upfront cost hump.
- Realign incentives: liability and insurance discounts for default architectures; penalties for shared‑risk dependencies not under control by a certified multinational or national organization.

## 2. Trusted hosting

Trusted hosting is a relatively new problem. We used to keep our data in our own buildings, but then the cloud happened. The cloud may or may not be cheaper. That discussion is not very intelligible because it primarily depends on the technical debt, technical skill, and framing of the transition by cloud customer management. The pricing model of the cloud provider is just an adaptation to the market. The cloud is not really about cost but about speed, or opportunity cost, if you insist.

### Solutions to the hosting challenge

Many cloud customers have experienced that once they have built an organization capable of building their own software rather than operating bought software, the cloud is not all that necessary. The agency gained from being able to build can be used to transition to any type of hosting, including your own. If, however, one has done a lift-and-shift of legacy systems from the basement to the cloud, it will be equally obvious that the lack of agency makes the cloud about as painful as the basement.

The hosting path is clearer for organizations that used the cloud transition to build agency.

## 3. Trusted operations

Lastly, we need to secure trusted operations, and this is often the most tractable near-term lever. Generally, nations have been able to operate their own systems with vetted personnel for the most critical infrastructure and services by now. There are, however, some common flaws. Many providers of more complex systems have a tendency to require some kind of remote management solution. Some organizations also do not have the internal technical capacity to operate all their own infrastructure and services, and typically rely on third-party providers to manage parts of their systems. This creates a market for common resources with widespread access across many organizations.

### Solutions to the operations challenge

Vet personnel and build in-house skills. This one is not hard to do, but it must be structured and auditable by treating security as a management system, not a technical add-on.

- Establish a security management system with clear ownership, risk acceptance authority, and periodic management reviews.
- Classify information and services, then map classification to access control, segregation, and handling routines.
- Enforce least-privilege operations: role-based access, short-lived credentials, and dual control for high-impact changes.
- Reduce remote administration risk: require secure jump hosts, strong MFA, and time-boxed approvals with full session recording. Also, work to avoid this type of risk by building in-house skills and refraining from buying systems that require remote administration.
- Log everything that matters, centralize logs, and monitor for anomalies with clear escalation paths and response playbooks.
- Practice incident response: run exercises, keep breach containment runbooks, and verify recovery with offline backups.
- Require supplier and subcontractor controls: security clauses, audit rights, and minimum operational baselines.
- Maintain continuity for critical services: redundant staffing, documented procedures, and tested failover.
- Train and retrain: mandatory security awareness, operational drills, and role-specific competence requirements.

These are operational guardrails, not bureaucracy. They are the minimum to keep control when systems are stressed or under attack.

There is a specific field of operations within the field of computer engineering that is best known as "chaos engineering". This is controlled experimentation on systems to build confidence in resilience and to quantify resilience engineering properties such as graceful degradation, recovery time objectives, and safety margins under fault. A lot of information systems are deemed as done when they solve the tasks they were supposed to solve when given the expected inputs. The problem is that this leaves out the much broader problem of implementing failure modes. That is the implementation of what the system should not do when it experiences an unwanted or unexpected event. Any system of importance should be under a chaos engineering regime and this should also be formally required.

## Architectural Necessities Explained

The scope is to point out the two most long-term, unappreciated aspects of computer engineering, not to enumerate every technical lever readily available to us. Hence there will not be a rich discussion about distributed computing. That topic is well covered and understood, albeit complex.

## 4. Maximally isolated components of least capability

My previous series on Substack:
[Liberal democracies need a new compute stack. Part 1](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute)
[Part 2](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-2fd),
[Part 3](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-523) and
[Part 4](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-d56)
may serve as a more comprehensive introduction to this topic. I will describe it more briefly here.

### Summary of the Four-Part Series

The series establishes a geopolitical and technical case for combining WebAssembly (Wasm) and the actor model to achieve durable isolation in information systems.

**Part 1** argues that digital sovereignty requires a low-complexity, secure, and fast compute stack. Liberal democracies face dependencies on adversarial regimes (Russian energy, Chinese manufacturing, questionable American security commitments) and need defensible systems that preserve trust and transparency while shifting cyber battlefields in favor of defenders.

**Part 2** proposes a strategic contract modeled on Nvidia's success with CUDA: establish a software-defined interface (Wasm + actor model) that allows incremental migration and fast iteration cycles, with eventual hardware support. The actor model (Carl Hewitt) provides isolation through private state and message passing. Wasm delivers sandboxing, polyglot support, and capability-based interfaces. Wasmcloud demonstrates a working implementation combining both.

**Part 3** diagnoses the problem: current IT stacks are "ossified" at lower layers due to conflicting incentives—hardware seeks economy of scale and backward compatibility, software seeks economy of composition. The result is the von Neumann bottleneck, where shared memory becomes both a performance wall and an exploitable communication channel. Software-based isolation faces a credible commitment problem: its flexibility means it can't guarantee future behavior, creating strategic vulnerability. Hardware-backed isolation is necessary to establish trust.

**Part 4** distinguishes "pliable containment" (software isolation on traditional architectures) from "durable isolation" (hardware-backed separation). Software actor frameworks on von Neumann machines provide "happy-path actors" that fail under adversarial pressure. The series proposes a cluster-on-a-chip architecture with actor enclaves, where each actor is a physically isolated compute unit with private state. This enables arbitrary scaling, eliminates cascading failures, and shifts from "maximum capability" designs (C, C++, shared memory) to "enabling constraints" (Wasm, actors, capability-based security, tagged unions). The evolution: single actor paradigm → containerization → Wasm sandboxing → actor enclaves with durable isolation.

### Solutions to Maximally Isolated Components of Least Capability

- Set defaults through procurement: mandate Wasm + actor‑based isolation in public and critical infrastructure builds; make it the easiest path to pass audits.
- Create a trusted supply chain: certify Wasm runtimes, actor libraries, compilers, and toolchains; require provenance and reproducible builds.
- Make risk visible: “systemic‑risk labels” on components and hosting providers; tie procurement points to lower‑risk stacks.
- Coordinate investment: pooled, multinational funding for reference runtimes, verification tools, and actor frameworks; reduce the upfront cost hump.
- Realign incentives: liability and insurance discounts for isolation‑first architectures; penalties for shared‑risk dependencies.
- Why WebAssembly + actor model fits the defensibility goal: everything is sandboxed and there are no implicit interfaces.

Wasm enables portable, sandboxed components with strong isolation, reducing blast radius and dependency on a single vendor.
The actor model enforces least‑privilege interfaces and message‑passing boundaries; failures do not cascade easily.
Together they match the “isolation‑first” architecture in the Digital Sovereignty roadmap, while fitting the political need for trusted supply chains, hosting, and operations.
Practical roadmap (policy + architecture):

- Define a sovereign stack baseline: Wasm runtimes, actor frameworks, build systems, and registries with verifiable provenance.
- Publish reference implementations and compliance tests; make certification cheap and repeatable.
- Seed adoption through public services, then expand to regulated sectors.
- Require hosting and operations to support Wasm isolation and actor‑based service boundaries.

Non-solutions:

- Third-party code: technically acceptable, but impractical to control
- Libraries: not sandboxed
- Script languages (Lua, embedded JS engine): inefficient

## 5. Least-privilege Interfaces

Least-privilege interfaces should be the default contract surface for every component. WebAssembly (Wasm) with WASI provides a practical standard: modules start with no ambient authority and must be granted explicit, capability-scoped access to the host. This is a clear improvement over traditional APIs that inherit broad process privileges, shared file systems, and implicit network access, making boundaries fuzzy and over-permissive. With WASI, interface design is a policy lever: narrow, auditable capability sets replace sprawling API surfaces and reduce the cost of trust.

### Solutions to Least-privilege Interfaces

Security boundaries fail when they are implicit. In many systems, permission is assumed by proximity (e.g., 'root' user, internal network), leading to 'pliable containment' where a single breach grants total control. Best practice demands that interfaces function as strict contracts: every interaction must require an explicit, unforgeable capability token.

- Define interfaces as capability sets, not just function signatures; every call should map to a specific, auditable permission.
- Adopt WASI as the baseline host contract: no ambient authority, explicit grants for files, sockets, clocks, and randomness.
- Prefer capability-based handles over global namespaces; avoid implicit access to the host file system and network.
- Make interfaces small and versioned: narrow modules, stable IDs, and strict deprecation paths.
- Gate privileged capabilities behind policy checks, short-lived tokens, and runtime attestations.
- Require interface conformance tests and least-privilege audits as part of supply-chain certification.

## Final thoughts

Defeatism is not necessary in information security. We tried formal verification in the 1960s and 1970s, essentially aiming to prove correctness, and we were overwhelmed by complexity. We then shifted to enumerating badness, cataloging unwanted artifacts like viruses, worms, and hostile behaviors, and we were overwhelmed again by the churn of successful attacks. Neither approach can carry the weight of pervasive digitization. The next paradigm is isolation: workloads that are sandboxed by default so failures do not cascade, and risk is engineered down at the ecosystem level rather than chased system by system.

## More to Read

[Liberal democracies need a new compute stack. Part 1 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute)

[Liberal democracies need a new compute stack. Part 2 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-2fd)

[Liberal democracies need a new compute stack. Part 3 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-523)

[Liberal democracies need a new compute stack. Part 4 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-d56)

[Maturity levels in the CISQ security model](https://acje.github.io/CISQ-maturity)
