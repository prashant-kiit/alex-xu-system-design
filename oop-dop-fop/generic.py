"""
Generics = write one function/class that works with ANY type,
while still letting type checkers (mypy/pyright) catch mismatches.
Without generics you'd use `Any`, which turns off type checking entirely.
"""

from typing import TypeVar, Generic, Protocol

# T is a "type variable" — a placeholder for whatever type gets used at call time.
T = TypeVar("T")


# ---- Generic function ----
def first_item(items: list[T]) -> T:
    # Works for list[int] -> int, list[str] -> str, etc.
    # The point: input type and return type are LINKED, not independent `Any`s.
    return items[0]


first_item([1, 2, 3])        # T = int, checker knows result is int
first_item(["a", "b"])       # T = str, checker knows result is str


# ---- Generic class ----
class Box(Generic[T]):
    """A container that holds exactly one item of some type T."""

    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item


int_box: Box[int] = Box[int](42)
str_box: Box[str] = Box("hello")

# int_box.get() -> checker infers int. Passing int_box to something expecting
# Box[str] would be a type error, even though both are just "Box" at runtime.


# ---- Constraining T (bound) ----
# Sometimes "any type" is too loose — you want "any type, but it must support X".
class Comparable(Protocol):
    def __lt__(self, other: object) -> bool: ...


C = TypeVar("C", bound=Comparable)


def smallest(items: list[C]) -> C:
    # Only accepts types that implement `<`, so items[i] < items[j] is guaranteed safe.
    result = items[0]
    for item in items[1:]:
        if item < result:
            result = item
    return result


# ---- Modern shorthand (Python 3.12+) ----
# Same as the TypeVar version above, just less boilerplate.
def first_item_new[T](items: list[T]) -> T:
    return items[0]


class Box_new[T]:
    def __init__(self, item: T) -> None:
        self.item = item
