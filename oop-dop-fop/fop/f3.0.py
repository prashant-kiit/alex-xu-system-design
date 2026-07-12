def produce(event):
    return event

def double(event):
    return (event[0]*2, event[1]*2)

def triple(event):
    return (event[0]*3, event[1]*3)

def quadruple(event):
    return (event[0]*4, event[1]*4)

def consume(event):
    print(event)

# functional but syntactically tedious
consume(quadruple(triple(double(produce((10, 20))))))