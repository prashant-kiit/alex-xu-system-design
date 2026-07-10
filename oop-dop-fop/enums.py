from enum import Enum, auto, IntEnum, Flag, unique


# 1. Basic Enum — named constants, safer than raw strings/ints
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.RED)          # Color.RED
print(Color.RED.name)     # RED
print(Color.RED.value)    # 1
print(Color.RED is Color(1))  # True — members are singletons


# 2. auto() — let Python assign values when you don't care what they are
class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()

print(list(Direction))     # [<Direction.NORTH: 1>, ...]


# 3. IntEnum — behaves like an int, useful for comparisons/serialization
class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

print(Priority.HIGH > Priority.LOW)   # True
print(Priority.HIGH == 3)             # True


# 4. Enum with methods — enums can have behavior like any class
class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    def describe(self):
        return f"Status is {self.value}"

print(Status.ACTIVE.describe())   # Status is active


# 5. @unique — raises an error if two members share a value
@unique
class Single(Enum):
    A = 1
    B = 2
    # C = 1  # would raise ValueError: duplicate values found


# 6. Flag — combine members with bitwise operators (like permission bits)
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()

rwx = Permission.READ | Permission.WRITE
print(rwx)                          # Permission.READ|WRITE
print(Permission.READ in rwx)       # True


# 7. Iteration — loop over members in definition order
for color in Color:
    print(color.name, color.value)
# RED 1
# GREEN 2
# BLUE 3

# only actual members are iterated, aliases are skipped (see #9)
print([c.name for c in Color])   # ['RED', 'GREEN', 'BLUE']


# 8. Lookup — by value, by name, or safe "does it exist" checks
print(Color(2))                     # Color.GREEN        (value -> member)
print(Color["GREEN"])               # Color.GREEN         (name -> member)

try:
    Color(99)
except ValueError:
    print("99 is not a valid Color")

print("GREEN" in Color.__members__)     # True  — check name exists
print(2 in [c.value for c in Color])    # True  — check value exists


# 9. Aliases — same value, extra name; iteration/lookup only sees canonical member
class Shape(Enum):
    CIRCLE = 1
    ROUND = 1        # alias for CIRCLE, not a separate member

print(Shape.ROUND is Shape.CIRCLE)      # True
print(list(Shape))                      # [<Shape.CIRCLE: 1>] — ROUND not listed
print(Shape["ROUND"])                   # Shape.CIRCLE — name lookup still works
