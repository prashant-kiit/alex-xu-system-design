"""
Definition: A behavioral design pattern that defines a family of interchangeable algorithms, encapsulates each one, and lets you swap them at runtime without changing the code that uses them.
Use case: When you have multiple ways to perform a task (e.g., different sorting algorithms, payment methods, discount rules, compression algorithms) and want to select the behavior dynamically instead of using long if/elif chains.
"""

from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def ignite(self):
        pass


class PetrolEngine(Engine):
    def ignite(self):
        print("Petrol engine ignites")


class DieselEngine(Engine):
    def ignite(self):
        print("Diesel engine ignites")


class Car:
    def __init__(self, engine: Engine):
        self.engine = engine

    def start(self):
        self.engine.ignite()


if __name__ == "__main__":
    car1 = Car(PetrolEngine())
    car2 = Car(DieselEngine())
    car1.start()
    car2.start()
