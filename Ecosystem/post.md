# An Ecosystem for Secure Information Systems

**WARNING: This is a work in progress.**

Employing Political Instruments and Architectural Constraints for the Ecosystem that builds our Critical National Infrastructure and Services.

## Summary

Critical infrastructure and services increasingly depend on information systems whose common vulnerable dependencies and inherent brittle design can create systemic vulnerabilities prone to cascading failures. The goal here is to describe an ecosystem that reduce systemic vulnerabilities to an acceptable level for all infrastructure and services. It will be  asserted that there are five principal necessities. By targeting the ecosystem rather than the information systems directly we create a situation where systems across all sectors of society benefits. This is done through politically mandated verifiable and trusted supply chains, hosting and operations. Further this must be combined with  architecture principles that limit blast radius and enforce least privilege integrations at all levels.

## The fundamental challenge of increasing the number of inherently insecure and critical systems

Times are changing with new rules that appear undefined at the moment. The systems and attitudes that got us here are unlikely to be the ones that will get us through it. For the purpose of this post I will defer the naming of the coming period to the historians. The adversary and its capabilities is not the big problem. The adversary is inevitable. The big problem is our own creation of a target rich environment of critically important systems with common vulnerabilities. There will be an adversary with the means and motivation to use the vulnerabilities against us. The additional risk posed by a nation state adversary is not its ability to exploit but its ability to coordinate  with other events. The list of attacks exploiting systemic weaknesses are many;  Stuxnet, SolarWinds, NotPetya, WannaCry, HeartBleed, Colonial Pipeline operations, Ukraine grid attacks and Salt Typhoon telecom attacks, to name a few famous examples.

## Self-organized criticality

Forest fires, avalanches and digital transformation may have one dangerous thing in common: Self-organizing to criticality. The spark that starts a large forest fire is not meaningfully different than the spark that does not. The snowflake that starts a large avalanche is not meaningfully different from those that do not. The meaningful difference is in the combined potential in the environment not the trigger event. The damage potential has built up over time from dead organic debris or snowflakes landing on top of each other. The trigger is just a statistically inevitable event, releasing the potential. This was described mathematically as “Self-organized criticality” by mathematicians Per Bak, Chao Tang and Kurt Wiesenfeld in 1987.

What I propose here is that forcefully engaging in digital transformation is highly likely to create a similar situation to forest fires and avalanches. This happens as we deploy an ever increasing number of inherently insecure systems across all critical sectors in our societies. Thereby creating a situation where a single event of shared vulnerability may trigger a ripple effect through our society, tearing down critical infrastructure and services like energy, communication, transportation, healthcare, and water supply.

To counter this scenario I propose a strategic application of political and architectural constraints on the ecosystem that produces these systems. The following outlines the three political and two architectural pillars of an ecosystem for creation of meaningfully more secure information systems. These systems will not have absolutely zero risk, but they should reduce the risk to such a level that the risk is acceptable for use across all critical infrastructure and services.

## Critical and non-critical information systems are largely built the same

Critical information system typically has more rigorous design, more controls are implemented and documented and more layers of isolation are typically implemented. Yet they tend to be built using the same services and components as non-critical systems. Because the functional needs are the same and there is rarely any gain in using lower grade software components or services in non-critical systems. The hardware may vary somewhat more in quantity and sometimes also in quality.

## A hierarchy of security aspects

Where we intervene is of importance for how far we can reach. A simplified model for how to understand how information systems are created, managed and cause security outcomes may be helpful. The ecosystem consists of all the available services, components and trained personnel that goes into creating information systems. The systems themselves are created from what is available at their time of creation and during their period of maintenance. These systems cause security events such as unexpected downtime due to internal, natural or adversarial actions on the system. Dependent on the systems ability to withstand these actions and the organizations ability to react, we get security outcomes. In this post we will look at actions we can take at the ecosystem level to create a situation where all new and actively maintained systems can be made to produce meaningfully better security outcomes. When we intervene at this level we are more likely to maximize impact compared to intervening at lower levels of this model.

Ecosystem -> information systems -> security events -> security outcomes

In this post we are going to look into how we can understand and modify the ecosystem that functions as the basis for how information systems are created. Three political and two architectural necessities have been identified in an ecosystem that will produce meaningfully more secure information systems, suitable for the pervasive digitalization that finds its way into most sectors of critical infrastructure and services.

## Necessities of an ecosystem that produce inherently secure systems

These are the necessities that have been identified for an ecosystem to produce meaningfully more secure information systems. To highlight structure for the different audiences the necessities has been categorized into two different areas. The political necessities are about aspects of the ecosystem that typically will need multi-national political effort to achieve. The architectural necessities may also need political help to advance at reasonable pace, but caution need to be used when mandating use because technological breakthroughs may change how architecture should be shaped.

The asserted principal necessities for an ecosystem that will create meaningfully more secure information systems are as follows.

### Principal political necessities

* Trusted supply chain
* Trusted hosting
* Trusted operations

### Principal architectural necessities

* Maximally isolated components of least capability
* Least privilege interfaces

## 1. Trusted supply chain

With supply chain in this document, the following resources for the creation of information systems are included

* Hardware
* Software
* Services, among these;
  * Trust services such as Identity and Access Management (IAM)
    * Notably; Entra ID, Okta, AWS IAM, GCP IAM
  * Code and package repositories
    * Notably; Github, Docker/AWS/GCP/Azure container registries, NPM and other programming language specific repositories

These supply chains are heavily relying on one of two kinds of deliveries that both present challenges for a non-US headquartered organization or non-US state:

* Supply chains relying on national or multi-national technology companies, often US headquartered.
* Supply chains relying on, often unpaid, individual open source contributors that may be both unidentified and vulnerable to pressure form nation state actors.

### Solutions to the trusted supply chain challenge

* Create multi-national organizations among cooperating nations that provide components and services for the shared ecosystem in the categories mentioned here.
* Alternatively create an ecosystem of multiple redundant national components and services that are interchangeable

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
* IaaS
* External operations

Challenges

### Solutions to the trusted operations challenge

## 4. Maximally isolated components of least capability

With components in this document, the following resources for the creation of information systems are included

Challenges

### Solutions to the components challenge

* Web assembly component - fast & sandboxed

Non-solutions

* Third party code - technically ok, but impractical to control
* Library - not sandboxed
* Script language (Lua, embedded JS engine) - inefficient

## 5. Least privilege interfaces

With interfaces in this document, the following resources for the creation of information systems are included

Challenges

### Solutions to the interface challenge

Clearly define interfaces derived from function signatures of exposed functions.

## Final thoughts

Doable
