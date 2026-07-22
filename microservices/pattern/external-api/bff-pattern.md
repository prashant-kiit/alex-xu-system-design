# What is BFF Pattern?

The **Backends for Frontends (BFF)** pattern is covered in **Chapter 8, Section 8.2.1** (pp. 265–266), as a variant/refinement of the API Gateway pattern.

**Problem it solves:** A single, shared API gateway used by *all* clients (mobile, browser JavaScript, third-party apps) tends to become a monolith in its own right — different client teams end up competing to change the same shared gateway codebase, creating ownership friction and a development bottleneck.

**Solution:** Implement a **separate API gateway for each type of client**, rather than one shared gateway for everyone.
- A mobile API gateway, owned and operated by the mobile client team
- A browser API gateway, owned by the browser/JS team
- A public API gateway, owned by the public API team
- ...and so on, one per client type

Each client team fully owns their own gateway — they can change their API module without needing to coordinate with or wait on a central "API gateway team." Common cross-cutting functionality (e.g., edge functions shared across all gateways) is ideally kept in a **shared library**, maintained by a dedicated API gateway team, so logic isn't duplicated across every gateway instance.

**Origin:** the book notes the pattern was pioneered by Phil Calçado and colleagues at SoundCloud.

**Benefits called out in the book:**
- **Isolation/reliability** — a misbehaving API in one gateway can't easily affect the others, since each is a separate process.
- **Better observability** — since each is its own process/deployment.
- **Independent scalability** — each client-specific gateway can be scaled based on its own traffic patterns.
- **Faster startup** — each gateway is smaller and simpler than one giant shared gateway.

**Real-world example the book gives:** Netflix — after initially trying a one-size-fits-all API for its streaming service across many device types (TVs, Blu-ray players, phones, etc.) and finding it didn't work well, Netflix moved to per-device APIs, each developed and owned by that device's client team. In the first version, teams wrote Groovy scripts to implement routing and API composition per device; at scale, the Netflix API gateway handles billions of requests/day, with each call fanning out to roughly six or seven backend services on average.

**Related patterns:** BFF is essentially a way of applying the general **API Gateway** pattern per-client rather than as one shared component. It doesn't replace API composition or request routing — it just distributes *ownership* of those functions across teams instead of centralizing them.

*Citation: Chapter 8, Section 8.2.1, pp. 265–267.*