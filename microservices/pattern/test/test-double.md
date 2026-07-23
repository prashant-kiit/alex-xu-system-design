Link: https://dev.to/mahata/whats-test-doubles-2c59

# Test Doubles

## Why Test Doubles Exist

Whenever a unit under test collaborates with something else — another class, a database, a hardware device — that collaborator gets in the way of testing the unit in isolation. It might be slow, non-deterministic, dangerous to invoke for real (imagine actually launching a rocket in a unit test), or simply not built yet.

A **test double** is a stand-in object that replaces a real collaborator during a test, the same way a stunt double replaces an actor for a dangerous scene. Martin Fowler's classification breaks test doubles into five kinds, and the differences between them are not cosmetic — each one exists to solve a specific problem that the previous one couldn't:

| Type | One-line definition |
|---|---|
| **Dummy** | A test double created to pass compilation. It will break if you try to use it. |
| **Fake** | A double that actually works, but is unsuitable for production (e.g. an in-memory database). |
| **Stub** | A double that returns a predetermined value when called. |
| **Spy** | A double that records how it was called. |
| **Mock** | A spy that asserts itself. |

Knowing these names precisely matters because it lets a team say "this is just a stub" or "why is this a mock and not a spy?" and be instantly understood, instead of everyone calling every test double a "mock object."

The rest of this note builds up a small rocket-launch system test-first, and introduces each type of test double at the exact moment the previous approach stops being good enough — the way it would actually happen in a real TDD session.

## The Launch Rocket Example

The system under test is a `Launcher` that decides whether a `Rocket` should be launched, based on a `LaunchCode`.

```typescript
export interface Rocket {
  // Launch the rocket
  launch(): void

  // Disable the rocket
  disable(): void
}

export interface LaunchCode {
  // Returns whether the launch code has expired
  isExpired(): boolean

  // Returns whether the launch code is signed
  isSigned(): boolean
}
```

`Launcher` depends on both interfaces through its constructor/method parameters, never on a concrete `Rocket` or `LaunchCode`. That's what makes it possible to substitute test doubles for them.

### Iteration 1 — Dummy (and a first Stub)

**The failing test.** The very first behavior worth testing: an expired launch code must never launch the rocket.

```typescript
it("When expired launch code is given, rocket is not launched", () => {
  const launcher = new Launcher()
  launcher.launchRocket(new DummyRocket(), new ExpiredLaunchCodeStub())
})
```

To even compile this test, `launchRocket` needs *some* object that implements `Rocket` and *some* object that implements `LaunchCode`. But the two arguments play very different roles in this particular test:

- The test is about the **launch code**, so that collaborator needs to actually behave like an expired code. A hand-rolled implementation that returns fixed, predetermined answers is enough — that's a **Stub**.
- The test doesn't care about the **rocket** at all — it only needs an object to satisfy the parameter type. Since a correct implementation must never call `launch()` in this scenario, the rocket collaborator can be built to explode if it's ever touched. That's a **Dummy**.

```typescript
export class DummyRocket implements Rocket {
  launch() {
    throw Error()
  }

  disable() {}
}

export class ExpiredLaunchCodeStub implements LaunchCode {
  isSigned() {
    return true
  }

  isExpired() {
    return true
  }
}
```

Minimal production code to make it pass:

```typescript
export class Launcher {
  launchRocket(rocket: Rocket, launchCode: LaunchCode) {
    if (!launchCode.isExpired()) {
      rocket.launch()
    }
  }
}
```

**Definition — Dummy.** An object passed around only to satisfy a parameter list or constructor signature. It is never meant to be exercised; if it is, that's a bug, and the implementation should make that failure loud (throwing is a common technique).

**Purpose.** Let a test compile and run when a collaborator is structurally required but behaviorally irrelevant to the scenario being tested.

**When to use it.** When a dependency must be passed in, but the code path under test provably never touches it.

**Advantages.**
- Zero implementation effort — often just a stub class with methods that throw.
- Makes accidental use of the "irrelevant" collaborator fail loudly instead of silently doing the wrong thing.

**Disadvantages.**
- The test has **no explicit assertion**. It "passes" simply because nothing threw — the intent ("rocket must not be launched") is implicit, not verified.
- Because it relies on an exception rather than a check, a *broken* implementation that happens not to touch the dummy for the wrong reason would still pass.
- Can't be used to test the "happy path" at all — if `launch()` is genuinely supposed to be called, a Dummy will blow up the test.

That last disadvantage becomes a real problem in the next iteration.

### Iteration 2 — Spy

**Why Dummy stops being enough.** Now a second scenario needs testing: when the code is valid, the rocket **must** be launched. `DummyRocket` can't be reused here — it throws the moment `launch()` is called, which is exactly the call this test needs to happen. And even the passing "expired code" test from Iteration 1 is unsatisfying: it never actually *proves* `launch()` wasn't called, it just never crashed.

What's needed is a collaborator that behaves like a normal, harmless object, but **remembers whether it was invoked** so the test can make that fact explicit — a **Spy**.

```typescript
export class RocketSpy implements Rocket {
  launchWasCalled = false

  launch() {
    this.launchWasCalled = true
  }

  wasLaunchCalled(): boolean {
    return this.launchWasCalled
  }

  disable() {}
}
```

The expired-code test is rewritten to assert on real state instead of relying on "nothing threw":

```typescript
it("When expired launch code is given, rocket is not launched", () => {
  const rocket = new RocketSpy()

  const launcher = new Launcher()
  launcher.launchRocket(rocket, new ExpiredLaunchCodeStub())

  expect(rocket.wasLaunchCalled()).toBe(false)
})
```

And the happy-path test, which was impossible with a Dummy, becomes trivial:

```typescript
it("When valid launch code is given, rocket is launched", () => {
  const rocket = new RocketSpy()

  const launcher = new Launcher()
  launcher.launchRocket(rocket, new ValidLaunchCodeStub())

  expect(rocket.wasLaunchCalled()).toBe(true)
})
```

**Definition — Spy.** A test double that records information about how it was called (whether a method was invoked, how many times, with what arguments), so the test can inspect that record afterward.

**Purpose.** Verify *interactions* — that the code under test called (or didn't call) a collaborator — rather than verifying a return value.

**How it differs from Dummy.** A Dummy is inert and unsafe to call; a Spy is safe to call and actively tracks the call so the test can make an explicit, honest assertion about it.

**When to use it.** When the correctness of the unit under test is defined by *whether/how it talks to a collaborator*, not by a value the collaborator returns.

**Advantages.**
- Assertions are explicit (`expect(...).toBe(...)`) instead of implicit ("didn't throw").
- Enables proper Given-When-Then structure in the test.
- Works for both the "should call" and "should not call" cases, unlike a Dummy.

**Disadvantages.**
- Exposes internal call-tracking state (`launchWasCalled`) as public fields/getters purely for testing purposes.
- As more behaviors need verifying (e.g. `disable()` too), the test accumulates more and more repeated assertion lines — seen next.

### Iteration 3 — Mock

**Why Spy alone starts to hurt.** A new safety requirement arrives: if the code is invalid, the rocket must not just be left alone — it must be explicitly **disabled**.

```typescript
export class Launcher {
  launchRocket(rocket: Rocket, launchCode: LaunchCode) {
    if (!launchCode.isExpired() && launchCode.isSigned()) {
      rocket.launch()
    } else {
      rocket.disable()
    }
  }
}
```

The spy grows a second tracked call:

```typescript
export class RocketSpy implements Rocket {
  launchWasCalled = false
  disableWasCalled = false

  launch() {
    this.launchWasCalled = true
  }

  wasLaunchCalled(): boolean {
    return this.launchWasCalled
  }

  disable() {
    this.disableWasCalled = true
  }

  wasDisableCalled() {
    return this.disableWasCalled
  }
}
```

Now every "abort" test needs *two* assertions, and there's about to be more than one such test (expired code, unsigned code, reused code...):

```typescript
it("When expired launch code is given, rocket is not launched", () => {
  const rocket = new RocketSpy()

  const launcher = new Launcher()
  launcher.launchRocket(rocket, new ExpiredLaunchCodeStub())

  expect(rocket.wasLaunchCalled()).toBe(false)
  expect(rocket.wasDisableCalled()).toBe(true)
})

it("When unsigned launch code is given, rocket is not launched", () => {
  const rocket = new RocketSpy()

  const launcher = new Launcher()
  launcher.launchRocket(rocket, new UnsignedLaunchCodeStub())

  expect(rocket.wasLaunchCalled()).toBe(false)
  expect(rocket.wasDisableCalled()).toBe(true)
})
```

The pair of assertions — "launch was NOT called AND disable WAS called" — is really a single concept: **"the launch was aborted."** Duplicating it in every test invites copy-paste drift (one test might forget the second `expect`). The fix is to let the double assert on itself. That's what turns a Spy into a **Mock**.

```typescript
export class RocketMock implements Rocket {
  launchWasCalled = false
  disableWasCalled = false

  launch() {
    this.launchWasCalled = true
  }

  disable() {
    this.disableWasCalled = true
  }

  verifyAbort() {
    expect(this.launchWasCalled).toBe(false)
    expect(this.disableWasCalled).toBe(true)
  }
}
```

```typescript
it("When expired launch code is given, rocket is not launched", () => {
  const rocket = new RocketMock()

  const launcher = new Launcher()
  launcher.launchRocket(rocket, new ExpiredLaunchCodeStub())

  rocket.verifyAbort()
})

it("When unsigned launch code is given, rocket is not launched", () => {
  const rocket = new RocketMock()

  const launcher = new Launcher()
  launcher.launchRocket(rocket, new UnsignedLaunchCodeStub())

  rocket.verifyAbort()
})
```

**Definition — Mock.** A spy that asserts itself: it doesn't just record calls, it carries its own verification logic (`verifyAbort()`), so the test body doesn't need to.

**Purpose.** Centralize the expectation ("this is what a correct abort looks like") in one place instead of scattering it across every test that needs it.

**How it differs from Spy.** A Spy passively records; the test does the checking. A Mock actively knows what "correct" means for itself and exposes that as a method — the recording is still there, it's just wrapped behind an assertion API.

**When to use it.** When the same interaction-verification logic would otherwise be copy-pasted across multiple tests, and giving it a name (`verifyAbort()`) makes the tests more readable, not less.

**Advantages.**
- Eliminates duplicated assertions.
- Gives the verification a name that documents intent (`verifyAbort` reads better than two raw `expect` calls).

**Disadvantages.**
- Readability can suffer in the other direction: the explicit assertions "fall out of the body of the test" and hide inside the double, so a reader has to go find `verifyAbort()` to know what's actually being checked.
- Overusing mocks for every collaborator turns tests into a description of *implementation* (which methods get called, in what order) rather than *behavior*, making them brittle to harmless refactors.

### Refining the Stub

Along the way, a second `LaunchCode` stub (`UnsignedLaunchCodeStub`) was needed, and it duplicated the "valid" defaults already written in `ExpiredLaunchCodeStub`. Once there are three variations of the same interface that differ by exactly one flag, that duplication is worth removing — a small but real lesson in stub hygiene:

```typescript
export class ValidLaunchCode implements LaunchCode {
  isSigned() {
    return true
  }

  isExpired() {
    return false
  }
}

export class UnsignedLaunchCodeStub extends ValidLaunchCode {
  isSigned(): boolean {
    return false
  }
}

export class ExpiredLaunchCodeStub extends ValidLaunchCode {
  isExpired() {
    return true
  }
}
```

**Definition — Stub.** A test double that returns a predetermined value when called — no recording, no assertions, just canned answers.

**Purpose.** Control the inputs a collaborator feeds into the unit under test, so a specific branch of logic can be exercised deterministically.

**How it differs from Dummy/Spy/Mock.** A Stub is about **output** (what it returns to the caller); Dummy is about **presence** (satisfying a signature); Spy/Mock are about **input observation** (what was called on them). A single class can technically do more than one job, but naming it for what it's actually being used for in a given test keeps intent clear.

**When to use it.** Whenever the test needs a collaborator to answer a query method (`isExpired()`, `isSigned()`) with a specific, fixed value to drive the unit under test down a particular path.

**Advantages.**
- Deterministic, trivial to reason about.
- Each subclass communicates precisely which single property is "abnormal" for that scenario (`UnsignedLaunchCodeStub` overrides only `isSigned`).

**Disadvantages.**
- A Stub can't accumulate state across calls or embody real logic — it always returns the same canned answer no matter what happened earlier in the test. That limitation is what forces the next test double into existence.

### Iteration 4 — Fake

**Why Stub stops being enough.** A new requirement: a launch code can only be used once. To verify "reusing a launch code aborts the second launch," a test needs a collaborator that can be told a code was used, and later asked whether it was — i.e., something with real, working, stateful behavior:

```typescript
export interface UsedLaunchCodes {
  contain(launchCode: LaunchCode): boolean
  add(launchCode: LaunchCode): void
}
```

A Stub genuinely cannot do this: `contain()` has to return different answers depending on whether `add()` was called earlier in *that same test*, and a Stub, by definition, always returns one fixed value. A Mock isn't the right shape either — this isn't about verifying *how* `UsedLaunchCodes` was called, it's about the unit under test getting *correct, working* collaboration back. That calls for a **Fake**: a lightweight but real implementation.

```typescript
export class FakeUsedLaunchCodes implements UsedLaunchCodes {
  private launchCodes: Set<LaunchCode> = new Set()

  add(launchCode: LaunchCode): void {
    this.launchCodes.add(launchCode)
  }

  contain(launchCode: LaunchCode): boolean {
    return this.launchCodes.has(launchCode)
  }
}
```

Because a Fake actually *works*, it earns its own unit test, just like production code would:

```typescript
it("contains() checks if a given launch code is already used", () => {
  const usedLaunchCodes = new FakeUsedLaunchCodes()
  const launchCode = new ValidLaunchCode()

  expect(usedLaunchCodes.contain(launchCode)).toBe(false)

  usedLaunchCodes.add(launchCode)

  expect(usedLaunchCodes.contain(launchCode)).toBe(true)
})
```

`Launcher` grows a third collaborator and a third condition:

```typescript
export class Launcher {
  launchRocket(
    rocket: Rocket,
    launchCode: LaunchCode,
    usedLaunchCodes: UsedLaunchCodes
  ) {
    if (
      !usedLaunchCodes.contain(launchCode) &&
      !launchCode.isExpired() &&
      launchCode.isSigned()
    ) {
      rocket.launch()
      usedLaunchCodes.add(launchCode)
    } else {
      rocket.disable()
    }
  }
}
```

And the reuse scenario becomes straightforward to express, reusing `RocketMock` from Iteration 3 and sharing one `FakeUsedLaunchCodes` instance across both calls so its state actually carries over:

```typescript
it("When launch code is used already, rocket is not launched", () => {
  const rocket1 = new RocketMock()
  const rocket2 = new RocketMock()
  const launchCode = new ValidLaunchCode()
  const usedLaunchCodes = new FakeUsedLaunchCodes()

  const launcher = new Launcher()
  launcher.launchRocket(rocket1, launchCode, usedLaunchCodes)
  launcher.launchRocket(rocket2, launchCode, usedLaunchCodes)

  rocket2.verifyAbort()
})
```

(Every earlier test now also needs a third `usedLaunchCodes` argument — a fresh `FakeUsedLaunchCodes()` is enough for those, since none of them care about reuse.)

**Definition — Fake.** A test double with a real, working implementation, just one that's unsuitable for production (an in-memory `Set` standing in for a database, cache, or persistent store).

**Purpose.** Provide genuine behavior for a collaborator that the unit under test depends on *functionally* (its logic, not just its interface), without paying the cost of the real infrastructure (a database, a filesystem, a queue) in a fast unit test.

**How it differs from the others.** Dummy/Stub/Spy/Mock are all, in some sense, pretending — they exist purely in service of the test. A Fake is "made to be indistinguishable from the real thing" from the caller's point of view. It's real code, with its own tests, that happens to make a different trade-off (speed and simplicity over durability, scale, or production-readiness).

**When to use it.** When a collaborator needs actual logic to make the test meaningful, and standing up the real dependency (a real database, a real external service) would make the test slow, flaky, or impossible to run in isolation.

**Advantages.**
- Tests exercise real logic instead of canned answers, catching a class of bugs stubs and mocks can't.
- Reusable across many tests without per-test setup of expected calls/returns.
- Defers the choice of real backend (RDBMS, KVS, in-memory) — the interface and a fake implementation can exist long before the production storage decision is made.

**Disadvantages.**
- Costs more to build and maintain than a Stub or Dummy — it's a small piece of real software.
- Can drift from the real implementation's behavior over time if not kept in sync, giving false confidence.

## Comparison Table

| Type | Has real logic? | Returns controlled values? | Records calls? | Asserts itself? | Primary question it answers |
|---|---|---|---|---|---|
| **Dummy** | No | No | No | No | "Does this compile/run without the collaborator ever being used?" |
| **Stub** | No | Yes | No | No | "What does the unit under test do when given this specific input?" |
| **Spy** | No | Optionally | Yes | No | "Did the unit under test call this collaborator?" |
| **Mock** | No | Optionally | Yes | Yes | "Did the unit under test interact with this collaborator *correctly*?" |
| **Fake** | Yes | N/A (real behavior) | No (usually) | No | "Does the unit under test work against a real, working collaborator?" |

## When to Use Which Test Double

- **Dummy** — the collaborator is required by a signature but structurally can't be exercised in this scenario. Prefer it only when a Spy would be overkill (no test cares whether it's called at all).
- **Stub** — the test needs to control what a query method returns, to steer the unit under test down a specific branch.
- **Spy** — the correctness of the scenario hinges on *whether* a command method was called, and no other test double already covers that collaborator.
- **Mock** — the same interaction-verification logic (like `verifyAbort()`) would otherwise be duplicated across several tests; wrap it once and name it.
- **Fake** — the collaborator has real logic that matters (state, computation) and using the production implementation would make the test slow, flaky, or hard to set up.

A practical decision order: start with a Stub or Dummy for the simplest need; reach for a Spy only when you must verify a call happened; upgrade to a Mock only once verification logic repeats; reach for a Fake only when canned answers genuinely can't express the collaborator's behavior.

## Common Mistakes

- **Calling everything a "mock."** Loosely calling every test double a mock erases exactly the distinctions that make the vocabulary useful — a Stub and a Mock solve different problems, and mislabeling one hides which problem is actually being solved.
- **Leaning on Dummy for assertions.** Relying on "the test didn't throw" as the assertion (Iteration 1's original problem) makes intent implicit and lets subtly wrong implementations slip through.
- **Mocking collaborators that should be Fakes.** Verifying *how* a stateful collaborator like a repository was called, instead of giving it a real (if lightweight) implementation, produces tests that assert on implementation details and break on harmless refactors.
- **Reusing one Stub instance where state should carry over.** A Stub always returns the same fixed answer; trying to make it "remember" something between calls is a sign a Fake is actually needed (see Iteration 4).
- **Over-verifying with Mocks.** Asserting every single interaction with every collaborator turns tests into a mirror of the implementation, so any refactor — even a correct one — breaks tests that were never actually about behavior.
- **Skipping tests for Fakes.** Because a Fake has real logic, it can have real bugs. Treat it like production code and test it directly, as `FakeUsedLaunchCodes` was tested above.

## Key Takeaways

- Test doubles are not interchangeable synonyms for "mock" — each of the five (Dummy, Fake, Stub, Spy, Mock) solves a distinct problem, and picking the wrong one either weakens the test or makes it unnecessarily brittle.
- A real TDD session tends to *discover* the need for each kind of double in order, as the previous, simpler double runs out of capability: Dummy → Spy (need to observe a call) → Mock (need to stop repeating the same verification) → Fake (need real, stateful behavior a Stub can't fake).
- The underlying goal is always the same regardless of which double is used: keep the unit under test isolated, fast, and deterministic, while keeping the test's intent explicit and readable.
- Be aware of the different types of test doubles and choose the appropriate one for the job — the choice should be driven by what the test actually needs to verify, not habit.
