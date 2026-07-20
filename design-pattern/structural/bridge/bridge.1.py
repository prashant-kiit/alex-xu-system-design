"""
Definition: Decouples an abstraction from its implementation so that both can vary independently, without one being tightly bound to the other. Instead of a rigid inheritance hierarchy, it uses composition — the abstraction holds a reference to an implementation object.
Use Case: You have multiple variants of an abstraction (e.g., shapes) and multiple variants of implementation (e.g., rendering engines), and you want to mix-and-match them without an explosion of subclasses (e.g., CircleOpenGL, CircleDirectX, SquareOpenGL, SquareDirectX...). Common in GUI toolkits, device drivers, and rendering systems.
"""

from abc import ABC, abstractmethod


class BreathSystem(ABC):
    @abstractmethod
    def breath():
        pass


class GillsBreath(BreathSystem):
    def breath():
        print("breath from gills")


class LungsBreath(BreathSystem):
    def breath():
        print("breath from lungs")


class LivingThings(ABC):
    def __init__(self, breathsystem: BreathSystem):
        self.breathsystem = breathsystem

    @abstractmethod
    def breath():
        pass


class Fish(LivingThings):
    def breath(self):
        self.breathsystem.breath()


class Human(LivingThings):
    def breath(self):
        self.breathsystem.breath()


if __name__ == "__main__":
    gillsbreath = GillsBreath()
    fish = Fish(gillsbreath)
    fish.breath()
