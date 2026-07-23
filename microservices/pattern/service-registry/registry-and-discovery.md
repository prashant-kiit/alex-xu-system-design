# What are service discovery and registry?

This is covered in **Chapter 3, "Interprocess communication in a microservice architecture,"** Section **3.2.4, "Using service discovery"** — part of the broader discussion of the **Remote Procedure Invocation (RPI)** communication style.

## Why it's needed
When one service calls another via RPI (e.g., REST), it needs the callee's network location (IP + port). In a modern, cloud-based deployment this is genuinely hard: **service instances have dynamically assigned IPs**, and the set of instances changes constantly due to autoscaling, failures, and upgrades. A static config file of addresses no longer works — you need a **dynamic** mechanism.

## Service Registry
**Definition:** The service registry is *"a database of the network locations of an application's service instances."* It's the core data store service discovery is built around — updated whenever instances start or stop, and queried whenever a client needs to find one.

## Service Discovery
**Definition:** The overall mechanism by which a client finds and connects to an available instance of the service it wants to call, using the registry as its source of truth. The book presents **two main approaches**, each a combination of two sub-patterns:

### Approach 1 — Application-level service discovery
- **Self Registration pattern** — a service instance registers its own network location directly with the service registry (and may supply a health-check URL for the registry to periodically verify it's alive).
- **Client-side Discovery pattern** — the client itself queries the service registry to get a list of available instances, then picks one using a load-balancing algorithm (round-robin, random, etc.) and calls it directly.
- **Example given:** Netflix Eureka (a highly available registry) + the Eureka Java client + Ribbon (an HTTP client integrating with Eureka); Spring Cloud makes this near-automatic for Spring-based services.
- **Benefit:** works across mixed deployment environments (e.g., part Kubernetes, part legacy) since it doesn't depend on any one platform's built-in mechanism.
- **Drawback:** you need a discovery library for every language/framework you use, and you're responsible for operating the registry yourself.

### Approach 2 — Platform-provided service discovery
- **3rd Party Registration pattern** — instead of the service registering itself, a separate component (the **registrar**, typically part of the deployment platform) handles registration on the service's behalf.
- **Server-side Discovery pattern** — instead of the client querying the registry directly, it just makes a request to a **DNS name**, which resolves to a **virtual IP (VIP)**; a platform router then queries the registry and load-balances the request across live instances.
- **Example given:** a client calls `http://order-service/...`, which resolves via DNS to a VIP; the platform's router queries the registry and distributes the request across the three live `order-service` instances.

## How this connects to what we've covered
- Service discovery is the missing piece underneath both **API Composition** and the **API Gateway** — when the gateway or composer calls Order Service, Kitchen Service, etc., it's service discovery that resolves those names to actual live instances.
- The **Self Registration pattern**'s health-check URL is exactly the **Health Check API** pattern from Chapter 11.
- Chapter 12 (deployment) is flagged as covering how platforms like Kubernetes implement server-side discovery natively — connecting forward to the **Service Mesh** discussion we just covered, which the book notes can also take over service discovery duties from the microservice chassis.