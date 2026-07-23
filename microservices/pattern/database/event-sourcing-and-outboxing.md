
# How Transactional Outbox and Event sourcing are related?

This confirms it directly — this is exactly the connection the book makes explicit in **Chapter 5, Section 5.3.3** ("How to reliably publish domain events?"), which then sets up **Chapter 6's** motivation for Event Sourcing.

## The relationship: two different answers to the same reliability problem

Both patterns solve the **same underlying problem**: *how do you guarantee an event gets published whenever an aggregate's state changes, atomically with the database update?* They're **alternative solutions**, not complementary pieces — you use one or the other, not both, for a given aggregate.

### Transactional Outbox's answer
Keep your existing "state in tables" persistence model (Chapter 5's approach: aggregate methods return domain events as a **side effect**), and bolt reliable publishing on top:
- The aggregate's business logic updates its row(s) *and* the service inserts the returned events into an `OUTBOX` table — same local ACID transaction.
- A **Message Relay** (the book's own framework, **Eventuate Tram**, implements this using the `DomainEventPublisher` interface) later drains the `OUTBOX` table to the broker via Polling Publisher or Transaction Log Tailing.
- **The catch the book flags:** this only works if the developer **remembers to actually call the publisher** with the right events every time state changes. Nothing forces it — miss a call, and the event silently never gets published while the business logic still "works."

### Event Sourcing's answer
Don't bolt events onto a separate persistence model at all — **make events themselves the primary persistence mechanism**. The aggregate's state is entirely derived by replaying its stored event sequence. Since the "state change" and the "event" are now **the same thing being saved**, publishing becomes structurally guaranteed rather than something a developer has to remember.

## Why the book introduces Event Sourcing right after this
Chapter 6 opens by revisiting this exact drawback of Chapter 5's design — the risk of a developer forgetting to publish an event is called out explicitly as one of the motivations for event sourcing. So the book's own narrative arc is:

1. **Chapter 3** — teach transactional messaging in general (Transactional Outbox, Polling Publisher, Transaction Log Tailing) as the *general-purpose* reliable-publish mechanism for any local-transaction + message combo.
2. **Chapter 5** — apply that same mechanism (via Eventuate Tram, which literally implements Transactional Outbox under the hood) to domain events specifically — but flag its weak point: publishing is manual and error-prone.
3. **Chapter 6** — offer **Event Sourcing** as a structurally safer alternative that eliminates that weak point entirely, at the cost of a steeper learning curve and a different way of thinking about persistence.

## Side-by-side

| | Transactional Outbox | Event Sourcing |
|---|---|---|
| Primary persistence | State in normal tables | Sequence of events *is* the state |
| How reliability is achieved | Extra `OUTBOX` table + same local transaction | Structural — the event *is* what's saved |
| Risk of a missed/forgotten publish | Yes — a real drawback the book names | No — publishing isn't a separate step to forget |
| Framework example given | Eventuate Tram (`DomainEventPublisher`) | Event store (covered later in Ch. 6) |
| Learning curve | Low — fits familiar ORM/table thinking | Higher — genuinely different persistence model |