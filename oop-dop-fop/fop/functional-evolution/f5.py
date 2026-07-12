class Promise:
    def produce(self, event):
        self.event = event
        return self

    def then(self, transfom):
        # even thought the self.event as input is in scope of Promise instance,
        # it is callback fuctions are pure since self.event are passed in a parameter (which avoids side effect)
        self.event = transfom(self.event)
        return self

# Promise.produce((10,20)).then(event, double).then(event_0, triple).then(event_1, quadruple).then(output, consume)
Promise().produce((10, 20)).then(lambda event: (event[0] * 2, event[1] * 2)).then(
    lambda event: (event[0] * 3, event[1] * 3)
).then(lambda event: (event[0] * 4, event[1] * 4)).then(lambda event: print(event))
# problem is same promise is return which breches immuntabilty rule
