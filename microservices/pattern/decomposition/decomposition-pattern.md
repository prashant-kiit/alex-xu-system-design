# How to decompose an application into services?

The site groups this under "Service boundaries" and offers two main patterns, both solving the same problem — how to decompose an application into services — with the same design forces guiding them.

**Shared forces both patterns must satisfy:**
- The architecture must be stable
- Services must be cohesive — each implementing a small set of strongly related functions
- Services must follow the Common Closure Principle — things that change together are packaged together, so a change affects only one service
- Services must be loosely coupled, each exposing an API that encapsulates its implementation
- Each service must be small enough for a "two pizza" team (6–10 people) to own and testable, and that team must be able to develop/deploy with minimal cross-team collaboration

**1. Decompose by business capability**
- Define services corresponding to business capabilities — a business capability is something the business does to generate value (e.g., *Order Management*, *Customer Management*), often organized into a multi-level hierarchy.
- Example: an online store's capabilities — product catalog management, inventory management, order management, delivery management — map directly to services.
- Benefits: stable architecture (capabilities rarely change), cross-functional autonomous teams organized around business value, cohesive/loosely-coupled services.
- Open issue: identifying capabilities requires deep business understanding; good starting points are the org structure and the high-level domain model.

**2. Decompose by subdomain**
- Define services corresponding to Domain-Driven Design (DDD) subdomains — subdomains are classified as **Core** (key business differentiator), **Supporting** (related but not differentiating), or **Generic** (not business-specific, often off-the-shelf).
- Example: same online store — product catalog, inventory management, order management, delivery management as subdomains.
- Benefits and identification approach mirror the business-capability pattern (org structure, domain model as starting points).

**How they relate:** the site lists each as an alternative to the other — you pick one lens (business capability vs. DDD subdomain) depending on which framing fits your organization better; in practice they often converge on similar service boundaries.

Related patterns mentioned elsewhere in the catalog: **Self-contained Service** and **Service per team**, both listed alongside these under "Service boundaries."

# Based on the above response Decompose by business capability and Decompose by subdomain, both sounds similar what is the difference b/w the two?

The site itself treats these as near-mirror patterns — same context, same problem, same forces, same benefits — and each page literally just calls the other "an alternative pattern" without spelling out a sharp contrast. But there is one real distinction the pages do draw, based on their differing "Solution" sections:

- **Decompose by business capability**: rooted in **business architecture**. A business capability is *"something that a business does in order to generate value"* and typically maps to a business object (e.g., Order Management, Customer Management). Capabilities are often organized into a multi-level hierarchy (e.g., top-level categories like Product/Service development, Product/Service delivery, Demand generation).
- **Decompose by subdomain**: rooted in **Domain-Driven Design (DDD)**. A subdomain is a slice of the business's "problem space" (the domain), and subdomains are explicitly classified into three types:
  - **Core** – the key differentiator, most valuable part of the app
  - **Supporting** – related to the business but not a differentiator (can be in-house or outsourced)
  - **Generic** – not business-specific, ideally bought off-the-shelf

So the practical difference the site implies:
- Business capability decomposition asks *"what does the business do?"* — a top-down, business-architecture view.
- Subdomain decomposition asks *"what is the shape of the problem domain, and which parts matter most?"* — a DDD-flavored view that also tells you where to invest engineering effort (core) vs. buy/outsource (generic).

In both cases the site's example (online store → product catalog, inventory, order, delivery management) ends up with **identical service boundaries** — the site doesn't show them producing different results, just different vocabularies/lenses for arriving there.

**Additional Context** (not from the site): in practice, many practitioners find subdomain/DDD decomposition more rigorous for complex domains because the core/supporting/generic classification directly informs prioritization, while business-capability decomposition is often easier to communicate to non-technical stakeholders since it mirrors how the business already talks about itself. The site doesn't make this comparative claim itself — treat it as general practitioner experience, not microservices.io content.

# Please give an example of a business to explain the difference.

The site's own example (an online store) doesn't actually show the two patterns diverging — both land on the same services. So to make the difference concrete, here's an illustrative example — flagged clearly since it goes beyond what the site provides.

**Additional Context** (not from microservices.io — illustrative only):

Imagine a **food delivery business** (like a restaurant marketplace app).

**Approach 1: Decompose by business capability**
You ask a business analyst "what does this business *do* to generate value?" and map its org chart / value chain:
- Restaurant Management (onboarding restaurants, menus)
- Order Management (placing, tracking orders)
- Delivery Management (assigning couriers, routing)
- Payments
- Customer Support
- Marketing/Promotions

Each becomes a service. The grouping mirrors how the *business itself* is organized — likely matching actual departments.

**Approach 2: Decompose by subdomain (DDD)**
You instead ask a domain expert to describe the *problem space* and classify it by business value:
- **Core subdomains** (the differentiator — where this company wins or loses): real-time courier dispatch/routing optimization, dynamic delivery-time estimation
- **Supporting subdomains** (necessary but not the differentiator): order management, restaurant catalog
- **Generic subdomains** (solved problems, buy off-the-shelf): payments (use Stripe), notifications/SMS (use Twilio), authentication

Here the split reveals something business-capability decomposition doesn't surface as naturally: **Payments** might look like its own important "capability" under approach 1, but under DDD subdomain analysis it's flagged as *generic* — meaning the company shouldn't build custom microservice logic there at all, just integrate a third-party service. Meanwhile "courier routing" — which might just be a sub-feature of "Delivery Management" under approach 1 — gets pulled out as its own **core** service deserving the most engineering investment, since it's the actual competitive differentiator.

So in this example:
- Business capability decomposition gives you a service map that mirrors the org chart.
- Subdomain decomposition gives you *the same rough boundaries*, but additionally tells you **where to invest** (core), **where to be efficient** (supporting), and **where to buy instead of build** (generic) — which is the extra layer of insight DDD's classification adds.