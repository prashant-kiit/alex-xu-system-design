class Car:
    company = "TATA"

    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.isMoving = False
    
    # instance method
    def move(self):
        # self will access the instance only attributes and methods 
        self.isMoving = True
        print(f"Car {self.company}-{self.name} of mode {self.model} is moving")
    
    # Operate on the class itself, not a specific instance. 
    # Can be access by Class and Object both unlike Class Atribute
    # If you set an instance attribute with the same name, it "shadows" the class attribute — it doesn't change it globally. eg: car_0.company = "Diesel"
    @classmethod
    def alterCompany(cls, company):
        cls.company = company
        return cls.company
    
    # Class method used as Constructor
    @classmethod
    def getInstance(cls, name, model):
        return cls(name, model)

    # Don't need self or cls — they're just regular functions placed inside a class for organizational purposes
    @staticmethod
    def makeSound(sound):
        print(f"Sound is {sound}")

if __name__ == "__main__":
    car_0 = Car("Maruti", "800")
    car_1 = Car.getInstance("Scorpio", "N")
    car_0.move()
    car_1.move()

    # Using object to access class method. Cls will still be Class only
    print(car_0.alterCompany("Mahindra"))
    print(Car.company)
    car_0.move()
    car_1.move()
    
    # Using object to access class method. Cls will still be Class only
    print(car_1.alterCompany("Toyota"))
    print(Car.company)
    car_0.move()
    car_1.move()

    # static method Class or Object any can access
    Car.makeSound("Vroom")
    car_0.makeSound("Groom")
    car_1.makeSound("Zroom")


    
    