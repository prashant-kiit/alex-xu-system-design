# Using nominal typing is violation of DOP and FOP. We should have Structural Tying.
Fair pushback — and it's actually more accurate than what I implied. Let me clarify precisely where you're right and where "violation" overstates it.

## Where you're right

Formal DOP (the discipline, e.g., from *Data-Oriented Programming* by Sharvit) **does prescribe structural typing**, specifically because:

- DOP's core rule: **data should be generic and represented with generic structures** (maps/dicts, not custom nominal types).
- Nominal types (`class Order`) re-introduce a rigid, named "schema" that behaves like a mini-OOP contract — you're back to asking "is this specifically an `Order`?" instead of "does this data have what I need?"
- Real-world DOP systems (Clojure especially) pass around plain maps everywhere, and functions are checked by required keys, not by a declared type name. That's structural by default, and it's central to the philosophy, not incidental.

So the *idealized* DOP+FP approach is more accurately:

```python
from typing import TypedDict
from functools import reduce

# --- DATA: generic structure, structurally typed ---
class OrderShape(TypedDict):
    id: int
    items: tuple
    discount: float

def order_total(order: OrderShape) -> float:
    subtotal = sum(price * qty for price, qty in order["items"])
    return subtotal * (1 - order["discount"])

def apply_discount(order: OrderShape, pct: float) -> OrderShape:
    return {**order, "discount": pct}   # new dict, immutable-by-convention

def add_item(order: OrderShape, price: float, qty: int) -> OrderShape:
    return {**order, "items": order["items"] + ((price, qty),)}

order: OrderShape = {"id": 1, "items": ((100, 2), (50, 1)), "discount": 0.0}
order = add_item(order, 20, 3)
order = apply_discount(order, 0.1)
print(order_total(order))  # 279.0
```

Here **any dict with the right keys works** — no `Invoice` vs `Order` gatekeeping, no `isinstance` checks, true structural compatibility. This matches DOP's spirit much more closely than the `@dataclass` version.

## Where "violation" is too strong

Two caveats worth being precise about:

1. **`dataclass` doesn't break the data/behavior separation** — that principle is satisfied either way (no methods on `Order`). Nominal vs. structural typing is a *separate axis*: it's about how the type checker verifies compatibility, not about whether behavior is coupled to data. So calling it a DOP violation conflates two independent rules of the discipline.

2. **Practical Python trade-off**: `TypedDict`/`Protocol` give you structural flexibility but weaker runtime guarantees — no `frozen=True` immutability enforcement, no `replace()` helper, easier to accidentally pass a malformed dict. `dataclass(frozen=True)` buys real immutability and validation at the cost of nominal rigidity. Many pragmatic "DOP-in-Python" codebases accept this trade intentionally.

## The accurate one-line summary

**Strict/idealized DOP → structural typing (generic maps, matched by shape).**
**Practical Python DOP → often nominal (`dataclass`) as a deliberate compromise for immutability/validation, at the cost of true structural genericity.**

Your correction stands for "textbook DOP." The dataclass version I gave earlier is DOP-*adjacent* and FP-compatible, but not DOP-*pure* by the structural-typing rule.