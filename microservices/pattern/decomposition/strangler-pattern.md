# What is Strangler Pattern?

The **Strangler Application** pattern (also known as the Strangler Fig pattern, per Martin Fowler) is the overarching strategy the book uses for migrating a monolith to microservices — covered in **Chapter 13, Section 13.1** and referenced on the pattern site under "Refactoring."

**Problem it solves:** How do you migrate a legacy monolithic application to a microservice architecture without doing a risky "big bang" rewrite?

**Solution:** Instead of rewriting everything at once, you incrementally build a new application — the **strangler application** — made up of microservices that run *alongside* the existing monolith. Over time:
- The strangler application grows (new features and extracted capabilities move into it)
- The monolith shrinks
- Eventually the monolith either disappears entirely, or what's left of it just becomes another service

**Where the name comes from:** it's named after the strangler fig vine found in rainforests, which grows around a host tree, gradually reaching the sunlight above the canopy — and often the host tree eventually dies, leaving a tree-shaped vine in its place. The book uses this as a metaphor: the new architecture "strangles" the old one over time rather than replacing it in one shot.

**Why the book favors it:**
- It's far less risky than a rewrite — described as "servicing your car while driving down the highway at 70 mph," challenging but much safer than starting over.
- You get **incremental value** — each newly built service can use a modern tech stack and DevOps practices immediately, rather than waiting years for a full rewrite to finish.
- It lets you **prioritize** — migrate the highest-value, most actively-changing parts of the business first (e.g., the FTGO book example prioritizes delivery scheduling, since it's a competitive differentiator).

**How the strangler application is populated:** the book gives two concrete mechanisms for growing it — feeding directly into the strategies we discussed earlier:
1. **Implement new features as services** — never add new code to the monolith again.
2. **Extract existing business capabilities into services** — incrementally carve functionality (domain logic + data) out of the monolith.

**Related patterns:** **Anti-corruption Layer** (keeps the old and new domain models from polluting each other as you strangle the monolith), and **Saga** (maintains data consistency across the shrinking monolith and the growing set of services).

*Citation: Chapter 13, Section 13.1, pp. 430–432.*