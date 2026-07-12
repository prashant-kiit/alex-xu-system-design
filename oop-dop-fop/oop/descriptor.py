# A descriptor is an object that customizes attribute access (get/set/delete) by defining special methods — __get__, __set__, and/or __delete__. 
class Descriptor:
    def __get__(self, obj, objtype=None):
        print("Getting...")
        return obj._value

    def __set__(self, obj, value):
        print("Setting...")
        if value < 0:
            raise ValueError("Can't be negative")
        obj._value = value
    
    def __delete__(self, obj):
        print("Deleting...")

class Product:
    price = Descriptor()      # class attribute — a descriptor instance

    def __init__(self, price):
        self.price = price    # triggers __set__

p = Product(100)
print(p.price)     # 100 — triggers __get__
p.price = 5        # ValueError!