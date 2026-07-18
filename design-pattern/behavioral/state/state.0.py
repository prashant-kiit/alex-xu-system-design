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

