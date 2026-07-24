# Caching Patterns (Cheat Sheet)

| Pattern                        | Definition                                                                                     | Best For                                    |
| ------------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------- |
| **Cache-Aside (Lazy Loading)** | Application checks cache first. On cache miss, fetches from DB, stores in cache, returns data. | Read-heavy workloads                        |
| **Read-Through**               | Application reads only from cache. Cache automatically loads data from DB on a miss.           | Simplifies application code                 |
| **Write-Through**              | Every write goes to cache, and cache synchronously writes to DB.                               | Strong consistency                          |
| **Write-Behind (Write-Back)**  | Application writes to cache immediately. Cache asynchronously persists to DB.                  | High write throughput                       |
| **Write-Around**               | Writes bypass cache and go directly to DB. Cache is populated only on future reads.            | Write-heavy workloads with infrequent reads |
| **Refresh-Ahead**              | Cache proactively refreshes frequently accessed entries before TTL expires.                    | Low-latency systems                         |
| **Cache-Through**              | Cache acts as the single interface for both reads and writes, internally handling DB access.   | Full cache abstraction                      |

---

## 1. Cache-Aside (Lazy Loading)

```python
def get_user(id):
    user = cache.get(id)
    if user is None:
        user = db.get(id)
        cache.set(id, user)
    return user
```

**Flow**

```
App -> Cache -> (Miss) -> DB -> Cache -> App
```

---

## 2. Read-Through

```python
# Cache handles DB lookup internally
user = cache.get(id)
```

Internal behavior:

```python
def cache.get(id):
    if id not in cache:
        cache[id] = db.get(id)
    return cache[id]
```

**Flow**

```
App -> Cache -> DB (if miss)
```

---

## 3. Write-Through

```python
def save_user(user):
    cache.set(user.id, user)
    db.save(user)
```

**Flow**

```
App -> Cache -> DB
```

---

## 4. Write-Behind (Write-Back)

```python
def save_user(user):
    cache.set(user.id, user)
    queue.enqueue(lambda: db.save(user))
```

**Flow**

```
App -> Cache
           ↓
      Async DB Write
```

---

## 5. Write-Around

```python
def save_user(user):
    db.save(user)

def get_user(id):
    user = cache.get(id)
    if user is None:
        user = db.get(id)
        cache.set(id, user)
    return user
```

**Flow**

```
Write: App -> DB

Read: App -> Cache -> DB (if miss)
```

---

## 6. Refresh-Ahead

```python
def refresh():
    if cache.ttl(id) < 60:
        cache.set(id, db.get(id))
```

**Flow**

```
TTL Near Expiry
      ↓
Refresh from DB
      ↓
Cache Updated
```

---

## 7. Cache-Through

```python
cache.write(user)   # cache persists to DB
user = cache.read(id)
```

Internal behavior:

```python
def write(user):
    cache[user.id] = user
    db.save(user)

def read(id):
    if id not in cache:
        cache[id] = db.get(id)
    return cache[id]
```

**Flow**

```
Reads:  App -> Cache -> DB
Writes: App -> Cache -> DB
```

---

# Quick Comparison

| Pattern       | Read Path        | Write Path                           | DB Access                     |
| ------------- | ---------------- | ------------------------------------ | ----------------------------- |
| Cache-Aside   | App → Cache → DB | App → DB (+ invalidate/update cache) | App                           |
| Read-Through  | App → Cache      | App → DB                             | Cache (reads)                 |
| Write-Through | Cache            | App → Cache → DB                     | Cache                         |
| Write-Behind  | Cache            | App → Cache → Async DB               | Cache                         |
| Write-Around  | Cache            | App → DB                             | App                           |
| Refresh-Ahead | Cache            | Any                                  | Cache refreshes automatically |
| Cache-Through | Cache            | Cache                                | Cache                         |

### Rule of thumb

* **Cache-Aside** → Most common pattern (Redis + application).
* **Read-Through** → Cleaner read logic managed by the cache.
* **Write-Through** → Consistency is more important than write latency.
* **Write-Behind** → Maximum write performance; tolerate delayed persistence.
* **Write-Around** → Avoid caching data that is rarely read.
* **Refresh-Ahead** → Prevent cache misses for hot keys.
* **Cache-Through** → Cache fully abstracts storage for both reads and writes.