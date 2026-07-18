from abc import ABC, abstractmethod

# Common interface
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass


# Concrete base object
class SimpleCoffee(Coffee):
    def cost(self):
        return 2.0
    
    def description(self):
        return "Coffee"

# Concrete decorators - each adds its own behavior
class MilkDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 0.5
    
    def description(self):
        return self._coffee.description() + " + Milk"


class SugarDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 0.2
    
    def description(self):
        return self._coffee.description() + " + Sugar"


class WhippedCreamDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
        
    def cost(self):
        return self._coffee.cost() + 0.7
    
    def description(self):
        return self._coffee.description() + " + Whipped Cream"

order = SimpleCoffee()
order = MilkDecorator(order)
order = SugarDecorator(order)
order = WhippedCreamDecorator(order)

print(order.description())  