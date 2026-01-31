# An Ecosystem for Secure Information Systems

| Published 2026-mm-dd  | An Ecosystem for Sovereign Information Systems - Part 3 Architectural constraints |
| :---                  |                                                                           ---: |
|                       |                                                             Updated 2026-mm-dd |

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

Doable. formal verification as explored nin the 60ies and 70ies was never going to be a big part of secure informations systems and the later strategy of "enumerating badness", that is the creation of software that catalogs anything that is unwanted such as viruses, worms, software behavior was never going to be more than a temporary stop gap.

defeatism is not necessary in information security. we been through formal verification and got overwhelmed by complexity. Enumerating badness and got overwhelmed by badness. no need to stop at

## Other posts in category Systems and security

[A case against the CIA triad](https://anderscj.substack.com/p/a-case-against-the-cia-triad)

[CISQ-Model of security qualities](https://acje.github.io/CISQ-model/post)

[Liberal democracies needs a new compute stack. Part 1 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute)

[Liberal democracies needs a new compute stack. Part 2 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-2fd)

[Liberal democracies needs a new compute stack. Part 3 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-523)

[Liberal democracies needs a new compute stack. Part 4 (Substack)](https://anderscj.substack.com/p/liberal-democracies-needs-a-new-compute-d56)

[Structured service addressing. A new take on load balancing in IPv6](https://github.com/acje/structured-service-addressing)

[Fiber semantics. Event sourcing for complex domains](https://github.com/acje/Fiber-semantics)
