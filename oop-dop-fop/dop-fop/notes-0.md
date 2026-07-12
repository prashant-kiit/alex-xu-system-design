# Data-Oriented Programming (DOP) + Functional Programming (FP)

**Core idea:** DOP says *separate data from behavior* — data is just plain, immutable structures (dicts, tuples, lists), not wrapped in custom classes. FP provides the *pure functions* that operate on that data. Together: **immutable data + stateless functions that transform it**, instead of objects that bundle data and methods.

## Example: Order processing

```python
from dataclasses import dataclass, replace
from functools import reduce

# --- DATA (plain, immutable) ---
@dataclass(frozen=True)
class Order:
    id: int
    items: tuple          # (price, qty) pairs
    discount: float = 0.0

# --- FUNCTIONS (pure, no side effects) ---
def order_total(order: Order) -> float:
    subtotal = sum(price * qty for price, qty in order.items)
    return subtotal * (1 - order.discount)

def apply_discount(order: Order, pct: float) -> Order:
    return replace(order, discount=pct)   # returns NEW order, doesn't mutate

def add_item(order: Order, price: float, qty: int) -> Order:
    return replace(order, items=order.items + ((price, qty),))

# --- USAGE ---
order = Order(id=1, items=((100, 2), (50, 1)))

order = add_item(order, price=20, qty=3)
order = apply_discount(order, 0.1)

print(order_total(order))   # 279.0
print(order)                 # original untouched by earlier steps; each step returned a new value
```

## Why this combo works

| DOP contributes | FP contributes |
|---|---|
| Data is just data — no hidden methods, easy to serialize/inspect/log | Functions are pure — same input, same output, easy to test |
| Immutability — no `order.discount = 0.1` mutating shared state | Composability — chain small functions (`add_item` → `apply_discount` → `order_total`) |
| Generic structures (dict/tuple/dataclass) instead of deep class hierarchies | No side effects — safe to run in any order, parallelize, cache |

Contrast with OOP, where you might write `order.apply_discount(0.1)` — a method that mutates `self` and couples the data to its behavior. DOP+FP keeps data "dumb" and pushes all logic into standalone functions that never touch the original.