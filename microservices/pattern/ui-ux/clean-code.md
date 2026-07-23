# Explain Clean Code:

According to **Robert C. Martin (Uncle Bob)** in *Clean Code: A Handbook of Agile Software Craftsmanship*, **clean code is code that is easy for humans to read, understand, and modify.** It is not merely code that works.

The book doesn't provide a single formal definition. Instead, it starts with opinions from experienced programmers and then derives principles. The essence can be summarized as:

> **Clean code is simple, readable, expressive, maintainable, and does one thing well.**

### Key characteristics of clean code

1. **Readable**

   * Code should read like well-written prose.
   * A new developer should understand it quickly.

   ```python
   # Bad
   d = 5

   # Good
   retry_delay_seconds = 5
   ```

2. **Simple**

   * Avoid unnecessary complexity.
   * Prefer the simplest design that works.

3. **One responsibility**

   * Functions should do one thing and do it well.

   ```python
   # Bad
   processOrder()

   # Good
   validateOrder()
   calculatePrice()
   chargeCustomer()
   sendConfirmationEmail()
   ```

4. **Meaningful names**

   * Variables, functions, and classes should explain their purpose.

   ```python
   # Bad
   x

   # Good
   customerBalance
   ```

5. **Small functions**

   * Most functions should be only a few lines long.
   * They should operate at a single level of abstraction.

6. **Minimal comments**

   * Good code explains itself.
   * Comments should explain **why**, not **what**.

   ```python
   # Bad
   # Increment i
   i += 1
   ```

7. **Proper formatting**

   * Consistent indentation.
   * Logical grouping.
   * Appropriate whitespace.

8. **Good error handling**

   * Handle failures explicitly.
   * Don't return error codes when exceptions express intent better (language permitting).

9. **Easy to test**

   * Clean code naturally leads to small, loosely coupled, testable units.

10. **Continuously improved**

    * Follow the **Boy Scout Rule**:

      > *Leave the campground cleaner than you found it.*

---

## Uncle Bob's famous quote

> **"Clean code always looks like it was written by someone who cares."**

---

## What clean code is NOT

* Clever code
* Over-engineered code
* Code optimized before necessary
* Code with lots of comments
* Code that only the original author understands

---

## One-line summary

> **Clean code is code that is easy to read, easy to understand, easy to change, and clearly communicates the programmer's intent while remaining simple and correct.**
