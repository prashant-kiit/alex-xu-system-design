# What is a pivot transcation in a saga?

A **pivot transaction** is a special transaction in the **Saga pattern** that divides a saga into:

1. **Compensatable transactions** (before the pivot)
2. **Retriable transactions** (after the pivot)

```
T1 → T2 → P → T3 → T4
↑     ↑     ↑    ↑    ↑
Comp. Comp. Pivot Retry Retry
```

Where:

* **T1, T2**: Can be undone using compensating transactions.
* **P (Pivot)**: The point of no return.
* **T3, T4**: Cannot be compensated, so they **must eventually succeed** (retry until successful).

---

## Why is a Pivot Transaction Needed?

Not every operation can be undone.

For example, suppose you're booking a flight:

```
Reserve Seat
↓
Charge Credit Card
↓
Issue Ticket
↓
Send Confirmation Email
```

Once the airline **issues the ticket**, it may not be possible (or practical) to reverse that action in the same way. That transaction becomes the **pivot**.

---

## Example

### Flight Booking Saga

```
1. Reserve seat          (Compensatable)
2. Charge payment        (Compensatable)
3. Issue ticket          (Pivot)
4. Send email            (Retriable)
5. Update loyalty points (Retriable)
```

### If failure occurs before pivot

```
Reserve seat ✓
Charge payment ✗
```

Compensate:

```
Release seat
Refund payment (if needed)
```

---

### If failure occurs after pivot

```
Reserve seat ✓
Charge payment ✓
Issue ticket ✓   ← Pivot
Send email ✗
```

Do **not** compensate.

Instead:

```
Retry Send Email
Retry Update Loyalty Points
Retry...
Retry...
Until success
```

Because the ticket has already been issued.

---

## Characteristics

A pivot transaction:

* Is executed **only after** all compensatable transactions succeed.
* Marks the **point of no return**.
* Usually **cannot be compensated**.
* Must succeed **exactly once**.
* After it succeeds, all remaining transactions are treated as **retriable**.

---

## Visualization

```
Before Pivot                After Pivot
--------------------|----------------------------
Can Undo            | Must Retry Until Success

Reserve Inventory   |
Charge Payment      |
                    |  Pivot
                    |  Confirm Order
                    |
Send Email          |
Create Invoice      |
Notify Warehouse    |
```

---

## Real-World E-commerce Example

Suppose you place an online order.

```
Reserve Inventory
↓
Authorize Payment
↓
Capture Payment   ← Pivot
↓
Generate Invoice
↓
Schedule Shipping
↓
Send Email
```

### Failure before pivot

```
Reserve Inventory ✓
Authorize Payment ✗
```

Compensate:

* Release inventory

---

### Failure after pivot

```
Reserve Inventory ✓
Authorize Payment ✓
Capture Payment ✓  ← Pivot
Generate Invoice ✗
```

Don't refund immediately.

Instead:

* Retry invoice generation.
* Retry shipping scheduling.
* Retry email.

Eventually everything completes.

---

## Why not compensate after the pivot?

Because the business has already crossed a **commit point** where reversing the action is either:

* impossible,
* expensive,
* legally undesirable,
* or inconsistent with business rules.

Instead of undoing, the system guarantees **eventual completion** of the remaining steps through retries.

---

## Summary

| Transaction Type  | Can be Undone?            | On Failure                                                              |
| ----------------- | ------------------------- | ----------------------------------------------------------------------- |
| **Compensatable** | ✅ Yes                     | Execute compensating transaction                                        |
| **Pivot**         | ❌ No (point of no return) | If it fails, the saga fails before committing; if it succeeds, continue |
| **Retriable**     | ❌ No                      | Retry until success (eventual completion)                               |

The pivot transaction is the **boundary** in a saga: **everything before it must be reversible, and everything after it must be reliably completed through retries rather than compensation**.
