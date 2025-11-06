# A structured view on information security
## The CISQ-model hypothesis

### What is the CISQ-model?
The CISQ-model (Composing Information Security Qualities) builds on the hypothesis that there are exactly four basic security qualities. A total of 16 qualities can be composed from these four basic qualities, if we include the “none” quality and the four basic qualities them selves.

### Why do we need more information security acronyms?
The goal is to create a vocabulary for information security that covers the field of component security qualities as much as possible while minimising overlap and ambiguity. Non-goals include legal, ethical and societal issues as well as describing system level properties such as defence in depth, resilience and isolation.

### Foundations
For information objects the four basic qualities are as follows;

1. If the object is intact it is considered to have the integrity quality
2. If the object has a known origin it is considered to have the authenticity quality
3. If the object can be reached in a timely manner it is considered to have the availability quality
4. If the object is exclusively controlled by an enumerated set of entities it is considered to have the control quality

For behaviour in an information system, such as a service, we have the same four qualities;

1. If the behaviour is intact it is considered to have the integrity quality
2. If the behaviour has a known origin it is considered to have the authenticity quality
3. If the behaviour can be reached in a timely manner it is considered to have the availability quality
4. If the behaviour is exclusively controlled by an enumerated set of entities it is considered to have the control quality

### Notable remarks
- It seems that integrity and authenticity are both discrete and absolute, whereas availability and control are continuous and open-ended. This has important consequences for how we can reason about information security. For instance the control quality will always be subject to “force majure”, no mater how well the system is designed and the availability quality can span towards infinite time, hence making absolute guarantees difficult to define. (Check for correctness: For instance an electronic arbiter does not have an upper bound on the time it needs to decide which signal arrived first, but the probability that it hasn’t decided yet is asymptotical to zero.)
- The CISQ-model deliberately use the wording “basic” security quality, as opposed to “atomic” or “axiomatic” because these qualities may very well be broken down even further, just like the atom. This can be trivially shown for availability with the concepts of time, completeness and (network) partitioning in distributed systems all contributing their own aspects of availability. In other words the CISQ-model is more like the composed building blocks of the periodic table and less like the standard model of physics.

### The Model

![CISQ-Model](CISQ-3-model-views.png)
