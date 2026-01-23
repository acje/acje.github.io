# An Ecosystem for Secure Information Systems

**This is part 3 of 3 in this series.**

Published: yyyy-mm-dd

---
<div align="right">
Updated yyyy-mm-dd
</div>

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
