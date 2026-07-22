# What are distributed transactions?

A **distributed transaction** is a transaction that spans **multiple independent systems** (databases, services, or applications) and guarantees that **either all of the operations succeed or all of them fail**.

Think of it as extending the ACID properties (Atomicity, Consistency, Isolation, Durability) across multiple systems.

### Example

Suppose you're transferring **$100 from Bank A to Bank B**.

The transaction involves two databases:

1. Bank A database:

   * Deduct $100 from Alice's account.
2. Bank B database:

   * Add $100 to Bob's account.

If the money is deducted from Bank A but adding it to Bank B fails, you have an inconsistent state.

A distributed transaction ensures one of two outcomes:

* ✅ Both operations succeed.
* ✅ Both operations are rolled back.

Never:

* ❌ Money deducted but not deposited.
* ❌ Money deposited without being deducted.

---

## Why are distributed transactions needed?

Modern applications often use:

* Multiple databases
* Microservices
* Different technologies (SQL, NoSQL, message queues)

For example, placing an order may involve:

```
Order Service
      │
      ├── Order Database
      ├── Inventory Service
      ├── Payment Service
      └── Shipping Service
```

If payment succeeds but inventory reservation fails, what should happen?

A distributed transaction coordinates all these services so they reach a consistent outcome.

---

## How are they implemented?

### 1. Two-Phase Commit (2PC)

The classic protocol.

**Phase 1: Prepare**

The coordinator asks every participant:

> "Can you commit?"

Each service replies:

* Yes (prepared)
* No (abort)

```
Coordinator
      │
      ├── Payment: Ready
      ├── Inventory: Ready
      └── Order DB: Ready
```

---

**Phase 2: Commit**

If everyone said "Yes":

```
Coordinator
      │
      ├── Commit Payment
      ├── Commit Inventory
      └── Commit Order
```

Otherwise:

```
Coordinator
      │
      ├── Rollback Payment
      ├── Rollback Inventory
      └── Rollback Order
```

This guarantees atomicity.

---

### 2. Three-Phase Commit (3PC)

A variation of 2PC that reduces blocking during failures, but it's less commonly used due to complexity and limited practical benefits.

---

### 3. Saga Pattern

Modern microservices often **avoid distributed transactions** because 2PC can be slow, tightly coupled, and difficult to scale.

Instead, they use a **Saga**:

```
Reserve Inventory
       ↓
Charge Payment
       ↓
Create Order
       ↓
Schedule Shipping
```

If shipping fails:

```
Cancel Order
Refund Payment
Release Inventory
```

Instead of rolling everything back in one atomic transaction, each successful step has a **compensating action** that undoes its effects.

---

## Challenges of distributed transactions

* Network failures
* System crashes
* Timeouts
* Locks held for long periods
* Performance overhead
* Difficult debugging
* Reduced scalability

These challenges are why many cloud-native architectures favor eventual consistency with patterns like Sagas.

---

## Real-world examples

Distributed transactions are common in scenarios like:

* Banking transfers
* Airline ticket booking
* E-commerce checkout
* Hotel reservation systems
* Inventory and payment coordination

---

## Summary

| Traditional Transaction | Distributed Transaction                                         |
| ----------------------- | --------------------------------------------------------------- |
| One database            | Multiple databases/services                                     |
| One transaction manager | Coordinator across systems                                      |
| Local commit/rollback   | Global commit/rollback                                          |
| Fast                    | Slower due to coordination                                      |
| Simple ACID             | ACID across distributed systems (often with protocols like 2PC) |

In short, a distributed transaction is a mechanism that coordinates changes across multiple independent systems so they behave like a single transaction, ensuring the overall operation either completes successfully everywhere or is undone everywhere. In modern distributed systems, this is often replaced with **Saga-based** approaches that trade strict atomicity for better scalability and resilience.
