# How NamedTuple is not Structurally Typed?

Good addition — but worth flagging upfront: **`NamedTuple` is actually nominal too**, same as `dataclass`. It's useful to include precisely to show that *not all "lightweight" data types are structural* — that's a common misconception.

```python
from typing import TypedDict, NamedTuple
from functools import reduce

# ============================================================
# OPTION 1: TypedDict — STRUCTURAL typing (true DOP)
# ============================================================
class OrderShape(TypedDict):
    id: int
    items: tuple
    discount: float

def order_total_td(order: OrderShape) -> float:
    subtotal = sum(price * qty for price, qty in order["items"])
    return subtotal * (1 - order["discount"])

def apply_discount_td(order: OrderShape, pct: float) -> OrderShape:
    return {**order, "discount": pct}

order_td: OrderShape = {"id": 1, "items": ((100, 2), (50, 1)), "discount": 0.0}
order_td = apply_discount_td(order_td, 0.1)
print(order_total_td(order_td))  # 252.0


# ============================================================
# OPTION 2: NamedTuple — looks lightweight, but NOMINAL typing
# ============================================================
class OrderNT(NamedTuple):
    id: int
    items: tuple
    discount: float = 0.0

def order_total_nt(order: OrderNT) -> float:
    subtotal = sum(price * qty for price, qty in order.items)
    return subtotal * (1 - order.discount)

def apply_discount_nt(order: OrderNT, pct: float) -> OrderNT:
    return order._replace(discount=pct)   # built-in immutable "update"

order_nt = OrderNT(id=1, items=((100, 2), (50, 1)))
order_nt = apply_discount_nt(order_nt, 0.1)
print(order_total_nt(order_nt))  # 252.0

# Proof it's nominal, not structural:
class InvoiceNT(NamedTuple):
    id: int
    items: tuple
    discount: float = 0.0

inv = InvoiceNT(id=2, items=((10, 1),), discount=0.0)
order_total_nt(inv)  # ❌ mypy flags: Argument has type "InvoiceNT", expected "OrderNT"
                      #    even though the shape is IDENTICAL — nominal check wins
```

## Comparison table

| | `TypedDict` | `NamedTuple` | `dataclass` |
|---|---|---|---|
| Typing discipline | **Structural** | Nominal | Nominal |
| Underlying data | `dict` | `tuple` (with named fields) | custom object |
| Immutability | Not enforced (convention only) | **Enforced** (tuples are immutable) | Enforced via `frozen=True` |
| "Update" helper | Manual `{**d, "k": v}` | `._replace()` built-in | `dataclasses.replace()` |
| Two same-shaped types interchangeable? | ✅ Yes | ❌ No | ❌ No |
| Closest fit to strict DOP | ✅ | Only partially | Only partially |

## Why `NamedTuple` still feels "DOP-ish" even though it's nominal

It's positional/tuple-based under the hood, immutable by construction (no `frozen=True` needed), and has zero custom methods — so it satisfies **data/behavior separation** perfectly. It just fails the **structural typing** rule specifically, same as `dataclass`.

## Bottom line

If you want to honor *both* DOP rules strictly (generic data **and** structural typing) → **`TypedDict`**.
If you're willing to trade structural typing for built-in immutability + convenience → **`NamedTuple`** or **`dataclass(frozen=True)`**, both nominal but still behavior-free.


