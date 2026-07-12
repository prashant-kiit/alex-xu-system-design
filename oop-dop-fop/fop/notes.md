# Functional Programming in Python — Quick Tutorial

Python isn't a purely functional language, but it supports FP concepts well: immutability, pure functions, and treating functions as first-class values.

## 1. Pure Functions

A pure function always returns the same output for the same input and has no side effects (no modifying external state).

```python
# Impure - depends on/modifies external state
total = 0
def add_impure(x):
    global total
    total += x
    return total

# Pure - no side effects
def add_pure(x, y):
    return x + y
```

## 2. First-Class Functions

Functions can be passed around like any other value.

```python
def square(x):
    return x * x

def apply(func, value):
    return func(value)

print(apply(square, 5))  # 25
```

## 3. Lambda Expressions

Anonymous, one-line functions.

```python
square = lambda x: x * x
add = lambda x, y: x + y
```

## 4. `map()`, `filter()`, `reduce()`

Core FP tools for transforming data without loops.

```python
from functools import reduce

nums = [1, 2, 3, 4, 5]

# map: apply a function to every item
squares = list(map(lambda x: x * x, nums))          # [1, 4, 9, 16, 25]

# filter: keep items matching a condition
evens = list(filter(lambda x: x % 2 == 0, nums))     # [2, 4]

# reduce: combine items into a single value
total = reduce(lambda acc, x: acc + x, nums)         # 15
```

## 5. List/Generator Comprehensions (Pythonic alternative)

Often preferred over `map`/`filter` for readability.

```python
squares = [x * x for x in nums]
evens = [x for x in nums if x % 2 == 0]
```

## 6. Immutability

Favor immutable structures where possible (tuples over lists, `frozenset`, etc.).

```python
point = (3, 4)  # tuple - can't be mutated
```

## 7. Function Composition

Combine small functions into bigger ones.

```python
def compose(*funcs):
    def composed(x):
        for f in reversed(funcs):
            x = f(x)
        return x
    return composed

add_one = lambda x: x + 1
double = lambda x: x * 2

add_then_double = compose(double, add_one)
print(add_then_double(3))  # (3+1)*2 = 8
```

## 8. Decorators (higher-order functions)

Functions that take/return functions — a very Pythonic FP pattern.

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def greet(name):
    return f"Hello, {name}!"

greet("Alice")
```

## 9. `functools` Toolkit

- `functools.partial` — pre-fill some arguments
- `functools.reduce` — fold a sequence into one value
- `functools.lru_cache` — memoization (caching pure function results)

```python
from functools import partial, lru_cache

double = partial(lambda x, y: x * y, 2)
print(double(5))  # 10

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)
```

---

**Rule of thumb:** In Python, use FP style for data transformations (map/filter/reduce or comprehensions), pure functions where practical, and decorators for cross-cutting concerns — but don't force strict FP where a simple loop or class is clearer.

Want me to go deeper into any of these (e.g., recursion patterns, `itertools`, or monad-like patterns with `Optional`/`Result` types)?