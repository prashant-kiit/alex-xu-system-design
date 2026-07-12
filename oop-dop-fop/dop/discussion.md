# What This Article Adds Beyond What We've Covered

This article (based on Yehonathan Sharvit's *Data-Oriented Programming* book) frames DOP around **four formal principles**, each with explicit benefits/costs. Here's what's genuinely new versus our earlier notes — the theoretical grounding, the trade-off analysis, and a few concrete techniques we hadn't covered. Link: https://towardsdatascience.com/data-oriented-programming-with-python-ef478c43a874/

---

## 1. Explicit Principle: "Separate Code from Data" (not just "use pure functions")

We'd emphasized pure functions, but the article frames it as a **formal architectural rule**: functions must never close over or depend on data trapped inside an object's context.

The principle is stated as separating code so that it resides in functions whose behavior does not depend on data that is encapsulated in the function's context.

**New concrete benefit — cross-domain code reuse:**
```python
@dataclass
class AuthorData:
    first_name: str
    last_name: str
    n_books: int

def calculate_name(first_name: str, last_name: str):
    return f"{first_name} {last_name}"
```

The key insight (new to our discussion): because `calculate_name()` doesn't know about `AuthorData` at all, the same function can be reused for any other data with first/last name fields, such as users or librarians, without inheritance, mixins, or shared base classes — something we hadn't explicitly called out as a DOP-specific reuse mechanism.

**New cost we hadn't flagged — "no packaging":** code that manipulates data can end up scattered anywhere, making it hard for developers to discover which functions are available and leading to wasted time and duplicated code. This is a real production pain point: without classes as a discovery mechanism (IDE autocomplete on `order.`), you need disciplined module organization (which we mentioned) *plus* good docs/naming conventions, or teams reinvent the same transform function in five files.

**Important Python-specific correction the article makes:** the "no access control" cost cited in Sharvit's original (Java/Clojure) book doesn't really apply to Python, since data held by a class can still be accessed by any code holding a reference to the object — Python doesn't enforce object-level encapsulation the way some OOP languages do. This is a useful nuance: Python was never strongly encapsulated to begin with, so DOP doesn't "give up" as much safety as it would in Java.

---

## 2. Formalized Principle: "Represent Data with Generic Structures" — with real trade-off data

We'd recommended dataclasses/NamedTuples as the default. This article adds an important **counter-argument we hadn't presented**: true DOP (per Sharvit) actually prefers raw `dict`/`list` over typed classes, and dataclasses are a *compromise*, not the "pure" form.

The article notes that Python's dataclass is a hybrid closer to OOP than DOP, whereas true generic data structures would be plain dictionaries and tuples — but dataclasses are less error-prone, more descriptive via type hints, and can easily convert to/from dicts.

**New benefit — "generic function reuse" at the *stdlib* level:**
```python
author = {"first_name": "Issac", "last_name": "Asimov", "n_books": 500}
author.get("first_name")
author["n_books"] = 703
```
The point here (new framing): using plain dicts means you can manipulate data with Python's built-in generic functions rather than learning and remembering custom methods on every class, and those generic functions won't break when a library version changes. This is a genuinely different angle from what we discussed — it's an argument for **less** structure in some cases, trading type safety for long-term API stability.

**New cost, with a concrete failure mode — silent typos:**
```python
names.append({"fist_name": "John", "last_name": "Smith"})  # typo!
print(f"{names[2].get('first_name')} {names[2].get('last_name')}")
# None Smith  <-- no error, just silently wrong
```
This is a sharp, new illustration: with generic data structures, mistyping a field doesn't raise an error — the field is just silently missing from the result, unlike a class-based approach where an unexpected keyword argument raises a TypeError immediately. This is a strong practical argument *for* our earlier Pydantic/dataclass recommendation — it validates why "plain dicts in production" is risky and dataclasses/Pydantic exist to close this exact gap.

**New performance nuance we hadn't mentioned:** lookup time for set and dict is more efficient than for list and tuple, because sets and dictionaries use a hash function for direct lookup rather than a search — relevant when choosing between tuple-of-records vs dict-of-records for large in-memory datasets.

---

## 3. New Concrete Illustrations for "Data is Immutable" (Principle #3)

We'd covered *how* to get immutability (frozen dataclass, NamedTuple, MappingProxyType). This article adds **why it matters with vivid failure-mode examples** we hadn't shown:

**a) The mutable default argument trap** (classic Python gotcha, reframed as a DOP argument):
```python
def append_to_list(el, ls=[]):   # BUG: default list is shared across calls
    ls.append(el)
    return ls
```
Because the list is mutable, each call mutates the same default object, so successive calls return accumulating results instead of independent ones — fixed by using `None` as sentinel. This is a good concrete "immutability prevents this class of bug" example, distinct from our earlier abstract explanation.

**b) `is` vs `==` and identity-based fast equality** — genuinely new content for us:
Immutable objects like strings have consistent identity, so `is` and `==` behave the same way, whereas mutable objects like lists get a new identity every time, making `is` unpredictable for them; since comparing object addresses via `is` is faster than comparing all fields via `==`, immutability enables faster equality checks. This is a concrete performance argument for immutable data (e.g., in NamedTuples/frozen dataclasses) we hadn't covered — worth knowing when choosing data structures for hash-heavy or comparison-heavy pipelines.

**c) Race-condition motivation for immutability in concurrency**, explained via a two-thread read-modify-write scenario rather than the abstract "safe to share across threads" statement we gave — two threads modifying a shared mutable value can produce three different possible outcomes depending on execution order, which is exactly the kind of corruption immutable data prevents.

**d) A concrete cost comparison via `id()`** showing tuples get new memory addresses on "modification" while lists keep the same one — expanding a mutable list keeps the same object identity, while expanding an immutable tuple creates a brand-new object with a different identity, and this copying requirement adds memory and CPU cost for large collections. Useful for justifying *why* teams sometimes deliberately choose mutable-then-freeze patterns for very large datasets rather than always using tuples.

---

## 4. Principle #4 — "Separate Data Schema from Data Representation" (a distinct principle we hadn't isolated)

We had folded "validation" into "use Pydantic at the edges," treating schema and data as bundled together in one model class. This article names a **separate, fourth principle**: keep the schema itself as its own standalone data structure, decoupled from both the data *and* the validation code.

```python
schema = {
    "required": ["first_name", "last_name"],
    "properties": {
        "first_name": {"type": str},
        "last_name": {"type": str},
        "books": {"type": int},
    }
}

def validate(data):
    assert set(schema["required"]).issubset(set(data.keys()))
    for k in data:
        if k in schema["properties"]:
            assert type(data[k]) == schema["properties"][k]["type"]
```

The distinction: the expected shape of data is represented as metadata kept separately from the main data representation, rather than being baked into a class definition. In Pydantic terms, this is roughly the difference between a `BaseModel` (schema + data coupled in one class) and a **JSON Schema document validated against a dict at runtime** — the latter is the "purer" DOP approach, useful when:
- schemas need to be **serialized themselves** (e.g., stored in a database, sent over a network, versioned independently of code)
- the same data needs to be validated against **different schemas** at different times (e.g., a "draft" schema vs a "published" schema for the same record)
- you're building **schema registries** (common in Kafka/Avro-based data pipelines) — the article's dict-schema pattern is essentially a simplified version of what JSON Schema / Avro / Protobuf do at industry scale.

**New concrete benefit — advanced runtime validation beyond types:**
```python
schema = {
    "properties": {
        "books": {"type": int, "min": 0, "max": 10000},
    }
}
```
Because validation happens at run time rather than compile time, DOP allows validation conditions that go beyond a field's type — this is exactly what Pydantic's `Field(ge=0, le=10000)` or custom validators do, but the article's framing makes clear *why* this is a distinct principle worth naming: schema-as-data is what lets you version, store, transmit, and dynamically generate validation rules, rather than validation logic being frozen into your class hierarchy at code-deploy time.

---

## Summary: What's Genuinely New Here

| New in this article | Not previously covered |
|---|---|
| Formal 4-principle framework (Sharvit's book) with named costs/benefits | We had informal "best practices," not principle-by-principle trade-offs |
| Python-specific rebuttal: Python was never strongly encapsulated, so "OOP safety loss" argument is weaker in Python | New nuance |
| Generic-dict approach as *purer* DOP vs dataclasses as a compromise | We presented dataclasses as the default without this tension |
| Concrete silent-typo failure mode with plain dicts | Motivates why Pydantic/dataclasses matter, shown as a bug not just asserted |
| `is` vs `==` identity-based fast equality argument for immutability | New performance argument |
| Schema-as-standalone-data (Principle #4) — decoupled from both data and validation code | We'd merged "schema" into "Pydantic model," this treats schema as its own artifact |
| dict vs list/tuple lookup performance (hash vs linear search) | New performance detail |

**One thing to flag:** the article is Python-adapted from a Java/Clojure book, so several of Sharvit's original "costs" (performance hit, type casting, packaging) are explicitly noted as **not fully applicable to Python** — worth keeping in mind if you read the original book, since dynamically-typed, non-compiled Python sidesteps several DOP trade-offs that matter more in statically-typed/compiled languages.