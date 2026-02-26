# Account Ledger – Product Requirement

## Overview

We need a lightweight account ledger component that can maintain balances for user accounts and record transactions for auditing purposes. This component will serve as a foundational building block for future financial features, so it should be reliable and reasonably extensible.

The ledger is not responsible for authentication or authorization. It assumes that callers are permitted to perform the requested operations.

---

## Scope for Current Iteration (Week 0)

This iteration focuses exclusively on defining correct behavior for basic ledger operations in a single-threaded, in-memory environment.

Engineering should concentrate on:

- Behavioral correctness
- Clear domain assumptions
- Explicit guarantees
- Identifying invariants

Advanced concerns such as persistence, distributed consistency, concurrency control, and fault tolerance are explicitly out of scope for this iteration.

---

## Functional Requirements

The system must support the following operations:

### 1. Create Account

- Create a new account using a unique account identifier.
- Optionally allow an initial balance to be set at creation time.
- The system should record account creation as part of the transaction history.

### 2. Deposit Funds

- Add funds to an existing account.
- The account balance should reflect the deposited amount.
- The deposit should be recorded as a transaction.

### 3. Withdraw Funds

- Remove funds from an existing account.
- The account balance should reflect the withdrawn amount.
- The withdrawal should be recorded as a transaction.

### 4. Transfer Funds

- Move funds from one account to another.
- The source account balance should decrease.
- The target account balance should increase.
- The transfer should be recorded in the transaction history in a way that supports auditing.

---

## Transaction History

- All balance-changing operations must be recorded.
- Each transaction record should include:
  - A unique identifier
  - A timestamp
  - The type of operation (create, deposit, withdraw, transfer)
  - Relevant account identifiers
  - The amount involved

- The transaction history should allow the system to be audited and inspected later.

---

## Behavioral Expectations

- The system should behave predictably under normal usage.
- Balances should accurately reflect user activity.
- The component should not lose transaction records.
- The system should be safe to use as a core financial building block.

---

## Non-Goals (For Now)

- No persistence is required at this stage (in-memory operation is acceptable).
- No user authentication or authorization logic is required.
- No external integrations are required.
- No concurrency guarantees are explicitly required in this phase.

---

## Open Questions / Clarifications (To Be Addressed by Engineering)

- How should the system behave when operations reference unknown accounts?
- How should invalid input (e.g., negative or zero amounts) be handled?
- Are negative balances allowed under any circumstances?
- Are there constraints around transfer atomicity?
- What exactly constitutes “auditable” in this context?

---

This is an initial draft and may evolve based on engineering feedback.

---

That’s a very healthy concern.

Right now your requirement reads like a **product-level document**, not a **week-0 lab requirement**.

There’s nothing wrong with that structurally — but it creates two risks:

1. Students may chase features that the scaffold does not support.
2. The lab may drift into feature completion rather than specification analysis.

For Week 0, your goal is not to build a production ledger.

Your goal is:

- Derive domain assumptions.
- Identify guarantees.
- Surface invariants.
- Strengthen oracles.
- Recognize specification gaps.

So the requirement should support ambiguity analysis — not roadmap planning.

---

# Where Your Current Requirement Is Potentially Too Large

These lines subtly expand scope:

- “Foundational building block for future financial features”
- “Reasonably extensible”
- “Safe to use as a core financial building block”
- “Support auditing”
- “Transfer atomicity”
- “Concurrency guarantees”
- “Component should not lose transaction records”

Those imply:

- durability
- atomicity
- safety guarantees
- extensibility concerns
- architectural robustness

But your Week 0 code is:

- in-memory
- no concurrency
- no persistence
- no atomicity model
- no exception discipline

So students may start asking:

- Should this be transactional?
- Should this use locks?
- Should transfers be atomic?
- Should we enforce ACID semantics?

That’s great thinking — but it’s not what this lab is about.

---

# What Week 0 Actually Needs

For this first iteration, you want:

- Enough ambiguity to force specification work.
- Enough incompleteness to expose missing invariants.
- Not so much scope that students redesign the system.

You want the tension to be about:

- balances
- transfers
- conservation of funds
- negative amounts
- unknown accounts
- domain assumptions
- explicit guarantees

Not:

- persistence
- extensibility
- transaction isolation
- concurrency models
