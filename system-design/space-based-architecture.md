## Space-Based Architecture (SBA)

**Definition:**
A **Space-Based Architecture (SBA)** is a distributed architecture where **application state and processing are colocated in an in-memory data grid ("space")**, eliminating the need for a centralized database during request processing.

### Core Idea

* Each node contains:

  * Business logic
  * In-memory data (space)
* Requests are processed locally using the data in memory.
* Data is asynchronously persisted to the database.

### Components

* **Processing Unit (PU):** Business logic + in-memory data.
* **Space (Data Grid):** Distributed in-memory storage shared across nodes.
* **Backup/Replication:** Keeps data available if a node fails.
* **Database:** Used mainly for persistence, not every request.

### Flow

```
Client
   |
Load Balancer
   |
+------------------------+
| Processing Units (PUs) |
| + Logic + In-Memory    |
| + Data Space           |
+------------------------+
          |
 Async persistence
          |
      Database
```

### Advantages

* Extremely **high throughput** and **low latency**
* Removes **database bottleneck**
* Easy horizontal scaling
* High availability through replication

### Disadvantages

* Increased memory usage
* Data consistency is more complex
* Recovery after failures requires replication/checkpointing
* Best suited for stateful, data-intensive workloads

### Use Cases

* Stock trading systems
* Online gaming
* Real-time analytics
* Fraud detection
* High-volume e-commerce sessions

> **One-line summary:**
> **Space-Based Architecture scales by keeping application data in a distributed in-memory "space" close to the business logic, using the database only for asynchronous persistence.**
