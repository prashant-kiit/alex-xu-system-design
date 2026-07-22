# Microservices Anti-Pattern: The Distributed Monolith

> **Source:** Mehmet Ozkaya – *Microservices Antipattern: The Distributed Monolith*  
> https://mehmetozkaya.medium.com/microservices-antipattern-the-distributed-monolith-%EF%B8%8F-46d12281b3c2

---

# What is a Distributed Monolith?

A **Distributed Monolith** is an **anti-pattern** where an application is split into multiple services, but those services remain **tightly coupled**, eliminating most of the benefits of microservices.

Instead of getting:

- Independent deployment
- Independent scaling
- Team autonomy
- Fault isolation

you get:

- Network overhead
- Distributed system complexity
- Tight coupling
- Coordinated deployments

In short:

> **You get all the disadvantages of both Monoliths and Microservices with almost none of their advantages.** :contentReference[oaicite:0]{index=0}

---

# Definition

A distributed monolith is a system where:

- Services cannot evolve independently.
- Services depend heavily on each other.
- Teams must coordinate changes.
- Deployments are synchronized.
- Data is tightly coupled.
- Every business operation requires several services to be online.

---

# Characteristics

## 1. Tight Coupling Between Services

Instead of independent services:

```text
Order
    │
    ▼
Payment
```

you have

```text
Order
   │
   ▼
Payment
   │
   ▼
Inventory
   │
   ▼
Shipping
   │
   ▼
Notification
```

Every request requires many synchronous calls.

Changing one service usually requires changing several others.

### Problems

- Difficult development
- Difficult testing
- Slow deployments
- High coordination cost

---

## 2. Synchronized Deployments

A major goal of microservices is:

```text
Deploy Payment
without touching Order
```

Distributed Monolith:

```text
Order changed

↓

Payment must change

↓

Inventory must change

↓

Shipping must change

↓

Deploy everything together
```

This defeats the purpose of independent deployment. :contentReference[oaicite:1]{index=1}

---

## 3. Shared Database

Example

```text
Order Service

Inventory Service

Payment Service

↓

All use SAME Database
```

Problems

- Schema changes affect multiple services.
- Database becomes the coupling point.
- Teams cannot evolve independently.
- Database migrations become risky.

### Better

```text
Order Service
     │
 Order DB

Payment Service
     │
 Payment DB

Inventory Service
     │
 Inventory DB
```

Each service owns its data.

---

## 4. Excessive Synchronous Communication

Instead of:

```text
Order

↓

Publish Event
```

you get

```text
Order

↓

Payment

↓

Inventory

↓

Shipping

↓

Email

↓

Analytics
```

One request becomes:

```
1 User Request

↓

8 HTTP Calls

↓

Response
```

Problems

- High latency
- Cascading failures
- Reduced resilience
- Difficult debugging

---

# Why Distributed Monoliths Happen

## 1. Poor Service Boundaries

Services are split by technical layers instead of business capabilities.

Bad

```text
User Controller Service

User Repository Service

User Validation Service
```

Good

```text
Customer Service

Order Service

Billing Service
```

Business capability should define the service boundary.

---

## 2. Ignoring Domain-Driven Design (DDD)

Without bounded contexts, services become highly interconnected.

DDD encourages:

- Bounded Contexts
- Business Capabilities
- High cohesion
- Loose coupling

---

## 3. Shared Database

Teams often keep one large database after splitting the application.

Result

```
Monolith Database

↓

Many services

↓

Still tightly coupled
```

---

## 4. Migrating Without Refactoring

Common migration

```
Monolith

↓

Split into Services

↓

Keep same database

↓

Keep same business logic

↓

Keep same dependencies
```

Result

```
Distributed Monolith
```

Simply moving code into separate services is **not** enough. The architecture and service boundaries must also change. :contentReference[oaicite:2]{index=2}

---

# Architecture Comparison

## Monolith

```text
One Application

One Deployment

One Database
```

---

## Modular Monolith

```text
One Application

Modules

├── Orders
├── Inventory
├── Payment

One Deployment

Well-defined boundaries
```

---

## Microservices

```text
Order Service

Inventory Service

Payment Service

Shipping Service

Each has

• Own Deployment
• Own Database
• Own Team
```

---

## Distributed Monolith

```text
Order

↓

Payment

↓

Inventory

↓

Shipping

↓

Shared Database

↓

Deploy Together
```

Many services

BUT

Low modularity

High coupling

This is considered the **worst architectural outcome** because it combines the complexity of distributed systems with the rigidity of a monolith. :contentReference[oaicite:3]{index=3}

---

# Impacts

## 1. Reduced Flexibility

Cannot

- Deploy independently
- Scale independently
- Replace services independently

---

## 2. Increased Complexity

Need to coordinate

- Development
- Testing
- Releases
- Database changes

---

## 3. Performance Bottlenecks

Many synchronous calls produce

- Higher latency
- Network overhead
- Lower throughput

---

## 4. Higher Failure Risk

Example

```text
Order

↓

Payment

↓

Inventory

↓

Shipping
```

Inventory crashes.

Entire checkout fails.

One service failure cascades through the system.

---

# How to Avoid a Distributed Monolith

## 1. Define Clear Service Boundaries

Use

- Domain-Driven Design (DDD)
- Bounded Contexts
- Business Capabilities

Every service should own exactly one business capability.

---

## 2. Database Per Service

Never

```text
10 Services

↓

1 Database
```

Instead

```text
1 Service

↓

1 Database
```

This improves autonomy and reduces coupling. :contentReference[oaicite:4]{index=4}

---

## 3. Minimize Synchronous Communication

Prefer

```text
Order Created Event

↓

Kafka

↓

Inventory

↓

Notification

↓

Analytics
```

instead of

```text
HTTP

↓

HTTP

↓

HTTP

↓

HTTP
```

Benefits

- Better resilience
- Lower coupling
- Better scalability

---

## 4. Define Stable API Contracts

Services should communicate through versioned APIs.

Never access another service's database directly.

---

## 5. Continuously Refactor

Monitor

- Service dependencies
- Chatty communication
- Shared models
- Shared libraries
- Deployment dependencies

Refactor before coupling becomes permanent.

---

# Modular Monolith as a Bridge

The article recommends considering a **Modular Monolith** as an intermediate step before adopting microservices.

Advantages

- One deployment
- Strong module boundaries
- Lower operational complexity
- Easier testing
- Easier debugging
- Can later extract modules into microservices

A modular monolith provides many of the organizational benefits of microservices without the operational overhead of a distributed system. :contentReference[oaicite:5]{index=5}

---

# Warning Signs

If your architecture has these symptoms, it may be a Distributed Monolith:

- Services must be deployed together.
- One feature requires changes across many services.
- Services share one database.
- Heavy synchronous HTTP communication.
- Teams cannot work independently.
- Frequent cascading failures.
- Tight coupling between service APIs.
- Difficult debugging and testing.
- Scaling one feature requires scaling multiple services.

---

# Best Practices

- Design services around **business capabilities**.
- Apply **DDD** and **Bounded Contexts**.
- Use **Database per Service**.
- Prefer **asynchronous messaging** where appropriate.
- Keep services **loosely coupled**.
- Enforce **API contracts**.
- Allow **independent deployment**.
- Continuously refactor service boundaries.

---

# Key Takeaways

- A **Distributed Monolith** is one of the most common and costly microservices anti-patterns.
- Splitting code into multiple services does **not** automatically create a good microservices architecture.
- The core principles of microservices are **autonomy**, **loose coupling**, and **independent deployability**.
- **Shared databases**, **chatty synchronous communication**, and **coordinated deployments** are strong indicators of a distributed monolith.
- If you're not ready for microservices, a **Modular Monolith** is often a simpler and safer architecture that preserves modularity while avoiding unnecessary distributed-system complexity.