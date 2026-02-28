---
title: "Information sharing is not a solved problem"
aliases:
  - "/information_sharing/"

---

## Information sharing is not a solved problem

**!!! Under construction !!!**

Technical article about a secure, cross-organizational platform for timely information-sharing depicted below.

![Information sharing](information_sharing_clean.png)

## A Common Challenge

When asked, "How can we share this information with X?", technical leads, architects, developers, and administrators invariably ask in return: "What are the requirements?" This follow-up question is rarely answered fully. Stakeholders often have vague or conflicting priorities regarding performance, completeness, correctness, security, maintenance, and budget. The design presented here aims to solve these technical requirements holistically, leaving only the budget to be determined, and reducing costs through economies of scale.

## Requirements

**Defense-in-depth.** Both source and destination systems must be shielded from common internet-based attack vectors. This protection should be achieved by isolating the endpoints from direct public internet access.

**Workload mobility.** Services should remain decoupled from underlying infrastructure dependencies like IP addresses or specific network topologies. This abstraction enables seamless migration of workloads across environments whether on-premises, cloud, or hybrid, without requiring code changes or service disruption.

**Security: Availability.** Availability of the system as a whole must be protected such that inevitable system and network disruptions are isolated and not spreading to other systems. See [security]({{< relref "systems/CISQ-maturity/index.md" >}}) for details.

**Security: Integrity.** Ensure correctness and completeness of data product.

**Security: Authenticity.** Strong authentication of every producer (source) and consumer (destination).

**Security: Control.** A central motivation for this system is to enhance national digital sovereignty. Therefore it must be deployable and operated under national control.

**Timely delivery.** Applications often require up-to-date information. Daily batch transfers may introduce unacceptable latency.

**Bandwidth Efficiency.** Transferring full datasets repeatedly (e.g., nightly dumps) is computationally expensive and bandwidth-intensive ($O(n)$ where $n$ is dataset size). An efficient system should transmit only state changes (deltas), reducing complexity to $O(\Delta)$ proportional to the rate of change.

**Data Discovery and Schema Validation.** Data is useless if it cannot be found or understood. The platform must provide a catalog for discovery and enforce schema validation to ensure semantic interoperability between decoupled systems.

**Completeness and correctness.** Ensuring data consistency between source and destination is a fundamental challenge in distributed systems. As established by the CAP theorem (Brewer), it is impossible for a distributed data store to simultaneously provide more than two out of the following three guarantees: Consistency, Availability, and Partition Tolerance. Given the physical inevitability of network partitions and latency (bounded by the speed of light), a system prioritizing high availability cannot guarantee strong consistency (linearizability) at all times.

Therefore, we design for _eventual consistency_, a model where the system guarantees that if no new updates are made to a given data item, eventually all accesses to that item will return the last updated value. This approach decouples the source from the destination's availability, ensuring system resilience.

To achieve this state convergence reliably, we implement _effectively-once processing_ (often referred to as _exactly-once semantics_ or EOS in stream processing) by combining two mechanisms:

1. **At-least-once delivery:** The transport layer guarantees that every message is delivered to the destination one or more times. This handles network failures where acknowledgments may be lost, necessitating retransmission.
2. **Idempotence:** The consumer application is designed to handle duplicate messages safely. Using mechanisms such as unique identifiers or deterministic state transitions, processing the same message multiple times yields the same side effects as processing it once.

This ensures the destination dataset correctly mirrors the source without duplication or data loss. In _Designing Data-Intensive Applications_, Martin Kleppmann refers to this pattern as _leader-based replication_, where the source system acts as the leader responsible for writing and broadcasting state changes to follower systems.

![Information sharing between organizations](information_sharing.png)

## Characteristics of the design

To satisfy the stringent requirements outlined above, the system architecture is built upon **NATS**, a high-performance cloud-native messaging system. The implementation leverages specific NATS features to map directly to our reliability and security needs.

**Secure: Availability.** To optimize availability we utilize NATS JetStream to provide the _at-least-once delivery_ guarantee and source independent availability of external data products. JetStream persists messages to disk, acting as an immutable log of state changes. This ensures that even if a consumer is offline for an extended period, it can replay the missed message stream upon reconnection, recovering the full dataset state without data loss. Further the central architectural trait underpinning a system of dataset replication is loose coupling, which reduces the shared faith problem of tightly coupled systems.

**Secure: Authenticity.** We enforce the Authenticity requirement using NATS  Multi-Tenancy with decentralized authentication (Nkeys) and granular authorization. Account isolation ensures that organizations can share the same infrastructure without accessing each other's data streams, preserving the principle of least privilege.

**Defense-in-Depth (Leaf Nodes).** To meet the requirement for isolating endpoints, we employ NATS Leaf Nodes. A Leaf Node runs locally within a secure enclave and initiates an _outbound_ connection to the central NATS cluster. This architecture requires no inbound firewall ports to be opened on the secure network, significantly reducing the attack surface while safely extending the messaging plane into restricted environments.

**Location Transparency (Subject-Based Addressing).** NATS decouples publishers from consumers using subject-based addressing (e.g., `agency.system.update`). Applications do not need to know the IP address or network location of their peers. This abstraction fulfills the _workload mobility_ requirement, allowing services to migrate between on-premises and cloud infrastructure without configuration changes or service discovery headaches.

**Efficiency (Push/Pull Consumers).** To optimize _bandwidth efficiency_ and _timely delivery_, JetStream supports both push and pull consumption models. Real-time updates are pushed to active consumers immediately, minimizing latency. Conversely, batch processes or bandwidth-constrained consumers can pull messages at their own pace, preventing flow-control issues and optimizing resource usage.

## Necessities for a national robust information sharing infrastructure

To escape the cycle of recurring systemic failures and strategic dependency, we must rethink our infrastructure through the lens of high-reliability theory. As Ken Thompson demonstrated in _Reflections on Trusting Trust_ (1984), a system's security is illusory if the tools used to build it are compromised; therefore, verified provenance in our software supply chain is a prerequisite for trust, protecting against the kind of hidden fragility Nassim Taleb warns can lead to catastrophic collapse. This technical autonomy is inseparable from political agency. Shoshana Zuboff’s analysis in _The Age of Surveillance Capitalism_ suggests that ceding infrastructure to hyperscale monopolies is not merely an outsourcing decision but a surrender of governance, necessitating a shift back to hosting environments where the organization retains full jurisdictional control.

Conceptually, we must accept Charles Perrow's thesis in _Normal Accidents_ that failure in tightly coupled systems is inevitable. Rather than striving for impossible perfection, we should emulate High Reliability Organizations (HROs) by designing for resilience and rigorous operational vetting. This requires a departure from monolithic architectures toward the "share nothing" principles of Carl Hewitt’s Actor Model (1973). By isolating components in a manner that prevents the "accidental complexity" of shared state described by Fred Brooks, and strictly enforcing Saltzer and Schroeder’s principle of _Least Privilege_ (1975) through capability-based interfaces, we can construct systems where individual faults are contained, preventing minor errors from cascading into national crises.

## More to Read

- [Digital Sovereignty]({{< relref "systems/digital_sovereignty/index.md" >}})
- [Fiber semantics. Event sourcing for complex domains (Repository)](https://github.com/acje/Fiber-semantics)
