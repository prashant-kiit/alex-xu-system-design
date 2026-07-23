## Service Registry — in detail

**What it is (book's definition, p. 81):** *"a database of the network locations of an application's service instances."*

**What it actually stores and does:**
- A mapping like: service name (`order-service`) → list of live instance addresses (`10.232.23.1`, `10.232.23.2`, `10.232.23.3`)
- It's kept **up to date dynamically** — entries are added when instances start, removed when they stop or fail
- It typically supports a **heartbeat mechanism**: instances must periodically "check in," or their registration expires (protects against stale entries if an instance crashes without deregistering)
- It can also store a **health check URL** per instance, which the registry itself invokes periodically to confirm the instance is actually able to serve traffic (tying back to the Health Check API pattern)

**Named implementations the book gives:** Netflix **Eureka** (a highly available registry) for application-level discovery; for platform-provided discovery, the registry role is played by the deployment platform itself (e.g., Kubernetes' internal registry, queried via DNS).

**Additional Context — illustrative code** (not from the book) showing what registering/querying a registry like Eureka conceptually looks like with Spring Cloud:

```java
// A service instance registers itself simply by being a Eureka client —
// Spring Cloud automates the registration call.

@SpringBootApplication
@EnableEurekaClient   // <-- triggers self-registration with the Eureka server on startup
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}
```
```yaml
# application.yml
spring:
  application:
    name: order-service   # <-- this becomes the registry key other services look up

eureka:
  client:
    service-url:
      defaultZone: http://eureka-server:8761/eureka/
  instance:
    lease-renewal-interval-in-seconds: 10   # heartbeat interval
```