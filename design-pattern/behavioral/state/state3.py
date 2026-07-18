class TrafficLight:
    def __init__(self):
        self.state = "RED"
        self.transitions = {
            "RED": "GREEN",
            "GREEN": "YELLOW",
            "YELLOW": "RED",
        }

    def next(self):
        self.state = self.transitions[self.state]
        print(f"Light is now {self.state}")

light = TrafficLight()
light.next()  # Light is now GREEN
light.next()  # Light is now YELLOW
light.next()  # Light is now RED