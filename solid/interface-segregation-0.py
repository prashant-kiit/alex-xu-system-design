# Refactor the Interfaces such that
# Principle 1, 2 and 3 hold valid
# i.e. Child Class only implements those methods that fall within its Unit of Work
# New Child Class can be with new method implementations
# Parent and Child Class have same interface and implementation contract

from abc import ABC, abstractmethod

class Order:
    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

type SecurityCode = str
type SecurityPIN = str

# Parent Payment
class Payment(ABC):
    @abstractmethod
    def pay(self, order):
        pass

# Parent CodePayment
class CodePayment(Payment):
    pass

# Parent PINPayment
class PINPayment(Payment):
    pass

# Parent PassportPayment
class PassportPayment(ABC):
    @abstractmethod
    def pay(self, order, passport_id):
        pass

# Child of Parent CodePayment
class DebitPayment(CodePayment):
    def __init__(self, security_code: SecurityCode):
        self.security_code = security_code

    def pay(self, order):
        print(f"Processing debit payment type for order {order}")
        print(f"Verifying security code: {self.security_code}") # Different Behaviour of UPI Payment to that of Debit Payment and Credit Payment
        self.status = "paid"

# Child of Parent CodePayment
class CreditPayment(CodePayment):
    def __init__(self, security_code: SecurityCode):
        self.security_code = security_code

    def pay(self, order):
        print(f"Processing credit payment type for order {order}")
        print(f"Verifying security code: {self.security_code}") # Different Behaviour of UPI Payment to that of Debit Payment and Credit Payment
        self.status = "paid"

# Child of Parent PINPayment 
class UPIPayment(PINPayment):
    def __init__(self, security_pin: SecurityPIN):
        self.security_pin = security_pin

    def pay(self, order):
        print(f"Processing UPI payment type for order {order}")
        print(f"Verifying security pin: {self.security_pin}") # Different Behaviour of UPI Payment to that of Debit Payment and Credit Payment
        self.status = "paid"

# Child of Parent PassportPayment 
class SwiftPayment(PINPayment):
    def __init__(self, security_pin: SecurityPIN):
        self.security_pin = security_pin

    def pay(self, order, passport_id):
        print(f"Processing UPI payment type for order {order}")
        print(f"Visa verification based on {passport_id}")
        print(f"Verifying security pin: {self.security_pin}") # Different Behaviour of UPI Payment to that of Debit Payment and Credit Payment
        self.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)
print(order.total_price())

payment = DebitPayment("0372846")
payment.pay(order)
payment = UPIPayment("0372864")
payment.pay(order)

payment = UPIPayment("0372846")
payment.pay(order)
payment = DebitPayment("0372864")
payment.pay(order)

payment = SwiftPayment("0372846")
payment.pay(order, "123456")