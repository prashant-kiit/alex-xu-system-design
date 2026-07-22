# What is API Composition pattern?

The **API Composition** pattern is covered in **Chapter 7, "Implementing queries in a microservice architecture"** (Section 7.1).

**Problem it solves:** In a monolith, a query that needs data spanning multiple business concepts is just a SQL `SELECT` with a `JOIN`. In a microservice architecture, each service owns its own database, so that data is scattered across multiple databases — you can't run a cross-service SQL join, and doing so would violate encapsulation anyway.

**Solution:** Implement the query operation by having a component invoke each of the relevant services via their APIs, then combine the results itself, in memory. The pattern has two roles:
- **API composer** — implements the query by calling all the necessary provider services and merging the results. This can be a client (e.g., a web app rendering a page), or a service — commonly an API Gateway or a Backend for Frontends.
- **Provider service(s)** — each owns a slice of the data the query needs, and exposes it via its own API.

**The book's example — `findOrder()`:** In the monolith, this was one SQL join. In the microservices version, the data needed lives across four services:
- Order Service — basic order info/status
- Kitchen Service — restaurant-side status, ready-time estimate
- Delivery Service — delivery status, ETA, location
- Accounting Service — payment status

A **Find Order Composer** exposes `GET /order/{orderId}`, then internally calls all four services' endpoints (`GET /orders/{orderId}`, `GET /tickets?orderId=...`, `GET /deliveries?orderId=...`, `GET /charges?orderId=...`) and joins the responses on `orderId` before returning a single combined `OrderDetails` response to the client.

**When it's a good fit — and when it isn't:**
- Works well when it's essentially a simple, primary-key-based equi-join across services that each expose the needed lookup API — like `findOrder()`.
- The book flags a real limitation: if the provider services' APIs don't support efficient retrieval, the composer may be forced into an **inefficient in-memory join over large datasets** — and there are query scenarios (covered later in the chapter) that simply can't be implemented this way, which is where the more complex **CQRS** pattern becomes necessary instead.

**Relationship to patterns we've already covered:**
- It's the **simplest of the two query-implementation patterns** the book presents in Chapter 7 — the other being **CQRS**, described as more powerful but more complex (maintains dedicated view databases purely for querying).
- It's exactly the mechanism the **API Gateway** pattern uses internally to implement composed endpoints like `getOrderDetails()` — the gateway *is* acting as the API composer in that earlier example.
- The **Backends for Frontends** variant of the gateway can likewise act as the API composer for a specific client type.