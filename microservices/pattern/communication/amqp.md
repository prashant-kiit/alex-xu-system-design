# AMQP (Advanced Message Queuing Protocol)

Link: https://www.rabbitmq.com/tutorials/amqp-concepts

## Overview
AMQP 0-9-1 is a messaging protocol where applications communicate through a broker. Publishers send messages to **exchanges**, which route them to **queues** based on **bindings**, and **consumers** retrieve messages from queues.

## Core Components

### Exchanges
Routing hubs that distribute messages to queues. Four types:
- **Direct** — routes based on exact routing key match.
- **Fanout** — broadcasts to all bound queues, ignores routing key.
- **Topic** — routes via pattern matching on routing keys (e.g. `*.orders.#`).
- **Headers** — routes based on message header attributes instead of routing keys.

The **default exchange** auto-binds every queue using the queue's name as the routing key.

### Queues
Store messages until consumed.
- **Durable** — survive broker restarts.
- **Transient** — do not.

### Bindings
Rules linking an exchange to a queue. May include a routing key that acts as a filter for which messages get delivered.

### Routing Keys
Message attribute used by exchanges to match against bindings and decide destination queue(s).

## Delivery Model

### Consumers
- **Push API** (recommended) — consumer subscribes, broker pushes messages.
- **Pull API** — consumer polls the queue (inefficient, avoid).

### Acknowledgments
Control when the broker removes a message from the queue:
- **Explicit ack** — broker waits for consumer confirmation before deleting.
- **Automatic ack** — message removed immediately on delivery (risk of loss if consumer crashes mid-processing).

## Infrastructure

- **Connections** — long-lived TCP links; support authentication and TLS.
- **Channels** — lightweight logical connections multiplexed over a single TCP connection; allow concurrent operations without opening multiple sockets.
- **Virtual Hosts (vhosts)** — isolated environments within one broker; separate users, exchanges, and queues (like namespaces).
- **Message Attributes** — metadata such as content type, delivery mode (persistent/transient), priority, timestamp.

## Takeaway for microservice communication
AMQP (via brokers like RabbitMQ) decouples producers and consumers: producers don't need to know which/how many consumers exist, exchange type + bindings determine routing, and durability/ack settings tune the reliability vs. throughput tradeoff.

---

# Queues vs Streams vs Event Bus

Link: https://joudwawad.medium.com/queues-vs-streams-vs-event-bus-the-mental-model-that-makes-system-design-click-02e28bfdc01a

## Mental model
**"Queues scale workers. Streams scale readers. Event buses scale routes."**

### Queues — work distribution
- Each message delivered to exactly **one** consumer, then deleted.
- Retention: gone once processed.
- Ordering: best-effort, or strict FIFO with message groups.
- Use case: background jobs, order processing, load leveling.
- (This is the AMQP/RabbitMQ model above.)

### Streams — historical record
- Append-only log; **multiple independent readers**, each with their own offset.
- Retention: time-bounded window (hours to a year+), not deleted on read.
- Ordering: guaranteed only within a partition (by partition key).
- Superpower: **replay** — readers can rewind and reprocess history.
- Use case: event sourcing, audit trails, analytics across teams.
- (This is the Kafka/Kinesis model.)

### Event Bus — fact broadcasting
- Publishes a fact **once**; many subscribers filter via rules/patterns.
- Retention: no replay guarantee.
- Ordering: best-effort, no guarantees.
- Carries "facts" (what happened), not "commands" (what to do).
- Use case: microservice choreography, decoupled reactions.

## Real-world pattern
Production systems typically layer all three: an event bus routes events, queues absorb parallel load per service, and a stream preserves history for replay/analytics.

---

# Enterprise Service Bus (ESB)

Link: https://pragyasapkota.medium.com/enterprise-service-bus-esb-48d25b891b22

## Definition
An architectural pattern where a **centralized** software component performs integration between applications — handling data transformation, connectivity, routing, protocol conversion, and request composition.

## Core capabilities
- Data model transformation
- Communication protocol conversion (e.g. SOAP ↔ REST)
- Message routing between services
- Composing/orchestrating multiple requests

## Advantages
- **Technology flexibility** — teams can upgrade tech in one app area without disrupting others.
- **Cost-effective scaling** — individual components scale independently.
- **Fault isolation** — one component failing doesn't necessarily take down others.

## Disadvantages
- **Single point of failure** — the bus itself is centralized; if it degrades, everything routed through it is affected.
- **Operational complexity** — significant setup/maintenance overhead.
- **Integration interdependence** — changes to one integration can destabilize others sharing the same bus.
- **Heavy testing burden** — any ESB change requires re-testing existing integrations.
- **Cross-team friction** — centralized ownership makes independent team velocity harder.

## Real-world examples
Azure Service Bus, IBM App Connect, Apache Camel, Fuse ESB.

## Takeaway
ESB theoretically standardizes cross-service communication, but the same centralization that gives it power (transformation, routing, orchestration in one place) also makes it a potential bottleneck/SPOF — a key reason many microservice architectures moved toward smarter endpoints + dumb pipes (queues/streams/event bus per above) instead of a smart centralized bus.


