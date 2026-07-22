# What is Event Sourcing?

**Event Sourcing** is covered in **Chapter 6, "Developing business logic with event sourcing,"** as an alternative to traditional persistence, closely tied to the **Domain Event** pattern from Chapter 5.

## The core idea (Section 6.1)
Instead of persisting an aggregate's *current state* in database tables (rows/columns), event sourcing **persists an aggregate as a sequence of events**. Each event represents a state change. The application recreates an aggregate's current state at any point by **replaying its events** from the beginning.

This is a fundamentally different persistence model than the traditional ORM approach (mapping classes to tables, e.g., `Order` → `ORDER` table, `OrderLineItem` → `ORDER_LINE_ITEM` table).

## Why it exists — problems with traditional persistence (Section 6.1.1)
The book lists four drawbacks of the traditional table-mapping approach that motivate event sourcing:
1. **Object-relational impedance mismatch** — the classic mismatch between a tabular relational schema and a rich, graph-structured domain model (the book even quotes Ted Neward calling ORM "the Vietnam of Computer Science").
2. **Lack of aggregate history** — a row only shows the *current* state; you lose the full sequence of changes that got there.
3. **Tedious, error-prone audit logging** — if you need a history for compliance/auditing, you have to bolt it on manually.
4. **Event publishing is bolted on to the business logic** — this directly connects to what motivated this chapter: in Chapter 5's approach, an aggregate's methods return domain events, and a *separate* step has to remember to publish them. That's error-prone — a developer can forget to publish an event, and the business logic will keep working fine, silently hiding the bug.

## The key benefit — event sourcing fixes exactly that last problem
Because the event **is** the persisted unit of truth (not a bolted-on side effect of a state change), event sourcing **guarantees** an event is published whenever an aggregate is created or updated — there's no separate "don't forget to publish" step to get wrong.

Other benefits the book names:
- **Preserves complete history** of an aggregate — valuable for auditing and regulatory purposes.
- **Reliably publishes domain events** — a natural fit for microservice architectures, since (as covered earlier) domain events drive choreography-based sagas (Chapter 4) and CQRS view updates (Chapter 7).

## Drawbacks (the book flags this too)
Event sourcing has a **learning curve** — it's a genuinely different way of writing business logic and persisting objects than what most developers are used to (the extraction cuts off here, but the book goes on to cover implementing an **event store** to hold the sequences of events).

## How it connects to everything we've covered so far
- It's presented as the natural next step after **Domain Events** (Ch. 5) — Mary (the book's running example character) specifically worries that manually publishing domain events is error-prone, and event sourcing is introduced as the fix.
- It feeds directly into **Sagas** (Ch. 4) — the book's chapter outline explicitly covers "integrating sagas and event sourcing-based business logic" and "implementing saga orchestrators using event sourcing," since an event store is a natural place to also track saga state.
- It's one of the two ways the book mentions domain events can be published, referenced back in Chapter 7's CQRS discussion ("using a framework such as Eventuate Tram **or using event sourcing**").

*Citation: Chapter 6, Sections 6.1–6.1.1, pp. 183–185.*