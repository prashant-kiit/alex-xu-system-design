# What is CQRS Pattern?

The **CQRS** (Command Query Responsibility Segregation) pattern is covered in **Chapter 7, Section 7.2**, as the second — more powerful, more complex — approach to querying in a microservice architecture, used when **API Composition** falls short.

**Problem it solves — three specific cases the book identifies where API Composition doesn't work well:**
1. **Expensive in-memory joins** — e.g., `findOrderHistory()` needs to filter/sort by attributes (like a restaurant-name keyword) that only some services store. An API composer would have to pull *all* of a consumer's orders from every service and join them in memory — inefficient at scale.
2. **The owning service's database can't efficiently support the query** — e.g., text search, geospatial queries.
3. **Separation of concerns** — sometimes the service that *owns* the data isn't the right team/service to *implement* the query. The book's example: Restaurant Service owns restaurant data, but the high-volume, business-critical `findAvailableRestaurants()` query is better owned by the Order Service team — Restaurant Service's team shouldn't have to live in fear of breaking order placement every time they touch restaurant management.

**Solution:** Split the service (or the whole query landscape) into two sides:
- **Command side** — handles create/update/delete (CUD) operations, using ACID transactions against its own database, and publishes **domain events** whenever data changes (via a framework like Eventuate Tram, or event sourcing).
- **Query side** — a separate, simpler model with its **own database**, purpose-built for the queries it needs to serve (e.g., a search index, a geospatial store). It has **event handlers** that subscribe to the command side's domain events and keep its database updated. There can even be **multiple query-side models**, one per query type.

**CQRS as standalone query services:** the pattern isn't limited to restructuring *within* one service — you can build a dedicated **query-only service** whose entire API is read-only, backed by a database it keeps in sync purely by subscribing to events published by other services (e.g., a service implementing `findOrderHistory()` by consuming events from Order, Kitchen, Delivery, and Accounting Services).

**Trade-off vs. API Composition:** CQRS trades simplicity for capability — it lets you support queries that API Composition genuinely can't do efficiently, but at the cost of maintaining extra databases, event subscriptions, and **eventual consistency** (the query-side view can lag slightly behind the command side).

**How it ties to what we've covered:**
- It's presented as the **second of the two query patterns** in Chapter 7 — API Composition is preferred first; CQRS is reached for only when API Composition can't do the job.
- It reuses the **domain events** and **eventual consistency / replica** mechanisms we already saw in Chapter 13 (e.g., Delayed Delivery Service maintaining a replica of `Order`/`Restaurant` data by subscribing to the monolith's events) — that replica-building technique is essentially CQRS applied during a monolith-to-microservices migration.

# Give an example of CQRS Pattern that can explain all the concepts invovled in it.

Let's use the book's own worked example — the **Order History View**, implemented with **AWS DynamoDB** — to walk through every CQRS concept end to end (Chapter 7, Sections 7.2–7.4).

## The scenario
`findOrderHistory()` needs to return a filterable, sortable, paginated list of a consumer's past orders — filtering by keyword (restaurant/menu item), status, and age. This data is spread across **Order Service**, **Kitchen Service**, **Delivery Service**, and **Accounting Service**. As we discussed, API Composition can't do this efficiently (it would force expensive in-memory joins), so the book builds a dedicated **Order History Service** using CQRS.

## Command side vs. query side
- The **command side** is the existing services (Order Service, Kitchen Service, etc.) — they own the authoritative data, handle create/update/delete, and publish **domain events** whenever something changes (`OrderCreated`, `DeliveryPickedUp`, `DeliveryDelivered`, etc.).
- The **query side** is the new **Order History Service** — a query-only service with no command operations. It exists purely to serve `findOrderHistory()` fast.

# Order History Service belongs to which domain Order, Kitchen, Delivery or something else?

Good catch — and the book is explicit about this: **Order History Service doesn't belong to any of Order, Kitchen, Delivery, or Accounting.** It's its own **standalone service**.

The book's reasoning (Section 7.2.2, "CQRS and query-only services," p. 233–234): a CQRS view built by subscribing to events from **multiple** services "doesn't belong to any particular service, so it makes sense to implement it as a standalone service." Order History Service is given as the direct example — it subscribes to events published by Order Service, Kitchen Service, Delivery Service, and Accounting Service, and none of them is a natural "owner" of the combined view.

**Why not just attach it to one of the four?**
- The view is a **join across all of them** — it needs order status, kitchen/ticket status, delivery status, *and* payment status all in one place. Picking, say, Order Service to own it would make Order Service responsible for reading and reacting to events from three other domains it doesn't otherwise care about — muddying its boundary.
- The book makes the same argument for a different example just before this one: `findAvailableRestaurants()` is a *single-service* query (it only needs restaurant data), yet the book still recommends **not** putting it inside Restaurant Service — instead defining a separate **Available Restaurants Service** (or letting Order Service's team own it). The reasoning there is pure **separation of concerns**: Restaurant Service's team owns restaurant *management* (a CRUD, low-stakes concern), and shouldn't also be on the hook for a high-volume, business-critical query that, if broken, stops consumers from placing orders at all.

**So the general rule the book is teaching:** ownership of a query-side view is decided by *who needs to query it and how critical/complex the query is* — not by which service happens to own the underlying write-side data. A multi-service join **always** becomes its own standalone query service; even a single-service query **sometimes** does too, if bundling it with the owning service would overload that team with responsibilities outside their core concern.

# More Info on CQRS

CQRS (Command Query Responsibility Segregation) separates the write model (commands) from the read model (queries) into different data stores optimized for their respective access patterns.

**Why separate read and write models?**

In many systems, the ideal data structure for writing is different from the ideal structure for reading. The write side needs normalization, constraints, and ACID transactions to maintain correctness. The read side needs denormalization, pre-computed aggregations, and fast lookups to serve queries quickly.

**Example: Order history page**

The write model stores orders in normalized tables: `orders`, `order_items`, `shipping_addresses`, `payment_records`. Writes enforce referential integrity and business rules.

The read model stores a denormalized order summary: order ID, customer name, total amount, item count, order status, and last updated timestamp in a single document. Reads serve the order history page with one query instead of joining four tables.

**When CQRS is justified:**

- Read and write volumes differ by 10x or more (far more reads than writes)
- The read model needs a different database technology than the write model (e.g., writes to PostgreSQL, reads from Elasticsearch)
- The read model needs different data shapes for different consumers (mobile app needs a summary, admin dashboard needs full details)

**When CQRS is overkill:**

- Read and write patterns are similar (basic CRUD with similar volume)
- The system is small enough that one database handles both efficiently
- The added complexity of maintaining two models and event synchronization is not justified by the performance gain

**Interview Relevance:** CQRS is a pattern that interviewers expect you to know but also expect you to justify. Proposing CQRS for a simple CRUD service signals over-engineering. Proposing it for a high-read system with complex query needs signals strong design sense.