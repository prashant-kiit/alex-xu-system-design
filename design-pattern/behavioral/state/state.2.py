from abc import ABC, abstractmethod

# --- State interface ---
class OrderState(ABC):
    @abstractmethod
    def next(self, order: "Order"):
        pass

    @abstractmethod
    def name(self) -> str:
        pass


# --- Concrete states ---
class Pending(OrderState):
    def next(self, order):
        order.state = Shipped()

    def name(self):
        return "Pending"

class Shipped(OrderState):
    def next(self, order):
        order.state = Delivered()

    def name(self):
        return "Shipped"

class Delivered(OrderState):
    def next(self, order):
        print("Order already delivered. No further transitions.")

    def name(self):
        return "Delivered"


# --- Context ---
class Order:
    def __init__(self):
        self.state: OrderState = Pending()

    def advance(self):
        self.state.next(self)

    def status(self) -> str:
        return self.state.name()


# --- Usage ---
order = Order()
print(order.status())   # Pending

order.advance()
print(order.status())   # Shipped

order.advance()
print(order.status())   # Delivered

order.advance()          # Order already delivered. No further transitions.
print(order.status())   # Delivered