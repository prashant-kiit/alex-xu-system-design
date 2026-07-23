# What is hexagonal architecture?

This is covered in **Chapter 2, "Decomposition strategies,"** Section **2.1.2** — introduced as an alternative to the traditional layered architecture, and it becomes the standard way the book structures the internals of every individual microservice.

## The problem it solves — drawbacks of layered architecture
The book first describes the familiar three-tier layered architecture (presentation → business logic → persistence) and names three real drawbacks:
- **Single presentation layer** — doesn't reflect that an application is often invoked by more than one kind of client (REST clients, message consumers, etc.)
- **Single persistence layer** — doesn't reflect that an app often talks to more than one external system/database
- **Business logic depends on the persistence layer** — this is backwards from how a well-designed app actually works (the business logic typically *defines* repository interfaces; the persistence layer implements them), and it wrongly implies you can't test business logic without a real database

## Definition
Hexagonal architecture puts the **business logic at the center**, with no dependency at all on what surrounds it. Everything external connects to it through:
- **Ports** — the business logic's own interface definitions (in Java, typically a Java interface) describing how it can be interacted with
- **Adapters** — the concrete implementations that plug into those ports

## The two kinds of ports/adapters
- **Inbound adapters** — handle requests *from* the outside world by invoking an **inbound port**. Examples: a Spring MVC `Controller` implementing REST endpoints, or a message broker client subscribing to messages. Multiple inbound adapters can call the same inbound port.
- **Outbound adapters** — implement an **outbound port**, and are invoked *by* the business logic to reach external systems. Examples: a DAO class implementing a repository interface for database access, or a proxy class invoking a remote service. Outbound adapters can also publish events.

## The key inversion
> The business logic doesn't depend on the adapters. Instead, they depend upon it.

This is the direct fix for layered architecture's backwards dependency — business logic defines the ports (interfaces); adapters (presentation, persistence, messaging) are all plugged in from the outside, depending on the business logic rather than the other way around.

## Benefits the book names
- **Decoupling** — business logic has zero dependency on presentation or data-access logic
- **Testability** — easy to test business logic in isolation, without a real database or web framework
- **Accurately reflects modern applications** — a service can be invoked by multiple different adapters (REST, messaging) and can itself call multiple different external systems, which layered architecture's "one presentation layer, one persistence layer" model can't represent

## How this connects to the microservice architecture itself
This is where it becomes structurally important, not just a nice internal pattern: the book states that **each service in a microservice architecture typically uses a hexagonal architecture internally** for its own logical view. The microservice architecture organizes the *implementation view* (how many deployable components exist); hexagonal architecture organizes the *logical view* (how one component's internals are structured) — they operate at different levels and compose together. FTGO's services (Order Management, Restaurant Management, etc.) are each internally structured this way.

## How this ties to what we've already covered
- **Anti-corruption Layer** (Ch. 13) — the translation logic we discussed sits naturally as part of an inbound or outbound adapter, keeping the legacy model from leaking past the port boundary into clean business logic.
- **Domain Events / Event Sourcing** (Ch. 5–6) — outbound adapters are explicitly called out as the place events get published from.
- **CQRS** (Ch. 7) — a query-side service's event handlers are essentially inbound adapters (subscribing to events) feeding a view-database outbound adapter.

# Give code example

## The book's own example: Order Service's hexagonal architecture (p. 147)

Per Figure 5.1, Order Service is structured as:
- **Business logic (center):** `Order Service business logic`, containing `Order command handlers`
- **Inbound adapters:** the REST API layer handling `POST /orders` and `GET /order/{Id}` — these invoke the business logic
- **Outbound adapters:** a `Database adapter` (invoked by the business logic to persist `Order` data) and a `Domain event publisher adapter` (invoked by the business logic to publish `Order events`)

This matches the general definition exactly: requests flow in through inbound adapters → hit inbound ports on the business logic → business logic calls outbound ports → outbound adapters carry those calls out to the database and message broker. The business logic itself references nothing about REST, SQL, or messaging — it only knows about its own ports.

---

## Additional Context — illustrative code (not from the book)

**1. The business logic defines the ports (interfaces) — no dependency on any adapter**

```java
// ---- INBOUND PORT ----
// The business logic exposes this interface; inbound adapters call it.
public interface OrderService {
    OrderId createOrder(CreateOrderCommand command);
    Order getOrder(OrderId orderId);
}

// ---- OUTBOUND PORTS ----
// The business logic defines these; outbound adapters implement them.
public interface OrderRepository {
    void save(Order order);
    Optional<Order> findById(OrderId orderId);
}

public interface DomainEventPublisher {
    void publish(String aggregateType, Object aggregateId, List<DomainEvent> events);
}
```

**2. The business logic implementation depends only on its own ports**

```java
public class OrderServiceImpl implements OrderService {   // implements the inbound port

    private final OrderRepository orderRepository;         // depends on outbound port (interface)
    private final DomainEventPublisher eventPublisher;      // depends on outbound port (interface)

    public OrderServiceImpl(OrderRepository orderRepository,
                             DomainEventPublisher eventPublisher) {
        this.orderRepository = orderRepository;
        this.eventPublisher = eventPublisher;
    }

    @Override
    public OrderId createOrder(CreateOrderCommand command) {
        Order order = Order.createOrder(command);          // pure business logic, no I/O concerns
        orderRepository.save(order);
        eventPublisher.publish("Order", order.getId(), order.getDomainEvents());
        return order.getId();
    }

    @Override
    public Order getOrder(OrderId orderId) {
        return orderRepository.findById(orderId)
                .orElseThrow(() -> new OrderNotFoundException(orderId));
    }
}
```

Notice: nothing in this class imports Spring MVC, JDBC, or a message broker client. It's fully testable with plain mocks/fakes of `OrderRepository` and `DomainEventPublisher` — no web server or real database required, which is exactly the testability benefit the book calls out.

**3. Inbound adapter — depends on the business logic, not the other way around**

```java
@RestController
public class OrderController {                     // <-- inbound adapter

    private final OrderService orderService;         // calls the inbound port

    public OrderController(OrderService orderService) {
        this.orderService = orderService;
    }

    @PostMapping("/orders")
    public ResponseEntity<OrderId> createOrder(@RequestBody CreateOrderCommand cmd) {
        return ResponseEntity.ok(orderService.createOrder(cmd));
    }

    @GetMapping("/order/{id}")
    public Order getOrder(@PathVariable String id) {
        return orderService.getOrder(new OrderId(id));
    }
}
```

**4. Outbound adapters — implement the outbound ports**

```java
@Repository
public class JpaOrderRepository implements OrderRepository {   // <-- outbound adapter
    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public void save(Order order) {
        entityManager.persist(order);
    }

    @Override
    public Optional<Order> findById(OrderId orderId) {
        return Optional.ofNullable(entityManager.find(Order.class, orderId));
    }
}

@Component
public class KafkaDomainEventPublisher implements DomainEventPublisher {  // <-- outbound adapter
    private final KafkaTemplate<String, DomainEvent> kafkaTemplate;

    public KafkaDomainEventPublisher(KafkaTemplate<String, DomainEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    @Override
    public void publish(String aggregateType, Object aggregateId, List<DomainEvent> events) {
        events.forEach(event -> kafkaTemplate.send(aggregateType + "-events", event));
    }
}
```

## Why this matters — tying back to the dependency inversion
The critical thing this code shows: `OrderController` (inbound adapter) depends on `OrderService` (business logic interface); `JpaOrderRepository` and `KafkaDomainEventPublisher` (outbound adapters) depend on `OrderRepository`/`DomainEventPublisher` (business logic interfaces). **The arrows all point inward, toward the business logic — never outward.** Swap Kafka for RabbitMQ, or JPA for MongoDB, and `OrderServiceImpl` doesn't change at all. That's the "business logic doesn't depend on the adapters; they depend upon it" principle from the book, made concrete.