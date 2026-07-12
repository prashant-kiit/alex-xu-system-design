import json


class Car:
    # class attributes (accessible by Class and all Instances of the Class)
    car_type = "Petrol"
    def __init__(self, name, model, _my_protected_attr, __my_private_attr):
        # instance attributes (accessible only by all Instances of the Class, not Class)
        self.name = name
        self.model = model
        self._my_protected_attr = _my_protected_attr  # "protected" — single underscore, convention only
        self.__my_private_attr= __my_private_attr # "private" — name-mangled
    
    @property
    def my_property(self):
        return "this is property method"
    
    @my_property.setter
    def my_property(self, value):
        print(f"This my_property value passed {value}")


if __name__ == "__main__":
    car_0 = Car("Maruti", "800", 100, 200)
    car_1 = Car("Thar", "Classic", 300, 400)

    # set instance attribute
    car_0.engine = "V8"
    car_1.engine = "V12"

    # set class attribute
    Car.car_type = "Ethanol"

    # If you set an instance attribute with the same name, it "shadows" the class attribute — it doesn't change it globally
    car_0.car_type = "Diesel"

    # get instance and class attributes
    print(car_0.name, car_0.model, car_0.engine, car_0.car_type, Car.car_type)
    print(car_1.name, car_1.model, car_1.engine, car_1.car_type, Car.car_type)

    # get protected and private instance attributes
    # Python doesn't enforce true privacy — it's convention-based:
    print(car_0._my_protected_attr) # accessible, but "please don't touch" by convention
    try:
        print(car_0.__my_private_attr) # AttributeError!
    except AttributeError as error:
        print(error, f"Use _Car__my_private_attr instead {car_0._Car__my_private_attr}") # works — Python renamed it internally (name mangling)

    # get instance attributes in map form
    print(json.dumps(car_0.__dict__, indent=4))
    print(json.dumps(car_1.__dict__, indent=4))
    # get class attributes in map form
    # print(Car.__dict__)

    # property
    # Lets you add logic (validation, computed values) while keeping attribute-like syntax
    print(car_0.my_property)
    car_0.my_property = "Test"

    # Dynamic alternatives:
    hasattr(car_0, "name")             # check existence
    getattr(car_0, "name")             # get
    setattr(car_0, "name", "Max")      # set
    # delattr(car_0, "name")             # delete
