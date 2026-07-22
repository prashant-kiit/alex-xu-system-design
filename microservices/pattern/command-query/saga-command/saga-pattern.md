# What is a Saga pattern?

The **Saga** pattern is covered in **Chapter 4, "Managing transactions with sagas"** (referenced again throughout Chapter 13).

**Problem it solves:** How do you maintain data consistency across multiple services, each with its own database, when a single business operation touches several of them — without using distributed transactions (2PC)?

**Why distributed transactions aren't the answer:** the book explains that traditional distributed transactions (e.g., the XA/2PC standard) don't work well for modern applications — they hurt availability, since per the CAP theorem, architects today prefer availability over strict consistency, and many modern technologies (NoSQL databases, message brokers) don't even support them.

**Solution:** A saga is **a sequence of local transactions**. Each local transaction updates data within a single service using ordinary ACID transactions. Completing one local transaction triggers the next one, coordinated via asynchronous messaging — so all steps eventually execute even if a participant is temporarily unavailable.

**Key difference from ACID transactions:**
- Sagas **lack isolation** — unlike ACID, other transactions can see a saga's intermediate, uncommitted-as-a-whole state.
- Since each local transaction commits on its own, there's no automatic rollback — if a later step fails, you must undo earlier steps manually using **compensating transactions**.

**Example — Create Order Saga (used throughout the chapter):**
1. Order Service: create `Order` (pending)
2. Consumer Service: verify consumer
3. Kitchen Service: create `Ticket`
4. Accounting Service: authorize credit card
5. Order/Kitchen Service: approve `Order`/`Ticket`

If step 4 fails (bad credit card), the saga runs **compensating transactions in reverse order** to undo steps 1–3 — e.g., rejecting the `Ticket` and the `Order`.

**Two ways to coordinate a saga:**
- **Choreography** — no central coordinator; each participant publishes events, and other participants subscribe and react (e.g., Order Service publishes "Order Created" → Consumer Service reacts → publishes its own event → Kitchen Service reacts, and so on).
- **Orchestration** — a central **saga orchestrator** class explicitly sends command messages telling each participant what to do, rather than participants inferring it from each other's events.

**Related terminology (also used in the Chapter 13 discussion):**
- **Compensatable transaction** — a step that needs a compensating transaction because a later step could still fail.
- **Pivot transaction** — the "point of no return" step; everything before it might need undoing, but nothing after it can fail.
- **Retriable transaction** — a step guaranteed to succeed if retried, so it never needs compensation.
- **Countermeasure / Semantic lock** — techniques to handle the lack of isolation between concurrent sagas.