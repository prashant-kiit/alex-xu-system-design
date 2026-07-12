# Data typing validation is similar to Method typing validation in protocol and ABC both. Yes or No?

* **Protocol:** ✅ **Yes**, type checkers (e.g. mypy, pyright) validate that required attributes have the correct types.
* **ABC:** ❌ **No**, Python does **not** enforce attribute type annotations at runtime. They are only hints unless you add your own validation (or use tools like `dataclasses` or `pydantic`).

### Example

```python
from typing import Protocol

class P(Protocol):
    age: int

class A:
    age = "20"   # str, not int

# mypy/pyright: Type error
```

```python
from abc import ABC

class P(ABC):
    age: int

class A(P):
    age = "20"   # No runtime error
```

### Summary

| Feature                 | Protocol         | ABC                         |
| ----------------------- | ---------------- | --------------------------- |
| Method requirement      | ✅ (type checker) | ✅ (runtime)                 |
| Attribute type checking | ✅ (type checker) | ❌ (not enforced at runtime) |

So the statement **"data type validation happens similarly in Protocol and ABC"** is **No**. They differ in how enforcement works.
