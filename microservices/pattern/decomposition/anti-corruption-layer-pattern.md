# What is anti corruption layer pattern?

The **Anti-corruption Layer (ACL)** pattern comes from Domain-Driven Design and is covered in **Chapter 13, Section 13.3.1** (pp. 446–448), as well as on the pattern site under "Refactoring."

**Problem it solves:** How do you prevent a legacy monolith's domain model from polluting the domain model of a new service?

**Why it's needed:** When you build a new service — either as a brand-new feature or by extracting a capability — you're free to design a clean, modern domain model using techniques like DDD. But the FTGO monolith's domain model is old, poorly defined, and often has "god classes" (like `Order`) juggling many responsibilities. If the new service talks to the monolith directly, using the monolith's vocabulary, class names, and field values, that mess starts leaking into your otherwise clean new model.

**Solution:** Insert a translation layer between the two domain models — a piece of code that converts between the monolith's "ubiquitous language" and the service's ubiquitous language, so each side can evolve independently without corrupting the other.

**Where it shows up in the book's example:**
- **Delayed Delivery Service** has a `CustomerContactInfoRepository` interface. Its implementation calls the monolith's REST endpoint and translates the response into the service's own `CustomerContactInfo` type — this translation is the ACL.
- **Event handlers** also need an ACL: when the monolith publishes `Order` domain events, an event handler in the new service must translate those events (using the monolith's language) into updates on the service's own entities (using the service's language) — remapping class names, field names, and sometimes values.
- It's **bidirectional** — the monolith uses an ACL too, when it calls a service or subscribes to a service's events, translating its own concepts into what the service expects.

**Key point from the book:** the translation can be trivial (a simple field mapping) or quite involved (e.g., mapping status codes between two different state models) — the complexity depends on how differently the two sides model the same concept.

**Related patterns:** it works hand-in-hand with the **Strangler Application** pattern (as you strangle the monolith, the ACL is what keeps each newly extracted service's model clean) and connects to the **integration glue** concept the book uses throughout Chapter 13 — the ACL is essentially the translation piece sitting inside that glue code.

*Citation: Chapter 13, Section 13.3.1, "Implementing an anti-corruption layer," pp. 446–448.*