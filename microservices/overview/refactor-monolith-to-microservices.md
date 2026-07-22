# What are the techniques to refactor monolith to micro services as per chapter 13?

According to **Chapter 13, "Refactoring to microservices"** (Section 13.2, "Strategies for refactoring a monolith to microservices," pp. 433–440), the author frames refactoring as an incremental process rather than a rewrite, then lays out three concrete strategies:

**Overall approach: the Strangler Application pattern (Section 13.1)**
Rather than a "big bang" rewrite, you incrementally grow a new **strangler application** made of services that runs alongside the monolith. Over time the monolith shrinks — either disappearing entirely or becoming just another service — while the strangler application grows. The author notes this typically takes months or years (citing Amazon.com's multi-year migration) and stresses demonstrating value early by migrating high-value, fast-changing areas first.

**The three strategies (Section 13.2):**

1. **Implement new features as services** (13.2.1)
   - Don't add new code to the monolith — build new features as standalone services from the start.
   - Reduces the monolith's growth rate, accelerates delivery of the new feature (fresh codebase), and quickly proves the value of microservices.
   - Requires **integration glue code** (adapters using REST, messaging, etc.) plus an **API gateway** to route requests between old and new functionality.
   - Not always feasible — if a feature is too tightly coupled to monolith code, excessive interprocess communication or data-consistency problems can result; in that case, implement it in the monolith first and extract it later.

2. **Separate presentation tier from the backend** (13.2.2)
   - Split the presentation layer (HTTP handling, UI/HTML generation) from the business logic and data access layers, using the business tier's existing coarse-grained facade API as the natural seam.
   - Benefits: the two resulting applications can be developed, deployed, and scaled independently, and it exposes a remote API that later-built microservices can call.
   - Explicitly called only a **partial solution** — one or both resulting pieces will likely still be an unmanageable monolith, so the third strategy is still needed.

3. **Extract business capabilities into services** (13.2.3)
   - The core strategy for actually breaking apart the monolith: incrementally migrate a vertical slice — inbound adapters, domain logic, outbound adapters, and the relevant slice of the database schema — out of the monolith into a new service.
   - Two main challenges called out: **splitting the domain model** and **refactoring the database**.
     - For the domain model: eliminate object references that would span service boundaries by modeling classes as DDD aggregates (referenced in Chapter 5) and replacing object references with primary keys (e.g., an `Order` referencing `Restaurant` becomes an `Order` holding a `restaurantId`).
   - Advice: prioritize extracting capabilities that are business-critical and under constant, active development — don't spend effort extracting where there's little benefit.

# Please explain "Refactoring the database" and "Maintaining data consistency (sagas)" more clearly.

Let me break both of these down more simply, since they're the two trickiest parts of the FTGO example.

## Refactoring the database

**The core problem:** When you pull a capability out of the monolith, you're not just moving code — you're moving *data*. If `Delivery` used to be a few columns bolted onto the `Order` table, those columns need to end up in their own table, in their own database, owned by the new Delivery Service.

**Why that's hard:** The moment you do this cleanly and all at once, every piece of monolith code that reads or writes those columns breaks, because the data isn't there anymore. Untangling all those call sites in one shot is slow and risky.

**The book's solution — a transition period, not a clean cut:**

1. Create the new `DELIVERY` table in Delivery Service's own database, and give it the delivery-related columns (`scheduledPickupTime`, `scheduledDeliveryTime`, etc.).
2. **Don't rip those columns out of the monolith's `ORDERS` table yet.** Leave them in place, but make them **read-only** in the monolith.
3. Keep the two copies in sync by **replicating data from Delivery Service back into the monolith** (e.g., whenever Delivery Service updates a delivery, it also updates the monolith's now-read-only copy).
4. Now, only the *small number of places* in the monolith that actually **write** to those fields need to change (to call Delivery Service instead) — everything that just *reads* them keeps working exactly as before, untouched.
5. Over time, as more of that reading code gets migrated/extracted too, you can eventually drop the replicated columns from the monolith entirely.

**Why this is clever:** it converts "change everything everywhere at once" into "change only the write paths now, migrate the rest later — maybe never." It buys you time and reduces risk, at the cost of temporarily maintaining a synced duplicate of the data.

---

## Maintaining data consistency (sagas)

**The core problem:** Before extraction, `createOrder()` was one clean ACID transaction — it either fully succeeds or fully rolls back, all in one database. Once part of that logic (say, ticket creation) moves to a separate service with its *own* database, you can no longer wrap the whole thing in one transaction. You need a **saga** instead — a sequence of smaller local transactions, each committing independently, coordinated by messages/events.

**The catch:** if step 2 of the saga fails, you can't "roll back" step 1 the normal database way — you have to *undo* it manually with a **compensating transaction**. And building compensating logic into old, poorly-tested monolith code is exactly the kind of risky, invasive work you're trying to avoid.

**Example 1 — the expensive case (extracting Kitchen Service first):**
- Step 1 (monolith): create `Order` in `APPROVAL_PENDING` state
- Step 2 (Kitchen Service): create `Ticket`
- Step 3 (monolith): authorize credit card, mark `Order` as `APPROVED`

Here, if step 2 fails, you must undo step 1 — meaning the *monolith's* transaction needs a compensating transaction. That means changing the monolith's `Order` entity to support a new "pending/undo" state, touching lots of existing code. Expensive and risky.

**Example 2 — the cheap case (extracting Order Service first instead):**
- Step 1 (Order Service): create `Order` in `APPROVAL_PENDING`
- Step 2 (monolith): verify consumer, authorize card, create `Ticket`
- Step 3 (Order Service): mark `Order` as `APPROVED`

Here, the monolith's transaction sits in the *middle* and nothing after it can fail — it's the **pivot transaction** (the saga's "point of no return": once it succeeds, the whole saga is guaranteed to finish). That means the monolith itself never needs to support undo logic — all the compensating-transaction complexity lives in Order Service, which is new, clean, and easy to test.

**The key insight — order of extraction matters:**
By choosing to extract **Order Service before Kitchen Service** (and later Accounting Service), the book shows you can keep engineering the saga so the monolith's step is always the pivot — never something that needs to be compensated. As more services get extracted, the pattern holds: each new service takes on the compensatable steps, the monolith's remaining step stays the safe middle pivot.

**Bottom line:** the sequence in which you extract services isn't arbitrary — done carefully, it can mean the difference between "I need to invasively rewire the monolith's transaction logic" and "the monolith's code barely changes at all."

*Citation: Chapter 13, Section 13.3.2, pp. 448–453 ("Refactoring the database" content appears earlier, in 13.2.3, pp. 439–441).*
