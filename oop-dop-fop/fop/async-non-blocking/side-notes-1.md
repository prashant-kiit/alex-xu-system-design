# Async / Non-Blocking Notes

**Problem:** Since DB Context is different from the Service Context, `db_operation_n` calls are Side Effects. Thus the Service layer has no control over DB Context, but has to wait for the DB Call to complete. This causes the stack to block the CPU with this DB call, preventing other processes from running on the CPU — compromising performance and memory.

**Solution:** The program pushes DB calls to the Event Queue in the OS and gets a Promise in return. The OS Event Loop runs the queued DB calls using epoll (polling technique). This can be done via the `async` keyword or `Promise`.

**Problem:** Transform calls depend on the response from DB calls to perform their action.

**Solution:** Transform calls must `await` the DB calls, i.e. the Promise from DB calls must be resolved by Transform calls. This can be done via the `await` keyword or `.then(callback)`.

**Problem:** The Event Loop does not guarantee order of execution without proper Promise resolution.

**Solution:** To maintain order of execution (sync-ness), make blocking calls using `await` (here, the main thread is blocked by the CPU, which has not yet processed the previous function).

## Example

```js
@pure
@logger(after=True, "transform_0 is done")
async function transform_0(response) {
    return response * 2
}

@pure
@logger(after=True, "transform_1 is done")
async function transform_1(response) {
    return response * 3
}

@pure
@logger(after=True, "transform_2 is done")
async function transform_2(response) {
    return response * 4
}

@sideeffect
@logger(after=True, "db_operation_0 is done")
async function db_operation_0(response) {
    return query_0()
}

@sideeffect
@logger(after=True, "db_operation_1 is done")
async function db_operation_1(response) {
    return query_1()
}

@sideeffect
@logger(after=True, "db_operation_2 is done")
async function db_operation_2(response) {
    return query_2()
}

@sideeffect
@logger(after=True, "db_operation_3 is done")
async function db_operation_3(response) {
    return query_3()
}

@coroutine
async function service(request) {
    response_0 = await db_operation_0(request)
    response_1 = await transform_0(response_0)
    response_2 = await db_operation_1(response_1)
    response_3 = await transform_1(response_2)
    response_4 = await db_operation_2(response_3)
    response_5 = await transform_2(response_4)
    response = await db_operation_3(response_5)
    return response
}

@coroutine
async function handler(request) {
    response = await service(request)
    return response
}

@route
map.set("/handler", handler)
```
