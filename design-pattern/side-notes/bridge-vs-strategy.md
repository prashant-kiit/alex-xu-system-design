Both are structural/behavioral GoF patterns that use composition + interfaces instead of inheritance, which is why people mix them up. Here's the core distinction:

## Strategy Pattern
**Intent:** Encapsulate interchangeable *algorithms* and let the client swap them at runtime.

- Focuses on **behavior/algorithm** variation for a single class.
- The client typically knows about and picks the strategy.
- One dimension of variation (the algorithm).

```java
interface SortStrategy {
    void sort(int[] data);
}

class QuickSort implements SortStrategy { ... }
class MergeSort implements SortStrategy { ... }

class Sorter {
    private SortStrategy strategy;
    Sorter(SortStrategy s) { this.strategy = s; }
    void sort(int[] data) { strategy.sort(data); }
}
```
Use case: payment methods (CreditCard, PayPal), compression algorithms, validation rules.

## Bridge Pattern
**Intent:** Decouple an **abstraction** from its **implementation** so both can vary/evolve independently.

- Focuses on separating a **class hierarchy into two hierarchies** — "what" and "how."
- Solves the "class explosion" problem when you have multiple dimensions of variation (e.g., Shape × Color, Remote × Device).
- The abstraction *owns* a reference to the implementation permanently (part of the object's structure), not just a plug-in behavior.

```java
interface Device {
    void turnOn();
}
class TV implements Device { ... }
class Radio implements Device { ... }

abstract class RemoteControl {
    protected Device device;
    RemoteControl(Device d) { this.device = d; }
    abstract void power();
}
class BasicRemote extends RemoteControl {
    void power() { device.turnOn(); }
}
class AdvancedRemote extends RemoteControl { ... }
```
Use case: GUI toolkit (Window abstraction × OS-specific rendering implementation), Remote × Device.

## The key difference

| Aspect | Strategy | Bridge |
|---|---|---|
| **Problem solved** | Swappable algorithms/behavior | Avoiding a combinatorial class hierarchy |
| **Dimensions of variation** | One (the algorithm) | Two or more, evolving independently |
| **When it's decided** | Often at runtime, per call | Usually at design/construction time, structural |
| **Intent** | Behavioral pattern | Structural pattern |
| **Relationship feel** | "Has-a behavior I can plug in" | "Is composed of an abstraction + implementation, both extensible" |

**Rule of thumb:** If you're thinking "I want to swap out *how this one thing is done*" → Strategy. If you're thinking "I have two hierarchies that would otherwise multiply into N×M subclasses" → Bridge.

Structurally, their class diagrams look nearly identical (both use composition over an interface) — the difference is really about **intent and design motivation**, not code shape.