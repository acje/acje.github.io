# A structured view on information security

## The CISQ-model hypothesis

### What is the CISQ-model?

The CISQ-model (Composing Information Security Qualities) builds on the hypothesis that there are exactly four basic security qualities. Integrity, Authenticity, Availability and Control. A total of 16 qualities can be composed from these four basic qualities, if we include the “none” quality and the four basic qualities them selves. The most useful subset of the model when dealing with a service is shown below.

![CISQ-model-simplified](CISQ-model-simplified.png)

### Why do we need more information security acronyms?

*"Rather than trying to change the world, change how people see the world. Because when they see the world differently, they behave differently and that will change the world" - Rory Sutherland*

The goal is to create a vocabulary for information security that covers the field of component security qualities as much as possible while minimising overlap and ambiguity. Non-goals include legal, ethical and societal issues as well as describing system level properties such as defence in depth, resilience and isolation.

### Foundations

For information objects the four basic qualities are as follows;

1. If the object is intact it is considered to have the **integrity** quality
2. If the object has a known origin it is considered to have the **authenticity** quality
3. If the object can be reached in a timely manner it is considered to have the **availability** quality
4. If the object is exclusively controlled by an enumerated set of entities it is considered to have the **control** quality

For behaviour in an information system, such as a service, we have the same four qualities;

1. If the behaviour is intact it is considered to have the **integrity** quality
2. If the behaviour has a known origin it is considered to have the **authenticity** quality
3. If the behaviour can be reached in a timely manner it is considered to have the **availability** quality
4. If the behaviour is exclusively controlled by an enumerated set of entities it is considered to have the **control** quality

### Notable remarks

- Integrity and authenticity are both considered as discrete and absolute, whereas availability and control are continuous and open-ended. This has important consequences for how we can reason about information security. For instance the control quality will always be subject to “force majure”, no mater how well the system is designed and the availability quality can span towards infinite time, hence making absolute guarantees difficult to define. (Check for correctness: For instance an electronic arbiter does not have an upper bound on the time it needs to decide which signal arrived first, but the probability that it hasn’t decided yet is asymptotical to zero.)
- The CISQ-model deliberately use the wording “basic” security quality, as opposed to “atomic” or “axiomatic” because these qualities may very well be broken down even further, just like the atom. This can be trivially shown for availability with the concepts of time, completeness and (network) partitioning in distributed systems all contributing their own aspects of availability. In other words the CISQ-model is more like the composed building blocks of the periodic table and less like the standard model of physics.

### The model in depth

The CISQ-model uses composition to expand the four basic security qualities (Integrity, Authenticity, Availability, Control) into a total of 16 qualities as shown in the table below.

![CISQ-table](CISQ-table.png)

Visualizing the composition of four aspects is not easy to get right. This view shows how we can simplify the model by splitting the model into to separate views. One model for systems that are controlled, typically by an organization and the other for public domain objects such as certificates.

![CISQ-Model](CISQ-3-model-views.png)

### Vocabulary of the CISQ-Model

These definitions are a work in progress. two principles are important:
- Keep the definitions as short as possible, which is easier since the overloading of terms are much less than in the CIA-triad.
- Symetry between information and behavior across all terms

**Reliability** – Trustworthy information and behaviour

**Sustainability** - Ability to maintain information and behaviour

**Confidentiality** - Access to information and behaviour being exclusively limited to authorized entities

**Authority** - Power to grant access to information and behaviour

**Accountability** - Assurance of the correctness, completeness and origin of information and behaviour

**Durability** - Ability to withstand damage of integrity of information and behaviour

**Credibility** - Verified information and behaviour

**Control** - Power to physically or logically influence information and behaviour

**Certifiability** - Ability to prove validity of information and behaviour

**Utility** - Usefulness of information and behaviour

**Veracity** - Accuracy of information and behaviour

**Availability** - Timely access to information and behaviour

**Traceability** - Ability to discover where and how information and behaviour was made

**Integrity** - Preserving correctness and completeness of information and behaviour

**Authenticity** - Origin of information and behaviour is from its purported source

**Unreliability** - Not capable of providing security qualities
