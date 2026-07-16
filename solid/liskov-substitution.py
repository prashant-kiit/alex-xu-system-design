# Parent should be replaceable by Child Class
# Without breaking on Interfacial and Implementational Contract

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

# Parent CodePayment
class CodePayment(ABC):
    @abstractmethod
    def pay(self, order):
        pass

# Parent PINPayment
class PINPayment(ABC):
    @abstractmethod
    def pay(self, order):
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