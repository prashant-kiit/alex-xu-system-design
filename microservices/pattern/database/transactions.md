# Explain Transactions.

This is covered in **Chapter 3, "Interprocess communication in a microservice architecture,"** Section **3.3.7, "Transactional messaging."**

## The problem
A service often needs to publish a message/event **as part of** a database transaction (e.g., publishing `OrderCreated` when it saves a new `Order`). If the database update and the message send aren't atomic, a crash between the two can leave the system inconsistent — e.g., the DB commits but the message never gets sent. The book rules out the traditional fix — **distributed transactions spanning the DB and broker** — because they're a poor fit for modern apps (bad for availability), and many modern brokers (e.g., Kafka) don't even support them.

## 1. Transactional Outbox
**Definition:** Use a database table (`OUTBOX`) as a **temporary message queue**, written to as part of the *same* local ACID transaction that updates the business data.
**How it works:** When Order Service creates/updates an `Order`, it also `INSERT`s the corresponding message into the `OUTBOX` table — same transaction, so atomicity is guaranteed for free (it's just a normal local DB transaction). A separate component, the **Message Relay**, later reads the `OUTBOX` table and actually publishes those rows to the message broker.
**NoSQL variant:** each business entity record carries an attribute holding a list of pending messages; appending to it is a single atomic operation. The challenge here is efficiently *finding* entities that have pending messages to publish.
**Role in the bigger picture:** this is the foundational pattern — it solves *where* to durably and atomically record "this message needs to be sent." The next two patterns are the two different ways to actually **move** those recorded messages out to the broker.

## 2. Polling Publisher
**Definition:** The Message Relay **polls the OUTBOX table** on a schedule, looking for unpublished rows.
**How it works:**
```sql
SELECT * FROM OUTBOX ORDERED BY ... ASC
```
It publishes each result to the broker, then removes it:
```sql
BEGIN
DELETE FROM OUTBOX WHERE ID in (....)
COMMIT
```
**Trade-off:** Simple, works fine at low scale — but frequent polling can get expensive, and whether it's even usable with a given NoSQL database depends on its query capabilities (since you'd be querying business entities directly rather than a dedicated `OUTBOX` table).

## 3. Transaction Log Tailing
**Definition:** Instead of polling, have the Message Relay **read the database's transaction log** (a.k.a. commit log) directly.
**How it works:** Every committed database update is already recorded as an entry in the DB's transaction log. A **Transaction Log Miner** reads that log, and for each relevant entry (e.g., an insert into `OUTBOX`), converts it into a message and publishes it to the broker. Works for both an RDBMS `OUTBOX` table and messages appended to NoSQL records.
**Trade-off:** More sophisticated and performant than polling — no repeated expensive queries — but it's a more complex piece of infrastructure to build/operate, since you're hooking into low-level, database-specific replication/log internals.

## How the three fit together
| Pattern | Role |
|---|---|
| **Transactional Outbox** | *Where* the message is durably, atomically recorded — the foundation |
| **Polling Publisher** | *How* to move outbox rows to the broker — simple, poll-based |
| **Transaction Log Tailing** | *How* to move outbox rows to the broker — sophisticated, log-based, better at scale |

So it's not "pick one of three" — it's really: **always use Transactional Outbox**, then choose **either** Polling Publisher **or** Transaction Log Tailing as the mechanism that drains it, based on your scale and database capabilities.

## How this connects to what we've covered
This is the mechanism underneath nearly everything we discussed earlier: it's exactly how **Domain Events** (Ch. 5) get reliably published, how **choreography-based Sagas** (Ch. 4) safely emit their step-completion events, and how a service's data gets safely replicated into a **CQRS** view (Ch. 7) — all of those assume events are published reliably alongside a DB write, and Transactional Outbox is *how* that reliability is actually achieved. It's also listed by the book as one of the two ways domain events get published, the other being full **Event Sourcing** (Ch. 6), where the event log itself *is* the database, sidestepping this dual-write problem entirely.