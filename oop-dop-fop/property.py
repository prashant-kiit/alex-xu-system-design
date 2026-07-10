class Dog:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):                # GETTER
        print("Getting name...")
        return self._name

    @name.setter
    def name(self, value):         # SETTER
        print("Setting name...")
        if not value:
            raise ValueError("Name can't be empty")
        self._name = value

    @name.deleter
    def name(self):                # DELETER
        print("Deleting name...")
        del self._name

d = Dog("Rex")
print(d.name)        # Getting name... → Rex   (looks like an attribute!)
d.name = "Max"        # Setting name... 
del d.name             # Deleting name...

# If you only define the getter (no setter), the attribute becomes read-only:
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):                     # computed, read-only
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)      # 78.53975
c.area = 100        # AttributeError: can't set attribute

# Validation
class Account:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance can't be negative")
        self._balance = value

acc = Account(100)
acc.balance = -50    # ValueError!

# Computed/derived values
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height    # always up to date, not stored separately

r = Rectangle(4, 5)
print(r.area)   # 20
r.width = 10
print(r.area)   # 50 — recalculated automatically