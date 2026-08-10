---
title: "A simple model for computing capabilities"
aliases:
  - "/computing_capabilities/"
date: 2026-08-10
lastmod: 2026-08-10
weight: 70
---
## A basic model of what a computing node can do

## The computing capabilities hypothesis

### What is the computing capabilities model?

I hold that there are exactly four basic capabilities of a computing node: **Processing, Persisting, Communicating and Transducing**. Processing transforms information. Persisting stores information over time. Communicating moves information across space. Transducing crosses the boundary between the digital and the physical world - sensors carry information from physical to cyber, actuators carry it from cyber to physical. Every computing node, from a microcontroller to a hyperscale data center, is doing some combination of these four things and nothing else.

### Why do we need another framing of what a computer does?

Most descriptions of a computing node reach for a components list - CPU, memory, disk, network card, sensor - or for an architecture diagram of boxes and arrows. These are useful for building the thing, but they are not useful for reasoning about what the thing does, because the same capability can be delivered by wildly different components depending on cost, scale and physical constraints. I want a vocabulary that is stable across implementations: a capability, not a part.

The goal is a small, complete vocabulary of what a computing node offers and what a workload demands of it, so I can reason about capacity, bottlenecks and attack surface without getting lost in a specific hardware or software stack. Non-goals include describing the internal implementation of any of the four capabilities, and describing system-level properties like reliability or scalability that emerge from how capabilities are composed and deployed.

### Foundations

For a computing node, the capabilities it can offer are as follows;

1. If the node can transform information it offers the **processing** capability
2. If the node can store information over time it offers the **persisting** capability
3. If the node can move information across space it offers the **communicating** capability
4. If the node can cross the boundary between the digital and the physical world it offers the **transducing** capability

For a workload running on a computing node, the same four capabilities are what it demands;

1. If the workload needs information transformed it demands the **processing** capability
2. If the workload needs information stored over time it demands the **persisting** capability
3. If the workload needs information moved across space it demands the **communicating** capability
4. If the workload needs to cross the boundary between the digital and physical world it demands the **transducing** capability

### Notable remarks

- A single physical component frequently offers more than one capability at once - a disk with an on-board cache is persisting and, briefly, processing; a smart sensor with a signal-conditioning chip is transducing and processing. The model classifies the capability, not the part.
- I deliberately use the wording "basic" capability, as opposed to "atomic" or "axiomatic", because each of the four can be broken down further. Persisting alone splits into durability, latency tiers and consistency guarantees; transducing alone splits into sampling rate, precision and the physical quantity being converted. The model is a starting vocabulary, not a claim of irreducibility.
- Transducing is directional and the direction matters. A sensor moves information physical to cyber. An actuator moves information cyber to physical. Collapsing both into a generic "I/O" capability is exactly the simplification this model avoids.

### The model in depth

I did not arrive at this model in a vacuum, and it is reassuring rather than surprising that the same four-way split shows up, independently phrased, in standards work aimed at rather different problems.

[NIST SP 1900-202](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1900-202.pdf), the unified framework for [Cyber-Physical Systems and the Internet of Things](https://www.nist.gov/publications/cyber-physical-systems-and-internet-of-things), separates a system into a Unified Components Model of four domains: Logical, Physical, Human and Transducing. NIST uses "transducing" for the same reason I do - it is the explicit, dedicated layer bridging the logical and physical domains, converting continuous physical signals into discrete digital logic and back.

The [Industrial Internet Reference Architecture](https://www.iiconsortium.org/wp-content/uploads/sites/2/2022/11/IIRA-v1.10.pdf) from the Industrial Internet Consortium draws a similar line to distinguish edge computing from legacy IT: an industrial computing node has data capabilities - storing, transferring and processing - and transducing capabilities, the functions that let it interact directly with physical entities of interest. The IIRA split maps exactly onto mine: data capabilities is persisting plus communicating plus processing, and transducing capabilities is transducing. Of the two, this is the closer match, since it groups three of my four capabilities under one label the same way I would.

| My model | NIST SP 1900-202 | IIRA |
|---|---|---|
| Processing | Logical (part) | Data capabilities (part) |
| Persisting | Logical (part) | Data capabilities (part) |
| Communicating | Logical (part), Physical (part) | Data capabilities (part) |
| Transducing | Transducing | Transducing capabilities |
| (not modeled - the operator) | Human | (not modeled) |

Neither standard treats "Human" as a computing capability, and neither should - a human operator is not a capability the node offers, it is a party the node's other capabilities serve or are directed by. I leave it out of the four for the same reason.

### Vocabulary

Two principles as before: keep the definitions as short as possible, and hold symmetry between what a node offers and what a workload demands.

**Processing** - Transforming information

**Persisting** - Storing information over time

**Communicating** - Moving information across space

**Transducing** - Crossing the boundary between the digital and the physical world

**Sensor** - A transducing function converting information from physical to cyber

**Actuator** - A transducing function converting information from cyber to physical

**Logical** - The cyber, computing part of a system - NIST's term for where processing and persisting happen

**Physical** - The tangible, non-computing environment or infrastructure a system operates in or on

**Human** - The users or operators interacting with a system, not itself a computing capability

### Why this terminology matters

Two arguments for "transducing" over the more casual "I/O".

First, bidirectional boundary crossing. "Transducing" unites sensors and actuators under a single functional concept - moving information across the physical-digital boundary in either direction - rather than treating input and output as unrelated device categories. That unification is what lets the same reasoning apply to a temperature sensor and a servo motor.

Second, explicit vulnerability mapping. Cybersecurity frameworks such as Japan's [METI Cyber/Physical Security Framework](https://www.meti.go.jp/policy/netsecurity/wg1/CPSF_ver1.0_eng.pdf) treat the transduction layer as its own attack surface, distinct from the logical and physical layers either side of it. This is where a digital system gets fooled by physical manipulation rather than by conventional software exploitation - blinding a camera with a laser, tricking an acoustic sensor with inaudible ultrasound, spoofing GPS. Naming transducing as a capability in its own right, rather than folding it into "physical security" or "input validation", keeps this attack surface visible instead of letting it fall between two more familiar categories.

### References

- [NIST SP 1900-202 - Cyber-Physical Systems and Internet of Things](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1900-202.pdf)
- [NIST - Cyber-Physical Systems and Internet of Things](https://www.nist.gov/publications/cyber-physical-systems-and-internet-of-things)
- [Industrial Internet Reference Architecture v1.10 - Industrial Internet Consortium](https://www.iiconsortium.org/wp-content/uploads/sites/2/2022/11/IIRA-v1.10.pdf)
- [METI Cyber/Physical Security Framework](https://www.meti.go.jp/policy/netsecurity/wg1/CPSF_ver1.0_eng.pdf)
- [arxiv.org/pdf/2508.16133](https://arxiv.org/pdf/2508.16133)
- [Of Brains and Computers - Emerald](https://www.emerald.com/ftics/article/2/1-2/1/1326506/Of-Brains-and-Computers)

## More to Read

{{% home-section-links section="systems" %}}
