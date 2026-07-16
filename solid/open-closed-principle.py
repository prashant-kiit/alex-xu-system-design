# Work should be divided into Units, where each Unit is a Class
# such that each Class is open to be changed exclusively (Open for Change)
# without any need to change the other Classes (Closed for Change)
# This ensures Decoupling and allow each Class to scale independently

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

class DebitPayment():
    def pay(self, order, security_code: SecurityCode):
        print(f"Processing debit payment type for order {order}")
        print(f"Verifying security code: {security_code}") # Different Behaviour of UPI Payment to that of Debit Payment and Credit Payment
        self.status = "paid"

class CreditPayment():
    def pay(self, order, security_code: SecurityCode):
        print(f"Processing credit payment type for order {order}")
        print(f"Verifying security code: {security_code}") # Different Behaviour of UPI Payment to that of Debit Payment and Credit Payment
        self.status = "paid"

class UPIPayment():
    def pay(self, order, security_pin: SecurityPIN):
        print(f"Processing UPI payment type for order {order}")
        print(f"Verifying security pin: {security_pin}") # Different Behaviour of UPI Payment to that of Debit Payment and Credit Payment
        self.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)
print(order.total_price())

debitpayment = DebitPayment()
debitpayment.pay(order, "0372846")
creditpayment = UPIPayment()
creditpayment.pay(order, "0372864")