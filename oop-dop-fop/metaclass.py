# A metaclass is "the class of a class" — it defines how classes themselves behave, 
# just like a class defines how objects behave.
# Metaclass  →  creates  →  Class  →  creates  →  Object (instance)
#    type     →           →   Dog   →           →   dog1
# type is the default metaclass in Python. Every class you write is secretly an instance of type.

class UpperAttrMeta(type):
    def __new__(mcs, name, bases, namespace):
        new_namespace = {
            (key.upper() if not key.startswith("__") else key): value
            for key, value in namespace.items()
        }
        return super().__new__(mcs, name, bases, new_namespace)

class Car(metaclass=UpperAttrMeta):
    company = "Toyota"
    def __init__(self, name, model):
        self.name = name
        self.model = model

if __name__ == "__main__":
    car = Car("A", "B")
    print(type(Car))
    print(type(car))

    # type(name, bases, namespace)
    NewCar = type('NewCar', (), {
    '__init__': lambda self, name, model: (setattr(self, 'name', name), setattr(self, 'model', model), None)[-1]
    })
    newcar = NewCar("C", "D")
    print(type(NewCar))
    print(type(newcar))

    print(car.COMPANY)

## __new__ vs __init__ in a metaclass
# class MyMeta(type):
#     def __new__(mcs, name, bases, namespace):
#         print(f"Creating class: {name}")
#         return super().__new__(mcs, name, bases, namespace)

#     def __init__(cls, name, bases, namespace):
#         print(f"Initializing class: {name}")
#         super().__init__(name, bases, namespace)

# class Dog(metaclass=MyMeta):
#     pass
# # Output:
# # Creating class: Dog
# # Initializing class: Dog