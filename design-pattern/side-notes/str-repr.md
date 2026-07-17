In Python, __str__ provides a human-readable, informal string representation intended for end-users, while __repr__ provides a detailed, unambiguous representation intended for developers. The __repr__ output should ideally contain enough information to recreate the object programmatically.

``` 
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} is {self.age} years old"

    def __repr__(self):
        return f"Person(name={self.name!r}, age={self.age!r})"

# Initialize object
p = Person("Alice", 30)

# Calls __str__
print(p) 
# Output: Alice is 30 years old

# Calls __repr__ (in the interactive terminal / REPL or explicitly with repr())
repr(p) 
# Output: Person(name='Alice', age=30)
