"""
Definition: Create Object of a Class without a Contructor, but using a method so that it becomes one unique way of creating a object
Use Case: 
- Centralized creation logic
- Decoupling — client code doesn't need to know the concrete class names, just the common interface
- Swappable implementations — useful when the exact class to create depends on configuration, user input, or runtime conditions 
"""

from abc import ABC, abstractmethod


# Common interface
class Steak(ABC):
    @abstractmethod
    def cook(self):
        pass


# Concrete products
class WellDoneSteak(Steak):
    def cook(self):
        return "Cooking steak well-done, no pink left."


class MediumSteak(Steak):
    def cook(self):
        return "Cooking steak medium, warm pink center."


class VeganSteak(Steak):
    def cook(self):
        return "Preparing a plant-based steak alternative."


# Factory
class SteakFactory:
    @staticmethod
    def create_steak(steak_type: str) -> Steak:
        steak_type = steak_type.lower()
        if steak_type == "well-done":
            return WellDoneSteak()
        elif steak_type == "medium":
            return MediumSteak()
        elif steak_type == "vegan":
            return VeganSteak()
        else:
            raise ValueError(f"Unknown steak type: {steak_type}")


# Usage — the client never needs to know the concrete classes
order = "medium"
steak = SteakFactory.create_steak(order)
print(steak.cook())   # "Cooking steak medium, warm pink center."