# Nominal or Structural Typing? How?

**Nominal. Because the type is identified by its declared class name (**`Order`**), not by the shape of its fields.**

```python
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

def order_total(order: Order) -> float:
    ...

inv = Invoice(id=1, items=((100, 2),), discount=0.1)
order_total(inv)   # ❌ type checker flags this — WRONG TYPE
```

Even though `Invoice` has **the exact same fields** as `Order` — same names, same types — a type checker (mypy/pyright) rejects passing an `Invoice` where an `Order` is expected. That's the signature of **nominal typing**: compatibility is decided by *the name/declaration of the type*, not by whether the shape matches.

## Contrast with structural typing

If we'd used `Protocol` or a `TypedDict`, shape alone would be enough:

```python
from typing import Protocol

class HasItemsAndDiscount(Protocol):
    items: tuple
    discount: float

def order_total(order: HasItemsAndDiscount) -> float:
    ...

order_total(inv)   # ✅ fine — Invoice structurally matches, no relation to Order needed
```

Here `Invoice` doesn't need to inherit from or be declared as `HasItemsAndDiscount` at all — it just needs the right fields. That's **structural typing** — "if it has the right shape, it's compatible," the way Go interfaces or Python's `Protocol`/duck typing work.

## Why the dataclass example is nominal


|                              | `@dataclass` (`Order`)                   | `Protocol`                               |
| ---------------------------- | ---------------------------------------- | ---------------------------------------- |
| Compatibility check          | "Is this literally an `Order` instance?" | "Does this have `items` and `discount`?" |
| Based on                     | The **name/identity** of the class       | The **shape** of the data                |
| Two identical-shaped classes | Treated as different, incompatible types | Treated as interchangeable               |


So even though the `Order` dataclass itself is DOP-friendly (no methods, immutable), the *typing discipline* around it is nominal — because `dataclass` creates a distinct named type, and functions like `order_total(order: Order)` are pinned to that specific name, not to "any object shaped like this."