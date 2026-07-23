# What are Gauge, Counter, Summary, Histogram in Log Metrics?

In monitoring systems like **Prometheus**, **OpenTelemetry**, **Datadog**, or **CloudWatch**, metrics are numerical measurements collected over time. The four most common metric types are:

* **Gauge** → "What is the value right now?"
* **Counter** → "How many times has something happened?"
* **Histogram** → "How are values distributed?"
* **Summary** → "What are the percentiles of observed values?"

Here's a detailed explanation.

---

# 1. Gauge

A **Gauge** represents a value that **can increase or decrease**.

Think of it as taking a snapshot of the current state.

### Examples

* Current CPU usage = 63%
* Memory usage = 2.1 GB
* Active users = 184
* Queue length = 42
* Temperature = 30°C

```
Time →

CPU Usage
70 ──────╮
65 ────╮ │
60 ─╮  │ │
55 ││  │ │
50 │╰──╯ ╰────
```

Notice it goes **up and down**.

### Example

```
active_connections = 10

New user arrives
active_connections = 11

User leaves
active_connections = 10
```

Gauge changed both directions.

---

### Prometheus example

```python
active_users = Gauge(
    "active_users",
    "Current active users"
)

active_users.inc()
active_users.dec()
active_users.set(20)
```

---

## Use Gauge when

* Current queue size
* Number of workers
* Memory usage
* CPU usage
* Active sessions

---

# 2. Counter

A **Counter only increases**.

It **never decreases** except when the application restarts.

It measures **events**.

### Examples

* HTTP requests served
* Login attempts
* Orders placed
* Errors occurred

```
Time →

Requests

100 ────────╮
80 ──────╮  │
60 ───╮  │  │
40 ─╮ │  │  │
20 ││ │  │  │
0──┴┴─┴──┴──┴────
```

Always increasing.

---

Example

```
Server starts

requests_total = 0

Request arrives

requests_total = 1

Another request

requests_total = 2

Another request

requests_total = 3
```

It never goes backwards.

---

### Prometheus

```python
requests = Counter(
    "http_requests_total",
    "Total HTTP requests"
)

requests.inc()
```

---

## Use Counter when

* API requests
* Database queries
* Errors
* Payments processed
* Emails sent

---

# 3. Histogram

A Histogram measures the **distribution of values** by placing observations into predefined **buckets**.

Instead of asking:

> How many requests?

It asks

> How long did requests take?

Suppose request durations are

```
20 ms
40 ms
50 ms
110 ms
200 ms
400 ms
```

Buckets:

```
<=50 ms

<=100 ms

<=200 ms

<=500 ms
```

Result

```
Bucket        Count

<=50            3

<=100           3

<=200           5

<=500           6
```

Notice the buckets are **cumulative**.

---

Histogram also stores

```
Count = 6
Sum = 820 ms
```

Average

```
820 / 6 = 136.7 ms
```

---

### Prometheus

```python
request_latency = Histogram(
    "request_latency_seconds",
    "Request latency"
)

request_latency.observe(0.12)
```

---

## Use Histogram for

* Request latency
* Payload size
* Query duration
* File upload size

---

# 4. Summary

A Summary also records observations, but instead of exposing buckets, it calculates **quantiles (percentiles)**.

Suppose request durations are

```
10
20
25
30
40
50
70
80
100
200
```

Summary might report

```
P50 = 45 ms

P90 = 100 ms

P95 = 180 ms

P99 = 198 ms
```

It directly tells you

> 99% of requests completed within **198 ms**.

---

### Prometheus

```python
latency = Summary(
    "request_latency_seconds",
    "Request latency"
)

latency.observe(0.2)
```

---

## Use Summary when

You mainly care about:

* P50
* P90
* P95
* P99

---

# Histogram vs Summary

| Feature                       | Histogram                 | Summary                |
| ----------------------------- | ------------------------- | ---------------------- |
| Stores buckets                | ✅                         | ❌                      |
| Stores count                  | ✅                         | ✅                      |
| Stores sum                    | ✅                         | ✅                      |
| Calculates percentiles        | Via buckets (server-side) | Directly (client-side) |
| Aggregatable across instances | ✅                         | ❌                      |
| Good for Prometheus           | ✅ Preferred               | Usually not preferred  |
| Configurable buckets          | ✅                         | ❌                      |

---

## Why Histograms are usually preferred

Imagine you have 100 servers.

Each server reports

```
P99 = 400 ms
```

You **cannot average** these P99 values to get the global P99.

Instead, with Histograms, each server reports bucket counts like:

```
<=100ms : 100
<=200ms : 250
<=500ms : 400
```

Prometheus can **sum the buckets from all servers** and compute an accurate global percentile (e.g., using `histogram_quantile()`). This makes Histograms suitable for distributed systems, whereas Summaries cannot be aggregated meaningfully across instances.

---

# Which metric should I choose?

| Situation                        | Metric    |
| -------------------------------- | --------- |
| Current memory usage             | Gauge     |
| CPU utilization                  | Gauge     |
| Active users                     | Gauge     |
| Total HTTP requests              | Counter   |
| Total errors                     | Counter   |
| Login attempts                   | Counter   |
| API latency                      | Histogram |
| DB query latency                 | Histogram |
| Response size                    | Histogram |
| Request P99 (single instance)    | Summary   |
| Request P99 (multiple instances) | Histogram |

---

# Quick analogy

Imagine you're monitoring a highway:

* **Gauge**: "There are **120 cars on the highway right now**."
* **Counter**: "A total of **1.2 million cars have passed** the toll booth today."
* **Histogram**: "Cars are grouped by speed: 30–50 km/h, 50–80 km/h, 80–100 km/h, etc."
* **Summary**: "95% of cars traveled at **90 km/h or below**, and 99% at **110 km/h or below**."

**Rule of thumb:**

* Use a **Gauge** for values that go up and down.
* Use a **Counter** for cumulative event counts.
* Use a **Histogram** for measuring distributions in distributed systems (especially request durations and sizes).
* Use a **Summary** when you only need local percentile estimates and don't need to aggregate them across multiple instances.