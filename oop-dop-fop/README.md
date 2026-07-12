# OOP vs DOP vs FOP in Python

A hands-on exploration of three programming paradigms — **Object-Oriented Programming (OOP)**, **Data-Oriented Programming (DOP)**, and **Functional-Oriented Programming (FOP)** — implemented in Python.

The goal isn't academic. Each paradigm is explored through practical, industry-relevant examples that show where it genuinely shines (and where it doesn't), with an eye toward two outcomes:

- **Writing better production code** — recognizing which paradigm fits a given problem (state management, data transformation pipelines, business logic, concurrency, etc.) instead of defaulting to one style everywhere.
- **Interview readiness** — being able to reason about and discuss trade-offs between paradigms, refactor a naive OOP solution into a data-oriented or functional one on the spot, and explain *why* one approach is more testable, immutable, or composable than another.

## Paradigms covered

- **OOP** — encapsulation, inheritance vs. composition, polymorphism, when classes actually earn their complexity.
- **DOP** — treating data as plain, immutable structures decoupled from behavior; favoring generic data manipulation over rigid class hierarchies (in the spirit of Yehonathan Sharvit's *Data-Oriented Programming*).
- **FOP** — pure functions, immutability, higher-order functions, composition/pipelines over inheritance.

## Structure

Each paradigm gets its own set of examples, tackling the same or similar problems so the implementations can be compared side by side — same problem, different lens.

## Why this matters

Real-world Python codebases rarely stick to one paradigm. Knowing when to reach for a class vs. a dataclass/dict vs. a pure function pipeline is a practical skill that shows up constantly in code review, system design discussions, and interviews.
