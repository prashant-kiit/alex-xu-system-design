# Nomial Typing by Abstracts
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable

class PaymentProcessor(ABC):
    # abstract attribute — enforced as a property, since ABC has no plain-attribute equivalent
    @property
    @abstractmethod
    def provider_name(self):
        pass

    @abstractmethod
    def process_payment(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    @property
    def provider_name(self):
        return "CreditCard"

    def process_payment(self, amount):
        return f"Processing ${amount} via credit card"

    def refund(self, amount):
        return f"Refunding ${amount} to credit card"

class PayPalProcessor(PaymentProcessor):
    @property
    def provider_name(self):
        return "PayPal"

    def process_payment(self, amount):
        return f"Processing ${amount} via PayPal"

    def refund(self, amount):
        return f"Refunding ${amount} via PayPal"

# Any new processor MUST implement provider_name and both methods, guaranteed
# (missing any of them, CreditCardProcessor/PayPalProcessor would fail to even instantiate)
def checkout(processor: PaymentProcessor, amount):
    print(f"[{processor.provider_name}]", processor.process_payment(amount))

checkout(CreditCardProcessor(), 100)
checkout(PayPalProcessor(), 50)

# Structual/Duck Typing by Protocol
@runtime_checkable
class PaymentProcessorProtocol(Protocol):
    provider_name: str  # data attribute, not just methods
    def process_payment(self, amount): ...
    def refund(self, amount): ...

# No inheritance needed — matching the shape (attribute + both methods) is enough
class StripeProcessor:
    provider_name = "Stripe"

    def process_payment(self, amount):
        return f"Processing ${amount} via Stripe"

    def refund(self, amount):
        return f"Refunding ${amount} via Stripe"

class UpiProcessor:
    provider_name = "UPI"

    def process_payment(self, amount):
        return f"Processing ${amount} via UPI"

    def refund(self, amount):
        return f"Refunding ${amount} via UPI"

# Any object with matching attribute/method names satisfies the protocol, no MUST-implement guarantee
def checkout_protocol(processor: PaymentProcessorProtocol, amount):
    print(f"[{processor.provider_name}]", processor.process_payment(amount))

checkout_protocol(StripeProcessor(), 200)
checkout_protocol(UpiProcessor(), 75)

# runtime_checkable only lets isinstance() verify names exist (methods AND data attributes),
# not their types/signatures
print(isinstance(StripeProcessor(), PaymentProcessorProtocol))

class NotAProcessor:
    pass

print(isinstance(NotAProcessor(), PaymentProcessorProtocol))

# has both methods but is missing provider_name — still fails the isinstance check
class IncompleteProcessor:
    def process_payment(self, amount):
        return f"Processing ${amount}"

    def refund(self, amount):
        return f"Refunding ${amount}"

print(isinstance(IncompleteProcessor(), PaymentProcessorProtocol))
