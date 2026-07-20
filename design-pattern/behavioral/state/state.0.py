"""
Definition: A behavioral design pattern that lets an object change its behavior when its internal state changes, making it appear as if the object changed its class. Instead of using conditionals (if/elif) to check state everywhere, each state is encapsulated in its own object, and the context delegates behavior to the current state object.

Use case: When an object's behavior depends heavily on its state and it has many state-dependent conditional statements — e.g., order processing (pending → shipped → delivered), traffic lights, media players (playing/paused/stopped), vending machines, connection handling (connected/disconnected/reconnecting).
"""

class PointState():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Point():
    def __init__(self):
        self.pointstate = PointState(10, 20)
    def set_point_state(self, x, y):
        self.pointstate = PointState(x, y)


if __name__ == "__main__":
    point = Point()
    point.set_point_state(30, 40)

