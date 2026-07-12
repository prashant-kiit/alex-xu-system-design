def produce(event):
    double(event)

def double(event):
    triple((event[0]*2, event[1]*2))

def triple(event):
    quadruple((event[0]*3, event[1]*3))

def quadruple(event):
    consume((event[0]*4, event[1]*4))

def consume(event):
    print(event)

# callback hell/recursion of normal function
produce((10, 20))
