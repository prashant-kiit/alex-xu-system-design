
from typing import Callable


def petrol_engine_ignite():
    print("Petrol engine ignites")


def diesel_engine_ignite():
    print("Diesel engine ignites")


class Car:
    def __init__(self, engine_ignite: Callable):
        self.engine_ignite = engine_ignite

    def start(self):
        self.engine_ignite()


if __name__ == "__main__":
    car1 = Car(petrol_engine_ignite)
    car2 = Car(diesel_engine_ignite)
    car1.start()
    car2.start()
