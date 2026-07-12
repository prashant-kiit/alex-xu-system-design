def produce():
    return (10, 20)

def double(event):
    return (event[0]*2, event[1]*2)

def triple(event):
    return (event[0]*3, event[1]*3)

def quadruple(event):
    return (event[0]*4, event[1]*4)

def consume(event):
    print(event)

event = produce()
event_0 = double(event)
event_1 = triple(event_0)
output = quadruple(event_1)
consume(output)

print(id(event))
print(event)
print(id(output))