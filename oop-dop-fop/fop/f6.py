class Promise:
    def __init__(self, event):
        self.event = event
    
    def then(self, transform):
        promise = transform(self.event)
        return promise

def produce(event):
    return Promise(event)

def double(event):
    return Promise((event[0]*2, event[1]*2))

def triple(event):
    return Promise((event[0]*3, event[1]*3))

def quadruple(event):
    return Promise((event[0]*4, event[1]*4))

def consume(event):
    print(event)

# promise based fop
produce((10, 20)).then(double).then(triple).then(quadruple).then(consume)
