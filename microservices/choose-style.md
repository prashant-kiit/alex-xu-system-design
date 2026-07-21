# Which architectural style should you choose for an application? Monolithic vs Microservices?

Both patterns solve the same problem — how to organize an application's subdomains into deployable components — and the site frames the choice around the same set of five **dark energy forces** (pushing toward decomposition: simple components, team autonomy, fast deployment pipeline, multiple tech stacks, segregation by characteristics) and five **dark matter forces** (resisting it: simple/efficient interactions, preferring ACID over BASE, minimizing runtime/design-time coupling).

**Monolithic architecture**
- Structures the application as a single deployable/executable component that uses a single database, containing all of the application's subdomains, so all operations are local.
- Strengths: interactions are simple and efficient since communication is local, operations can usually be implemented as ACID transactions, and there's no runtime or design-time coupling between components.
- Weaknesses: as a single large component it can become difficult to understand and maintain, team autonomy suffers since teams share one codebase, the deployment pipeline can get slow, and it's stuck with one technology stack.
- Netflix, Amazon.com and eBay all started out with a monolithic architecture.

**Microservice architecture**
- Structures the application as a set of two or more independently deployable, loosely coupled services, each consisting of one or more subdomains and owned by the team(s) that own those subdomains.
- Strengths: services are simpler and easier to maintain, teams gain autonomy to develop/test/deploy independently, each service's pipeline is faster since it's smaller, different services can use different tech stacks, and subdomains can be segregated by characteristics like scalability or security needs.
- Weaknesses: distributed operations can be complex and hard to troubleshoot, potentially inefficient, and often need complex eventually-consistent transaction management since each service has its own database; there's also risk of tight runtime or design-time coupling between services.
- Netflix, Amazon, and eBay have all since evolved from monolithic to microservice architectures as they scaled.

**How the site frames the decision:** the first key issue is whether to use the monolithic or microservice architecture, and the Assemblage process uses the dark energy/dark matter forces to help decide — the outcome of applying Assemblage is either a monolithic or a microservice architecture. In short: monolith favors simplicity and low coupling for smaller/less complex apps or teams that don't yet need independent scaling; microservices favor team autonomy, independent deployability, and tech-stack flexibility as the app and organization grow.