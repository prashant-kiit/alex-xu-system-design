def produce(event):
    return lambda event=event: double(event)

def double(event):
    return lambda event=(event[0]*2, event[1]*2): triple(event)

def triple(event):
    return lambda event=(event[0]*3, event[1]*3): quadruple(event)

def quadruple(event):
    return lambda event=(event[0]*4, event[1]*4): consume(event)

def consume(event):
    print(event)

def apply():
    return produce

# callback hell/recursion of lambda function
apply()((10, 20))()()()()
