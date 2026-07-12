# Industry-Standard, Production-Ready Data-Oriented Programming (DOP) in Python

## 1. Why DOP in Production

Traditional OOP couples data with behavior via methods, which makes testing, serialization, and reasoning about state harder as systems grow. Production DOP separates **immutable data** from **pure functions**, giving you:

- Predictable state (no hidden mutation bugs)
- Easy testing (pure functions need no mocks)
- Easy serialization (data structures map cleanly to JSON/DB rows)
- Safe concurrency (immutable data can be shared across threads without locks)

This is the same philosophy behind Redux (JS), Clojure's persistent data structures, and Rust's ownership model — Python's ecosystem has converged on a few standard tools to achieve it.

---

## 2. Core Building Block #1: Frozen Dataclasses

The industry default for representing structured domain data with many fields is `@dataclass(frozen=True, slots=True)`.

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True, slots=True)
class Order:
    id: str
    items: tuple[str, ...]   # tuple, not list -> deep immutability
    discount: float
```

**Why each part matters:**
- `frozen=True` → raises `FrozenInstanceError` on any attempted mutation (`order.discount = 0.5` fails). This *enforces* the DOP principle instead of relying on convention.
- `slots=True` → removes the per-instance `__dict__`, cutting memory use and speeding up attribute access — important at scale (e.g., millions of order objects in a pipeline).
- `tuple[str, ...]` instead of `list[str]` → prevents the classic "frozen dataclass, mutable field" trap, where someone does `order.items.append(x)` and silently mutates supposedly-immutable data.

**Updating data** (never mutate — always produce a new object):

```python
def apply_discount(order: Order, pct: float) -> Order:
    return replace(order, discount=pct)

new_order = apply_discount(order, 0.2)
# original `order` is untouched
```

---

## 3. Core Building Block #2: `typing.NamedTuple`

For **small, flat, positional records** — points, coordinates, RGB tuples, lightweight events — `NamedTuple` is the industry-preferred alternative to a dataclass. It's immutable *by construction* (no need to even specify `frozen=True`), lighter weight than a dataclass, and doubles as a real tuple.

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

class PriceTick(NamedTuple):
    symbol: str
    price: float
    timestamp: float
```

**Why teams reach for it in production:**
- **Immutable natively** — no decorator needed, can't be misconfigured (unlike forgetting `frozen=True` on a dataclass).
- **Tuple-compatible** — unpacks (`x, y = point`), indexes (`point[0]`), hashable by default → safe to use as dict keys or in sets, which frozen dataclasses only get if you explicitly enable it.
- **Cheaper than dataclasses** — no `__dict__` overhead even without `slots`, since tuples are already compact; commonly used in **hot paths** (e.g., streaming market data ticks, high-frequency event pipelines) where every allocation counts.
- **Drop-in for pandas/numpy interop** — `df.itertuples()` returns NamedTuple-like rows; many data pipelines already speak this format natively.

```python
def translate(p: Point, dx: float, dy: float) -> Point:
    return p._replace(x=p.x + dx, y=p.y + dy)   # same "produce new data" pattern
```

**When to choose NamedTuple vs frozen dataclass in production:**

| Use `NamedTuple` when | Use `frozen` dataclass when |
|---|---|
| Data is small (2–5 fields), flat, positional | Data has many fields or nested structures |
| You need unpacking / indexing / hashability out of the box | You need computed properties, custom `__post_init__` validation |
| Hot-path / high-frequency objects (ticks, events, coordinates) | Rich domain models (Order, User, Invoice) |
| No need for inheritance or mutable defaults | Long-term evolving schemas with more fields over time |

Many production codebases use **both**: `NamedTuple` for lightweight internal events/records flowing through pipelines, `frozen` dataclasses for the main domain model.

---

## 4. Validation at the Boundary: Pydantic

Dataclasses and NamedTuples assume the data is already correct — they don't validate. In production, data enters your system from untrusted places — API requests, config files, database rows — and needs **validation**, not just typing. The industry standard here is **Pydantic v2**.

```python
from pydantic import BaseModel, ConfigDict

class OrderIn(BaseModel):
    model_config = ConfigDict(frozen=True)  # immutable after creation
    id: str
    items: list[str]
    discount: float = 0.0
```

- Pydantic parses and validates incoming JSON/dict data (type coercion, range checks, custom validators), raising clear errors on bad input.
- `frozen=True` in `model_config` makes Pydantic models immutable too, keeping them consistent with your internal dataclasses/NamedTuples.
- Convert to your internal frozen dataclass once validated:

```python
def to_domain(order_in: OrderIn) -> Order:
    return Order(id=order_in.id, items=tuple(order_in.items), discount=order_in.discount)
```

**Rule of thumb:** *Pydantic at the edges (API/DB/file I/O), frozen dataclasses / NamedTuples in the core business logic.* This avoids paying Pydantic's validation overhead repeatedly inside hot loops, while still getting strict guarantees where the data is riskiest.

---

## 5. Pure Functions as Behavior

Instead of methods on classes, group transformation functions in modules by domain concept.

```python
# orders.py
def total(order: Order, prices: dict[str, float]) -> float:
    return sum(prices[item] for item in order.items) * (1 - order.discount)

def validate(order: Order) -> bool:
    return 0 <= order.discount <= 1 and len(order.items) > 0
```

Each function: takes data in, returns new data or a value out, has no side effects. This makes unit testing trivial:

```python
def test_apply_discount():
    order = Order(id="1", items=("book",), discount=0.1)
    result = apply_discount(order, 0.5)
    assert result.discount == 0.5
    assert order.discount == 0.1   # original unaffected
```

No mocking, no setup/teardown of object state — just input/output assertions.

---

## 6. Deep Immutability

Shallow immutability (top-level `frozen=True`, or NamedTuple's native immutability) isn't enough if nested fields are mutable containers. Standard practice:

| Instead of | Use |
|---|---|
| `list` | `tuple` |
| `set` | `frozenset` |
| nested mutable dataclass | nested `frozen=True` dataclass or `NamedTuple` |
| dict (if truly needed) | `types.MappingProxyType` or restructure as frozen dataclass |

```python
@dataclass(frozen=True, slots=True)
class Cart:
    orders: tuple[Order, ...]        # tuple of frozen Order objects
    checkpoints: tuple[Point, ...]   # tuple of NamedTuples — fully immutable tree
```

---

## 7. Serialization Boundary

Keep the *internal* pipeline strongly typed (dataclasses/NamedTuples), and only convert to dict/JSON at the edges — logging, API responses, DB writes.

```python
from dataclasses import asdict
import orjson  # fast JSON library, standard in production for perf

payload = orjson.dumps(asdict(order))          # dataclass -> dict -> JSON
tick_payload = orjson.dumps(tick._asdict())     # NamedTuple -> dict -> JSON
```

`orjson` is the industry-preferred JSON library for performance-sensitive services (faster than stdlib `json`, native datetime/dataclass support via helpers). `NamedTuple._asdict()` is the built-in equivalent of `asdict()` for tuples.

---

## 8. Production Checklist

| Concern | Standard Tool / Practice |
|---|---|
| Static type safety | `mypy --strict` or `pyright` in CI |
| Runtime validation | Pydantic v2 at API/DB/file boundaries |
| Immutability enforcement | `frozen=True` + `slots=True` dataclasses; `NamedTuple` for lightweight records |
| Nested mutation bugs | Tuples/frozensets instead of lists/sets internally |
| Performance / hot paths | `NamedTuple` for high-frequency small records; `slots=True` on dataclasses |
| Fast serialization | `orjson`, `NamedTuple._asdict()`, `dataclasses.asdict()` |
| Testing | Pure functions → simple input/output unit tests |
| Config/schema evolution | Pydantic's versioned models, or `attrs` for legacy codebases |

---

## 9. Summary Flow

```
Untrusted input (API/DB/file)
        ↓  [Pydantic: validate + parse]
Validated Pydantic model
        ↓  [convert once]
Frozen dataclass (rich domain data) / NamedTuple (lightweight records)
        ↓  [pure functions: transform → new immutable data]
Frozen dataclass / NamedTuple (result)
        ↓  [asdict / _asdict / model_dump + orjson]
Serialized output (API response / DB write)
```

This pipeline — **validate at the edge, stay immutable in the core (dataclasses for rich models, NamedTuples for lightweight/hot-path records), transform via pure functions, serialize at the exit** — is the pattern used across most production Python services doing DOP today (common in FastAPI backends, data pipelines, and event-driven systems).