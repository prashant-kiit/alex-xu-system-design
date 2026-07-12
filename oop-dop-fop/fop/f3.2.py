def apply(event, produce, double, triple, quadruple, consume):
    produce(event, double, triple, quadruple, consume)

def produce(event, double, triple, quadruple, consume):
    double(event, triple, quadruple, consume)

def double(event, triple, quadruple, consume):
    triple((event[0]*2, event[1]*2), quadruple, consume)

def triple(event, quadruple, consume):
    quadruple((event[0]*3, event[1]*3), consume)

def quadruple(event, consume):
    consume((event[0]*4, event[1]*4))

def consume(event):
    print(event)

# function currying (callback hell/recursion of normal function)
apply((10, 20), produce, double, triple, quadruple, consume)