from abc import ABC, abstractmethod
from math import sqrt

class PointState(ABC):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    @abstractmethod
    def distance_from_center(self):
        pass

class CenterState(PointState):
    def distance_from_center(self):
        return 0

class NonCenterState(PointState):
    def distance_from_center(self):
        return sqrt(self.x ^ 2 + self.y^2)

class Point():    
    def set_point_state(self, pointstate: PointState):
        self.pointstate = pointstate

    def get_point_state(self):
        return self.pointstate


if __name__ == "__main__":
    point = Point()
    centerstate = CenterState()
    point.set_point_state(centerstate)
    print(point.get_point_state().distance_from_center())

    noncenterstate = NonCenterState(10, 20)
    point.set_point_state(noncenterstate)
    print(point.get_point_state().distance_from_center())