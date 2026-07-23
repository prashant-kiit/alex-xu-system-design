Per **Chapter 11, "Developing production-ready services,"** Section 11.3 ("Designing observable services") — the book presents six patterns, each with a **developer responsibility** (make your service expose the right information) and an **operations responsibility** (run the infrastructure that collects it).

## 1. Health Check API
**Definition:** A service exposes an endpoint that returns its health, so the deployment infrastructure knows whether to route traffic to it (or restart it).
**Example:** FTGO's Consumer Service takes ~10 seconds to initialize messaging/database adapters — its health endpoint (like Spring Boot Actuator's `GET /actuator/health`) returns `200` only once those connections are actually live, so the deployment infra won't route requests to it prematurely, and can detect and restart it if it later fails silently (e.g., runs out of DB connections).

## 2. Log Aggregation
**Definition:** Services log their activity, and a pipeline ships all instances' logs to a centralized logging server that supports searching and alerting — since with dozens of service instances, "check the log file on the box" no longer works.
**Example:** The **ELK stack** — Elasticsearch (search-oriented NoSQL store as the logging server), Logstash (the aggregation pipeline), Kibana (visualization). FTGO services log to `stdout` (rather than a local file, since containers/serverless often have no persistent filesystem), and the pipeline collects it centrally.

## 3. Distributed Tracing
**Definition:** Each external request gets a unique ID; as it flows across services, the system traces and times each hop (a **trace**, made of nested **spans** — each span an operation with a name, start time, and end time).
**Example:** Debugging a slow `getOrderDetails()` call — a distributed tracing server (e.g., **Zipkin**, originally built by Twitter) shows the API Gateway's call to Order Service as a parent span with a child span, with exact timings for each. An instrumentation library (e.g., **Spring Cloud Sleuth**) auto-injects a `traceId`/`spanId` (via the B3 header standard) so the request ID can also be cross-referenced in aggregated logs. Link: https://www.youtube.com/watch?v=CYz3aA9Lvp0

## 4. Application Metrics
**Definition:** Services maintain metrics — counters, gauges — and expose them to a metrics server, which can alert when values cross a threshold.
**Example:** FTGO's Order Service increments Micrometer counters like `placed_orders`, `approved_orders`, `rejected_orders` whenever those events occur; **Prometheus** *pulls* these from a `GET /actuator/prometheus` endpoint (as opposed to AWS CloudWatch's *push* model), and **Grafana** visualizes them — with an alert configurable if, say, the rate of `placed_orders` drops unexpectedly.

## 5. Exception Tracking
**Definition:** Report exceptions to a dedicated exception-tracking service, rather than just leaving them scattered in log files — because logs are single-line-oriented (bad fit for multi-line stack traces), don't de-duplicate repeat exceptions, and don't track whether an exception has been resolved.
**Example:** Services like **Sentry.io** or **Honeybadger** — Order Service's client library `POST`s a `NullPointerException` (with full stack trace) to the tracking service, which de-duplicates repeated occurrences, alerts developers, and gives a console to manage resolution status.

## 6. Audit Logging
**Definition:** Record each user's actions in a database — who did what, to which business object(s) — to support customer support, compliance, and detecting suspicious behavior.
**Example:** Not detailed with a specific FTGO code sample in this excerpt, but the book's pattern definition (linked to `microservices.io/patterns/observability/audit-logging.html`) frames it as: every user action gets an audit-log entry recording the user's identity, the action performed, and the affected business object — typically stored in its own database table.

**How this connects to what we've covered:** the API Gateway from our earlier discussion is exactly where distributed tracing typically starts (the top-level span), and the domain events pattern we discussed can double as an input to audit logging or metrics — an `OrderCreated` event handler, for instance, could just as easily increment a metric or write an audit entry as update a CQRS view.

*Citation: Chapter 11, Sections 11.3–11.3.6, pp. 365–377.*