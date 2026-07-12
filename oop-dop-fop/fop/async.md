    Using **only `async`/`await`**, the equivalent code is:

```javascript
function getUser() {
    return new Promise(resolve => {
        setTimeout(() => resolve("Alice"), 2000);
    });
}

async function main() {
    console.log("1");

    const user = await getUser();

    console.log(user);
    console.log("2");
}

console.log("Start");
main();
console.log("End");
```

### Output

```text
Start
1
End
Alice
2
```

(`Alice` and `2` are printed after approximately **2 seconds**.)

### Why is `"End"` printed before `"Alice"`?

Execution timeline:

1. `console.log("Start")` → prints `Start`
2. `main()` is called.
3. Inside `main()`, `1` is printed.
4. `await getUser()` pauses **only `main()`**.
5. Control returns to the caller.
6. `console.log("End")` executes immediately.
7. After 2 seconds, the Promise resolves with `"Alice"`.
8. `main()` resumes, printing:

   * `Alice`
   * `2`

So `await` pauses the current `async` function, but **does not block the rest of the JavaScript program**.

----

Here's the equivalent code **using only Promises** (no `async`/`await`):

```javascript
function getUser() {
    return new Promise(resolve => {
        setTimeout(() => resolve("Alice"), 2000);
    });
}

function main() {
    console.log("1");

    return getUser().then(user => {
        console.log("2");
    });
}

console.log("Start");
main();
console.log("End");
```

### Output

After running:

```text
Start
1
End
2
```

(`2` is printed after approximately **2 seconds**.)

---

### If you also want the resolved value (`"Alice"`)

The `await` version:

```javascript
async function main() {
    console.log("1");

    const user = await getUser();

    console.log(user);
    console.log("2");
}
```

becomes:

```javascript
function getUser() {
    return new Promise(resolve => {
        setTimeout(() => resolve("Alice"), 2000);
    });
}

function main() {
    console.log("1");

    return getUser().then(user => {
        console.log(user);
        console.log("2");
    });
}

console.log("Start");
main();
console.log("End");
```

### Output

```text
Start
1
End
Alice
2
```

after about **2 seconds**.

This demonstrates that `await getUser()` is effectively equivalent to attaching a `.then(...)` callback to the Promise and resuming execution inside that callback when the Promise resolves.
