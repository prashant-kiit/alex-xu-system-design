"""
Definition: The Prototype pattern creates new objects by copying (cloning) an existing object — the "prototype" — rather than instantiating a class from scratch.
Use Case: 
- Expensive object creation
- instead of creating a new subclass for every slight variation of an object, you keep a set of pre-configured prototype instances and clone + tweak them as needed.
- Runtime object configuration — when the exact configuration of an object is only known at runtime, and it's easier to copy a similar existing object than to figure out its construction parameters from scratch.
- Preserving state snapshots — e.g., cloning a game character's current state, or duplicating a document template that already has formatting/structure in place. Ideal for stateful beans that need to maintain unique, independent data
"""

from abc import ABC, abstractmethod
from copy import copy


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


class CharacterRegistry:
    _prototypes = {}

    @classmethod
    def register(cls, key, prototype: Prototype):
        cls._prototypes[key] = prototype

    @classmethod
    def create(cls, key) -> Prototype:
        prototype = cls._prototypes.get(key)
        if prototype is None:
            raise ValueError(f"No prototype registered under: {key}")
        return prototype.clone()


# Setup — register pre-built templates once
CharacterRegistry.register("warrior", Character("Template", "Warrior", 1, ["Sword", "Shield"]))
CharacterRegistry.register("mage", Character("Template", "Mage", 1, ["Staff", "Spellbook"]))

# Usage — client just asks for a type, gets an independent clone back
new_mage = CharacterRegistry.create("mage")
new_mage.name = "Gandalf"
print(new_mage)  # Gandalf (Lvl 1 Mage) - Inventory: ['Staff', 'Spellbook']