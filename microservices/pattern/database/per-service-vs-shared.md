# Explain Database per Service vs Shared Database.

This isn't framed by the book as a standalone "pattern vs. pattern" comparison the way Saga/API Composition were — it's introduced in **Chapter 1** as one of the defining characteristics of the microservice architecture, contrasted directly against the shared-database approach used by monoliths and SOA.

## Database per Service

**Definition (Section 1.4.3, "Each service has its own database"):** A key characteristic of the microservice architecture is that services are loosely coupled and communicate only via APIs. One way this loose coupling is achieved is by giving **each service its own datastore**. In the book's online store example: Order Service has a database containing the `ORDERS` table; Customer Service has its own database containing the `CUSTOMERS` table — separate, private, not shared.

**Benefits the book calls out directly:**
- **Development-time independence** — developers can change a service's schema without coordinating with developers on other services.
- **Runtime isolation** — services don't block each other; one service is never stuck waiting because another service is holding a database lock.
- This is what makes services **truly loosely coupled** — if they all read/wrote the same tables, they'd be coupled at the data layer even if their code was cleanly separated.

## Shared Database

The book doesn't name this as a formal pattern, but describes it as the traditional approach used by **monolithic applications** and **SOA**:

- A **monolith** has a single database (as covered in our earlier monolith-vs-microservices discussion) — this is the natural, simplest form of a shared database.
- **SOA** (Service-Oriented Architecture) is explicitly compared to microservices in a table (Section 1.4.4) — SOA applications typically have a **global data model and shared databases**, in contrast to microservices' data model and database *per service*.

**Why shared databases were historically appealing / what they lose:**
- Simple, familiar, easy to run cross-entity SQL joins and ACID transactions (this is exactly the tradeoff we discussed earlier — monoliths get "simple interactions" and ACID transactions as one of their "dark matter" forces).
- But it directly undermines loose coupling: schema changes require coordinating across every team using that database, and one service's heavy database load or lock contention can affect every other service sharing it.

## The comparison table from the book (Section 1.4.4)

| | SOA | Microservices |
|---|---|---|
| Data | Global data model and shared databases | Data model and database per service |
| Inter-service communication | Smart pipes (ESB), heavyweight (SOAP/WS*) | Dumb pipes, lightweight (REST/gRPC) |
| Typical service size | Larger, monolithic | Smaller |

## The tradeoff this creates (tying back to what we've already covered)

Choosing Database per Service is exactly *why* the rest of the patterns we've discussed exist:
- You lose the ability to do a simple cross-entity **SQL join** → that's why **API Composition** and **CQRS** exist (Chapter 7).
- You lose the ability to wrap a multi-entity update in **one ACID transaction** → that's why **Saga** exists (Chapter 4).
- When migrating a monolith with one shared database, splitting it into per-service databases is exactly the "refactoring the database" work we walked through earlier in Chapter 13.

So the book's real answer to "which one should you use" is implicit in its whole structure: **Database per Service is a defining requirement of the microservice architecture** (not really an optional choice within it), and everything else — sagas, API composition, CQRS, anti-corruption layers — exists specifically to deal with the consequences of giving up the shared database.


# So Microservices must have DB per service?

Per the book: **essentially yes, at the database-table level — "not sharing database tables"** is treated as a defining characteristic, not an optional extra. But the framing is more precise than a blanket "must have a separate database server," so let's be exact about what the book actually says (Sections 1.4.3 and 2.1.2, p. 43):

**What the book requires:** Services must **not share database tables**. This is what actually matters — the book's stated benefits (independent schema evolution, no cross-service lock contention, true loose coupling) come specifically from *not sharing tables*, not from any particular deployment topology.

**What "own database" can mean in practice** — the book is flexible here, and this nuance matters:
- A dedicated database **server** per service (most isolation)
- A shared database **server**, but a separate **schema** per service
- Even a shared schema, as long as each service strictly owns and is the only one accessing **its own tables**

The mechanism can vary, but the *rule* — no service reaches into another service's tables directly, ever, only through that service's API — is what the book treats as non-negotiable for a "true" microservice architecture.

**Why it's non-negotiable rather than a nice-to-have:** the book states plainly that not sharing database tables is *how* loose coupling is achieved. If two services share tables, a schema change in one can silently break the other, and one service's database lock or heavy query load can stall the other — exactly the coupling microservices are meant to eliminate. Sharing tables gets you back to something functionally like the SOA "global data model" the book contrasts microservices against.

**The honest tradeoff the book names in the same breath:** it immediately flags that this comes at a cost — maintaining data consistency and querying across services are more complex once you stop sharing databases. That's precisely why the rest of the pattern language exists — Saga (Chapter 4) for consistency, API Composition/CQRS (Chapter 7) for querying.

**One related caution from Chapter 2, on a different but easily confused idea — shared *libraries*:** the book warns against packaging business logic (like `Order` handling) into a shared library used by multiple services, since a change would then force you to rebuild/redeploy every service using it — reintroducing coupling through the back door. Shared libraries are fine for stable, unlikely-to-change utility code (e.g., a generic `Money` class), but not for business logic. This isn't the same as the database question, but it's the same underlying principle: **coupling can sneak back in through shared code just as easily as through a shared database.**

**Bottom line per the book:** yes — no shared tables is treated as essential to actually having a microservice architecture, not a stylistic preference. Skip it, and the book calls the result exactly what it is elsewhere: a **distributed monolith** — a system with all the deployment complexity of microservices and all the coupling drawbacks of a monolith.