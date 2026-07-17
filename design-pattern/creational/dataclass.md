A **data class** is a Python class designed primarily to **store data**. It automatically generates common methods like `__init__()`, `__repr__()`, `__eq__()`, and others, so you don't have to write them yourself.

The `@dataclass` decorator (introduced in Python 3.7) is from the `dataclasses` module.

Your example:

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Pizza:
    size: str = "medium"
    crust: str = "regular"
    cheese: str = "mozzarella"
    sauce: str = "tomato"
    toppings: List[str] = field(default_factory=list)
```

### Without `@dataclass`

You would have to write:

```python
class Pizza:
    def __init__(self, size="medium", crust="regular",
                 cheese="mozzarella", sauce="tomato",
                 toppings=None):
        self.size = size
        self.crust = crust
        self.cheese = cheese
        self.sauce = sauce
        self.toppings = toppings if toppings is not None else []

    def __repr__(self):
        return (
            f"Pizza(size={self.size!r}, crust={self.crust!r}, "
            f"cheese={self.cheese!r}, sauce={self.sauce!r}, "
            f"toppings={self.toppings!r})"
        )

    def __eq__(self, other):
        if not isinstance(other, Pizza):
            return False
        return (
            self.size == other.size and
            self.crust == other.crust and
            self.cheese == other.cheese and
            self.sauce == other.sauce and
            self.toppings == other.toppings
        )
```

The dataclass generates these methods automatically.

---

## What gets generated?

Given:

```python
@dataclass
class Pizza:
    size: str = "medium"
    crust: str = "regular"
```

Python generates approximately:

```python
class Pizza:
    def __init__(self, size="medium", crust="regular"):
        self.size = size
        self.crust = crust

    def __repr__(self):
        ...

    def __eq__(self, other):
        ...
```

---

## Example

```python
p1 = Pizza()
p2 = Pizza(size="large", toppings=["pepperoni"])

print(p1)
print(p2)
```

Output:

```
Pizza(size='medium', crust='regular', cheese='mozzarella',
      sauce='tomato', toppings=[])

Pizza(size='large', crust='regular', cheese='mozzarella',
      sauce='tomato', toppings=['pepperoni'])
```

Notice how `__repr__()` was automatically created.

---

## Equality

```python
p1 = Pizza()
p2 = Pizza()

print(p1 == p2)
```

Output:

```
True
```

Because dataclasses compare all fields by default.

---

## Why `field(default_factory=list)`?

Don't do this:

```python
@dataclass
class Pizza:
    toppings: List[str] = []      # ❌
```

All `Pizza` objects would share the **same list**.

Instead:

```python
@dataclass
class Pizza:
    toppings: List[str] = field(default_factory=list)
```

Each object gets its **own** list.

```python
p1 = Pizza()
p2 = Pizza()

p1.toppings.append("mushroom")

print(p1.toppings)
# ['mushroom']

print(p2.toppings)
# []
```

---

## Other useful options

```python
@dataclass(frozen=True)
```

Makes instances immutable.

```python
@dataclass(order=True)
```

Generates comparison methods (`<`, `<=`, `>`, `>=`).

```python
@dataclass(slots=True)
```

Uses `__slots__` to reduce memory usage and speed up attribute access.

---

## Summary

A `@dataclass` automatically generates:

| Method                            | Purpose                                           |
| --------------------------------- | ------------------------------------------------- |
| `__init__`                        | Constructor                                       |
| `__repr__`                        | Printable representation                          |
| `__eq__`                          | Equality comparison                               |
| `__hash__`                        | Hashing (in some cases, e.g., frozen dataclasses) |
| Ordering methods (`__lt__`, etc.) | If `order=True`                                   |

**In short:** Use a dataclass when your class is mainly a **container for data**. It eliminates boilerplate code while keeping your class readable and maintainable.
