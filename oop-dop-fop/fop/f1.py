def double(event):
    return (event[0]*2, event[1]*2)

def triple(event):
    return (event[0]*3, event[1]*3)

def quadruple(event):
    return (event[0]*4, event[1]*4)

event = (10, 20)

event_0 = double(input:=event)
event_1 = triple(event_0)
event_2 = quadruple(event_1)

output = event_2

print(id(event))
print(event)
print(id(output))
print(output)