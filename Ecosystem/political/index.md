# An Ecosystem for Secure Information Systems

<style>
    table {
        width: 100%;
    }
</style>

| Published 2026-mm-dd  | An Ecosystem for Secure Information Systems - Part 2 Political means |
| :---                  |                                                                 ---: |
|                       |                                                   Updated 2026-mm-dd |

[Previous: An Ecosystem for Secure Information Systems - Part 1](<https://acje.github.io/Ecosystem>)

Part 1 argued that pervasive deployment of inherently insecure systems has created a target‑rich environment prone to self‑organized criticality, where small triggers can cascade into large societal failures. The remedy is ecosystem‑level action: politically mandated, verifiable trust across supply chains, hosting, and operations, reinforced by architectural constraints such as isolation and least‑privilege interfaces.

This part turns that argument into action. Embracing a builder’s mindset, we focus on constructing institutional capacity and concrete mechanisms that make trust durable under stress. The goal is to replace fragile dependencies with redundancy, verifiable assurance, and the ability to build at scale across cooperating nations.

## Breakdown of the three principal political necessities

Reshaping the ecosystem that creates our information systems will most likely require political will to both regulate and fund some of the most fundamental components in our shared ecosystem. Many of these components do not generate

Here we will make a detailed analysis of the context, challenges, solutions and tempting non-solutions for each of the principal necessities.

## 1. Trusted supply chain

With supply chain in this document, the following resources for the creation of information systems are included

* Hardware
* Software
* Services, notably among these;
  * Trust services such as Identity and Access Management (IAM)
    * Notably; Entra ID, Okta, AWS IAM, GCP IAM
  * Code and package repositories
    * Notably; Github, Docker/AWS/GCP/Azure container registries, NPM and other programming language specific repositories
  * Build systems
    * Notably; Github actions

These supply chains are heavily relying on one of two kinds of actors that both present challenges for a non-US headquartered organization or non-US state:

* Supply chains relying on national or multi-national technology companies, often US headquartered.
* Supply chains relying on, often unpaid, individual open source contributors that may be both unidentified and vulnerable to pressure form nation state actors.

### Solutions to the trusted supply chain challenge

* Create multi-national organizations among cooperating nations that create and maintain components and services for the shared ecosystem in the categories mentioned here.
* Alternatively create an ecosystem of multiple redundant national components and services that are interchangeable, but note that this will be extremely costly.

**Non-solutions:** Hope that the inherent leverage over national organizations and individual contributors will not be used against us during conflict.

**WARNING: The article is not finished. From here onwards it is only a skeleton.**

## 2. Trusted hosting

With hosting in this document, the following resources for the creation of information systems are included

* Platforms
  * Notably; AWS, Azure, GCP (all US headquartered)
* Infrastructure
* Housing

Challenges

### Solutions to the trusted hosting challenge

## 3. Trusted operations

With operations in this document, the following resources for the creation of information systems are included

* Personnel
* Infrastructure as a Service (IaaS) and Platform as a Service (PaaS)
* External operations

Challenges

### Solutions to the trusted operations challenge

## Upcoming parts in this series

In the next part I will break down the architectural necessities in more detail.

[TODO Next: An Ecosystem for Secure Information Systems - Part 3 architectural constraints](<https://acje.github.io/Ecosystem/architecture>)

## Other posts in category Systems and security

[A case against the CIA triad](https://anderscj.substack.com/p/a-case-against-the-cia-triad)

[CISQ-Model of security qualities](https://acje.github.io/CISQ-model/post)

[Liberal democracies needs a new compute stack. Part 1 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute)

[Liberal democracies needs a new compute stack. Part 2 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-2fd)

[Liberal democracies needs a new compute stack. Part 3 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-523)

[Liberal democracies needs a new compute stack. Part 4 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-d56)

[Structured service addressing. A new take on load balancing in IPv6](https://github.com/acje/structured-service-addressing)

[Fiber semantics. Event sourcing for complex domains](https://github.com/acje/Fiber-semantics)
