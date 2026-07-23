
## Service Discovery — in detail

**What it is:** the *mechanism* — everything around using that registry to actually route a request from a client to a live instance. The book splits this into two full approaches, each pairing a **registration** pattern with a **lookup** pattern:

### Approach 1: Self Registration + Client-side Discovery
- **Self Registration** — the instance itself calls the registry's registration API on startup (as shown above).
- **Client-side Discovery** — the *calling* service queries the registry directly, gets back a list of instances, and picks one itself (e.g., round-robin) before making the call.

**Additional Context — illustrative code:**
```java
// Client-side discovery: the caller queries the registry and load-balances itself.

@Autowired
private DiscoveryClient discoveryClient;   // Spring Cloud abstraction over Eureka

public Order getOrder(String orderId) {
    List<ServiceInstance> instances = discoveryClient.getInstances("order-service");
    if (instances.isEmpty()) {
        throw new ServiceUnavailableException("order-service");
    }
    // simple round-robin / random pick — the client owns this logic
    ServiceInstance chosen = instances.get(new Random().nextInt(instances.size()));
    String url = chosen.getUri() + "/orders/" + orderId;
    return restTemplate.getForObject(url, Order.class);
}

// In practice, Spring Cloud's @LoadBalanced RestTemplate hides this entirely:
@LoadBalanced
@Bean
public RestTemplate restTemplate() {
    return new RestTemplate();
}
// ...then callers just do:
restTemplate.getForObject("http://order-service/orders/" + orderId, Order.class);
// "order-service" here isn't a real hostname — Ribbon/Eureka resolve it at call time.
```

### Approach 2: 3rd Party Registration + Server-side Discovery
- **3rd Party Registration** — a separate **registrar** component (part of the deployment platform, e.g., Kubernetes) watches instances start/stop and registers/deregisters them — the service code does nothing itself.
- **Server-side Discovery** — the client doesn't query the registry at all; it just calls a fixed **DNS name**, which resolves to a virtual IP; a platform router intercepts, queries the registry, and load-balances behind the scenes.

**Additional Context — illustrative code** (this is the simpler side, precisely *because* the service and client don't need discovery-aware code at all):
```java
// Client code — no discovery library, no registry query. Just a normal HTTP call
// to a stable DNS name; the platform (e.g., Kubernetes Service) handles the rest.

public Order getOrder(String orderId) {
    String url = "http://order-service/orders/" + orderId;  // Kubernetes Service DNS name
    return restTemplate.getForObject(url, Order.class);
}
```
```yaml
# Kubernetes Service definition — this IS the "registrar" + "server-side discovery" router.
# The service instance's Deployment doesn't register itself; Kubernetes does it automatically.
apiVersion: v1
kind: Service
metadata:
  name: order-service        # <-- becomes the DNS name other services call
spec:
  selector:
    app: order-service        # <-- Kubernetes watches Pods matching this label
  ports:
    - port: 80
      targetPort: 8080
```

---

## Key difference the code above illustrates
- **Client-side discovery** puts the registry-querying and load-balancing logic **inside every service's code** (via a library like Ribbon/Eureka client) — more control, but a library dependency per language.
- **Server-side discovery** keeps services completely unaware of discovery — they just call a DNS name — because the platform (registrar + router) does all the work externally. This is why the book ultimately favors platform-provided discovery when available: **less code, less to maintain, works the same regardless of language.**