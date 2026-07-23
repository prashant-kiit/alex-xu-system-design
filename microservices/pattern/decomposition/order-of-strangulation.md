# How order of service migration is important in Strangular Pattern?

This ties directly back to what we covered in our earlier walkthrough of Chapter 13 — the book makes the case that **extraction order isn't just a scheduling detail; it directly determines how much invasive, risky change the monolith needs to undergo.** Two separate reasons are given.

## Reason 1: Prioritize by business value (Section 13.2.3)
The book's first-order advice on ordering: extract capabilities that are **business-critical and under active, constant development** first. The logic:
- If you migrate a stable, rarely-touched part of the monolith, you spend real effort but get little ongoing benefit — nobody was struggling to develop it anyway.
- If you migrate a capability the business is actively investing in, the payoff (faster iteration, team autonomy, independent deployability) compounds every sprint afterward.
- This is why FTGO's own example prioritizes **delivery management** — it's called out as a genuine competitive differentiator, not a generic CRUD concern.

## Reason 2: Extraction order determines who carries the compensating-transaction burden (Section 13.3.2)
This is the more subtle, and more important, reason — and it's the one the book demonstrates concretely with FTGO's saga redesign.

**Recall the setup:** `createOrder()` used to be one ACID transaction in the monolith. Once part of it moves to a new service, it becomes a **saga** — and any step *before* the last one that could still fail needs a **compensating transaction** to undo it.

**Scenario A — extract Kitchen Service first:**
1. Monolith: create `Order` (pending)
2. Kitchen Service: create `Ticket`
3. Monolith: authorize card, approve `Order`

If step 2 fails, step 1 must be undone — meaning **the monolith** needs a compensating transaction. That means retrofitting the monolith's old, poorly-tested `Order` entity with new "pending/undo" states — exactly the kind of invasive, risky change to legacy code the whole migration is trying to avoid.

**Scenario B — extract Order Service first instead:**
1. **Order Service:** create `Order` (pending)
2. Monolith: verify consumer, authorize card, create `Ticket`
3. **Order Service:** approve `Order`

Now the monolith's step sits in the *middle* — nothing after it can fail, so it's the saga's **pivot transaction** (the point of no return). **The monolith never needs a compensating transaction at all.** All the tricky undo logic lives in Order Service — a brand-new, clean, well-tested piece of code, which is a far safer place to put that complexity.

## The general principle this establishes
By **choosing which service to extract first**, you're effectively choosing **where the compensating-transaction burden lands**. The book's strategy: sequence extractions so the **monolith's remaining participation in any saga stays the pivot (or later) step**, never an earlier, compensatable one. As you continue extracting — Kitchen Service next, then Accounting Service — each new extraction can be designed the same way, keeping the shrinking, harder-to-modify monolith core out of the "needs to be undone" business entirely.