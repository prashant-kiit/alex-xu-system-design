class Functional:
    def produce(self):
        self.event = (10, 20)
        return self

    def double(self):
        self.event = (self.event[0]*2, self.event[1]*2)
        return self

    def triple(self):
        self.event = (self.event[0]*3, self.event[1]*3)
        return self

    def quadruple(self):
        self.event = (self.event[0]*4, self.event[1]*4)
        return self

    def consume(self):
        print(self.event)

# produce().double(event).triple(event_0).quadruple(event_1).consume(output)
functional = Functional()
functional.produce().double().triple().quadruple().consume()
# problem intermediate events are referenced outside the function scope make the transformations impure
# This is just Builder Pattern which is OOP based design pattern