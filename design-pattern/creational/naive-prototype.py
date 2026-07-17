"""
Definition: The Prototype pattern creates new objects by copying (cloning) an existing object — the "prototype" — rather than instantiating a class from scratch.
Use Case: 
- Expensive object creation
- instead of creating a new subclass for every slight variation of an object, you keep a set of pre-configured prototype instances and clone + tweak them as needed.
- Runtime object configuration — when the exact configuration of an object is only known at runtime, and it's easier to copy a similar existing object than to figure out its construction parameters from scratch.
- Preserving state snapshots — e.g., cloning a game character's current state, or duplicating a document template that already has formatting/structure in place. Ideal for stateful beans that need to maintain unique, independent data
"""

import copy
from abc import ABC, abstractmethod


class Prototype(ABC):
    @abstractmethod
    def clone(self):
        pass


class Character(Prototype):
    def __init__(self, name, char_class, level, inventory=None):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.inventory = inventory if inventory is not None else []

    def clone(self):
        # deepcopy so the cloned character's inventory list
        # isn't shared/mutated alongside the original's
        return copy.deepcopy(self)

    def __str__(self):
        return f"{self.name} (Lvl {self.level} {self.char_class}) - Inventory: {self.inventory}"


# Build an expensive "template" character once —
# imagine this involved loading stats from a database, applying balancing rules, etc.
warrior_template = Character("Template", "Warrior", level=1, inventory=["Sword", "Shield"])

# Clone it to create new characters instead of rebuilding from scratch each time
player1 = warrior_template.clone()
player1.name = "Aragorn"
player1.level = 5

player2 = warrior_template.clone()
player2.name = "Boromir"
player2.inventory.append("Horn of Gondor")

print(warrior_template)  # Template (Lvl 1 Warrior) - Inventory: ['Sword', 'Shield']
print(player1)           # Aragorn (Lvl 5 Warrior) - Inventory: ['Sword', 'Shield']
print(player2)           # Boromir (Lvl 1 Warrior) - Inventory: ['Sword', 'Shield', 'Horn of Gondor']