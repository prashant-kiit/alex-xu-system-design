// Problem:
// Since DB Context is different from the Service Context, db_operations_n are Side Effects
// Thus Service layer is no control over DB Context, However have to wait for the DB Call to Complete
// This causes the Stack to Block the CPU with this DB Call
// This prevents other Processes from running on CPU
// This compromises Performance and Memory
// Solution:
// Program Pushed DB Calls to Event Queue in OS and get Promise in return
// OS Event Loop will run the Event Queued DB Calls using Epoll (Polling technique)
// This can be done by async keyword or Promise
// Problem:
// Transform Calls depend of the response from DB Calls to perform action
// Solution:
// So Transform Calls must await for the DB Calls ie. Promise from DB calls must be resolved by Tranform Calls
// This can be done by await keyword or .then(callback)
// Problem:
// Event Loop do not guareentee the order of execution without proper Promise Resolution
// Solution:
// To maintain order of execution (Sync-ness) make blocking calls using await (here, Main thread is blocked by CPU which has yet not processed the previous function)

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
fasync unction db_operation_1(response) {
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
    

    