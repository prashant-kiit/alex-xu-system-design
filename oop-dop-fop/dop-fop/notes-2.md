# But in dataclass approach also we are using constructors to instantiate the data object. That is also OOP. So why not avoid that?

Sharp question — and it exposes a real nuance. The answer: **not all class usage is "OOP."** The concern in DOP isn't "no classes anywhere," it's "no behavior coupled to data." A constructor is not behavior in that sense — it's just a way to *stamp out a validated record*. Let's unpack this.

## Two different things classes give you

| Feature | What it does | Is it "OOP" in the DOP-violating sense? |
|---|---|---|
| Constructor (`__init__`) | Builds a data shape, validates fields | No — it's just a record/struct factory |
| Instance methods (`self.foo()`) | Attaches behavior to the data, hides logic inside the object | **Yes** — this is what DOP avoids |
| Inheritance | Behavior/interface reuse across a type hierarchy | Yes — implies polymorphism, exactly what DOP replaces with functions |

A `@dataclass(frozen=True)` with **no methods** is functionally identical to a tuple, a `NamedTuple`, or a `TypedDict` — it's a labeled bag of fields with a constructor. The constructor is not an "action on data," it's just *how you make the data exist*. Even Haskell — the poster child of pure FP — uses constructors for records (`data Order = Order { items :: [Item] }`) and nobody calls that OOP.

## Proof: you can literally swap it for a non-class

```python
# dataclass version
from dataclasses import dataclass

@dataclass(frozen=True)
class Order:
    id: int
    items: tuple

# dict version — same DOP principle, zero classes
def make_order(id, items):
    return {"id": id, "items": items}

order = make_order(1, ((100, 2),))
```

Both are equally "DOP-compliant." The dataclass is just nicer because you get type checking, `replace()`, immutability enforcement, and IDE autocomplete — all *tooling* benefits, not behavioral ones.

## The actual line DOP draws

It's not "avoid classes." It's:

> **Does this class have logic that depends on its own state (`self`) to decide what to do?**

```python
# ❌ Violates DOP — behavior bound to data, decides based on self
class Order:
    def total(self):
        return sum(p*q for p,q in self.items) * (1 - self.discount)

# ✅ Fine — class is just a labeled container, zero decisions made by it
@dataclass(frozen=True)
class Order:
    items: tuple
    discount: float
```

The second one *could* have been a dict or namedtuple with no loss of principle — it's a class only in the "struct" sense, not the "object" sense.

**Bottom line:** DOP isn't anti-class, it's anti-*method*. A constructor manufactures data; a method makes decisions using data. Only the latter breaks the separation.