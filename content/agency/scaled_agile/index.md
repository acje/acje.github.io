---
title: "Scaling Agile"
aliases:
  - "/scaled_agile/"
homeFeatured: true
homePrefix: "Under construction"
weight: 10
---

## Scaling Agile

**!!! Under construction !!!**

These notes document how an organization transformed from facing challenges with concurrent digitalization projects and inconsistent value delivery into a fast-moving agile organization. I have observed this type of transition twice as an architect in two different organizations, both with dozens of projects and, later, dozens of teams running in parallel. The first transition targeted the Scaled Agile Framework (SAFe). The second transition took a much more deliberate and tailored approach. This bespoke transition is the primary focus of these notes, though I reference the first transition where appropriate.

## Summary

Obtaining significant improvements in speed, domain knowledge, and short-term value creation is feasible. Following practices from *Accelerate* and implementing stream-aligned teams and platform teams from *Team Topologies* are now well-established techniques [1,2]. Ensure your teams have a clear "mission" limited to a reasonably sized business domain, while protecting them from organizational pressures to prioritize immediate requests over strategic goals [5].

The lessons discussed here are more subtle and deal with aspects that arise from the success of scaling agile organizations.

* **First lesson** - Speed can temporarily mask a lack of direction, but speed alone does not scale well.
* **Second lesson** - Managing second-order effects of success. New assets introduce risks and opportunities that may be latent or overlooked in the implementation structure.
* **Third lesson/hypothesis** - Within the concept of "mission command," use the backbrief to empower the relationship between stakeholders and product teams [4,5].

## Setting the Context

This section covers:

* **Steps taken to establish a productive digitalization organization.**
  * *Initial Transition:* Moving from projects to teams secures continuity in knowledge about the business domain and the produced asset (often referred to as the product).
    * *Splitting stream-aligned teams and platform teams to leverage scale [2].*
      * The initial implementation faced challenges because applications were too tightly coupled to the platform. This prevented the platform from evolving into a capability with sufficient self-service. Consequently, the effort ratio between platform and application work was nearly 1:1. A redesign of the underlying application architecture and platform was required.
      * The second attempt yielded a nearly fully self-service platform, with efforts made to minimize deep dependencies on custom cloud features. While architecture is outside this scope, we established separate sandboxes for each system, relying heavily on self-hosted NATS on cloud VMs to create a communication mesh that also persists data streams. Teams freely choose other cloud services but are incentivized to use containers and Postgres-as-a-Service. Teams requiring bespoke solutions must manage their own VMs. The result is a 1:10 effort ratio between platform and application, allowing us to scale up stream-aligned teams while significantly reducing platform maintenance costs.
* **Leadership and Scale.**
  * We eventually approached the transition from both the bottom up and top down. The IT department transformed first, with the remaining 1,300-person organization following suit. However, significant upfront effort was required over multiple years to create continuous deployment, container-based runtimes, Git-as-a-Service, team vs. project awareness, and more. When the first two teams were established, much sudden uncertainty was eliminated, and confidence in our capabilities grew. Concurrently, a significant shift in mindset occurred in large parts of management. Teams were to become the new normal. Projects had often shown limitations in timely delivery, creating a subsequent need for remediation efforts.

## Observations

* **First lesson** – Speed can temporarily mask a lack of direction, but it does not scale well alone.
  * *Discovery through serendipity:* e.g., allocating capacity for exploration outside the plan.
  * *Alignment scales speed.* Extremes of alignment—either total absence or rigid enforcement—create traps of local optimization [4].
* **Second lesson** – Managing second-order effects of success. New assets introduce risks and opportunities that may be latent or overlooked in the implementation structure.
  * Kent Beck: Behavior and Structure [6]
    ![Behavior and structure](/agency/scaled_agile/behavior_structure.png)

    * *Risks as second-order effects of successfully creating new assets.*
    ![Production vs protection](/agency/scaled_agile/protection_production.png)

    * **Managing Opportunities with Architecture**
      * Architecture is often overlooked or discarded when organizations move to agile methodologies [3].
* **Third lesson/hypothesis** – todo

## Improvements

* **Places to Innovate.**
  * *The Art of Action – Directed Opportunism [4]*
    * *Operational Gaps*
        ![Decision making at scale](/agency/scaled_agile/three_gaps.png)
        [Three Critical Gaps](https://medium.com/10x-curiosity/taking-the-project-management-theme-one-step-further-and-examining-why-the-agile-styles-of-project-5ec97cb2eb37)

    * *Hierarchy of Cascading Intent* (<https://planadigm.com/knowledge/the-art-of-action-part-2/>) [4]
     ![cascading intent](/cascading_intent.png)
    * *Instituting the Backbrief [4,5]*
* **Alignment and Autonomy.**

  ![Decision making at scale](/agency/scaled_agile/Decision_making_at_scale.png)
  
    See [Alignment and autonomy](https://github.com/acje/Alignment_autonomy) for more details (self-reference)

* **Managing Transition Costs.**
  * *Organizational Costs*
  * *Personal Costs*

## References

1. Forsgren N, Humble J, Kim G. Accelerate: the science of lean software and DevOps: building and scaling high performing technology organizations. Portland (OR): IT Revolution Press; 2018.
2. Skelton M, Pais M. Team topologies: organizing business and technology teams for fast flow. Portland (OR): IT Revolution Press; 2019.
3. Conway ME. How do committees invent? Datamation. 1968;14(4):28-31.
4. Bungay S. The art of action: how leaders close the gaps between plans, actions and results. London: Nicholas Brealey Publishing; 2011.
5. Department of the Army. ADP 6-0 mission command: command and control of Army forces. Washington (DC): Headquarters, Department of the Army; 2019.
6. Beck K. Tidy first?: a personal exercise in empirical software design. Sebastopol (CA): O'Reilly Media; 2023.
