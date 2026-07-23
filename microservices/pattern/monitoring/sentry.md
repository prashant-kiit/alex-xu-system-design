# Sentry.io Guide for Senior Developers

Sentry is more than an error logging tool. Modern engineering teams use it as an **Application Observability Platform** that combines:

* Error Monitoring
* Distributed Tracing
* Performance Monitoring (APM)
* Session Replay
* Profiling
* Logs
* Cron Monitoring
* Uptime Monitoring
* Release Health

Its goal is to answer:

> **What broke? Why did it break? Where did it break? Who is affected? How do I fix it?** ([Sentry][1])

---

# 1. High-Level Architecture

```
               User Request
                     │
                     ▼
              Application
                     │
       ┌─────────────┴─────────────┐
       │                           │
   Sentry SDK                 OpenTelemetry
       │                           │
       └─────────────┬─────────────┘
                     │
             Instrumentation
                     │
                     ▼
            Sentry Ingestion API
                     │
                     ▼
         Processing & Event Grouping
                     │
     ┌───────────────┼────────────────┐
     │               │                │
  Errors         Traces         Performance
     │               │                │
     └───────────────┼────────────────┘
                     ▼
               Sentry Dashboard
```

---

# 2. Major Features

| Feature             | Purpose                    |
| ------------------- | -------------------------- |
| Error Monitoring    | Exceptions, crashes        |
| Performance         | Slow endpoints             |
| Distributed Tracing | End-to-end request flow    |
| Profiling           | CPU hotspots               |
| Session Replay      | Browser replay             |
| Release Health      | Crash-free sessions        |
| Logs                | Correlate logs with traces |
| Cron Monitoring     | Scheduled jobs             |
| Uptime              | Ping HTTP endpoints        |
| Alerts              | Slack, PagerDuty, Email    |

---

# 3. Error Monitoring

This is the feature everyone starts with.

SDK automatically captures:

* Exceptions
* Stack trace
* Source code context
* Environment
* Release
* User
* Request
* Headers
* Breadcrumbs
* Tags
* Custom Context

Example

```python
try:
    process_payment()
except Exception as e:
    sentry_sdk.capture_exception(e)
```

Captured:

```
Error:
    PaymentTimeout

Stack:
    PaymentService
      ↓
    StripeClient
      ↓
    HTTPS call
      ↓
    Timeout
```

---

# 4. Issue Grouping

Sentry doesn't show 10,000 exceptions.

It groups similar exceptions into one Issue.

Instead of

```
Timeout
Timeout
Timeout
Timeout
Timeout
```

Dashboard

```
Issue:
Payment Timeout

Occurrences:
18,442

Users affected:
1,211

First seen:
Yesterday

Last seen:
2 min ago
```

---

# 5. Breadcrumbs

Breadcrumbs show everything that happened before the crash.

```
User Login

↓

Clicked Checkout

↓

POST /payment

↓

Redis lookup

↓

Stripe API

↓

Timeout

↓

Exception
```

Without breadcrumbs:

```
TimeoutException
```

With breadcrumbs:

```
User clicked Pay
↓

Inventory Reserved

↓

Redis OK

↓

Payment Started

↓

Stripe Timeout

↓

Rollback

↓

Exception
```

Huge debugging improvement.

---

# 6. Distributed Tracing

One request may travel through many services.

```
Browser

↓

API Gateway

↓

User Service

↓

Order Service

↓

Payment Service

↓

Inventory Service

↓

Kafka

↓

Email Service
```

Sentry shows the complete request.

```
Trace

HTTP
 │
 ├── User Service
 │      8ms
 │
 ├── Order Service
 │      40ms
 │
 ├── Payment
 │      2100ms
 │
 └── Inventory
        18ms
```

Immediately obvious:

Payment is slow.

---

# 7. Transactions

Every incoming request becomes a Transaction.

Example

```
GET /users/123
```

Inside transaction

```
Transaction

GET /users

├── Authentication
├── Database Query
├── Redis
├── HTTP Request
├── Serialization
└── Response
```

Transaction duration

```
640 ms
```

---

# 8. Spans

A span is one operation inside a transaction.

Example

```
GET /orders
```

Spans

```
HTTP Request
     │
     ├── JWT Validation
     ├── PostgreSQL Query
     ├── Redis GET
     ├── Kafka Publish
     └── HTTP Call
```

Every span has

* Start time
* End time
* Duration
* Parent span
* Trace ID

---

# 9. Trace IDs

Every request gets

```
Trace ID

abc123
```

All services use it.

```
Gateway

Trace ID abc123

↓

Order Service

Trace ID abc123

↓

Payment

Trace ID abc123

↓

Inventory

Trace ID abc123
```

Easy correlation.

---

# 10. Performance Monitoring

Shows

* Slow endpoints
* Slow DB queries
* N+1 queries
* Cache misses
* External API latency
* Long transactions

Example

```
GET /checkout

P50
140ms

P95
820ms

P99
2.9s
```

You instantly know latency distribution.

---

# 11. Flame Graph

```
Request

██████████████████

Database

██████

Stripe API

██████████████

Redis

██

JSON

█
```

Immediately shows

Stripe consumed most time.

---

# 12. Profiling

Tracing tells

> Which request is slow?

Profiling tells

> Which function is slow?

Example

```
Request

↓

processOrder()

↓

calculateDiscount()

↓

sortCoupons()

↓

regexMatch()

↓

CPU Hotspot
```

---

# 13. Session Replay

Browser records user actions.

```
Move Mouse

↓

Click Button

↓

Form Input

↓

Exception
```

Developer watches replay.

Useful for reproducing UI bugs.

---

# 14. Release Tracking

Deploy

```
Release 2.3.1
```

Dashboard

```
Crash Free Sessions

99.91%

↓

99.31%

↓

98.1%
```

Regression detected.

---

# 15. Environment Support

Separate

```
Development

Staging

Production
```

No mixing.

---

# 16. Alerts

Examples

```
Payment errors > 50

↓

Slack Alert
```

```
P95 > 2 sec

↓

PagerDuty
```

```
Crash Free Rate < 99%

↓

Email
```

---

# 17. Tags

Tags allow filtering.

```
country=IN

browser=Chrome

service=payment

tenant=ABC

region=us-east

version=2.3.1
```

Search

```
service:payment
```

---

# 18. Context

Custom data

```python
set_context(
{
    "cart_value":2000,
    "coupon":"NEW50"
})
```

Shown inside exception.

---

# 19. User Context

```
User ID

Email

Organization

Subscription

Tenant
```

Useful for customer support.

---

# 20. Sampling

Sending every trace can be expensive.

Instead

```
100%

↓

10%

↓

1%
```

Example

```python
traces_sample_rate = 0.1
```

Only 10% of transactions are collected for performance monitoring. Errors are billed separately from tracing/performance data, so tuning sampling helps control performance-event volume without disabling error reporting. ([Sentry][2])

---

# 21. SDK Flow

```
Request

↓

SDK Starts Transaction

↓

Create Spans

↓

Capture Exception

↓

Attach Context

↓

Send Event

↓

Dashboard
```

---

# 22. Typical Backend Integration

```
Express

↓

Sentry Middleware

↓

Routes

↓

Database

↓

Redis

↓

Kafka

↓

External API
```

The SDK instruments many frameworks automatically and can be extended with manual spans where needed. ([Sentry][1])

---

# 23. Typical Frontend Integration

```
React

↓

Navigation

↓

API Calls

↓

Redux

↓

Console

↓

Replay

↓

Errors
```

---

# 24. Sentry vs Logs

Logs

```
User Logged In

Cache Miss

Query Executed

```

Sentry

```
Exception

Stack Trace

Trace

Replay

Performance

User

Release

Tags
```

Logs tell **what happened**.

Sentry tells

**why it happened.**

---

# 25. Sentry vs Prometheus

| Prometheus  | Sentry              |
| ----------- | ------------------- |
| Metrics     | Errors              |
| CPU         | Exceptions          |
| Memory      | Stack traces        |
| Grafana     | Trace visualization |
| Time Series | Request tracing     |

Prometheus answers

> Is system healthy?

Sentry answers

> Why is this request failing?

---

# 26. Sentry vs OpenTelemetry

| OpenTelemetry       | Sentry                      |
| ------------------- | --------------------------- |
| Standard            | Platform                    |
| Generates telemetry | Stores & analyzes telemetry |
| Vendor-neutral      | Opinionated UI              |
| Export anywhere     | Built-in dashboard          |

Many teams use **OpenTelemetry for instrumentation** and **Sentry as the backend** for visualization and analysis. ([Sentry][1])

---

# 27. Best Practices

* Instrument every service.
* Use distributed tracing across microservices.
* Set meaningful release versions.
* Add user and tenant context.
* Tag by environment and service.
* Tune `traces_sample_rate` instead of collecting every transaction.
* Create alerts for latency, crash rate, and error spikes.
* Use profiling only where needed to reduce overhead.
* Integrate Sentry with Slack/PagerDuty for faster incident response.

---

# 28. Senior Engineer Interview Questions

* How does Sentry group similar errors?
* What is the difference between a transaction and a span?
* How does distributed tracing work across microservices?
* What is a Trace ID?
* What are breadcrumbs and why are they useful?
* How do you reduce Sentry event volume?
* What is `traces_sample_rate` vs error event sampling?
* How would you instrument Kafka or RabbitMQ consumers?
* How do you correlate Sentry with Prometheus, Grafana, and logs?
* When should you use profiling instead of tracing?
* How would you monitor an asynchronous workflow (e.g., SQS/Kafka/Step Functions)?
* How do releases, environments, and tags improve debugging?

For a senior backend engineer, the most valuable Sentry capabilities are **distributed tracing**, **performance monitoring**, **error grouping**, **profiling**, and **release health**, as these provide end-to-end visibility into production systems and help reduce mean time to resolution (MTTR).

[1]: https://sentrydocs.dev/introduction?utm_source=chatgpt.com "Sentry Documentation - Sentry"
[2]: https://sentry.zendesk.com/hc/en-us/articles/38178374253339-Do-tracing-events-count-against-the-error-quota?utm_source=chatgpt.com "Do tracing events count against the error quota? – Sentry Help Center"
