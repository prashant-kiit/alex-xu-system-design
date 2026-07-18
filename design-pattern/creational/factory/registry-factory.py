"""
Definition: Create Object of a Class without a Contructor, but using a method so that it becomes one unique way of creating a object
Use Case: 
- Centralized creation logic
- Decoupling — client code doesn't need to know the concrete class names, just the common interface
- Swappable implementations — useful when the exact class to create depends on configuration, user input, or runtime conditions 
"""

from abc import ABC, abstractmethod


class Steak(ABC):
    @abstractmethod
    def cook(self):
        pass

class SteakFactory():
    __instance = {}

    @classmethod
    def register(cls, steak_type):
        def wrapper(steak_cls):
            cls.__instance[steak_type] = steak_cls
        return wrapper


    @classmethod
    def create_steak(cls, steak_type):
        steak_cls = cls.__instance.get(steak_type)
        if not steak_cls:
            raise Exception(f"{steak_type} not valid")
        return steak_cls()

@SteakFactory.register("welldone")
class WelldoneSteak(Steak):
    def cook(self):
        print("Well done steak")

@SteakFactory.register("medium")
class MediumSteak(Steak):
    def cook(self):
        print("Medium steak")

if __name__ == "__main__":
    steak = SteakFactory.create_steak("medium")
    print(steak.cook())