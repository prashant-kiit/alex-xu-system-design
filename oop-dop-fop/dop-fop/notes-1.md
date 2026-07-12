# Why no protocol or ABC used?

## The core reason

Protocols and ABCs exist to define **behavioral contracts** — "any object of this type must implement these methods." That's fundamentally an OOP concern: polymorphism through interfaces, where different classes provide different implementations of the same method.

DOP explicitly avoids attaching behavior to data at all. The `Order` dataclass has **zero methods** — not even ones defined via an ABC. All behavior lives in free functions (`order_total`, `apply_discount`). There's nothing to "implement" because there's no interface being satisfied — just a shape of data that functions happen to accept.

## What each one *would* imply

```python
# ABC — implies subclasses, inheritance, and a method contract
class Priceable(ABC):
    @abstractmethod
    def total(self) -> float: ...

# Protocol — implies structural typing on OBJECTS with methods
class Priceable(Protocol):
    def total(self) -> float: ...
```

Both assume: "here's a family of objects, each knows how to compute its own total." That's OOP polymorphism (each type defines its own `.total()`). DOP's answer to the same problem is different: **one function, dispatched over the shape of the data**, not the type's own method.

## Where typing *does* still belong in DOP+FP

You don't drop type safety — you just move it from "does this object implement the method" to **"does this data have the right shape."** That's what `TypedDict`, `NamedTuple`, or frozen `dataclass` + `Union` are for:

```python
from typing import Union

@dataclass(frozen=True)
class DigitalOrder:
    items: tuple

@dataclass(frozen=True)
class PhysicalOrder:
    items: tuple
    shipping_fee: float

AnyOrder = Union[DigitalOrder, PhysicalOrder]

def order_total(order: AnyOrder) -> float:
    subtotal = sum(p * q for p, q in order.items)
    if isinstance(order, PhysicalOrder):
        subtotal += order.shipping_fee
    return subtotal
```

This is **pattern matching over data variants**, not interface conformance — closer to how FP languages (Haskell, F#) use algebraic data types + pattern matching than to Python's `Protocol`/`ABC` machinery.

## When you *would* reach for Protocol

If you need to accept a **function itself** as a parameter and want to type-check its signature — e.g., a `Callable` shape — `Protocol` is genuinely useful and still fits FP fine, since it's typing a function, not an object's behavior:

```python
class DiscountFn(Protocol):
    def __call__(self, order: Order) -> Order: ...
```

That's typing a *function*, not giving data a *method* — so it doesn't violate the data/behavior separation.

**Bottom line:** ABC/Protocol model "objects that know how to behave." DOP+FP models "data that functions act on." Mixing in ABCs would just be OOP wearing a DOP costume.