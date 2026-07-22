# Monolith vs SOA vs Macroservices vs Microservices

| Aspect | Monolith | SOA (Service-Oriented Architecture) | Macroservices | Microservices |
|--------|----------|--------------------------------------|---------------|---------------|
| **Definition** | Entire application is built and deployed as a single unit. | Architectural style where reusable business services communicate over a network. | Application split into a few large business services. | Application split into many small, independently deployable services. |
| **Architecture Type** | Architecture | Architecture | Service granularity | Architecture |
| **Service Size** | Single application | Medium to large services | Large services | Small services |
| **Deployment Unit** | One deployment | Multiple service deployments | Few deployments | Many independent deployments |
| **Codebase** | Single codebase | Multiple codebases | Multiple codebases | Multiple codebases |
| **Database** | Single shared database | Often shared database | Usually shared within a service | Database per service |
| **Communication** | In-process method calls | ESB, SOAP, REST, Messaging | REST/gRPC/Messaging | REST, gRPC, Messaging |
| **Coupling** | Tight | Loosely coupled | Moderately coupled | Very loosely coupled |
| **Scalability** | Scale entire application | Scale services | Scale large services | Scale individual services |
| **Technology Stack** | Usually one stack | Usually standardized | Usually standardized | Polyglot (different stacks allowed) |
| **Fault Isolation** | Poor | Moderate | Good | Excellent |
| **Deployment Speed** | Slow | Moderate | Fast | Very fast |
| **Operational Complexity** | Low | Medium | Medium | High |
| **Team Ownership** | One or few teams | Multiple teams | One team per large service | One team per service |
| **Best For** | Small applications | Enterprise integration | Medium-sized products | Large cloud-native applications |

---

# 1. Monolith

Everything is part of one application.

```text
Ecommerce Application

├── Users
├── Authentication
├── Cart
├── Orders
├── Inventory
├── Payments
└── Shipping

One Codebase
One Deployment
One Database
```

### Characteristics

- Single codebase
- Single deployment
- Shared database
- Easy to develop initially
- Difficult to scale individual modules
- Entire application must be redeployed for every change

---

# 2. SOA (Service-Oriented Architecture)

Application is built from reusable enterprise services.

```text
          CRM
            │
            ▼
    Customer Service
      /           \
 ERP               Mobile App

          │
          ▼
    Payment Service

          │
          ▼
 Notification Service
```

### Characteristics

- Enterprise-wide architecture
- Business capability reuse
- Often uses an Enterprise Service Bus (ESB)
- Services are relatively coarse-grained
- Shared databases are common
- Focuses on integrating multiple applications

---

# 3. Macroservices

Application is divided into a few large services.

```text
Commerce Service
├── Cart
├── Orders
├── Inventory
├── Pricing

Identity Service
├── Users
├── Authentication

Payment Service

Notification Service
```

### Characteristics

- Large business domains
- Fewer services (typically 5–20)
- Easier to maintain than hundreds of microservices
- Less network communication
- Good balance between monolith and microservices

---

# 4. Microservices

Application is divided into many small services.

```text
User Service

Auth Service

Cart Service

Order Service

Inventory Service

Pricing Service

Payment Service

Shipping Service

Email Service

Recommendation Service
```

### Characteristics

- Small business capability
- Independent deployment
- Independent database
- Independent scaling
- Independent ownership
- High operational complexity

---

# Evolution

```text
Monolith
    │
    ▼
Macroservices
    │
    ▼
Microservices

SOA is a separate architectural style that focuses on enterprise-wide reusable services and can coexist with either coarse-grained (macroservice-like) or finer-grained services.
```

---

# Quick Comparison

| Feature | Monolith | SOA | Macroservices | Microservices |
|---------|----------|-----|---------------|---------------|
| Number of Services | 1 | 10–100 | 5–20 | 50–1000+ |
| Deployment | Single | Multiple | Multiple | Independent |
| Database | One | Often shared | Shared per macroservice | One per service |
| Communication | Function calls | ESB/SOAP/REST | REST/gRPC | REST/gRPC/Messaging |
| Independent Scaling | ❌ | ✅ | ✅ | ✅ |
| Independent Deployment | ❌ | Partial | ✅ | ✅ |
| Team Autonomy | Low | Medium | High | Very High |
| Operational Complexity | Low | Medium | Medium | High |

---

# Which One Should You Choose?

| Scenario | Recommended Architecture |
|----------|--------------------------|
| Small startup or MVP | Monolith |
| Medium-sized product with a small engineering team | Macroservices |
| Large cloud-native application with many teams | Microservices |
| Enterprise integration across multiple applications and legacy systems | SOA |