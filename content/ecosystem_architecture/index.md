---
title: "An Ecosystem For Sovereign Digital Nations - Architectural constraints"
aliases:

- "/ecosystem_architecture/"
---

# An Ecosystem for Secure Information Systems

Published 2026-mm-dd, Updated 2026-mm-dd

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
