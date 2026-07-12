# So why cannot we use dataclass and Protocol together to get best of both worlds. Immutabilty from data class and structual typing from Protocol?

Excellent instinct — and yes, **this is actually the best practical pattern**. You're not choosing between nominal and structural; you're using each where it's strongest: `dataclass` for the concrete data (immutability, validation), `Protocol` for the function signatures (structural compatibility).

## How it works

```python
from dataclasses import dataclass, replace
from typing import Protocol

# --- STRUCTURAL CONTRACT: what shape a function needs ---
class HasOrderFields(Protocol):
    items: tuple
    discount: float

# --- CONCRETE DATA: immutable, nominal dataclasses ---
@dataclass(frozen=True)
class Order:
    id: int
    items: tuple
    discount: float = 0.0

@dataclass(frozen=True)
class Invoice:
    id: int
    items: tuple
    discount: float = 0.0
    due_date: str = ""

# --- FUNCTIONS typed against the PROTOCOL, not a specific class ---
def order_total(data: HasOrderFields) -> float:
    subtotal = sum(price * qty for price, qty in data.items)
    return subtotal * (1 - data.discount)

def apply_discount(data: HasOrderFields, pct: float) -> HasOrderFields:
    return replace(data, discount=pct)   # works on ANY frozen dataclass w/ these fields


# --- USAGE ---
order = Order(id=1, items=((100, 2), (50, 1)))
invoice = Invoice(id=2, items=((10, 5),), due_date="2026-08-01")

print(order_total(order))     # ✅ works — Order structurally matches
print(order_total(invoice))   # ✅ works too — Invoice structurally matches, no inheritance needed!
```

## Why this is genuinely "best of both worlds"

| Concern | Solved by |
|---|---|
| Immutability, validation, `replace()` helper | `dataclass(frozen=True)` |
| Function accepts *any* type with the right shape (no `Invoice` vs `Order` gatekeeping) | `Protocol` |
| Data/behavior separation | Neither class has methods — still pure DOP |
| Type safety at function boundaries | `Protocol` checked structurally by mypy/pyright |

`Order` and `Invoice` never declare "I implement `HasOrderFields`" — mypy verifies compatibility purely by field match. That's structural typing, fully preserved, **while still getting real immutability from the concrete dataclasses.**

## The one nuance to be aware of

The **concrete instances** (`Order`, `Invoice`) are still nominal types themselves — `isinstance(order, Invoice)` is `False`, and if you construct with a plain dict or wrong class, you don't get automatic coercion. What becomes structural is only the **function's declared parameter type**. So:

- Constructing/storing data → still nominal (dataclass identity)
- Passing data into functions → now structural (Protocol shape)

That's actually the correct scope for the fix — DOP mainly cares about function boundaries being generic/reusable across shapes, not about how you choose to construct a particular immutable record.

## One-line takeaway

**`dataclass(frozen=True)` for construction and immutability + `Protocol` for function signatures = nominal at the data layer, structural at the behavior layer — which is exactly the boundary DOP cares about.**