# Give one one example of sync non blocking and async blocking.

Strictly speaking, **"async blocking" is usually a contradiction**. Asynchronous code is designed to avoid blocking the caller. However, people sometimes use the term to mean "an async task that waits internally for a long operation." Here are examples of all four combinations:

| Type                     | Example                                                   | Blocks thread?       |
| ------------------------ | --------------------------------------------------------- | -------------------- |
| **Sync + Blocking**      | `time.sleep(2)` in Python                                 | ✅ Yes                |
| **Sync + Non-Blocking**  | `socket.recv(..., MSG_DONTWAIT)` on a non-blocking socket | ❌ No                 |
| **Async + Non-Blocking** | `await asyncio.sleep(2)`                                  | ❌ No                 |
| **Async + "Blocking"**   | Calling `time.sleep(2)` inside an `async def`             | ✅ Yes (bad practice) |

### 1. Sync + Blocking

```python
import time

print("Start")
time.sleep(2)   # Blocks the thread
print("End")
```

---

### 2. Sync + Non-Blocking

```python
import socket

sock = socket.socket()
sock.setblocking(False)

try:
    data = sock.recv(1024)   # Returns immediately or raises BlockingIOError
except BlockingIOError:
    print("No data yet")
```

The function is synchronous (no `await`), but it **doesn't wait**.

---

### 3. Async + Non-Blocking

```python
import asyncio

async def main():
    print("Start")
    await asyncio.sleep(2)   # Doesn't block the event loop
    print("End")

asyncio.run(main())
```

While waiting, other async tasks can run.

---

### 4. Async + Blocking (Bad Practice)

```python
import asyncio
import time

async def main():
    print("Start")
    time.sleep(2)    # Blocks the event loop!
    print("End")

asyncio.run(main())
```

Although `main()` is asynchronous, `time.sleep()` blocks the entire event loop, preventing other async tasks from running.

### Summary

| Combination          | Common?                      | Example                                      |
| -------------------- | ---------------------------- | -------------------------------------------- |
| Sync + Blocking      | ✅ Very common                | `time.sleep()`, normal file I/O              |
| Sync + Non-Blocking  | ✅ Exists                     | Non-blocking socket (`setblocking(False)`)   |
| Async + Non-Blocking | ✅ Standard async programming | `await asyncio.sleep()`, async HTTP requests |
| Async + Blocking     | ⚠️ Possible but incorrect    | `time.sleep()` inside `async def`            |
