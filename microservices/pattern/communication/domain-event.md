# What is Domain Event?

The **Domain Event** pattern is covered in **Chapter 5, "Designing business logic in a microservice architecture,"** Section 5.3.

**Definition (the book's own pattern box, p. 189):**
> An aggregate publishes a domain event when it's created or undergoes some other significant change.

In DDD terms: a domain event is **something that has happened to an aggregate** — usually representing a state change. The book's example: an `Order` aggregate has state-changing events like `OrderCreated`, `OrderCancelled`, `OrderShipped`, and it publishes one of these each time it transitions state (if there are interested consumers).

## What a domain event looks like in code
- It's a class named with a **past-participle verb** (`OrderCreated`, not `CreateOrder`) with properties that meaningfully describe the event — each a primitive or a value object.
- It typically has **metadata** — event ID, timestamp, possibly the user who triggered the change — either baked into the event class (e.g., via a superclass) or wrapped in an **envelope object** (`DomainEventEnvelope`) alongside the event, which also carries the aggregate's type and ID.
- The book's example: `OrderCreated` itself has no fields at all in its base form, because the order ID lives in the envelope, not the event.

## Why publish domain events — the book lists six concrete use cases, several of which we've already covered:
1. **Choreography-based sagas** (Chapter 4) — participants react to each other's published events instead of being told what to do by a central orchestrator.
2. **CQRS** (Chapter 7) — notifying a service that maintains a query-side replica that the source data changed, so it can update its view.
3. Notifying an external application via a **webhook or message broker**, to trigger the next step in a business process.
4. Notifying another component of the *same* application (e.g., pushing a WebSocket update to a browser, or updating a search index like Elasticsearch).
5. Sending user-facing **notifications** — texts/emails ("your order has shipped").
6. **Monitoring/behavioral analysis** — verifying correct behavior or modeling user behavior from the event stream.

## Event enrichment
A basic event (like bare `OrderCreated`) often lacks detail consumers need — forcing them to call back to the source service, adding overhead. **Event enrichment** means packing extra data directly into the event (e.g., `OrderCreated` including line items, delivery info, payment info, restaurant name) so consumers — like Order History Service from our CQRS discussion — don't need an extra round-trip.
- **Trade-off:** enriched events are less stable — they may need to change whenever any consumer's requirements change, which can hurt maintainability. The book notes it's often fairly obvious what to include, but "satisfying every consumer" isn't always achievable.

## Identifying domain events
Two techniques the book gives:
- Look for **"When X happens, do Y"** language in requirements (e.g., "When an Order is placed, send the consumer an email" implies an `OrderCreated`/`OrderPlaced` event).
- **Event storming** — a workshop-style technique where domain experts map out a domain's events using sticky notes on a large surface, to collaboratively surface the full set of meaningful events.

## How this connects to everything we've already discussed
Domain events are the **glue mechanism** underneath nearly every pattern we've covered:
- **Saga** (Ch. 4) — choreography-style sagas are literally built from a chain of domain events.
- **CQRS / Order History Service** (Ch. 7) — the event handlers we walked through (idempotency, foreign-key lookups, etc.) all consume domain events.
- **Strangler Application / Delayed Delivery Service** (Ch. 13) — replicated monolith data was kept in sync exactly by subscribing to the monolith's domain events.
- **Aggregate** (Ch. 5, same chapter) — domain events are emitted *by* aggregates, tying directly into the aggregate design we referenced earlier when discussing splitting the domain model during extraction.