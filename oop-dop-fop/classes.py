from random import randint


class Car:
    # constructor method used for creating the instance of the class in the heap with fields and methods
    # and self is context specifier of that newly created instance of the class
    def __init__(self, name, model):
        # instance fields
        self.name = name
        self.model = model
    
    def move(self):
        # instance method
        return f"Car {self.name} of model {self.model} is moving"
    
    def __eq__(self, other):
        print("Custom equality on Car Class")
        return isinstance(other, Car) and self.name == other.name and self.model == other.model

    def __hash__(self):
        print("Custom hash on Car Class")
        # We can play arounf with custom hash as per our wish
        return hash((self.name, self.model))
        # return randint(1, 10)

    # Makes the objects of this class unhashable
    # __hash__ = None

if __name__ == '__main__':
    # An object is a concrete instance of a class
    car = Car("Maruti", "800") # instantiation of the object from a class
    new_car = Car("Maruti", "800") # instantiation of the object from a class
    # What every object has
    # Identity — a unique id in memory (id(obj))
    print(id(car))
    print(id(car) == id(new_car))
    # Type/Class — what kind of object it is (type(obj))
    print(type(car))
    # State — its attribute values (obj.name, obj.breed)
    print(car.name, car.model)
    # Behavior — its methods (obj.bark())
    print(car.move())
    # every object in Python has a hash, accessible via the built-in hash() function, 
    # which calls the object's __hash__() method under the hood.
    # array, stack, queue, set and map do not have hash despite being objects
    print(hash(car))
    # hash() is based on the object's identity (roughly derived from id(obj)), not its data,
    # unlike other types like byte, boolean, int, float, tuple and string which has their data/value hashed
    print(hash(car) == hash(new_car))

    # equality of objects 
    # for other types byte, boolean, int, float, tuple and string and array, stack, queue, set and map 
    # have equality based on value
    # but object have equality based on object address or id(object) ie. reference value
    ## Rule of thumb: if you override __eq__, you should also override __hash__ (or explicitly set __hash__ = None),
    ## because Python expects: if two objects are equal, they must have the same hash.
    ## simply defining __eq__ (without __hash__) makes Python set __hash__ to None automatically, so the class stays unhashable even after you remove the explicit __hash__ = None line.
    print(car == new_car)

    # is in object as usual compares object address ie. reference value
    print("car is new_car", car is new_car)

    car_table = {}
    car_table[car] = "car"
    print(car in car_table) # here hashing happens twise once of RHS and then LHS
    car.model = "Swift" # mutated after being custom hashed
    # False, as value based custom hashed changed. However, True, when no custom hash.
    # Thus, objects that have mutable value should not be value-hashed in such case hashing is unreliable
    print(car in car_table) 
