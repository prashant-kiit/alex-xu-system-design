# Microservices Notes

Source: https://microservices.io/patterns/microservices.html

## Steps

1. What is the Business?
2. How is the Business Organized? What are the Domains and Sub Domains?
3. How to map the Business Domains and SubDomains to the Engineering Bounded Contexts and SubContexts?
4. How the Engineering Team Topology will look like? How the DevOps will be done?
5. Within the Bounded Context (A boundary where a domain/subdomain model has a single, consistent meaning), what is the:
   - Ubiquitous Language (A common vocabulary shared by developers and domain experts)
   - Entity (An object with a unique identity) — Child Joined Data Model mapped to Table
   - Aggregate (A cluster of related entities treated as one unit, with an Aggregate Root controlling access) — Parent Joined Data Model mapped to Table
   - Service (Business logic that doesn't naturally belong to a single entity)
   - Repository (Provides access to aggregates without exposing persistence details)
   - Value Object (An object defined by its values, not identity) — DTO and DAO

## How to organize the subdomains into one or more deployable/executable components?

There are five **dark energy** forces:
- Simple components — simple components consisting of few subdomains are easier to understand and maintain than complex components
- Team autonomy — a team needs to be able to develop, test and deploy their software independently of other teams
- Fast deployment pipeline — fast feedback and high deployment frequency are essential and are enabled by a fast deployment pipeline, which in turn requires components that are fast to build and test.
- Support multiple technology stacks — subdomains are sometimes implemented using a variety of technologies; and developers need to evolve the application’s technology stack, e.g. use current versions of languages and frameworks
- Segregate by characteristics — e.g. resource requirements to improve scalability, their availability requirements to improve availability, their security requirements to improve security, etc.

There are five **dark matter** forces:
- Simple interactions — an operation that’s local to a component or consists of a few simple interactions between components is easier to understand and troubleshoot than a distributed operation, especially one consisting of complex interactions
- Efficient interactions — a distributed operation that involves lots of network round trips and large data transfers can be too inefficient
- Prefer ACID over BASE — it’s easier to implement an operation as an ACID transaction rather than, for example, eventually consistent sagas
- Minimize runtime coupling — to maximize the availability and reduce the latency of an operation
- Minimize design time coupling — reduce the likelihood of changing services in lockstep, which reduces productivity

Design principles:
- Design an architecture that structures the application as a set of two or more independently deployable, loosely coupled, components, a.k.a. services. Each service consists of one or more subdomains. Each subdomain is part of a single service except for shared library subdomains that are used by multiple services. A service is owned by the team (or teams) that owns the (non-library) subdomains.
- An API gateway is typically the application’s entry point. Some system operations will be local to a single service, while others will be distributed across multiple services.
- In order to be independently deployable each service typically has its own source code repository and its own deployment pipeline, which builds, tests and deploys the service.

---

Source: https://microservices.io/post/architecture/2023/02/09/assemblage-architecture-definition-process.html

## Assemblage

### Overview

When designing and evolving an architecture there are numerous decisions that you must make. Three key decisions are:
- Monolithic architecture or the microservice architecture?
- Define a new service or enhance existing services?
- Which collaboration patterns should you use and how across services?

![Logo Description](https://microservices.io/i/posts/assemblage-overview/Defining_Microservice_Architecture_V2.png)

### Step 1

- A subdomain is a team-sized chunk of business functionality, a.k.a. business capability. It consists of the entities/aggregates acted upon by system operations.
- A (microservice) is a collection of subdomains.

Ways to identify subdomains:
- Talking with domain experts to understand the business, and its structure
- Conducting event storming and using pivotal events and swimlanes to identify candidate subdomains
- Mapping business capabilities identified by business architects to subdomains

A few things that it’s important to remember about subdomains:
- They are a model. Subdomains are not like real world islands, for example, that are waiting to be discovered
- They should primarily be aligned to business concepts
- They should be (Team topologies) team-sized
- They should be loosely coupled and highly cohesive
- Each of the entities/aggregates identified in step 1 should be part of a subdomain

The grouping of subdomains is determined by the dark energy and dark matter forces.

![Logo Description](https://microservices.io/i/posts/dark-energy-dark-matter/Dark_Energy_Dark_Matter_overview.png)
![Logo Description](https://microservices.io/i/assemblage/subdomains-operations-and-forces.png)

### Step 3

- Define System Attributes and Operations
- A system operation is an externally invokable behavior implemented by the application. It reads and/or writes one or more business entities, a.k.a. DDD aggregates, such as Customer and Order.
- A system operation is technology independent. However, the actual implementation of the operation is invoked using some combination of technologies including:
  - Synchronously via a HTTP or gRPC request
  - Asynchronously via a message
  - By a scheduler, such as Quartz or Cron

![Logo Description](https://microservices.io/i/posts/assemblage-overview/Defining_System_Operations_Simplified.png)

### Step 4

- The services are a grouping/partitioning of the application’s subdomains that were defined in step 2.
- Each service consists of one or more subdomains. Each subdomain is in one and only one service. (If the service architecture consists of one service, it’s a monolith and if there’s more than one, it’s a microservice architecture.)
- Then define the technical architecture. The technical architecture consists of a set of specific technology choices.
- A microservice architecture has an API Gateway
- The service architecture implements the system operations

A system operation is invoked in one of several ways:
- A HTTP/gRPC/etc request to an API Gateway endpoint, which typically routes the request to a service, which has a service operation endpoint.
- A message published to a message channel that’s consumed by a (entry point) service that has an event handler, which subscribes to the channel
- A scheduling framework that is either external to the services that invokes an operation on an entry point service or embedded with a service, such as Spring’s @Scheduled annotation, that invokes a method on a @Bean

**Local system operations**

![Logo Description](https://microservices.io/i/assemblage/local-operation-collaboration.png)

**Distributed system operations**

![Logo Description](https://microservices.io/i/assemblage/distributed-operation-collaboration.png)
