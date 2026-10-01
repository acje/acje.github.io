---
title: "Pardosa: Event-Driven Storage with Fiber Semantics"
description: "Append-only line storage enforcing event-driven correctness, auditability, and verifiable deletion"
weight: 20
homeFeatured: true
---

## Pardosa: Event-Driven Storage with Fiber Semantics

Modern distributed applications increasingly adopt Event-Driven Architecture (EDA) to decouple services and scale ingestion. However, when complex enterprise systems migrate to event sourcing, they frequently run into severe correctness hazards: split-brain concurrent mutations, silent aggregate state corruption, and the architectural inability to satisfy legal deletion mandates (such as GDPR "right to be forgotten") without corrupting immutable event histories.

`Pardosa` is an append-only event-driven storage engine implemented in Rust, built specifically upon the principles of **Fiber Semantics**. It is designed for enterprise domains where **correctness, strict auditability, and deterministic deletion policies matter far more than raw ingestion volume**. Pardosa guarantees per-aggregate linearizability and single-writer fencing, backed by a formal 5-state lifecycle state machine.

```mermaid
flowchart TD
    subgraph Ingestion [Single-Writer Ingestion]
        CMD[Domain Command] --> CAS[CAS Single-Writer Fencing]
        CAS --> ADMIT[State Machine Admission]
    end

    subgraph Core [Pardosa Storage Core]
        SM[5-State Fiber Lifecycle]
        BLAKE[BLAKE3 Framing & Checksum]
        DRAG[Interleaved Dragline Stream]
    end

    subgraph Downstream [Decoupled Consumption]
        ECST[Event Carried State Transfer]
        PROJ[Autonomous Projections]
        AUDIT[Immutable Audit Trails]
    end

    ADMIT --> SM
    SM --> BLAKE
    BLAKE --> DRAG
    DRAG --> ECST
    ECST --> PROJ
    ECST --> AUDIT
```

---

## Domain State Governance & Verifiable Deletion

High-integrity enterprise applications require event storage that enforces two foundational invariants:

1. **Domain State Governance**: In enterprise systems, business entities transition through structured lifecycles governed by formal domain rules. Without aggregate-level fencing and state-transition admission control, concurrent mutations risk overwriting entity state and committing illegal transitions. Pardosa enforces first-class aggregate fencing and deterministic lifecycle admission directly at the storage boundary, guaranteeing that every committed event represents a validated, sequential state transition for that specific entity.
2. **The Immutability vs. Deletion Paradox**: Event-sourced systems require immutable historical streams for auditability, replayability, and provenance. However, regulated enterprises operate under strict legal mandates (such as GDPR Article 17, healthcare data privacy standards, and statutory retention expirations) requiring verifiable, physical data deletion. Traditional workarounds—such as breaking audit trails via out-of-band record patching, or encrypting payloads and discarding keys (crypto-shredding)—leave metadata exposed, historical commitments unverifiable, and physical storage un-reclaimed.

Pardosa resolves this tension by separating physical append-only container files (**draglines**) from aggregate lifecycle governance (**fibers**) and introducing cryptographically auditable, verifiable **line migrations**.

---

## Fiber Semantics: Entities as Ordered Event Chains

In Fiber Semantics, the lifecycle history of each domain entity is modeled as an independent **fiber**:

- **Definition**: A fiber is a singly linked list of immutable events belonging to a unique, domain-scoped identifier (`fiber_id`).
- **Chain Topology**: Rather than storing events in a forward array that must be rewritten on mutation, each event in a fiber explicitly references its immediate predecessor through a `precursor` pointer (a 16-byte predecessor event ID and a 32-byte BLAKE3 precursor hash).
- **Head-Anchored Traversal**: The active state of a fiber is always anchored at its newest event (the head). Reading an entity's current state requires inspecting only the head; traversing backward reconstructs historical state transitions without requiring full-log scans.

---

## Draglines: Append-Only Interleaved Commit Streams

While domain entities exist logically as independent fibers, disk I/O and network replication achieve maximum efficiency through sequential streaming. Pardosa unifies these models through the **dragline**:

```mermaid
flowchart LR
    subgraph Dragline ["Dragline (Physical Append-Only Stream)"]
        direction LR
        E1["E1: Id=A<br/>seq=0 (Create)"]
        E2["E2: Id=B<br/>seq=0 (Create)"]
        E3["E3: Id=A<br/>seq=1 (Update)"]
        E4["E4: Id=C<br/>seq=0 (Create)"]
        E5["E5: Id=B<br/>seq=1 (Update)"]
        E6["E6: Id=A<br/>seq=2 (Detach)"]

        E1 --> E2 --> E3 --> E4 --> E5 --> E6
    end

    subgraph FiberA ["Fiber A (Singly Linked History)"]
        E6 -. precursor .-> E3
        E3 -. precursor .-> E1
    end

    subgraph FiberB ["Fiber B (Singly Linked History)"]
        E5 -. precursor .-> E2
    end

    subgraph FiberC ["Fiber C (Singly Linked History)"]
        E4
    end

    classDef fiberA fill:#2563eb,stroke:#1d4ed8,stroke-width:2px,color:#ffffff
    classDef fiberB fill:#059669,stroke:#047857,stroke-width:2px,color:#ffffff
    classDef fiberC fill:#d97706,stroke:#b45309,stroke-width:2px,color:#ffffff

    class E1,E3,E6 fiberA
    class E2,E5 fiberB
    class E4 fiberC

    style FiberA stroke:#2563eb,stroke-width:2px
    style FiberB stroke:#059669,stroke-width:2px
    style FiberC stroke:#d97706,stroke-width:2px
```

- **Interleaving**: Events from thousands of concurrent fibers are committed sequentially onto a shared dragline.
- **Per-Aggregate Linearizability**: Sequential consistency is enforced strictly per fiber. Single-writer fencing using Compare-And-Swap (CAS) ensures that an append succeeds if and only if the event's declared `precursor` matches the active head of that fiber. If a concurrent writer attempts to append to the same fiber simultaneously, the CAS check fails immediately, preventing aggregate state corruption.
- **Atomic Durability**: Frames are appended with strict atomic durability (`write` $\rightarrow$ `fsync` $\rightarrow$ `atomic rename` $\rightarrow$ `parent dir fsync`), guaranteeing crash resilience against power loss or operating system faults.

---

## Physical Data Structure: On-Disk Dragline Layout

Pardosa separates line state into an artefact pair on disk:

1. **`<stem>.meta` (Descriptor File)**: Stores line metadata, schema commitments, domain namespace scope, and partition ownership.
2. **`<stem>.pgno` (Dragline Container File)**: Append-only storage file containing the container header followed by framed event records.

```text
+===================================================================================================+
| Offset 0x00 .. 0x0B (12 Bytes) : Container Header                                                 |
| +-------------------------------------------------------+---------------------------------------+ |
| | Magic: "PARDOSA\x01" (8 B: 0x50 41 52 44 4F 53 41 01) | Version: 1 LE (4 B: 0x01 00 00 00)    | |
| +-------------------------------------------------------+---------------------------------------+ |
+===================================================================================================+
| Offset 0x0C .. Offset 0x0C + frame_length_0 + 7 : FRAME 0 (Event 0 : Genesis on Fiber A)          |
| +----------------------+------------------------------------------------+-----------------------+ |
| | frame_length_0 (4 B) | Envelope 0 Payload: 85 + payload_length_0 bytes| CRC32C Checksum (4 B) | |
| | u32 LE               | (Castagnoli protected; folded into H_0 digest) | IEEE 802.3 / SSE4.2   | |
| +----------------------+------------------------------------------------+-----------------------+ |
|                                                                                                   |
| Envelope 0 Layout (Event E0, Fiber A Genesis Aggregate):                                          |
| +-----------------------------------------------------------------------------------------------+ |
| | EnvelopeHeader (81 bytes, Invariant C4.19)                                                    | |
| | +-----------------------+-----------------------+-----------+-------------------------------+ | |
| | | event_id: 0x01.. [E0] | fiber_id: 0xAA.. [A]  | detached  | precursor: [0u8; 16]          | | |
| | | (16 bytes, UUID/ULID) | (16 bytes, Aggregate) | 0x00 (1B) | (all zeroes: root genesis)    | | |
| | +-----------------------+-----------------------+-----------+-------------------------------+ | |
| | | precursor_hash: [0u8; 32] (all zeroes: root genesis on Fiber A, no predecessor)           | | |
| | +-------------------------------------------------------------------------------------------+ | |
| |                                                                                               | |
| | Payload Length & Domain Event Body (Initial State)                                            | |
| | +------------------------------------+------------------------------------------------------+ | |
| | | payload_length_0 (4 bytes, u32 LE) | payload_bytes: domain event payload (GenesisState)   | | |
| | +------------------------------------+------------------------------------------------------+ | |
| +-----------------------------------------------------------------------------------------------+ |
|                                                                                                   |
|   PHYSICAL STREAM INTEGRITY:                                                                      |
|   Rolling Digest H_0 = BLAKE3(Frame 0)                                                            |
+===================================================================================================+
|                                  ^  ^                                                             |
|   LOGICAL FIBER A LINKAGE        |  | precursor      : 0x01.. (E0) points to Frame 0 event_id     |
|   (Backward Causal Chain C5.40)  |  | precursor_hash : BLAKE3(Env 0) commits to Frame 0 envelope  |
+===================================================================================================+
| Offset: 0x0C + frame_length_0 + 8 (immediately follows Frame 0 without padding)                   |
| FRAME 1 (Event 1 : State Mutation on Fiber A)                                                     |
| +----------------------+------------------------------------------------+-----------------------+ |
| | frame_length_1 (4 B) | Envelope 1 Payload: 85 + payload_length_1 bytes| CRC32C Checksum (4 B) | |
| | u32 LE               | (Castagnoli protected; folded into H_1 digest) | IEEE 802.3 / SSE4.2   | |
| +----------------------+------------------------------------------------+-----------------------+ |
|                                                                                                   |
| Envelope 1 Layout (Event E1, Fiber A State Mutation):                                             |
| +-----------------------------------------------------------------------------------------------+ |
| | EnvelopeHeader (81 bytes, Invariant C4.19)                                                    | |
| | +-----------------------+-----------------------+-----------+-------------------------------+ | |
| | | event_id: 0x02.. [E1] | fiber_id: 0xAA.. [A]  | detached  | precursor: 0x01.. [E0]        | | |
| | | (16 bytes, UUID/ULID) | (16 bytes, Aggregate) | 0x00 (1B) | --> CAUSAL LINK to Event E0   | | |
| | +-----------------------+-----------------------+-----------+-------------------------------+ | |
| | | precursor_hash: BLAKE3(Envelope 0) (32 bytes cryptographic digest)                        | | |
| | | --> CRYPTOGRAPHIC COMMITMENT to predecessor Envelope 0 header + payload (Invariant C5.40) | | |
| | +-------------------------------------------------------------------------------------------+ | |
| |                                                                                               | |
| | Payload Length & Domain Event Body (Mutation Delta)                                           | |
| | +------------------------------------+------------------------------------------------------+ | |
| | | payload_length_1 (4 bytes, u32 LE) | payload_bytes: domain event payload (AccountUpdated) | | |
| | +------------------------------------+------------------------------------------------------+ | |
| +-----------------------------------------------------------------------------------------------+ |
|                                                                                                   |
|   PHYSICAL STREAM INTEGRITY:                                                                      |
|   Rolling Digest H_1 = BLAKE3(H_0 || Frame 1)  (Sequential tamper-evidence, Invariant C5.26)      |
+===================================================================================================+
| DUAL CRYPTOGRAPHIC COMMITMENTS SUMMARY (Orthogonal Chains):                                       |
|   1. Logical Precursor Linkage (Fiber A):                                                         |
|      Frame 1.precursor      == Frame 0.event_id (0x01.. [E0])                                     |
|      Frame 1.precursor_hash == BLAKE3(Envelope 0 Header || Payload)                               |
|   2. Physical Rolling Commitment (Dragline):                                                      |
|      H_0 = BLAKE3(Frame 0)                                                                        |
|      H_1 = BLAKE3(H_0 || Frame 1)                                                                 |
+===================================================================================================+
```

### 1. Container Header (12 Bytes)
At file offset `0x00000000` of `<stem>.pgno`, the container header establishes format identity:
- **Magic Bytes (`0x00..0x07`, 8 bytes)**: Fixed byte sequence `PARDOSA\x01` (`[0x50, 0x41, 0x52, 0x44, 0x4F, 0x53, 0x41, 0x01]`).
- **Format Version (`0x08..0x0B`, 4 bytes)**: 32-bit little-endian integer (`1` = `0x01, 0x00, 0x00, 0x00`).

Any file lacking this 12-byte signature is rejected during container initialization.

### 2. Frame Framing (Invariant C3.4)
Every commit to the dragline is framed with length demarcations and hardware-accelerated checksums:
- **Length Prefix (4 bytes)**: 32-bit little-endian unsigned integer declaring the byte length of the enclosed frame payload.
- **Frame Payload (`frame_length` bytes)**: The unpadded event envelope.
- **CRC32C Checksum (4 bytes)**: Castagnoli polynomial checksum (IEEE 802.3 / SSE4.2 CRC32C) computed over the frame payload bytes. Torn writes, truncated disk blocks, or silent disk bit-rot are detected prior to envelope parsing.

### 3. Event Envelope Header (Invariant C4.19)
The frame payload contains an unpadded, fixed 81-byte `EnvelopeHeader` followed by the domain event payload:

| Field | Offset | Width | Type | Description |
|---|---|---|---|---|
| `event_id` | `0x00` | 16 bytes | `[u8; 16]` | Globally unique event identifier (UUID/ULID). |
| `fiber_id` | `0x10` | 16 bytes | `[u8; 16]` | Scoped domain entity / aggregate identifier. |
| `detached` | `0x20` | 1 byte | `bool` (`u8`) | Lifecycle flag: `0x00` = active, `0x01` = soft-deleted. |
| `precursor` | `0x21` | 16 bytes | `[u8; 16]` | Predecessor `event_id` on this fiber (`[0u8; 16]` for root). |
| `precursor_hash` | `0x31` | 32 bytes | `[u8; 32]` | 256-bit BLAKE3 cryptographic hash of precursor event. |
| `payload_length` | `0x51` | 4 bytes | `u32` LE | Byte length $N$ of domain event payload. |
| `payload_bytes` | `0x55` | $N$ bytes | `[u8; N]` | Serialized domain-specific event payload. |

Total unpadded envelope length is exactly $81 + 4 + N = 85 + \text{payload\_length}$ bytes.

### 4. Physical vs. Logical Cryptographic Commitments

Pardosa maintains two complementary, orthogonal cryptographic chains:

```mermaid
flowchart TD
    subgraph PhysicalChain ["Physical Integrity Chain (Invariant C5.26)"]
        direction LR
        P0["Frame 0"] -->|BLAKE3 Fold| P1["Frame 1"]
        P1 -->|BLAKE3 Fold| P2["Frame 2"]
        P2 -->|BLAKE3 Fold| P3["Frame 3"]
        P3 -->|Rolling Digest H_k| PROOF["Physical Log Commitment"]
    end

    subgraph LogicalChains ["Logical Precursor Chains (Invariant C5.40)"]
        direction TB
        subgraph FiberAlpha ["Fiber Alpha"]
            A0["E0 (Root)"]
            A1["E2 (Update)"]
            A1 -. precursor_hash .-> A0
        end
        subgraph FiberBeta ["Fiber Beta"]
            B0["E1 (Root)"]
            B1["E3 (Update)"]
            B1 -. precursor_hash .-> B0
        end
    end
```

- **Physical Rolling Commitment (Invariant C5.26)**: A running 256-bit BLAKE3 hash digest computed sequentially across all container frames in `<stem>.pgno`. Each frame $k$ is folded into the rolling commitment:
  $$\mathcal{H}_k = \text{BLAKE3}(\mathcal{H}_{k-1} \parallel \text{Frame}_k)$$
  This guarantees immediate tamper-evidence for the physical stream: missing frames, reordered writes, or bit flips corrupt the rolling digest.
- **Logical Precursor Chain (Invariant C5.40)**: Independent, fiber-scoped hash linkage. Each event's `precursor_hash` contains the BLAKE3 digest of the preceding event on the same `fiber_id`.
- **Orthogonality**: Because physical commitments track file framing and logical commitments track aggregate state transitions, events from distinct fibers interleave freely without invalidating entity provenance. During line migrations, purged fibers can be pruned from `<stem>.pgno` without breaking the precursor chains of surviving fibers.

---

## The 5-State Lifecycle State Machine

At the core of Pardosa is an explicit, formal state machine governing every fiber's lifecycle. An aggregate does not merely exist or get deleted; it transitions across five strictly defined states:

1. **`Undefined`**: The entity has never existed within the domain namespace.
2. **`Defined`**: The fiber is active, exists, and accepts updates.
3. **`Detached`**: The fiber is soft-deleted; it remains on the dragline for historical auditability and can be rescued or migrated.
4. **`Purged`**: The fiber has been permanently removed from the line following an auditable migration, satisfying regulatory deletion mandates while preserving optional audit records.
5. **`Locked`**: The fiber has been pruned and frozen; the identifier cannot be reused, preventing replay attacks or accidental recreation.

### The 10 Legal Transitions

Pardosa encodes exactly **10 legal state transitions**. Any action attempting an unlisted transition is rejected at compile time and runtime by the `IllegalStateTransition` error:

```mermaid
stateDiagram-v2
    [*] --> Undefined
    
    Undefined --> Defined: 1. Create
    Defined --> Defined: 2. Update
    Defined --> Detached: 3. Detach
    Detached --> Defined: 4. Rescue
    Detached --> Detached: 5. Migrate(Keep)
    Detached --> Locked: 6. Migrate(LockAndPrune)
    Detached --> Purged: 7. Migrate(Purge)
    Locked --> Defined: 8. Rescue
    Locked --> Purged: 9. Migrate(Purge)
    Purged --> Defined: 10. Create
```

| # | Action | Source State | Target State | Operational Semantics |
|---|---|---|---|---|
| 1 | `Create` | `Undefined` | `Defined` | Initial creation of an entity from an empty state. |
| 2 | `Update` | `Defined` | `Defined` | Appending a new state-modifying event to an active fiber. |
| 3 | `Detach` | `Defined` | `Detached` | Soft-deleting an aggregate; marks head as detached. |
| 4 | `Rescue` | `Detached` | `Defined` | Reversing a soft delete; returns the fiber to active status. |
| 5 | `Migrate(Keep)` | `Detached` | `Detached` | Retains the soft-deleted fiber across a line migration. |
| 6 | `Migrate(LockAndPrune)` | `Detached` | `Locked` | Prunes fiber history, retaining only the tombstone; prevents reuse. |
| 7 | `Migrate(Purge)` | `Detached` | `Purged` | Verifiably scrubs all event payloads and keys from the active line. |
| 8 | `Rescue` | `Locked` | `Defined` | Administrative rescue of a locked fiber under an explicit audit policy. |
| 9 | `Migrate(Purge)` | `Locked` | `Purged` | Permanently purges a previously locked fiber during migration. |
| 10 | `Create` | `Purged` | `Defined` | Re-allocates the domain identifier cleanly following a complete purge. |

---

## Consumer Idempotency & Deterministic Projections

In event-driven architectures, downstream systems build read models, search indexes, and caches by projecting the event stream. Pardosa guarantees deterministic consumption and effectively exactly-once processing through explicit core invariants:

```mermaid
flowchart LR
    PARDOSA["Pardosa Dragline<br/>(Physical .pgno Log)"] -->|Stream Frames| DISPATCH["Event Dispatcher"]

    subgraph ConsumerTransactional ["Pattern A: Transactional Projections"]
        direction TB
        TX["Atomic Unit of Work"]
        STORE_A["Relational / Key-Value Store"]
        CURSOR_A["Checkpoint Cursor (C5.22)"]
        TX --> STORE_A
        TX --> CURSOR_A
    end

    subgraph ConsumerIdempotent ["Pattern B: Non-Transactional Sinks"]
        direction TB
        DEDUP["Deduplication Filter<br/>(16-byte event_id / 32-byte BLAKE3)"]
        STORE_B["Search Index / External Sink"]
        DEDUP -->|Unique| STORE_B
        DEDUP -->|Duplicate| DROP["No-Op Discard"]
    end

    DISPATCH --> TX
    DISPATCH --> DEDUP
```

### Core Invariants

1. **Total Replay Determinism (Invariant C3.8)**: Replaying the identical sequence of dragline frames produces identical projection state bit-for-bit. Projections rely strictly on immutable event facts—timestamps, precursors, and state payloads—eliminating dependencies on consumer arrival time, wall-clock skew, or execution environment non-determinism.
2. **Dragline-Local Resume Cursors (Invariant C5.22)**: Dragline consumers track progress using monotonic, container-local cursor offsets. Cursors represent verifiable physical frame boundaries within `<stem>.pgno`. They are valid by construction: a consumer cannot construct or advance to an unaligned offset or an uncommitted frame.
3. **Unique Event Identity & BLAKE3 Commitments**: Every event carries an unforgeable, globally unique 16-byte `event_id` and is cryptographically bound to a 32-byte BLAKE3 commitment (both frame-level digest and fiber precursor hash).

### Consumer Demarcation & Side-Effect Elimination

To achieve effectively exactly-once processing across network retries, worker restarts, or consumer rebalances, downstream projections implement explicit consumer demarcation:

- **Atomic Cursor Checkpointing (Transactional Sinks)**: When writing to datastores supporting transactional multi-row writes (such as relational databases or transactional key-value engines), projections store the dragline cursor position in the exact same transaction as the projection update:
  ```sql
  BEGIN TRANSACTION;
  -- Apply projection updates from event
  UPDATE customer_balances SET balance = balance + 500 WHERE customer_id = 'cust_8f2a';
  -- Checkpoint dragline-local cursor atomically
  UPDATE projection_checkpoints SET resume_cursor = 0x0004A2F0 WHERE projection_id = 'balance_view';
  COMMIT;
  ```
  On crash recovery or consumer failover, the worker queries `resume_cursor` and requests the dragline stream starting from that exact frame offset. Events already committed within prior transactions are never re-applied.

- **Idempotent Deduplication (Non-Transactional Sinks)**: When projecting into systems lacking atomic multi-resource transactions (e.g., search indexes, analytical column stores, distributed message queues, or third-party webhooks), consumers eliminate duplicate side-effects using the 16-byte `event_id` or 32-byte BLAKE3 commitment:
  - **Natural Upsert Keys**: Projections use `event_id` or deterministic entity head versions as document keys or idempotency tokens, turning repeated frame deliveries into no-op updates.
  - **Deduplication Windows**: Downstream workers maintain a lightweight, bounded deduplication set of processed `event_id` values within the replay buffer window. Re-delivered frames are recognized, recorded as duplicates, and dropped before invoking external side-effects.

### Event Carried State Transfer (ECST)
- **Self-Contained Domain Facts**: Events emitted by Pardosa carry full state transition facts rather than thin notifications. Downstream consumers receive all data necessary to project their read models without executing synchronous callback queries to the producer.
- **Autonomous Projections**: Read models (search indexes, reporting databases, HTML caches) consume the dragline independently at their own pace. If a consumer crashes or lags, write ingestion remains unaffected.

---

## Regulatory Compliance & Verifiable Deletion

In enterprise architectures, compliance cannot be an afterthought. Pardosa satisfies privacy legislation (such as GDPR Article 17) through **auditable line migrations**:

1. **Separation of Line and Audit**: A line contains the active operational stream. An optional audit log captures raw events separately under strict access controls.
2. **Cryptographic Integrity**: Payloads and envelope headers are hashed using BLAKE3. Tampering with any historical event on a fiber breaks the precursor hash chain immediately.
3. **Physical Purging via Line Migration**: When an operator executes a line migration with `Migrate(Purge)` on detached fibers:
   - Pardosa constructs a new, compacted line version (`<new_stem>.pgno` and `<new_stem>.meta`).
   - Events belonging to purged fibers are physically excluded from the new container file.
   - Active fibers are preserved, retaining their exact logical precursor hash relationships.
   - A fresh physical rolling BLAKE3 commitment is computed sequentially over the new container.
   - The old line version is verifiably scrubbed from disk, providing provable physical data destruction while preserving cryptographic proof of the migration transaction itself.

