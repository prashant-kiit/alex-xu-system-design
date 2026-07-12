# Single Inheritance
class Animal:
    def eat(self):
        return "Eating..."

class Dog(Animal):
    def bark(self):
        return "Woof!"

d = Dog()
print(d.eat())    # Eating... (inherited)
print(d.bark())   # Woof!

# Multilevel Inheritance
class Animal:
    def eat(self):
        return "Eating..."

class Dog(Animal):
    def bark(self):
        return "Woof!"

class Puppy(Dog):
    def weep(self):
        return "Weeping..."

p = Puppy()
print(p.eat())    # Eating...   — from Animal
print(p.bark())   # Woof!       — from Dog
print(p.weep())   # Weeping...  — its own

# Hierarchical Inheritance
class Animal:
    def eat(self):
        return "Eating..."

class Dog(Animal):
    def bark(self):
        return "Woof!"

class Cat(Animal):
    def meow(self):
        return "Meow!"

d = Dog()
c = Cat()
print(d.eat())    # Eating... (shared)
print(c.eat())    # Eating... (shared)

# Hybrid
class Animal:
    def eat(self):
        return "Eating..."

class Pet(Animal):
    def domesticated(self):
        return "I'm a pet"

class WorkAnimal(Animal):
    def work(self):
        return "I work"

class Dog(Pet, WorkAnimal):    # multiple + multilevel combined
    def bark(self):
        return "Woof!"

d = Dog()
print(d.eat())            # Eating...
print(d.domesticated())   # I'm a pet
print(d.work())           # I work
print(d.bark())           # Woof!


# Method Resolution Order (MRO)
class A:
    def greet(self):
        return "Hello from A"

class B(A):
    def greet(self):
        return "Hello from B"

class C(A):
    def greet(self):
        return "Hello from C"

class D(B, C):
    pass

d = D()
print(d.greet())        # Hello from B — leftmost parent wins first
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
# Python searches left to right, depth-first, but respecting that a parent is only checked after all its children — this is the "Diamond Problem" solved cleanly.

# Using super() across inheritance
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)    # calls Animal's __init__
        self.breed = breed

d = Dog("Rex", "Labrador")
print(d.name, d.breed)   # Rex Labrador

# MRO Chain applies uniformly to every method call in Python. __init__ is just the most common example because constructors chain naturally, 
# but the exact same mechanics apply to regular methods, @classmethod, @staticmethod calls, dunder methods, properties — everything.
class A:
    def greet(self):
        print("A.greet")
        # no super() here — A is the "top"

class B(A):
    def greet(self):
        print("B.greet")
        super().greet()

class C(A):
    def greet(self):
        print("C.greet")
        super().greet()

class D(B, C):
    def greet(self):
        print("D.greet")
        super().greet()
d = D()
d.greet()
# D.greet
# B.greet
# C.greet
# A.greet

print(D.__mro__)
# (D, B, C, A, object)

# Method Overriding: 
# A child class redefines a method that already exists in its parent class, replacing (or extending) its behavior. 
# This is fully and natively supported in Python.
class Animal:
    def speak(self):
        return "Some generic animal sound"

class Dog(Animal):
    def speak(self):                # overrides parent's method
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

animals = [Animal(), Dog(), Cat()]
for a in animals:
    print(a.speak())
# Some generic animal sound
# Woof!
# Meow!

# Method Overloading
# Python does NOT support this natively
class Calculator:
    def add(self, a, b):
        return a + b

    def add(self, a, b, c):     # this just OVERWRITES the previous 'add'
        return a + b + c

calc = Calculator()
calc.add(1, 2)          # TypeError: missing 1 required positional argument
calc.add(1, 2, 3)       # 6 — only the last definition survives

# Side-by-side comparison: Method Overloading vs Method Overridding
class Shape:
    # OVERLOADING attempt (simulated via *args)
    def area(self, *dimensions):
        if len(dimensions) == 1:
            radius = dimensions[0]
            return 3.14159 * radius ** 2          # circle
        elif len(dimensions) == 2:
            width, height = dimensions
            return width * height                  # rectangle

class Circle(Shape):
    # OVERRIDING — customizing inherited method fully
    def area(self, radius):
        return f"Circle area: {3.14159 * radius ** 2}"

s = Shape()
print(s.area(5))          # 78.53975 (treated as circle, 1 arg)
print(s.area(4, 5))       # 20 (treated as rectangle, 2 args)

c = Circle()
print(c.area(5))          # Circle area: 78.53975 (overridden, always circle)