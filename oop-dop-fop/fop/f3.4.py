def produce(event, callback):
    callback(event)

def double(event, callback):
    callback((event[0]*2, event[1]*2))

def triple(event, callback):
    callback((event[0]*3, event[1]*3))

def quadruple(event, callback):
    callback((event[0]*4, event[1]*4))

def consume(event):
    print(event)

# callback hell/recursion of lambda function
produce((10, 20), 
    lambda event: double(event, 
        lambda event: triple(event, 
            lambda event: quadruple(event,
                lambda event: consume(event)))))