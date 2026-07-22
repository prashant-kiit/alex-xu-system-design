# What is API gateway pattern?

The **API Gateway** pattern is covered in **Chapter 8, "External API patterns"** (Section 8.2), and is also used throughout the Chapter 13 refactoring examples.

**Problem it solves:** How do external clients (mobile apps, browser JavaScript, third-party developers) efficiently and safely access an application built as multiple microservices?

**Why direct client-to-service access doesn't work well** — the book lays out several drawbacks:
- **Chatty APIs / poor UX:** a client (e.g., a mobile app) often needs data spread across several services, forcing multiple round-trips. Over high-latency mobile/internet networks (the book notes latency here is typically ~100x worse than a LAN), this makes the app feel slow and drains battery.
- **Lack of encapsulation:** if clients know about individual services directly, changing how the backend is decomposed (splitting/merging services, changing APIs) becomes very hard — you can't update a mobile app instantly the way you can a server-side component.
- **Protocol mismatch:** some internal IPC protocols aren't client-friendly or firewall-friendly.
- **Third-party API stability:** external developers need a stable API, but backend teams can't reasonably be responsible for indefinite backward compatibility on every internal service.

**Solution:** Introduce an **API gateway** — a service that acts as the single entry point for all API requests coming from outside the firewall. It sits between clients and the backend services and is responsible for:
- **Request routing** — consults a routing map (similar to reverse-proxy behavior, e.g., NGINX) to forward a request to the right backend service.
- **API composition** — for requests that need data from multiple services, the gateway itself calls each service and aggregates the results into one response, so the client makes just **one** request instead of many. The book's example: a mobile client calls a single `getOrderDetails()` on the API gateway, which internally calls `getOrder()`, `getDelivery()`, `getTicket()`, and `getBill()` across Order, Delivery, Kitchen, and Accounting Services.
- **Protocol translation** — e.g., translating between client-friendly protocols (HTTP, WebSockets) and whatever protocols the services use internally.
- Other cross-cutting functions such as **authentication** and rate limiting.

**How it showed up in our earlier discussions:** in the Chapter 13 refactoring example, the API Gateway routes new-feature requests (like `getDelayedOrders()`) to the new Delayed Delivery Service while routing everything else to the monolith — letting the strangler application grow without clients needing to know which backend actually serves each request. It's also the component that maps the monolith's `USERINFO` cookie into an `Authorization` header for services, handling authentication translation.

**Related patterns:** works closely with **API Composition** (the aggregation technique it uses internally) and, in the migration context, with the **Strangler Application** pattern — the gateway is what makes it possible for clients to be unaware that some requests go to new services and others still go to the old monolith.