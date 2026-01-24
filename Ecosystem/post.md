# An Ecosystem for Secure Information Systems

Employing political instruments and architectural constraints to reshape the ecosystem that builds our digital infrastructure and services.

<style>
    table {
        width: 100%;
    }
</style>

| Published 2026-01-22  | An Ecosystem for Secure Information Systems - Part 1 Introduction |
| :---                  |                                                              ---: |
|                       |                                                Updated 2026-01-24 |

## Summary

Infrastructure and services across all levels of criticality increasingly depend on information systems whose common vulnerable dependencies and inherent brittle design can create systemic vulnerabilities prone to cascading failures. The goal here is to describe an ecosystem that reduces systemic vulnerabilities to an acceptable level for all infrastructure and services. It will be asserted that such an ecosystem consists of five principal necessities. By targeting the ecosystem rather than the information systems directly we create a situation where systems across all sectors of society benefit. This must be done through politically mandated verifiable and trusted supply chains, hosting and operations. Further this must be combined with  architecture principles that limit blast radius and enforce least privilege integrations at all levels.

## The fundamental challenge of increasing the number of inherently insecure and critical systems

Times are changing with new geopolitical rules that appear undefined at the moment. The systems and attitudes that got us here are unlikely to be the ones that will get us through it. For the purpose of this post I will defer the naming of the coming period to the historians. When considering this looming challenge it is important to realize that the adversaries and their capabilities are not the significant source of the problem. The adversary is inevitable. The big problem is our own creation of a target rich environment of critically important systems with common vulnerabilities. There will eventually be an adversary with the means and motivation to use the vulnerabilities against us. The additional risk posed by a nation state adversary is not its ability to penetrate and exploit information systems, but its ability to coordinate  with other events. The list of historic attacks exploiting systemic weaknesses are many;  Stuxnet, NotPetya, WannaCry, HeartBleed, SolarWinds, Colonial Pipeline operations, Ukraine grid attacks and Salt Typhoon telecom attacks, to name a few famous examples. These kind of attacks will occur with uneven intervals, and the size of these attacks will grow proportionally to the number of available targets, because the size is largely a function of the environment, and less related to the attackers capabilities.

### Self-organized criticality

Forest fires, avalanches and digital transformation may have one dangerous thing in common: Self-organizing to criticality. The spark that starts a large forest fire is not meaningfully different from the spark that does not. The snowflake that starts a large avalanche is not meaningfully different from those that do not. The meaningful difference is in the combined potential in the environment, not the trigger event. The damage potential has built up over time from dead organic debris or snowflakes landing on top of each other. The trigger is just a statistically inevitable event, releasing the potential. This was described mathematically as “Self-organized criticality” by mathematicians Per Bak, Chao Tang and Kurt Wiesenfeld in 1987.

What I propose here is that forcefully engaging in digital transformation is highly likely to create a similar situation to forest fires and avalanches. This happens as we deploy an ever increasing number of inherently insecure systems across all critical sectors in our societies. Thereby creating a situation where a single mode of attack or shared vulnerability may trigger a ripple effect through our society. This could end up tearing down critical infrastructure and services like energy, communication, healthcare, finance, transportation, and water supply.

To counter this scenario I propose a strategic application of political instruments and architectural constraints on the ecosystem that produces these systems. The following outlines the three political and two architectural pillars of an ecosystem for creation of meaningfully more secure information systems. These systems will not have absolutely zero risk, but they should reduce the risk to such a level that the risk is acceptable for use across all critical infrastructure and services.

### Critical and non-critical information systems are largely built the same

Critical information system typically has more rigorous design, more controls are implemented and documented and more layers of isolation are typically implemented. Yet they tend to be built using the same services and components as non-critical systems. When the functional needs are the same, there is rarely any gain in using lower grade software components or services in non-critical systems. The hardware may vary somewhat more in quantity and sometimes also in quality, but most systems attributes are software defined these days.

## A hierarchy of security aspects

Where we intervene is of importance for how far we can reach. A simplified model of how to understand how information systems are created, managed and cause security outcomes, may be helpful. The ecosystem consists of all the available services, components and trained personnel that goes into creating information systems. The systems themselves are created from what is available at their time of creation and during their period of maintenance. These systems cause security events such as unexpected downtime due to internal, natural or adversarial actions on the system. Dependent on the systems ability to withstand these actions and the organizations ability to react, we get security outcomes. In this post we will look at actions we can take at the ecosystem level to create a situation where all new and actively maintained systems can be made to produce meaningfully better security outcomes. When we intervene at this level we are more likely to maximize impact compared to intervening at lower levels of this model.

Ecosystem -> information systems -> security events -> security outcomes

In this post we are going to look into how we can understand and modify the ecosystem that functions as the basis for how information systems are created. Three political and two architectural necessities have been identified in an ecosystem that will produce meaningfully more secure information systems, suitable for the pervasive digitalization that finds its way into most sectors of critical infrastructure and services.

## Necessities of an ecosystem that produce inherently secure systems

Here we present the necessities that have been identified for an ecosystem to produce meaningfully more secure information systems. To highlight structure for the different audiences the necessities has been categorized into two different areas. The political necessities are about aspects of the ecosystem that typically will need multi-national political effort to achieve. The architectural necessities may also need political help to advance at reasonable pace, but caution need to be used when mandating their use because technological breakthroughs may change how architecture should be shaped.

The asserted principal necessities for an ecosystem that will create meaningfully more secure information systems are as follows.

### Principal political necessities

* Trusted supply chain
* Trusted hosting
* Trusted operations

### Principal architectural necessities

* Maximally isolated components of least capability
* Least privilege interfaces

## Upcoming parts in this series

In the next two parts I will break down the political and architectural necessities in more detail.

[TODO Next: An Ecosystem for Secure Information Systems - Part 2 Political means](<https://acje.github.io/Ecosystem/political>)

## Other posts in category Systems and security

[A case against the CIA triad](https://anderscj.substack.com/p/a-case-against-the-cia-triad)

[CISQ-Model of security qualities](https://acje.github.io/CISQ-model/post)

[Liberal democracies needs a new compute stack. Part 1 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute)

[Liberal democracies needs a new compute stack. Part 2 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-2fd)

[Liberal democracies needs a new compute stack. Part 3 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-523)

[Liberal democracies needs a new compute stack. Part 4 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-d56)

[Structured service addressing. A new take on load balancing in IPv6](https://github.com/acje/structured-service-addressing)

[Fiber semantics. Event sourcing for complex domains](https://github.com/acje/Fiber-semantics)
