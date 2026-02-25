---
title: "Scaling Agile"
aliases:
  - "/scaled_agile/"
---

## Scaling Agile

These are my notes on how an organization transformed from facing challenges with concurrent digitalization projects and inconsistent value delivery, into a fast-moving agile organization. I have observed this type of transition twice in the role of architect in two different organizations, both with tens of projects and later, tens of teams running in parallel. The first transition was targeting the SAFe-Framework. The second transition was a much more deliberate and tailored approach. The deliberate and tailored transition will be the main topic of these notes, but I might reference the first transition explicitly where appropriate.

## Summary

Obtaining significant improvements in speed, domain knowledge and short-term value creation is very achievable. Following the practices from "Accelerate" and implementing stream aligned teams and platform teams from "Team topologies" are well established techniques by now. Then make sure your teams have a clear "mission" limited to a reasonably sized business domain, while protecting them from organizational pressures to prioritize immediate requests over strategic goals.

The lessons discussed here are more subtle and deal with aspects that arise from the success of scaling agile organizations.

* First lesson - Speed can temporarily mask a lack of direction, but speed alone doesn´t scale well.
* Second lesson - Managing second-order effects of success. New assets introduce risks and opportunities that may be latent or overlooked in the implementation structure.
* Third lesson/hypothesis - Within the concept of "mission command" use the backbrief to empower the relation between stakeholders and product teams.

## __Work in progress__

For the rest of this post I will proceed to explain:

## Setting the context

* Steps taken to establish a productive digitalization organization.
  * Initial Transition breakdown; transition from projects to teams secures continuity in knowledge about the business domain and the produced asset, often referred to as the product.
    * Splitting stream aligned teams and platform teams to leverage scale.
      * Initial implementation faced challenges because the applications were too tightly coupled to the platform and this also caused the platform not to evolve into a capability with sufficiently self-service. The result was that we largely ended up with a 1:1 of platform and application effort. A redesign of the underlying application architecture and platform was needed.
      * The second attempt yielded a almost fully self service platform and we even put some effort into not depending too deeply on custom cloud features. Architecture is not the scope here, but we largely created separate sandboxes for each system, relying heavily on self-hosted NATS on cloud VMs to create a communication mesh that also can persist streams of data. Other cloud services are freely chosen by the teams but they are incentivized to use containers and postgres-as-a-service. Run your own VM if you need something bespoke. The result is more like a 1:10 effort in platform and application, allowing us to scale up stream aligned teams while spending much less on creating and maintaining a platform.
* Leadership and scale; We eventually got to working at the transition from both bottom and top, transforming the IT department first and the rest of the 1300 person organization is about to follow.There was however significant upfront effort over multiple years to create continuous deployment, container based runtimes, git as a service, team vs project awareness and so forth. When the two first teams were established a lot of the uncertainty was eliminated. Confidence in our capabilities grew. Concurrently, a significant shift in mindset occurred in large parts of management around this time. Teams were to become the new normal. Projects had often shown limitations in timely delivery, creating a subsequent need for remediation efforts.

## Observations

* First lesson - Speed can temporarily mask a lack of direction, but it doesn´t scale well alone.
  * Discovery through serendipity; e.g., allocating capacity for exploration outside the plan.
  * Some alignment scales speed. Extremes of alignment—either total absence or rigid enforcement—create traps of local optimization.
* Second lesson - Managing second-order effects of success. New assets introduce risks and opportunities that may be latent or overlooked in the implementation structure.
  * Kent Beck — behavior and structure
    ![Behavior and structure](/agency/scaled_agile/behavior_structure.png)

    * Risks as second order effects of successfully creating new assets
    ![Production vs protection](/agency/scaled_agile/protection_production.png)

    * Managing Opportunities with Architecture
    * Architecture is one of those things that has a tendency to get overlooked/discarded when organizations move to agile methodologies.

## Improvements

* Places to innovate
  * The Art of Action — directed opportunism
    * Operational gaps
        ![Decision making at scale](/agency/scaled_agile/three_gaps.png)
        [Three Critical Gaps](https://medium.com/10x-curiosity/taking-the-project-management-theme-one-step-further-and-examining-why-the-agile-styles-of-project-5ec97cb2eb37)

    * Hierarchy of cascading intent
    * Institute backbrief
* Alignment and autonomy

  ![Decision making at scale](/agency/scaled_agile/Decision_making_at_scale.png)
  
    See [Alignment and autonomy](https://github.com/acje/Alignment_autonomy) for more details (self-reference)

* Managing costs of transition
  * Organizational costs
  * Personal costs
